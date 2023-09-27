"""
Spotify Authentication Helper
Developed by [Your Name]
Description: This script is designed to facilitate the OAuth2 authorization flow with the Spotify API.
             The script uses the `spotipy` Python library and tkinter for the graphical interface.
             It guides the user through the process of authorizing the application, opening a web browser
             for the user to log in to their Spotify account, and then prompts the user to enter the
             authorization code from the redirected URL. Once the authorization code is verified,
             the script fetches the access and refresh tokens. It then saves the refresh token
             into the `.env` file for future use.

Dependencies:
    - spotipy: A lightweight Python library for accessing the Spotify Web API.
    - python-dotenv: A Python module that allows easy reading of .env files.
    - tkinter: A built-in Python library for creating simple GUI applications.
    - webbrowser: A built-in Python module to open web browsers.
"""
import os
import webbrowser

import tkinter as tk
from dotenv import load_dotenv
from spotipy import SpotifyOAuth
from tkinter import messagebox, simpledialog

# Load environment variables
load_dotenv()

sp_oauth = SpotifyOAuth(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    redirect_uri=os.getenv("REDIRECT_URI"),  # Use a valid redirect URI
    scope="user-library-read user-modify-playback-state"
)

auth_url = sp_oauth.get_authorize_url()

root = tk.Tk()
root.withdraw()  # Hide the root window

messagebox.showinfo("Authorization", f"Please visit this URL to authorize the application: {auth_url}")

# Open the auth_url in a web browser
webbrowser.open(auth_url)

code = simpledialog.askstring("Authorization", "Enter the code from the redirect URL:")

# Check for a valid code entry and prompt again if not valid
while not code:
    messagebox.showwarning("Invalid Code", "Please enter a valid code.")
    code = simpledialog.askstring("Authorization", "Enter the code from the redirect URL:")

token_info = sp_oauth.get_cached_token()

if not token_info:
    token_info = sp_oauth.get_access_token(code=code)

refresh_token = token_info['refresh_token']

# Read the contents of the .env file and update the SPOTIPY_REFRESH_TOKEN value
with open('.env', 'r') as file:
    lines = file.readlines()

with open('.env', 'w') as file:
    for line in lines:
        if line.startswith('SPOTIPY_REFRESH_TOKEN'):
            file.write(f'SPOTIPY_REFRESH_TOKEN={refresh_token}\n')
        else:
            file.write(line)

root.destroy()  # Destroy the root window when done
