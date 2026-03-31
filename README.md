# CESAR - The AI bot that estimates real estate worth

### Context:
This repository is created as part of an academic endeavour to learn to deploy machine learning models in professional setting.
It is owned by:
Joshua Alexander
Monica Nathalie Bertolini 
Modhura Das

For further contribution or ideas of extension contact: joshua.alexander2705@gmail.com

## How does it help?
Cesar acts as your personal real estate agent!
His sole purpose is to help you make the right decisions by giving you estimate of property thoroughout France!
You are able to talk to the bot as if chatting with a human without clunky interfaces. 
The underlying CESAR Prediction API doesn't just blindly guess; it uses a random forest ML model trained on extensive dataset for estimation. The bot never gives an estimate without a prior health check to the API.

![ScreenShot](CesarBotSS.jpeg)

## Features 
- Model trained on data available in the official  **DVF — Demande de Valeur Foncière**  
https://www.pricehubble.com/fr/blog/base-dvf-ventes-immobilieres-france

- Additional parameter "Code commune" added to have a more accuracy with respect to the area. 

- MCP server allows usage of the Gemini SDK which connects to a streamlit inteface enabling a chatbot type interface

- /health API created for the Gemini SDK to know when server is down and reply accordingly 

## AI usage declaration
- AI was used in the streamlit interface UI and for programming how to store a session history 

## Project Structure and Installation 
- Skipping this part for now

## Possible Next steps
- Dockerise the MCP and get it running with Kubernetes in Cloud
- Optimize model by removing Department
- Enhance security aspects - CORS
- Manage chat window size (rolling window or summarize)
