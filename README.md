# Music Genre Tagger with Spotify Integration

### Overview
This project is a Python script designed to enhance your music library by automatically adding genre metadata to FLAC files. Using the Spotify API, the script fetches genre information based on the track's title and artist metadata and updates the FLAC files accordingly. 

### ⚠️Warning
Your FLAC files **MUST** contain valid **title** and **artist** tags. Use a tool like [MusicBrainz Picard](https://picard.musicbrainz.org/) to help automate this first process. 

### Features
- **Automatic Genre Detection**: Queries Spotify's database to fetch genre information.
- **Metadata Update**: Writes genre data into FLAC file metadata.
- **Skip Existing Genres**: Provides real-time logs during processing.
- **Batch Processing**: Processes all FLAC files in the working directory and all subdirectories.

### Requirements
1. Spotify Developer Account
	Sign up at [Spotify's Developer Dashboard](https://developer.spotify.com/dashboard/) and create a new app to get your:
	- `Client ID`
	- `Client Secret`
2. Python Libraries
    Install the following Python packages:
    ```pip install spotipy mutagen```

## Setup
1. Download the script from this repository
2. Add your API Credentials:
     - Open the script in your choice of text editor.
     - Replace `your_client_id` and `your_client_secret` with YOUR Spotify API credentials.

## Usage
1. Copy the Python file to your music directory
2. Run the file using the following command:
    `python genre_spotify.py`
3. The script will:
    - Search for FLAC files.
    - Query Spotify for genre metadata using the `title` and `artist` tags.
    - Update the FLAC file's metadata with the retrieved genre(s).
    - Provide a summary of processed and skipped files.

### Example Output
```
       FLAC Genre Tagger with Spotify       

       Created by SteadyStatus21, uses Spotify's API

🔎📁 Scanning for FLAC files in: /path/to/folder
==================================================
[🔎 - SEARCH] example.flac - Searching genre for: Song Title by Artist Name
[✅ - UPDATE] example.flac - Found genre(s): rock, alternative
[⏩ - SKIP] another_example.flac - Genre already exists: pop
[❓ - MISSING METADATA] missing_metadata.flac - Missing title or artist. Skipping.
==================================================
🏁✅ - Finished processing! 1 file(s) updated, 2 file(s) skipped.
All done!
```

### Notes
- Ensure your FLAC files have `title` and `artist` metadata filled. Files missing this information will be skipped entirely.
- The script includes a 1-second delay between Spotify API calls to prevent rate-limiting.

### License
This project is licensed under the GNU General Public License v3.0.

### Warranty
**This software is provided "as is," without any warranties, express or implied, including but not limited to fitness for a particular purpose or non-infringement. The author (SteadyStatus21) is not liable for any damages, data loss, or issues arising from its use. Use at your own risk.**

### Contributing
Feel free to fork the repository and submit your own pull requests! Contributions and improvements are always welcome!
