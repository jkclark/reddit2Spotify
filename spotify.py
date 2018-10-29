import sys
import spotipy
import spotipy.util as util


class SpotifyAgent():
    def __init__(self, username, scope, creds):
        self.username = username
        self.scope = scope
        self._client_id = creds["SPOTIPY_CLIENT_ID"]
        self._client_secret = creds["SPOTIPY_CLIENT_SECRET"]
        self._redirect_uri = creds["SPOTIPY_REDIRECT_URI"]
        self.token = util.prompt_for_user_token(username,
                                                scope,
                                                self._client_id,
                                                self._client_secret,
                                                self._redirect_uri)
        if self.token is None:
            print("Error: Failed to create token.", file=sys.stderr)

        self.agent = spotipy.Spotify(auth=self.token)

    def create_playlist(self, name, description, public=True):
        """Create a playlist named (name) with description (description).

        Args:
            name (string): The name of playlist to be created.
            description (string): The description of playlist to be created.
            public (bool, optional): Public if True, private otherwise.

        Returns:
            A playlist object representing the new playlist.

        """
        playlist = self.agent.user_playlist_create(self.username,
                                                   name,
                                                   public,
                                                   description)
        if playlist is None:
            print("Error: Failed to create playlist.", file=sys.stderr)
        return playlist

    def add_songs_to_playlist(self, track_ids, playlist_id):
        """Add each song in (track_ids) to (playlist_id).

        Args:
            track_ids (list of strings): A list of track URIs, URLs, or IDs.
            playlist_id (string): The ID of the playlist.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.agent.user_playlist_add_tracks(self.username,
                                                playlist_id,
                                                track_ids)
            return True
        except spotipy.client.SpotifyException as fail:
            sp_error_message = fail.args[-1].split('\n')[-1].strip()
            full_error = f"Error: {sp_error_message}"
            print(full_error, file=sys.stderr)
            return False
