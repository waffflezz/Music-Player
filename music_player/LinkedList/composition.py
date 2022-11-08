import base64
from tinytag import TinyTag


class Composition:
    def __init__(self, song_path, song_number, right_song_path, song_id):
        self.path = right_song_path
        self.song_number = song_number
        self.song_id = song_id
        self.tag = TinyTag.get(song_path, image=True)

    @property
    def artist(self):
        return self.tag.artist

    @property
    def song_path(self):
        return self.path

    @property
    def album(self):
        return self.tag.album

    @property
    def song_name(self):
        return self.tag.title

    @property
    def image(self):
        return self.tag.get_image()
