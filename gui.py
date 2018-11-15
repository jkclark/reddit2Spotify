import configparser
import os.path
import sip
import sys
from PyQt5.QtWidgets import (QWidget,
                             QVBoxLayout,
                             #  QHBoxLayout,
                             QLabel)
from PyQt5 import uic, QtCore


class r2sGUI(QWidget):
    def __init__(self, sp_agent, reddit):
        super().__init__()
        self.sp_agent = sp_agent
        self.reddit = reddit
        self.mvb = QVBoxLayout()
        self.subreddit_count = 0
        self.config = None
        self.settings_file = f"{self.sp_agent.username}.ini"
        self.initialize_UI()

    def initialize_UI(self):
        config = configparser.ConfigParser()
        if os.path.isfile(self.settings_file):
            config.read(self.settings_file)
            self.config = config
            # should probably check that config file is valid (not corrupted)

        # load subreddits
        if not config.sections():
            self.display_no_reddits()
        else:
            for section in config.sections():
                subreddit_box = self.load_subreddit(config[section])
                self.mvb.addWidget(subreddit_box)
                self.subreddit_count += 1

        # add button
        add_widget = uic.loadUi("addsubreddit.ui")
        add_subreddit_button = add_widget.add_subreddit_button
        add_subreddit_button.clicked.connect(self.create_new_subreddit)
        self.mvb.addWidget(add_widget)

        self.setLayout(self.mvb)
        self.setWindowTitle("reddit2Spotify")

    def resize_after_subreddit_count_change(self):
        #  height = self.mvb.sizeHint().height()
        #  print("hinted height = ", height)
        #  width = self.width()
        self.resize(self.sizeHint())
        # this is currently not working

    def display_no_reddits(self):
        # no_subreddits_m --> no_subreddits_message
        no_subreddits_m = f"No subreddits added for {self.sp_agent.username}."
        no_subreddits = QLabel(no_subreddits_m)
        no_subreddits.setObjectName("no_subreddits_label")
        self.mvb.addWidget(no_subreddits)

    def load_subreddit(self, section):
        # load ui from qtdesigner-made widget
        ss = uic.loadUi("singlesubreddit.ui")

        # subreddit name
        ss.subreddit_entry_textbox.setText(section["name"])

        # sorting method dropdown
        # only show time sorting if "top" is selected
        def time_lambda(): self.allow_time(ss.sorting_method_combo,
                                           [ss.pre_top_time_label,
                                            ss.top_time_combo])
        ss.sorting_method_combo.currentIndexChanged.connect(time_lambda)
        index = ss.sorting_method_combo.findText(section["sorting method"],
                                                 QtCore.Qt.MatchFixedString)
        if index >= 0:
            ss.sorting_method_combo.setCurrentIndex(index)

        # flair text
        flair_placeholder_text = "Case sensitive. Leave blank for all posts."
        ss.post_flair_textbox.setPlaceholderText(flair_placeholder_text)
        ss.post_flair_textbox.setText(section["flair text"])

        # new and existing playlist radio buttons
        def playlist_radio_toggled(): self.playlist_radio_toggled(ss)
        ss.new_pl_radio.toggled.connect(playlist_radio_toggled)
        ss.existing_pl_radio.toggled.connect(playlist_radio_toggled)
        pl_type = section["playlist type"]
        ss.new_pl_radio.setChecked(pl_type == "new")
        ss.existing_pl_radio.setChecked(pl_type == "existing")

        # save button
        def save_button_clicked(): self.save_subreddit(ss)
        ss.save_button.clicked.connect(save_button_clicked)

        # delete button
        def delete_button_clicked(): self.delete_subreddit(ss)
        ss.delete_button.clicked.connect(delete_button_clicked)

        # run button
        def run_button_clicked(): self.run_now(ss)
        ss.run_now_button.clicked.connect(run_button_clicked)

        # schedule button
        def schedule_button_clicked(): self.schedule(ss)
        ss.schedule_button.clicked.connect(schedule_button_clicked)

        return ss

    @QtCore.pyqtSlot(object, list)
    def allow_time(self, sorting, to_be_hidden):
        if sorting.currentIndex() == 0:
            #  time_hb.show()
            for widget in to_be_hidden:
                widget.show()
        else:
            #  time.setEnabled(False)
            for widget in to_be_hidden:
                widget.hide()

    @QtCore.pyqtSlot(QWidget)
    def playlist_radio_toggled(self, ss):
        if ss.new_pl_radio.isChecked():  # new
            # hide existing playlist stuff
            ss.existing_pl_id_label.hide()
            ss.existing_pl_id_textbox.hide()
            # show new playlist stuff
            ss.new_pl_name_label.show()
            ss.new_pl_name_textbox.show()
            ss.new_pl_desc_label.show()
            ss.new_pl_desc_textbox.show()
        else:  # existing
            # show existing playlist stuff
            ss.existing_pl_id_label.show()
            ss.existing_pl_id_textbox.show()
            # hide new playlist stuff
            ss.new_pl_name_label.hide()
            ss.new_pl_name_textbox.hide()
            ss.new_pl_desc_label.hide()
            ss.new_pl_desc_textbox.hide()

    def create_new_subreddit(self):
        print("Creating new subreddit...")
        # remove add button
        add_button = self.mvb.takeAt(self.mvb.count()-1).widget()

        # remove "no subreddit" label if there are currently no subreddits
        if self.subreddit_count == 0:
            no_subreddit_label = self.mvb.takeAt(self.mvb.count()-1).widget()
            sip.delete(no_subreddit_label)

        # add new subreddit
        new_subreddit = self.load_subreddit(self.config["DEFAULT"])
        self.mvb.addWidget(new_subreddit)
        self.subreddit_count += 1

        # add add button back
        self.mvb.addWidget(add_button)
        self.resize_after_subreddit_count_change()

    @QtCore.pyqtSlot(QWidget)
    def save_subreddit(self, ss):
        section = ss.subreddit_entry_textbox.text().lower()
        cf = self.config
        cf.read(self.settings_file)

        try:
            cf.add_section(section)
        except configparser.DuplicateSectionError:
            pass

        cf[section]["name"] = section
        cf[section]["sorting method"] = ss.sorting_method_combo.currentText()
        # saves top time period even if not sorting by top
        cf[section]["top time period"] = ss.top_time_combo.currentText()
        cf[section]["flair text"] = ss.post_flair_textbox.text()
        pl_type = "new" if ss.new_pl_radio.isChecked() else "existing"
        cf[section]["playlist type"] = pl_type

        with open(self.settings_file, 'w') as configfile:
            cf.write(configfile)

    @QtCore.pyqtSlot(QWidget)
    def delete_subreddit(self, ss):
        print("Deleting subreddit...")
        self.mvb.removeWidget(ss)
        self.remove_subreddit_from_settings(ss)
        sip.delete(ss)  # honestly have no clue what this is but it works
        self.subreddit_count -= 1

        # add "no subreddits" label if we just deleted the last subreddit
        if self.subreddit_count == 0:
            add_button = self.mvb.takeAt(self.mvb.count()-1).widget()
            self.display_no_reddits()
            self.mvb.addWidget(add_button)

        self.resize_after_subreddit_count_change()
        self.resize_after_subreddit_count_change()

    def remove_subreddit_from_settings(self, ss):
        section = ss.subreddit_entry_textbox.text().lower()
        cf = self.config
        cf.read(self.settings_file)
        deleted = cf.remove_section(section)
        if not deleted:
            print(f"Error deleting section {section}.", file=sys.stderr)
        with open(self.settings_file, 'w') as configfile:
            cf.write(configfile)

    def run_now(self, ss):
        print("Running subreddit settings now...")
        self.save_subreddit(ss)
        playlist_id = None
        if ss.new_pl_radio.isChecked():  # new
            pl_name = ss.new_pl_name_texbox.text()
            pl_desc = ss.new_pl_desc_textbox.text()
            playlist = self.sp_agent.create_playlist(pl_name, pl_desc)
            playlist_id = playlist["id"]
        else:  # existing playlist
            playlist_id = ss.existing_pl_id_textbox.text()
        print("Playlist ID:", playlist_id)

        #
        # move this function over to main.py
        #

    def schedule(self, ss):
        print("Scheduling subreddit settings now...")
