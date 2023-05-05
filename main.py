from pathlib import Path as path
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from pytube import YouTube
import sys
import os


def download_vid():
    # link = "https://www.youtube.com/watch?v=BaW_jenozKc"
    link = fen.vid_url.text()
    new_title = fen.vid_title.text()
    preferred_res = fen.vid_res.text()

    fen.res.setText("Searching for the video...")
    # fetching the video
    try:
        video = YouTube(link, use_oauth=True, allow_oauth_cache=True)
    except Exception:
        fen.res.setText("An Error happened ! maybe the link is incorrect.")
        return

    # fetch with the preferred resolution
    if preferred_res != "":
        # print(video.streams.all())
        video = video.streams.get_by_resolution(preferred_res + "p")
        if video == None:
            fen.res.setText("This resolution isn't available")
            return
    else:
        video = video.streams.get_highest_resolution()

    fen.res.setText("Downloading...")
    # downloading and saving the video
    download_folder = str(path.home()) + "/Downloads/"
    video.download(download_folder)
    if new_title != "":
        os.rename(
            download_folder + video.default_filename,
            download_folder + new_title + ".mp4",
        )
    fen.res.setText("Video downloaded successfully !")
    cancel()


def cancel():
    fen.vid_url.setText("")
    fen.vid_title.setText("")
    fen.vid_res.setText("")


App = QtWidgets.QApplication(sys.argv)
fen = loadUi("main.ui")

fen.download_btn.clicked.connect(download_vid)
fen.cancel_btn.clicked.connect(cancel)

fen.show()
App.exec()
