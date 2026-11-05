import os
import requests
from dotenv import load_dotenv

# Max seconds to wait for the API before giving up
TIMEOUT_SECONDS = 10


def _require_env(name):
    """
    Returns an environment variable, or raises if it is missing.
    """
    value = os.getenv(name)
    # Raises on empty/unset values as missing
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _fetch(url_env, league_id):
    """
    Sends a GET request to the URL stored in the given env var and returns the parsed JSON.
    """
    # Loads credentials
    load_dotenv()

    # Reads the endpoint URL and builds the RapidAPI auth headers
    url = _require_env(url_env)
    headers = {
        "x-rapidapi-key": _require_env("API_KEY"),
        "x-rapidapi-host": _require_env("API_HOST"),
        "Content-Type": "application/json"}

    # Sends request to API
    response = requests.get(
        url,
        headers=headers,
        # league parameter
        params={"leagueid": league_id},
        timeout=TIMEOUT_SECONDS)

    # Raises HTTPError on 400/500 for bad keys or outages
    response.raise_for_status()
    return response.json()


def _get_response_field(payload, *keys):
    """
    Returns payload, otherwise raises if the shape is unexpected.
    """
    try:
        # Descends one key at a time, e.g. payload["response"]["standing"]
        for key in keys:
            payload = payload[key]
        return payload
    # KeyError: key absent. TypeError: a level was not a dict (e.g. None)
    except (KeyError, TypeError) as e:
        raise ValueError(f"Unexpected API response shape, missing key {e}") from e


def get_standings(LEAGUE_ID = 47):
    """
    Gathers standings data from the API connection.
    """
    # API_URL points at the standings endpoint
    payload = _fetch("API_URL", LEAGUE_ID)
    return _get_response_field(payload, "response", "standing")


def league_details(LEAGUE_ID = 47):
    """
    Gathers league and season data from the API connection.
    """
    # API_URL2 points at the league details endpoint
    payload = _fetch("API_URL2", LEAGUE_ID)
    return _get_response_field(payload, "response", "leagues")
