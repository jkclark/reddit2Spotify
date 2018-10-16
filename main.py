import praw
import pickle


def load_credentials(credentials_pickle_file):
    try:
        with open(credentials_pickle_file, 'rb') as c:
            return pickle.load(c)
    except IOError:
        print("Error: Couldn't open credentials file. Exiting.")


def main():
    print("Loading credentials from credentials file...")
    credentials = load_credentials("credentials.p")

    user_agent = "reddit2Spotify by /u/zelfed"
    reddit = praw.Reddit(client_id=credentials["CLIENT_ID"],
                         client_secret=credentials["CLIENT_SECRET"],
                         password=credentials["PASSWORD"],
                         user_agent=user_agent,
                         username=credentials["USERNAME"])

    print("User:", reddit.user.me())

    subreddit = reddit.subreddit('edm')

    # dir(object) returns a list of attributes for object
    for post in subreddit.top('week'):
        print("url:", post.url)


if __name__ == "__main__":
    main()
