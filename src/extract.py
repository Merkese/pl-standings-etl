import os
import requests
from dotenv import load_dotenv



def get_standings(LEAGUE_ID = 47):
    """
    Gathers standings data from the API connection. 
    """
# Loads credentials
    load_dotenv()

    API_KEY = os.getenv("API_KEY")
    API_HOST = os.getenv("API_HOST")
    API_URL = os.getenv("API_URL")

    # API parameters
    querystring = {"leagueid":LEAGUE_ID}
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST,
        "Content-Type": "application/json"}
    
    # Sends request to API
    response = requests.get(
        API_URL,
        headers=headers, 
        # (league) parameter 
        params=querystring)

    payload = response.json()
    return payload["response"]["standing"]