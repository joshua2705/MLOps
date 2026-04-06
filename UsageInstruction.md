


How to Use CESAR

1. Setup

Install dependencies:

```bash
pip install -e .
````

2. Train the Model

Place your dataset (e.g., DVF extract) in the data/ folder.

Minimum required columns:

```text
surface_reelle_bati
nombre_pieces_principales
code_departement
type_local
valeur_fonciere
code_commune
```

Run training:

```bash
python -m training.scripts.train_from_minimal_csv
```

This generates:

* a trained model (.joblib)
* a contract file (.json)

Both are stored in artifact_storage/ and will be used for all predictions.

3. Start the Prediction Service

Set environment variables:

```bash
export CESAR_MODEL_PATH=artifact_storage/model_minimal.joblib
export CESAR_CONTRACT_PATH=artifact_storage/contract_minimal.json
```

Start the API:

```bash
uvicorn runtime.prediction_api.app:app --reload --port 8000
```

Verify the service:

[http://localhost:8000/docs](http://localhost:8000/docs)

4. Using CESAR

CESAR can be used through multiple interfaces depending on the use case.

4.1 API (integration in applications)

```bash
curl -X POST "http://localhost:8000/estimate/" \
-H "Content-Type: application/json" \
-d '{
  "surface_reelle_bati": 50,
  "nombre_pieces_principales": 3,
  "code_departement": "75",
  "type_local": "Appartement",
  "code_commune": "75115"
}'
```

4.2 CLI (automation / internal tools)

Single prediction:

```bash
cesar predict-one run \
  --surface 50 \
  --pieces 3 \
  --departement 75 \
  --type Appartement \
  --commune 75115
```

Batch prediction:

```bash
cesar batch run --input input.csv --output output.csv
```



Open in browser:

[http://localhost:5173](http://localhost:5173)

