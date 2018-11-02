import unittest
from unittest import mock
import spotify


class SpotifyTestCase(unittest.TestCase):
    """Tests for spotify.py"""

    def test_create_playlist(self):
        """Agent can succesfully create playlists."""
        # patch __init__ to return None (avoids config, prompt for token, etc.)
        with mock.patch.object(spotify.SpotifyAgent,
                               "__init__",
                               lambda self, name, scope, config: None):
            sp = spotify.SpotifyAgent("test_user", "test_scope", "test_file")
            sp.username = "test_username"

            mock_agent = mock.MagicMock()
            mock_playlist = mock.MagicMock()
            sp.agent = mock_agent
            sp.agent.user_playlist_create = mock_playlist

            sp.create_playlist("test_pl_name", "test_pl_desc")
            assert(mock_playlist.call_count > 0)


if __name__ == "__main__":
    unittest.main()
