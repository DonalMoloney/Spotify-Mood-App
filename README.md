# Spotify-Mood-App



## Description

The Mood-Based Spotify Player is an interactive Python application that captures live video feed from the user's camera, analyzes facial expressions to detect the user's mood, and plays music on Spotify based on the detected mood. It offers a simple graphical user interface (GUI) and integrates with the Spotify API for music playback.

## Dependencies

- `opencv-python`: For video capture and processing.
- `tkinter`: For creating the graphical user interface.
- `deepface`: For facial emotion recognition.
- `PIL (Pillow)`: For image processing.
- `python-dotenv`: For managing environment variables.
- `spotipy`: For interacting with the Spotify Web API.
- `requests`: For making HTTP requests.

## Features

- Real-time mood detection from the webcam feed.
- Dynamic selection of artists based on the detected mood.
- Playback control of Spotify based on detected emotions.
- A user-friendly graphical user interface built with Tkinter.

## Getting Started

1. Obtain Spotify API credentials (client ID, client secret, and redirect URI) by creating a Spotify Application in your [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).

2. Start Spotify on your computer or mobile device.

3. Run `get_spotify.py` to initiate the OAuth2 authentication process. This script will open a web browser for you to log in to your Spotify account and authorize the application. Once authorized, it should retrieve and display the refresh token in the terminal.

4. Note down the `DEVICE_ID` of the Spotify device you want to control. You can obtain this device ID by running `id.py` provided in your code.

5. Create a `.env` file in the same directory as your script (if not already created).

6. Add the following environment variables to the `.env` file:

    ```
    CLIENT_ID=your_client_id
    CLIENT_SECRET=your_client_secret
    REDIRECT_URI=your_redirect_uri
    SPOTIPY_REFRESH_TOKEN=your_refresh_token
    DEVICE_ID=your_device_id
    ```

7. Execute the main script (`mood_based_spotify_player.py`) to start the application. The GUI interface will display the live video feed and allow you to interact with the application.

## Usage

- Launch the application and grant camera permissions.
- Click the "Play my vibe" button to detect your mood and play a song based on it.
- Enjoy music tailored to your mood!

## Credits

- [OpenCV](https://opencv.org/)
- [DeepFace](https://github.com/serengil/deepface)
- [Spotipy](https://spotipy.readthedocs.io/en/2.19.0/)

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Special thanks to the creators of the libraries and frameworks used in this project.

