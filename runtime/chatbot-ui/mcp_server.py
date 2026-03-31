from fastmcp import FastMCP
import httpx

mcp = FastMCP(name="Real Estate Estimate")
API_BASE_URL = "http://127.0.0.1:8000"

@mcp.tool()
async def get_property_estimate(
    surface_area: float,
    number_of_rooms: int,
    code_departement: str,
    type_local: str
) -> str:
    """
    Calculates the estimated value of a property based on its characteristics.
    Use this when a user asks about worth of a property.
    """

    payload = {
        "surface_reelle_bati": surface_area,
        "nombre_pieces_principales": number_of_rooms,
        "code_departement": code_departement,
        "type_local": type_local
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(f"{API_BASE_URL}/estimate/", json=payload)
        
        if response.status_code != 200:
            return f"Error from estimation API: {response.text}"
            
        data = response.json()
        val = data.get("estimated_value_eur")
        
        # Error hanlding if LLM works but the API breaks 
        if val is None:
            return "Error: The estimated value was not found in the API response."
        
        return f"Estimated Value: {val}€"

if __name__ == "__main__":
    mcp.run()