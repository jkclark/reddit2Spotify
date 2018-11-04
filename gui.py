import configparser
import os.path
from PyQt5.QtWidgets import (QWidget,
                             QVBoxLayout,
                             #  QHBoxLayout,
                             QLabel)


class r2sGUI(QWidget):
    def __init__(self, spotify_username):
        super().__init__()
        self.username = spotify_username
        self.initialize_UI()

    def initialize_UI(self):
        main_vertical_box = QVBoxLayout()

        config = configparser.ConfigParser()
        settings_file_name = f"{self.username}.ini"
        if os.path.isfile(settings_file_name):
            config.read(settings_file_name)
        # Should probably check that config file is valid (not corrupted)

        if not config.sections():
            no_subreddits_message = f"No subreddits added for {self.username}."
            no_subreddits = QLabel(no_subreddits_message)
            main_vertical_box.addWidget(no_subreddits)
        else:
            for section in config.sections():
                subreddit_box = self.add_subreddit_layout(config[section])
                main_vertical_box.addLayout(subreddit_box)

        self.setLayout(main_vertical_box)
        self.setWindowTitle('reddit2Spotify')

    def add_subreddit_layout(self, subreddit_settings=None):
        # load ui from qtdesigner widget
        pass
