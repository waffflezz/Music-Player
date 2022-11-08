from django.urls import path

from .views import (index, open_playlist, update_playlists, play_song,
                    next_song, prev_song, all_songs, add_song_to_playlist,
                    delete_song_from_playlist, delete_playlist, add_playlist,
                    swap)

urlpatterns = [
    path('', index),
    path('open_playlist', open_playlist),
    path('playlists', update_playlists),
    path('play', play_song),
    path('next_song', next_song),
    path('prev_song', prev_song),
    path('all_songs', all_songs),
    path('add_to_playlist', add_song_to_playlist),
    path('delete_song', delete_song_from_playlist),
    path('delete_playlist', delete_playlist),
    path('add_playlist', add_playlist),
    path('swap', swap),
]
