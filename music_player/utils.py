from .models import Playlist, Songs
from django.conf import settings
from music_player.LinkedList.play_list import PlayList as CurrentPlayList


def update_playlists():
    settings.PLAYLISTS = {}
    for playlist in Playlist.objects.all():
        settings.PLAYLISTS[playlist.title] = (Songs.objects.filter(
            playlist=playlist.pk), playlist.pk)


def update_current_playlist():
    settings.CURRENT_PLAYLIST = CurrentPlayList()
