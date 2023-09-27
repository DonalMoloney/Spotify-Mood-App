"""
Mood-Based Spotify Player
Developed by [Your Name]
Description: This application captures a live video feed from the user's camera and uses facial
             emotion recognition to detect the user's current mood. Based on the detected mood,
             the application plays a song from a predefined artist associated with that mood on Spotify.
             The application offers a graphical user interface built with Tkinter and uses OpenCV
             for video capture and facial detection, DeepFace for emotion recognition, and Spotipy
             for Spotify API interactions.

Dependencies:
    - opencv-python: A library that contains functions for image and video analysis.
    - tkinter: A built-in Python library for creating simple GUI applications.
    - deepface: A deep learning framework for deep-face recognition.
    - PIL (Pillow): Python Imaging Library used for image processing.
    - python-dotenv: A Python module that allows easy reading of .env files.
    - spotipy: A lightweight Python library for accessing the Spotify Web API.
    - requests: A library for making HTTP requests.

Features:
    - Real-time mood detection from webcam feed.
    - Dynamic selection of artists based on the detected mood.
    - Playback control of Spotify based on detected emotions.
    - GUI interface using Tkinter.
"""
import os
import queue
import random
import threading

import cv2
import tkinter as tk
from PIL import Image, ImageTk
from deepface import DeepFace
from dotenv import load_dotenv
from requests import put, get
from spotipy import SpotifyOAuth

# Load environment variables from .env file
load_dotenv()

# Define mood artists
mood_artists = {
    "happy": ["Dua Lipa", "Bruno Mars"],
    "sad": ["Adele", "Billie Eilish"],
    "angry": ["Rage Against the Machine", "Eminem"],
    "surprised": ["David Bowie", "ROSALÍA"],
    "fearful": ["Halsey", "Lorde"],
    "disgusted": ["Nirvana", "Nine Inch Nails"],
    "neutral": ["John Mayer", "Ed Sheeran"]
}

# Function to get the Spotify access token
def get_token():
    # Create a SpotifyOAuth object with credentials and scope
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        scope="user-library-read user-modify-playback-state"
    )

    # Retrieve the Spotify refresh token from environment variables
    refresh_token = os.getenv("SPOTIPY_REFRESH_TOKEN")

    # Refresh the access token using the refresh token
    token_info = sp_oauth.refresh_access_token(refresh_token)

    return token_info["access_token"]

# Function to detect mood from a frame
def detect_mood(frame, q):
    try:
        # Use DeepFace to analyze the emotion in the frame
        predictions = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion_data = predictions[0]

        if 'emotion' in emotion_data and 'dominant_emotion' in emotion_data:
            emotion = emotion_data['dominant_emotion']
            q.put(emotion)
    except Exception as e:
        print(f"Unexpected error: {e}")

# Function to play a song on Spotify
def play_song(token, artist_name, device_id):
    # Search for tracks by the selected artist
    search_url = f"https://api.spotify.com/v1/search?q=artist%3A{artist_name.replace(' ', '%20')}&type=track&limit=1"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    # Send an HTTP GET request to Spotify to search for the artist's track
    search_response = get(search_url, headers=headers)

    if search_response.status_code == 200:
        track_data = search_response.json()
        if "tracks" in track_data and "items" in track_data["tracks"] and len(track_data["tracks"]["items"]) > 0:
            # Get the ID of the first track found for the artist
            track_id = track_data["tracks"]["items"][0]["id"]
            play_url = f"https://api.spotify.com/v1/me/player/play?device_id={device_id}"
            # Define the payload to play the track
            payload = {
                "uris": [f"spotify:track:{track_id}"]
            }
            # Send an HTTP PUT request to Spotify to start playback
            play_response = put(play_url, headers=headers, json=payload)

            if play_response.status_code == 204:
                print(f"Playback of {artist_name}'s song started successfully on device {device_id}.")
            else:
                print(f"Error starting playback: {play_response.status_code} - {play_response.text}")
        else:
            print(f"No tracks found for artist: {artist_name}")
    else:
        print(f"Error searching for artist: {search_response.status_code} - {search_response.text}")

# Function to play Spotify based on detected emotion
def play_spotify(emotion, device_id):
    token = get_token()

    # Convert the detected emotion to lowercase
    emotion = emotion.lower()

    # Check if the emotion exists in mood_artists or if it is 'neutral'
    if emotion in mood_artists:
        artists = mood_artists[emotion]
        selected_artist = random.choice(artists)
        print(f"Selected artist for {emotion}: {selected_artist}")

        # Call the play_song function with the selected artist and device ID
        play_song(token, selected_artist, device_id)
    else:
        print(f"No artists found for emotion: {emotion}")

# Function to capture and show the camera feed
def capture_and_show_screen(device_id):
    ret, frame = cap.read()

    if ret:
        # Use DeepFace to analyze the dominant emotion in the frame
        emotion_predictions = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        dominant_emotion = emotion_predictions[0]['dominant_emotion']
        print(dominant_emotion)
        # Play Spotify based on the detected emotion
        play_spotify(dominant_emotion, device_id)  # Play based on the detected emotion
    else:
        print("Unable to capture frame")


# Initialize the Tkinter window
root = tk.Tk()
root.title("Mood Detector App")

# Initialize the camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Create GUI elements
live_feed_label = tk.Label(root, text="Live Feed", font=("Helvetica", 16))
live_feed_label.pack()

label = tk.Label(root)
label.pack()

play_button = tk.Button(root, text="Play my vibe", command=lambda: capture_and_show_screen(os.getenv("DEVICE_ID")),
                        fg="white", bg="gray", height=2, width=15,
                        font=("Helvetica", 12, "bold"))
play_button.pack(pady=10)


q = queue.Queue()

running = True

while running:
    ret, frame = cap.read()

    if ret:
        faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml').detectMultiScale(
            frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face_roi = frame[y:y + h, x:x + w]
            threading.Thread(target=detect_mood, args=(face_roi, q)).start()

            try:
                emotion = q.get_nowait()
                cv2.putText(frame, emotion, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
                predictions = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
                emotion_data = predictions[0]
                other_emotions = {k: v for k, v in emotion_data['emotion'].items() if k != emotion}
                sorted_emotions = sorted(other_emotions.items(), key=lambda x: x[1], reverse=True)
                text = "Other Emotions:"
                for emo, score in sorted_emotions:
                    text += f" {emo}: {score:.2f},"
                text = text.rstrip(',')
                cv2.putText(frame, text, (10, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            except queue.Empty:
                pass

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(frame))
        label.config(image=img)
        label.image = img

    root.update_idletasks()
    root.update()

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Start the Tkinter main loop
root.mainloop()
