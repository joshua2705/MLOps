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

## How to Use CESAR
1. Setup

Install dependencies:

pip install -e .
cd runtime/rating_ui && npm install

2. Train the Model

Place your dataset (e.g., DVF extract) in the data/ folder.

Minimum required columns:

surface_reelle_bati
nombre_pieces_principales
code_departement
type_local
valeur_fonciere
code_commune

Run training:
python -m training.scripts.train_from_minimal_csv

This generates:

a trained model (.joblib)
a contract file (.json)

Both are stored in artifact_storage/ and will be used for all predictions.

3. Start the Prediction Service

Set environment variables and launch the API:
export CESAR_MODEL_PATH=artifact_storage/model_minimal.joblib
export CESAR_CONTRACT_PATH=artifact_storage/contract_minimal.json

uvicorn runtime.prediction_api.app:app --reload --port 8000

You can verify the service at: http://localhost:8000/docs

4. Using CESAR

CESAR can be used through multiple interfaces depending on the use case.
API (integration in applications)

curl -X POST "http://localhost:8000/estimate/" \
-H "Content-Type: application/json" \
-d '{
  "surface_reelle_bati": 50,
  "nombre_pieces_principales": 3,
  "code_departement": "75",
  "type_local": "Appartement",
  "code_commune": "75115"
}'
CLI (automation / internal tools)

Single prediction:

cesar predict-one run \
  --surface 50 \
  --pieces 3 \
  --departement 75 \
  --type Appartement \
  --commune 75115

Batch prediction:

cesar batch run --input input.csv --output output.csv
Web UI (non-technical users)
cd runtime/rating_ui
npm run dev

Open:

http://localhost:5173

## Additional Features 
1. Model trained on data available in the official  **DVF — Demande de Valeur Foncière**  
https://www.pricehubble.com/fr/blog/base-dvf-ventes-immobilieres-france

2. Location Enhancement – Commune Code

A new feature (code_commune) was introduced to improve geographic precision, as department-level data can be too coarse
Commune-level input captures local price variations for more accurate valuation in dense urban areas.

3. REST API with Health Monitoring

The system exposes a REST API:

POST /estimate/ → returns property valuation
GET /health → checks if the service is running

The /health endpoint is used by external systems (e.g., chatbot) to:

Verify API availability
Avoid failed requests
Improve system reliability

4. Chatbot Interface (MCP + Gemini SDK)

CESAR is accessible through a chatbot interface.

Capabilities: Natural language interaction, no need for structured forms, integrated with backend API

Example:

“Estimate a 60m² apartment in Paris 15”


## AI usage declaration
- AI was used in the streamlit interface UI and for programming how to store a session history 
- AI tools were used selectively to assist with debugging (e.g., resolving CORS issues and environment configuration)

## Project Structure and Installation 
- Skipping this part for now

## Cloud Deployment

We dockerized the chatbot and deployed the full stack to **Render** so that CESAR works without needing anyone's local machine.

**This is the link to our chatbot**
   - **Chatbot UI** → https://cesar-chatbot.onrender.com



## Possible Next steps
- Dockerise the MCP and get it running with Kubernetes in Cloud
- Optimize model by removing Department
- Enhance security aspects - CORS
- Manage chat window size (rolling window or summarize)
