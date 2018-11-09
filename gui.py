import configparser
import os.path
from PyQt5.QtWidgets import (QWidget,
                             QVBoxLayout,
                             #  QHBoxLayout,
                             QLabel)
from PyQt5 import uic, QtCore


class r2sGUI(QWidget):
    def __init__(self, spotify_username):
        super().__init__()
        self.username = spotify_username
        self.mvb = QVBoxLayout()
        self.subreddit_count = 0
        self.config = None
        self.initialize_UI()

    def initialize_UI(self):
        config = configparser.ConfigParser()
        settings_file_name = f"{self.username}.ini"
        if os.path.isfile(settings_file_name):
            config.read(settings_file_name)
            self.config = config
            # Should probably check that config file is valid (not corrupted)

        if not config.sections():
            self.display_no_reddits()
        else:
            for section in config.sections():
                subreddit_box = self.load_subreddit(config[section])
                self.mvb.addWidget(subreddit_box)
                self.subreddit_count += 1

        self.setLayout(self.mvb)
        self.setWindowTitle("reddit2Spotify")

    def display_no_reddits(self):
        no_subreddits_message = f"No subreddits added for {self.username}."
        no_subreddits = QLabel(no_subreddits_message)
        self.mvb.addWidget(no_subreddits)

    def load_subreddit(self, section):
        # load ui from qtdesigner-made widget
        ss = uic.loadUi("singlesubreddit.ui")

        # subreddit name
        ss.subreddit_entry_textbox.setText(section["name"])

        # sorting method dropdown
        index = ss.sorting_method_combo.findText(section["sorting method"],
                                                 QtCore.Qt.MatchFixedString)
        if index >= 0:
            ss.sorting_method_combo.setCurrentIndex(index)

        return ss

    def create_new_subreddit(self):
        pass
