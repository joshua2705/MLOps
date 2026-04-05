FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY chatbot.py .
COPY mcp_server.py .

EXPOSE 8501
#Streamlit is running on this port by default 

CMD ["streamlit", "run", "chatbot.py", "--server.port=8501", "--server.address=0.0.0.0"]
#The --server.address= makes sure that we can access it even when we are outside the container