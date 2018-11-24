import praw
import spotify
import sys
import configparser
import gui
from PyQt5.QtWidgets import (QApplication)
from PyQt5.QtCore import pyqtSlot
#  import custom_console as cc


def tester():
    if len(sys.argv) < 2:
        print("Usage: main.py username", file=sys.stderr)
        exit(0)

    config = configparser.ConfigParser()
    config_file = "config.ini"
    # TODO: Change read to read_file for required config file
    config.read(config_file)
    reddit_creds = config["reddit"]

    user_agent = "reddit2Spotify by /u/zelfed"
    reddit = praw.Reddit(client_id=reddit_creds["CLIENT_ID"],
                         client_secret=reddit_creds["CLIENT_SECRET"],
                         password=reddit_creds["PASSWORD"],
                         user_agent=user_agent,
                         username=reddit_creds["USERNAME"])

    print("User:", reddit.user.me())

    sp_username = sys.argv[1]
    sp_scope = "playlist-modify-public"
    sp_agent = spotify.SpotifyAgent(sp_username,
                                    sp_scope,
                                    config_file)

    # Subreddits to create playlists for
    subreddits = ["edm"]
    time_period = "week"

    for subreddit in subreddits:
        # Create playlist
        playlist_name = f"TEST - r/{subreddit}"
        playlist_desc = f"Top posts on /r/{subreddit} from the past\
                         {time_period}"
        playlist = sp_agent.create_playlist(playlist_name, playlist_desc)
        playlist_id = playlist["id"]

        # Fetch top posts
        subreddit = reddit.subreddit(subreddit)

        # dir(object) returns a list of attributes for object
        for post in subreddit.top(time_period):
            #  is_new = (post.link_flair_text == "New")
            is_new = (post.link_flair_text == "new")
            is_spotify = ("spotify" in post.url)
            is_track = ("track" in post.url)
            if is_new and is_spotify and is_track:
                print("New Spotify track:", post.url)
                valid_part = post.url.split('?')[0]
                sp_agent.add_songs_to_playlist([valid_part], playlist_id)


def check_args():
    if len(sys.argv) < 2:
        usage = "Usage: reddit2spotify username"
        print(usage)
        sys.exit(0)


def create_reddit_instance(config_file):
    config = configparser.ConfigParser()
    # TODO: Change read to read_file for required config file
    config.read(config_file)
    reddit_creds = config["reddit"]

    user_agent = "reddit2Spotify by /u/zelfed"
    reddit = praw.Reddit(client_id=reddit_creds["CLIENT_ID"],
                         client_secret=reddit_creds["CLIENT_SECRET"],
                         password=reddit_creds["PASSWORD"],
                         user_agent=user_agent,
                         username=reddit_creds["USERNAME"])

    print("User:", reddit.user.me())
    return reddit


# update label by redrawing after text changes
@pyqtSlot()
def redraw(app):
    app.processEvents()


def main():
    check_args()
    print("hello")

    config_file = "config.ini"  # have to change this
    sp_agent = spotify.SpotifyAgent(sys.argv[1],
                                    "playlist-modify-public",
                                    config_file)

    reddit = create_reddit_instance("config.ini")

    app = QApplication(sys.argv)

    def redraw_func(): redraw(app)
    r2s = gui.r2sGUI(sp_agent, reddit, redraw_func)

    #  ss.show()
    r2s.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    #  tester()
    main()
