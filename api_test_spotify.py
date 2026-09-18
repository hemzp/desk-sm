import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="c4caf170a9b747db8cefc2f0795e9b90",
    client_secret="f54b467432cc476cb21c777617f715aa",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-read-currently-playing user-read-playback-state"))

playback = sp.current_playback()

if playback and playback.get("item"):
    item = playback["item"]
    print("Track:   ", item["name"])
    print("Artist:  ", ", ".join(a["name"] for a in item["artists"]))
    print("Album:   ", item["album"]["name"])
    print("Art URL: ", item["album"]["images"][0]["url"])
    progress_ms = playback["progress_ms"]
    duration_ms = item["duration_ms"]
    print(f"Progress: {progress_ms // 1000}s / {duration_ms // 1000}s")
else:
    print("Nothing playing right now.")