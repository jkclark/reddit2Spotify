import unittest
from unittest import mock
import spotify


class SpotifyTestCase(unittest.TestCase):
    """Tests for spotify.py"""

    def setUp(self):
        # patch __init__ to return None (avoids config, prompt for token, etc.)
        with mock.patch.object(spotify.SpotifyAgent,
                               "__init__",
                               lambda self, name, scope, config: None):
            self.sp = spotify.SpotifyAgent("test_user",
                                           "test_scope",
                                           "test_file")
            self.sp.username = "test_username"

    def test_create_playlist(self):
        """Agent can create playlists."""
        mock_agent = mock.MagicMock()
        mock_playlist_snapshot = mock.MagicMock()
        self.sp.agent = mock_agent
        self.sp.agent.user_playlist_create = mock_playlist_snapshot

        self.sp.create_playlist("test_pl_name", "test_pl_desc")
        assert(mock_playlist_snapshot.call_count > 0)

    def test_add_songs_to_playlist(self):
        """Agent can add songs to a playlist."""
        mock_agent = mock.MagicMock()
        mock_playlist_snapshot = mock.MagicMock()
        self.sp.agent = mock_agent
        self.sp.agent.user_playlist_add_tracks = mock_playlist_snapshot

        self.sp.add_songs_to_playlist(["test_track_id_1"], "test_pl_id")
        assert(mock_playlist_snapshot.call_count > 0)


if __name__ == "__main__":
    unittest.main()
