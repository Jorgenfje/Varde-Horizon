import os
import requests
from dotenv import load_dotenv

# Load environment variables from local .env file
load_dotenv()

# Retrieve BarentsWatch OAuth2 API credentials from environment
CLIENT_ID = os.getenv("BARENTSWATCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("BARENTSWATCH_CLIENT_SECRET")

def get_access_token():
    """
    Requests an OAuth2 Client Credentials access token from BarentsWatch Identity Provider.

    Returns:
        str or None: Bearer access token string if successful, None otherwise.
    """
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: Missing BARENTSWATCH_CLIENT_ID or BARENTSWATCH_CLIENT_SECRET in environment.")
        return None

    token_url = "https://id.barentswatch.no/connect/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'api'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    try:
        response = requests.post(token_url, data=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get('access_token')
        
        print(f"Authentication failed [Status {response.status_code}]: {response.text[:200]}")
        return None
    except requests.RequestException as e:
        print(f"Network error requesting access token: {e}")
        return None


def fetch_live_positions(token):
    """
    Fetches open real-time AIS vessel positions for Norwegian waters from BarentsWatch API.

    Args:
        token (str): Valid OAuth2 Bearer token obtained from get_access_token().

    Returns:
        list: A list of vessel position records (dictionaries), or empty list on failure.
    """
    api_url = "https://www.barentswatch.no/bwapi/v1/geodata/ais/openpositions"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json()
        
        print(f"API Error [Status {response.status_code}]: {response.text[:200]}")
        return []
    except requests.RequestException as e:
        print(f"Network error fetching AIS positions: {e}")
        return []