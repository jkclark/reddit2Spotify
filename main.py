import praw
import pickle
import spotify
import sys


class User():
    def __init__(self, username, scope, credentials_dict):
        self.username = username
        self.scope = scope
        self.credentials_dict = credentials_dict

        self.token = self.requestToken()

    def getUsername(self):
        return self.username

    def getScope(self):
        return self.scope

    def getCredentialsDict(self):
        return self.credentials_dict

    def requestToken(self):
        token = spotify.get_user_token(
                    self.username,
                    self.scope,
                    self.credentials_dict,
                )
        return token

    def getToken(self):
        return self.token


def load_credentials(credentials_pickle_file):
    try:
        with open(credentials_pickle_file, 'rb') as c:
            return pickle.load(c)
    except IOError:
        print("Error: Couldn't open credentials file. Exiting.")


def main():
    print("Loading credentials from credentials file...")
    credentials = load_credentials("reddit_credentials.p")

    user_agent = "reddit2Spotify by /u/zelfed"
    reddit = praw.Reddit(client_id=credentials["CLIENT_ID"],
                         client_secret=credentials["CLIENT_SECRET"],
                         password=credentials["PASSWORD"],
                         user_agent=user_agent,
                         username=credentials["USERNAME"])

    print("User:", reddit.user.me())

    sp_username = sys.argv[1]
    sp_scope = "playlist-modify-public"
    sp_credentials = load_credentials("spotify_credentials.p")
    sp_agent = spotify.SpotifyAgent(sp_username,
                                    sp_scope,
                                    sp_credentials)

    # Subreddits to create playlists for
    subreddits = ['edm']

    for subreddit in subreddits:
        # Create playlist
        playlist_name = f"TEST - r/{subreddit}"
        playlist_desc = "A test playlist from Josh"
        playlist = sp_agent.create_playlist(playlist_name, playlist_desc)
        playlist_id = playlist['id']

        # Fetch top posts
        subreddit = reddit.subreddit('edm')

        # dir(object) returns a list of attributes for object
        for post in subreddit.top('week'):
            is_new = (post.link_flair_text == "New")
            is_spotify = ("spotify" in post.url)
            is_track = ("track" in post.url)
            if is_new and is_spotify and is_track:
                print("New Spotify track:", post.url)
                valid_part = post.url.split('?')[0]
                sp_agent.add_songs_to_playlist([valid_part], playlist_id)


if __name__ == "__main__":
    main()
