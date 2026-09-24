from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import ais_service

app = FastAPI(
    title="Varde Horizon API",
    description="Geospatial OSINT API for real-time AIS maritime tracking in Norwegian waters.",
    version="0.1.0"
)

# Enable CORS for future Next.js frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory token cache (simple optimization)
token_cache = {"token": None}

@app.get("/")
def read_root():
    return {"status": "online", "system": "Varde Horizon OSINT Engine"}

@app.get("/api/v1/vessels")
def get_vessels():
    """
    Fetches live AIS vessel positions from BarentsWatch.
    """
    # Obtain or reuse access token
    if not token_cache["token"]:
        token_cache["token"] = ais_service.get_access_token()

    if not token_cache["token"]:
        raise HTTPException(status_code=500, detail="Failed to authenticate with BarentsWatch")

    positions = ais_service.fetch_live_positions(token_cache["token"])

    # If token expired (HTTP error), refresh once and retry
    if not positions:
        token_cache["token"] = ais_service.get_access_token()
        positions = ais_service.fetch_live_positions(token_cache["token"])

    return {
        "count": len(positions),
        "vessels": positions
    }