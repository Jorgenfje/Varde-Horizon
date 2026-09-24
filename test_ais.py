import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CLIENT_ID = os.getenv("BARENTSWATCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("BARENTSWATCH_CLIENT_SECRET")

def get_access_token():
    """
    Authenticate with BarentsWatch OAuth2 service to obtain a bearer token.
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
        print("Token error:", response.status_code, response.text)
        return None
    except Exception as e:
        print("Network error fetching token:", e)
        return None

def test_ais_connection(token):
    """
    Fetches real-time AIS vessel positions from the confirmed BarentsWatch endpoint.
    """
    url = "https://www.barentswatch.no/bwapi/v1/geodata/ais/openpositions"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        print(f"Connecting to endpoint: {url} ...")
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json()
        print(f"API Error status {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"Request failed: {e}")
        
    return None

if __name__ == "__main__":
    print("Fetching access token...")
    token = get_access_token()
    
    if token:
        print("Access token retrieved successfully!")
        data = test_ais_connection(token)
        
        if data:
            print(f"\nSuccess! Received live data for {len(data)} vessels.\n")
            print("Sample data from first element:")
            print(json.dumps(data[0], indent=2)[:500])
        else:
            print("\nFailed to retrieve AIS data.")