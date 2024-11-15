import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from mutagen.flac import FLAC
import os
import re

### REMEMBER TO ADD YOUR SPOTIFY API TOKENS!!! ###
SPOTIFY_CLIENT_ID = 'your_client_id'
SPOTIFY_CLIENT_SECRET = 'your_client_secret'

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

ASCII_ART = """   
       FLAC Genre Tagger with Spotify       

       Created by SteadyStatus21, uses Spotify's API
"""

def get_genre_from_spotify(track_name, artist_name):
    # Primary search using explicit filters
    query = f"track:{track_name} artist:{artist_name}"
    results = spotify.search(q=query, type="track", limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        artist_id = track['artists'][0]['id']
        artist_info = spotify.artist(artist_id)
        return artist_info.get('genres', [])

    # Fallback search: Clean track name to remove "(feat. ...)"
    print(f"[🔄 - RETRY] Trying fallback search for track: {track_name} by {artist_name}")
    cleaned_track_name = re.sub(r"\(feat\..*?\)", "", track_name, flags=re.IGNORECASE).strip()
    query = f"track:{cleaned_track_name} artist:{artist_name}"
    results = spotify.search(q=query, type="track", limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        artist_id = track['artists'][0]['id']
        artist_info = spotify.artist(artist_id)
        return artist_info.get('genres', [])

    # Final fallback: Search by track name only
    print(f"[🔄 - RETRY] Trying search with track name only: {track_name}")
    query = f"track:{track_name}"
    results = spotify.search(q=query, type="track", limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        artist_id = track['artists'][0]['id']
        artist_info = spotify.artist(artist_id)
        return artist_info.get('genres', [])

    return []

def update_flac_metadata(file_path, genre):
    audio = FLAC(file_path)
    audio['GENRE'] = genre
    audio.save()

def process_flac_files(folder_path):
    print(ASCII_ART)
    print(f"🔎📁 Scanning for FLAC files in: {folder_path}")
    print("=" * 50)

    # Collect all FLAC files first to determine total count
    flac_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.flac'):
                flac_files.append(os.path.join(root, file))

    total_files = len(flac_files)
    print(f"Found {total_files} FLAC file(s) to process.")
    print("=" * 50)

    processed_count = 0
    skipped_count = 0

    for file_path in flac_files:
        file = os.path.basename(file_path)
        audio = FLAC(file_path)

        if 'GENRE' in audio and audio['GENRE']:
            skipped_count += 1
            print(f"[⏩ - SKIP] {file} - Genre already exists: {audio['GENRE'][0]}")
        else:
            track_name = audio.get('title', [None])[0]
            artist_name = audio.get('artist', [None])[0]

            if track_name and artist_name:
                print(f"[🔎 - SEARCH] {file} - Searching genre for: {track_name} by {artist_name}")
                genres = get_genre_from_spotify(track_name, artist_name)

                if genres:
                    genre = ', '.join(genres)
                    print(f"[✅ - UPDATE] {file} - Found genre(s): {genre}")
                    update_flac_metadata(file_path, genre)
                    processed_count += 1
                else:
                    print(f"[❌ - NOT FOUND] {file} - No genre found on Spotify")
            else:
                print(f"[❓ - MISSING METADATA] {file} - Missing title or artist. Skipping.")
                skipped_count += 1

            time.sleep(1)  # Delay of 1 second to prevent rate limiting through Spotify's API

    print("=" * 50)
    print(f"🏁✅ - Finished processing! {processed_count} file(s) updated, {skipped_count} file(s) skipped.")
    print("All done!")

if __name__ == "__main__":
    current_directory = os.getcwd()
    print(f"Starting script in directory: {current_directory}")
    process_flac_files(current_directory)
