import os
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException

from runtime.inference.load_artifact import load_artifact_from_path, ArtifactNotFoundError
from runtime.inference.estimate_from_artifact import estimate_from_model, InvalidFeatureError
from prediction_contract.request_schema import EstimateRequest
from prediction_contract.response_schema import EstimateResponse
from prediction_contract.contract_version import ContractVersion

app = FastAPI(title="CESAR Prediction API", version="0.1.0")

# Load the model and contract once and reuse for every request. We cache in _loaded so we do not
# read from disk on each call. If CESAR_MODEL_PATH or CESAR_CONTRACT_PATH are missing, we return 503
# (service unavailable) so callers know the API is not ready yet.
_loaded: tuple[object, ContractVersion] | None = None


def get_artifact() -> tuple[object, ContractVersion]:
    global _loaded
    if _loaded is not None:
        return _loaded
    model_path = Path(os.environ.get("CESAR_MODEL_PATH", ""))
    contract_path = Path(os.environ.get("CESAR_CONTRACT_PATH", ""))
    if not model_path or not contract_path:
        raise HTTPException(status_code=503, detail="API is down. Model and contract paths are not configured.")
    try:
        _loaded = load_artifact_from_path(model_path, contract_path)
        return _loaded
    except ArtifactNotFoundError as e:
        raise HTTPException(status_code=503, detail=f"API is down. Could not load model or contract from disk: {e}")

''' Injected get_artifact() as a FastAPI dependency, FastAPI calls get_artifact() before running the function body.
    If CESAR_MODEL_PATH or CESAR_CONTRACT_PATH are not set then get_artifact() raises HTTP 503.
    If either file is missing or unreadable , then also get_artifact() will raise HTTP 503.
    Only if both files load successfully , the execution will reach the return stage
    '''
@app.get("/health")
def health(

    artifact: Annotated[tuple[object, ContractVersion], Depends(get_artifact)],
) -> dict[str, object]:
    # ContractVersion will tells us everything our operator needs to verify that the right
    # model version is deployed and which features it expects.
    _, contract = artifact

    # Returns the live contract metadata alongside "status: ok".
    # This lets monitoring tools (or the future chatbot) confirm not just that the API
    # is alive but also *which* model is running and what its expected input looks like.
    return {
        "status": "API is up and running. Model and contract loaded successfully.",
        "model_version": contract.model_version,
        "feature_names": contract.feature_names,
        "target_name": contract.target_name,
    }


@app.post("/estimate/", response_model=EstimateResponse)
def post_estimate(
    request: EstimateRequest,
    artifact: Annotated[tuple[object, ContractVersion], Depends(get_artifact)],
) -> EstimateResponse:
    model, contract = artifact
    try:
        return estimate_from_model(model, request, contract)
    except InvalidFeatureError as e:
        raise HTTPException(status_code=422, detail=str(e))
