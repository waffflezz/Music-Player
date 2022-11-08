from music_player.LinkedList.linked_list import LinkedList


class PlayList(LinkedList):
    def __init__(self):
        super(PlayList, self).__init__()
        self.current_track = None
        self.current_playlist_id = None

    def play_all(self, item):
        self.current_track = self[item]

    def next_track(self):
        self.current_track = self.current_track.next_item

    def previous_track(self):
        self.current_track = self.current_track.previous_item

    def delete_track(self, index):
        self.pop(index)

    @property
    def current(self):
        return self.current_track
