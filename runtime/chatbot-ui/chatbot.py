import streamlit as st
from google import genai
from google.genai import types
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
import sys

# --- CONFIGURATION ---
# Using the modern google-genai SDK
API_KEY = ""  # Replace with your actual API key or use environment variables for security
client = genai.Client(api_key=API_KEY)

SYSTEM_INSTRUCTION = """
You are a Real Estate Valuation Assistant. 
Your ONLY goal is to provide property estimates using the 'get_property_estimate' tool.
"""

# Normalize path to handle Windows spaces properly
current_dir = os.path.dirname(os.path.abspath(__file__))
server_path = os.path.normpath(os.path.join(current_dir, "mcp_server.py"))

server_params = StdioServerParameters(
    command=sys.executable,
    args=["-u", server_path],
    env=os.environ.copy() # Essential for subprocess to see installed packages
)

# --- MCP INTERACTION LOGIC ---
async def call_gemini_with_mcp(user_input):
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # 1. Handshake with MCP Server
                await session.initialize()
                
                # 2. Map MCP tools to Gemini's FunctionDeclaration format
                mcp_result = await session.list_tools()
                
                declarations = []
                for tool in mcp_result.tools:
                    declarations.append(
                        types.FunctionDeclaration(
                            name=tool.name,
                            description=tool.description,
                            parameters=tool.inputSchema
                        )
                    )
                
                gemini_tools = [types.Tool(function_declarations=declarations)]

                # 3. Model interaction using the new google-genai SDK
                # This automatically handles the "Model calls tool -> MCP runs tool -> Result to Model" loop
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=user_input,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        tools=gemini_tools,
                        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)
                    )
                )
                
                return response.text

    except Exception as e:
        # Logging to terminal for academic debugging
        import traceback
        print("\n--- MCP Error Traceback ---")
        print(traceback.format_exc())
        return f"⚠️ Connection Error: {str(e)}"

# --- STREAMLIT UI ---
st.set_page_config(page_title="Cesar AI - Real Estate Estimator", page_icon="🏠")
st.title("🏠 Real Estate Estimator")
st.caption("Academic Prototype: Localhost MCP + Gemini 1.5 Flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ex: What is my house in dept 75 worth?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Invoking MCP Server..."):
            # Create a clean async loop for this specific chat interaction
            # This is the safest way to run async MCP within Streamlit's sync flow
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                res_text = loop.run_until_complete(call_gemini_with_mcp(prompt))
                loop.close()
            except Exception as loop_err:
                res_text = f"Loop Error: {loop_err}"

            st.markdown(res_text)
            st.session_state.messages.append({"role": "assistant", "content": res_text})