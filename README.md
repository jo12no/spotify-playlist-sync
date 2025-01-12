# Spotify Playlist Sync 🎧🎵
Automates syncing tracks from one or multiple Spotify playlists into a single destination playlist. 

Ensures your curated collection stays up-to-date with new additions (or removals) from source playlists.

It can be scheduled to run (eg. daily) or run manually. 

## Technical Infrastructure


The GCP (Google Cloud Platform) portion is skipped if running locally. 

## Usage
* The script can be run manually `main.py` or scheduled to run (eg. daily) via `cron` or Cloud. 

## Getting Started
* Add your Spotify API info to either the `config.py` file or optionally if preferred as an environment variable via terminal:
_export SPOTIFY_CLIENT_ID="KEY"_
* Add your `destination playlist` ID and `source playlists` to check for in the `config.py` file. 
* You can find playlist IDs a few ways, eg. in Spotify `right click > share playlist > copy link` and copy the ID. 
* Install required libraries using `pip install -r requirements.txt`.
* Run the script. 

## Installation

Before running the script, you need to ensure you have Python installed on your system and the necessary Python package:

```
pip install -r requirements.txt
```

## Dependencies

- Python 3.x
- `spotipy`

## _Optional_ Cloud Configuration
* Enable Cloud mode in `config.py`.
* After following the auth prompts locally, Spotipy saves credentials in `.cache` which can be used if scheduling in a server-to-server manner (which would prevent auth via browser). 
* This file can be saved in a Cloud Storage Bucket, which the script will use instead of saving `.cache` to the local working directory (which is the Spotipy default).
* Add your Cloud bucket info to the `config.py` file if wanting to use this method. 
* We do not typically want files to persist in memory for Cloud functions, which is avoided using the Cloud Storage Bucket. 


## Acknowledgments

- Thanks to Spotify for providing a great API and the `spotipy` library! 

## Contributions

- Are welcomed! 😃 

