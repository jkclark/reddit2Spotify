import praw
import spotify
import sys
import configparser


def main():
    config = configparser.ConfigParser()
    config_file = "config.ini"
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
