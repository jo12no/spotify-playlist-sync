import os


class SpotifyConfig:
    """
    Configuration settings specific to the Spotify API.

    Attributes:
        SPOTIPY_SCOPE (str): The scope of access required from Spotify to perform
                             playlist and library actions (write).
        SPOTIFY_CLIENT_ID (str): The Client ID provided by Spotify when you register
                             your application. This should be kept secret.
        SPOTIFY_CLIENT_SECRET (str): The Client Secret provided by Spotify upon
                             application registration.
                             This should also be kept confidential.
        SPOTIFY_RATE_LIMIT (float): Precautionary limit to avoid rate limiting (secs).
        SPOTIFY_PLAYLIST_MAX_TACKS (int): Must be less than 10k to avoid the cap. 
    """

    SPOTIPY_SCOPE = "playlist-modify-public playlist-modify-private user-library-read"
    SPOTIFY_CLIENT_ID = ""
    SPOTIFY_CLIENT_SECRET = ""

    SPOTIFY_RATE_LIMIT = 0.5  # in seconds
    SPOTIFY_PLAYLIST_MAX_TACKS = 9050


class PlaylistConfig:
    """
    Add your destination and source playlist IDs here.

    Attributes:
        PLAYLISTS_TO_SCRAPE (str): Playlists to grab tracks from.
        PLAYLIST_DESTINATION (str): Destination playlist to add new tracks into.
    """

    PLAYLISTS_TO_SCRAPE = ["", ""]
    PLAYLIST_DESTINATION = ""  


class EnvironmentConfig:
    """
    Configuration settings for the application locally or Google Cloud Platform (GCP).

    Attributes:
        CACHE_FILE_NAME (str):Filename used to cache data locally or in cloud storage.
        GCP_MODE (bool): Flag to indicate if the application is running on GCP.
        LOCAL_CACHE_DIR (str): Local directory path for caching.
        LOCAL_CACHE_PATH (str): Full local file path for caching.
        GCP_BUCKET_NAME (str): Name of the GCP bucket used for caching.
        GCP_CACHE_DIR (str): Directory path in GCP where cache files are stored.
        GCP_CACHE_PATH (str): Full file path in GCP for caching.
    """

    CACHE_FILE_NAME = ".cache"

    # Enviroment setting
    GCP_MODE = True  # True --> running on GCP

    # Local settings
    LOCAL_CACHE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOCAL_CACHE_PATH = os.path.join(LOCAL_CACHE_DIR, CACHE_FILE_NAME)

    # Cloud Storage bucket details
    GCP_BUCKET_NAME = "spotipy-cache"
    GCP_CACHE_DIR = "/tmp/"
    GCP_CACHE_PATH = os.path.join(GCP_CACHE_DIR, CACHE_FILE_NAME)
