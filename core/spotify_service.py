import os
import time
import config
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from google.cloud import storage


class SpotifyService:
    """
    Provides a service layer for interacting with the Spotify API.

    This class handles authentication and provides methods to interact with
    the Spotify API, such as creating playlists, searching for tracks,
    adding tracks to playlists, and fetching user playlist information.
    """

    def __init__(self):
        """
        Initializes the SpotifyService with necessary credentials and scopes.

        The client ID, client secret, and scopes are retrieved from environment variables
        or a configuration object. An authenticated spotipy.Spotify client is created.
        """
        self.SPOTIPY_CLIENT_ID = os.getenv(
            "SPOTIFY_CLIENT_ID", config.SpotifyConfig.SPOTIFY_CLIENT_ID
        )
        self.SPOTIPY_CLIENT_SECRET = os.getenv(
            "SPOTIFY_CLIENT_SECRET", config.SpotifyConfig.SPOTIFY_CLIENT_SECRET
        )
        self.SPOTIPY_REDIRECT_URI = "http://localhost/"
        self.SPOTIPY_SCOPE = config.SpotifyConfig.SPOTIPY_SCOPE

        self.storage_client = None
        self.bucket = None
        self.blob = None

        if config.EnvironmentConfig.GCP_MODE:
            self.initialize_gcp_storage()

        self.sp = self.create_spotipy_client()

    def initialize_gcp_storage(self):
        """
        Initializes the GCP storage client, bucket, and blob.
        """
        try:
            self.storage_client = storage.Client()
            self.bucket = self.storage_client.bucket(
                config.EnvironmentConfig.GCP_BUCKET_NAME
            )
            self.blob = self.bucket.blob(config.EnvironmentConfig.CACHE_FILE_NAME)
        except Exception as e:
            print(f"Error initializing GCP storage: {e}")

    def create_spotipy_client(self):
        """
        Creates an authenticated Spotify client using OAuth.

        Returns:
            spotipy.Spotify: An authenticated spotipy.Spotify client instance.
        """
        cache_path = (
            config.EnvironmentConfig.GCP_CACHE_PATH
            if config.EnvironmentConfig.GCP_MODE
            else config.EnvironmentConfig.LOCAL_CACHE_PATH
        )

        handler = spotipy.oauth2.CacheFileHandler(cache_path=cache_path)

        if config.EnvironmentConfig.GCP_MODE and self.blob and self.blob.exists():
            self.blob.download_to_filename(cache_path)

        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope=self.SPOTIPY_SCOPE,
                client_id=self.SPOTIPY_CLIENT_ID,
                client_secret=self.SPOTIPY_CLIENT_SECRET,
                redirect_uri=self.SPOTIPY_REDIRECT_URI,
                open_browser=False,
                cache_handler=handler,
            )
        )

        return sp

    def upload_refreshed_cache_token(self):
        """
        Uploads the refreshed cache token to the GCP bucket.
        """
        if config.EnvironmentConfig.GCP_MODE and os.path.exists(
            config.EnvironmentConfig.GCP_CACHE_PATH
        ):
            if self.blob:
                self.blob.upload_from_filename(config.EnvironmentConfig.GCP_CACHE_PATH)

    def retrieve_tracks_from_playlist(self, playlist_id):
        """
        Retrieves all track IDs from a specified Spotify playlist.

        This method fetches tracks from the given playlist ID and compiles a list of track IDs.
        It handles pagination to ensure all tracks are retrieved, adhering to Spotify's rate limits.

        Args:
            playlist_id (str): The Spotify ID of the playlist to retrieve tracks from.

        Returns:
            list: A list of track IDs contained in the specified playlist.
        """
        results = self.sp.playlist_tracks(playlist_id)
        track_list = []

        while results:
            track_list.extend(track["track"]["id"] for track in results["items"])
            results = self.sp.next(results)
            if results:
                time.sleep(config.SpotifyConfig.SPOTIFY_RATE_LIMIT)

        return track_list

    def add_tracks_to_playlist(self, playlist_id, tracks):
        """
        Adds a list of track IDs to a specified Spotify playlist.

        This method splits the list of track IDs into batches and adds them to the playlist,
        respecting Spotify's API limits on the number of tracks that can be added at once.

        Args:
            playlist_id (str): The Spotify ID of the playlist to add tracks to.
            tracks (list): A list of track IDs to be added to the playlist.

        Returns:
            None
        """
        batch_size = 100  # per Spotify API limits
        for i in range(0, len(tracks), batch_size):
            self.sp.playlist_add_items(playlist_id, tracks[i : i + batch_size])
            time.sleep(config.SpotifyConfig.SPOTIFY_RATE_LIMIT)
