import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import time

# Spotify API credentials
SPOTIPY_CLIENT_ID = '0b260de8dc8a4a88a950bfa3cd455406'
SPOTIPY_CLIENT_SECRET = '4bac4237b2a44c44895f94cdff567fa9'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

# Spotify user authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="user-library-read user-read-playback-state"))

# Function to mute the system volume
def mute_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(1, None)

# Function to unmute the system volume
def unmute_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(0, None)

# Get the initial playback state to check if an ad is already playing
initial_track = sp.current_playback()

# Main loop
while True:
    track = sp.current_playback()
    
    # Check if an ad starts
    if initial_track and initial_track.get('currently_playing_type') != 'ad' and track and track.get('currently_playing_type') == 'ad':
        print("Muting volume during ad...")
        mute_volume()
    
    # Check if an ad ends
    elif initial_track and initial_track.get('currently_playing_type') == 'ad' and track and track.get('currently_playing_type') != 'ad':
        print("Unmuting volume after ad...")
        unmute_volume()
    
    # Update the initial track for the next iteration
    initial_track = track
    
    # Check every 10 seconds (adjust as needed)
    time.sleep(5)
