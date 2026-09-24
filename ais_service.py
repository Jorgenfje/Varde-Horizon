import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CLIENT_ID = os.getenv("BARENTSWATCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("BARENTSWATCH_CLIENT_SECRET")

def get_access_token():
    """
    Requests an OAuth2 bearer token from the BarentsWatch authentication server.
    """
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: Missing BarentsWatch credentials in environment variables.")
        return None

    url = "https://id.barentswatch.no/connect/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'api'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get('access_token')
        return None
    except Exception as e:
        print(f"Error fetching access token: {e}")
        return None

def fetch_live_positions(token):
    """
    Fetches real-time AIS vessel positions using a valid OAuth2 bearer token.
    """
    url = "https://www.barentswatch.no/bwapi/v1/geodata/ais/openpositions"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching live positions: {e}")
        
    return []