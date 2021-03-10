def read(path_music):
    import os
    import sys
    from pathlib import Path
    from itertools import chain
    from mutagen.mp4 import MP4
    from mutagen.flac import FLAC
    from mutagen.mp3 import MP3
    from mutagen.easyid3 import EasyID3
    from mutagen.mp4 import MP4Tags

    filename = os.path.split(path_music)[1]
    filename, ext = os.path.splitext(filename)  # ファイルの形式確認で使用
    ext = ext.lower()

    if ext == ".mp3":
        audio = EasyID3(path_music)
        title = audio["title"]
        album = audio["album"]
        artist = audio["artist"]
    elif ext in [".m4a"]:
        audio = MP4(path_music)
        title = audio["\xa9nam"]
        album = audio["\xa9alb"]
        artist = audio["\xa9ART"]

    data = [title, album, artist]
    return (data)
