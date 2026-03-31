import streamlit as st
import asyncio
from fastmcp import Client
from google import genai
from mcp_server import mcp

# Dear professor, I tried stdio, sse even uvstdio to connect to the MCP server, but I kept running into issues.
# So I finally resorted to this quick and dirty fix of importing it directly

mcp_client = Client(mcp)
gemini_client = genai.Client(api_key="")

SYSTEM_INSTRUCTION = """
You are a Real Estate Valuation Assistant. 
Your ONLY goal is to provide property estimates using the 'get_property_estimate' tool.
Aparment is "Appartement", House is "Maison", Dependency is "Dépendance", and commercial or industrial space is "Local industriel. commercial ou assimilé"

GUARDRAILS:
1. If the user asks about topics unrelated to real estate, 
   respond: "I am limited to real estate valuation."
2. Do not invent data. If details are missing, ask for: surface area, department, number of rooms, and property type.
3. Once you have ALL required details (surface area, department code, number of rooms, property type),
   call get_property_estimate IMMEDIATELY. Do not ask for information already provided.
"""


# I used AI to add the conversation history to the Gemini call. 

async def call_gemini_with_mcp(conversation_history: list[dict]) -> str:
    async with mcp_client:
        chat = gemini_client.aio.chats.create(
            model="gemini-2.5-flash-lite",
            config=genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                tools=[mcp_client.session],
                automatic_function_calling=genai.types.AutomaticFunctionCallingConfig()
            ),
            history=conversation_history[:-1],
        )
        # Send only the latest user message
        latest_message = conversation_history[-1]["parts"][0]["text"]
        response = await chat.send_message(latest_message)
        return response.text


# I used AI to add the conversation history to the Gemini call. 
# --- STREAMLIT UI ---
st.set_page_config(page_title="Cesar AI - Real Estate Estimator", page_icon="🏠")
st.title("🏠 CESAR BOT")
st.caption("Academic Prototype: Localhost MCP + Gemini 2.5 Flash Lite")


if "messages" not in st.session_state:
    st.session_state.messages = [] 
if "gemini_history" not in st.session_state:
    st.session_state.gemini_history = [] 

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ex: What is my apartment in dept 75 worth?"):
    
    # Append to display history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Append to Gemini history
    st.session_state.gemini_history.append({
        "role": "user",
        "parts": [{"text": prompt}]
    })

    with st.chat_message("assistant"):
        with st.spinner("Invoking MCP Server..."):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                res_text = loop.run_until_complete(
                    call_gemini_with_mcp(st.session_state.gemini_history)
                )
                loop.close()
            except Exception as loop_err:
                res_text = f"Loop Error: {loop_err}"

        st.markdown(res_text)

    # Append assistant response to both histories
    st.session_state.messages.append({"role": "assistant", "content": res_text})
    st.session_state.gemini_history.append({
        "role": "model",
        "parts": [{"text": res_text}]
    })