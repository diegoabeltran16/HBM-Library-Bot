import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv('configs/.env')

# Retrieve Microsoft Graph credentials from environment variables
MS_CLIENT_ID = os.getenv('MS_CLIENT_ID')
MS_CLIENT_SECRET = os.getenv('MS_CLIENT_SECRET')
MS_TENANT_ID = os.getenv('MS_TENANT_ID')

# Microsoft Graph authentication URL
AUTH_URL = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"



def get_access_token():
    """
    Authenticates with Microsoft Graph using the client credentials flow
    and retrieves an access token.

    Returns:
    str: The access token for making Microsoft Graph API requests.
    """
    try:
        # Prepare the request payload
        data = {
            "client_id": MS_CLIENT_ID,
            "client_secret": MS_CLIENT_SECRET,
            "scope": "https://graph.microsoft.com/.default",
            "grant_type": "client_credentials"
        }

        # Send a POST request to the authentication URL
        response = requests.post(AUTH_URL, data=data)
        response.raise_for_status()  # Raise an error if the request fails

        # Parse the JSON response to get the access token
        access_token = response.json().get("access_token")
        return access_token

    except requests.exceptions.RequestException as e:
        print(f"Error during authentication: {e}")
        print(f"Response content: {response.content}")  # Log the response content
        return None
