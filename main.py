import logging
from core import spotify_service
from google.cloud import storage
import config

# Configure logging
logging.basicConfig(level=logging.INFO)

DESTINATION_PLAYLIST = config.PlaylistConfig.PLAYLIST_DESTINATION
PLAYLISTS_TO_SCRAPE = config.PlaylistConfig.PLAYLISTS_TO_SCRAPE


def find_new_tracks(destination_playlist_tracks, scraped_playlist_tracks):
    """
    Identifies tracks in the scraped playlists that are not present in the destination playlist.

    Args:
        destination_playlist_tracks (list): List of track IDs in the destination playlist.
        scraped_playlist_tracks (list): List of track IDs from the scraped playlists.

    Returns:
        list: A list of track IDs that are in the scraped playlists but not in the destination playlist.
    """
    tracks_to_add = []
    for track in scraped_playlist_tracks:
        if track not in destination_playlist_tracks:
            tracks_to_add.append(track)

    return tracks_to_add


def main(gcp_arg):
    """
    The entry point and logic handling of the process.

    Args:
        gcp_arg (str): A string argument typically used for logging or configuration,
        which is specific to Google Cloud Platform (GCP) services.

    Returns:
        list: A list of track IDs that are in the scraped playlists but not in the destination playlist.
    """
    logging.info(f"Initiated script from source: {gcp_arg}")
    logging.info(f"Running in GCP mode: {config.EnvironmentConfig.GCP_MODE}")
    
    try:
        logging.info("Attempting to create Spotify service...")
        service = spotify_service.SpotifyService()
        logging.info("Created Spotify service!")
    except Exception as e:
        logging.error(f"Error retrieving destination playlist tracks: {e}")
        return False

    logging.info("Retrieving destination playlist tracks...")
    try:
        destination_playlist_tracks = service.retrieve_tracks_from_playlist(
            DESTINATION_PLAYLIST
        )
        destination_playlist_size = len(destination_playlist_tracks)
        logging.info(f"Retrieved {destination_playlist_size} tracks from playlist!")
    except Exception as e:
        logging.error(f"Error retrieving destination playlist tracks: {e}")
        return False
    
    if destination_playlist_size >= config.SpotifyConfig.SPOTIFY_PLAYLIST_MAX_TACKS:
        raise Exception("Playlist exceeds maximum allowed tracks.")

    # Retrieve and compile tracks from all playlists to scrape
    logging.info(f"Retrieving tracks from {len(PLAYLISTS_TO_SCRAPE)} playlists...")
    scraped_playlist_tracks = []
    for playlist in PLAYLISTS_TO_SCRAPE:
        try:
            retrieved_playlist_tracks = service.retrieve_tracks_from_playlist(playlist)
            scraped_playlist_tracks.extend(retrieved_playlist_tracks)
        except Exception as e:
            logging.error(f"Error retrieving tracks from playlist {playlist}: {e}")

        logging.info(
            f"Found {len(retrieved_playlist_tracks)} tracks in scraped playlist: {playlist}"
        )

    logging.info(
        f"Found {len(scraped_playlist_tracks)} total tracks in scraped playlists"
    )
    tracks_to_add = find_new_tracks(
        destination_playlist_tracks, scraped_playlist_tracks
    )

    logging.info(f"Found {len(tracks_to_add)} unique tracks: {tracks_to_add}")
    if tracks_to_add:
        try:
            service.add_tracks_to_playlist(DESTINATION_PLAYLIST, tracks_to_add)
            logging.info("Added to playlist!")
        except Exception as e:
            logging.error(f"Error adding tracks to destination playlist: {e}")

    if config.EnvironmentConfig.GCP_MODE:
        logging.info(f"Attempting to upload cache file to GCP bucket")
        try:
            service.upload_refreshed_cache_token()
            logging.info(f"Upload cache file to GCP bucket success!")
        except Exception as e:
            logging.error(f"Error uploading cache file to GCP bucket: {e}")

    return ("Complete.", 200)


if __name__ == "__main__":
    main("Running locally.")
