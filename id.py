"""
Spotify Device Lister
Developed by [Your Name]
Description: This script connects to the Spotify API using the `spotipy` Python library.
             It authenticates a user, obtains an access token, and lists all available devices
             that can control playback for the authenticated user.
             The script uses environment variables for client credentials and relies on the OAuth2 flow.

Dependencies:
    - spotipy: A lightweight Python library for accessing the Spotify Web API.
    - python-dotenv: A Python module that allows easy reading of .env files.
"""
import os

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables
load_dotenv()

sp_oauth = SpotifyOAuth(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    redirect_uri=os.getenv("REDIRECT_URI"),  # Use a valid redirect URI
    scope="user-library-read user-modify-playback-state user-read-playback-state"
)

# Get the access token
token_info = sp_oauth.get_access_token()
access_token = token_info['access_token']

# Create a Spotipy instance
sp = spotipy.Spotify(auth=access_token)

# List available devices
devices = sp.devices()
for device in devices['devices']:
    print(f"Device ID: {device['id']}, Device Name: {device['name']}")
