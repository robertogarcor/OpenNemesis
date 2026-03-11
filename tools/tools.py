import logging
import requests
from datetime import datetime
import os

def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    try:
        response = requests.get(f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            logging.info(f"Weather for {city}: {response.text.strip()}")
            return response.text.strip()
        else:
            logging.error(f"Failed to get weather for {city}: {response.status_code}")
            return f"Could not retrieve weather for {city}."
    except Exception as e:
        logging.error(f"Error retrieving weather for {city}: {e}")
        return f"An error occurred while retrieving weather for {city}."


def get_time() -> str:
    """Get current time."""
    try:
        now = datetime.now()
        return f"Hora actual: {now.strftime('%H:%M:%S')}\nFecha: {now.strftime('%Y-%m-%d')}"
    except Exception as e:
        logging.error(f"Error retrieving time: {e}")
        return f"An error occurred while retrieving time."
