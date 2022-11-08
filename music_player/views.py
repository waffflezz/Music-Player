from . import utils
from django.shortcuts import render

from base64 import b64encode

from django.conf import settings
from music_player.LinkedList.composition import Composition
from django.http import HttpResponse, JsonResponse

from .models import Playlist, Songs


def index(request):
    songs = Songs.objects.all()

    return render(request, 'music_player/index.html', {'songs': songs})


def all_songs(request):
    songs = Songs.objects.all()

    song_list = []
    for i, song in enumerate(songs):
        song_list.append(Composition(settings.BASE_DIR.__str__() + song.song_path.url, i, song.song_path.url, song.pk))

    return render(request, 'music_player/all_songs.html', {'songs': song_list,
                                                           'playlists': Playlist.objects.all})


def update_playlist(playlist_id):
    utils.update_current_playlist()

    for i, song in enumerate(Songs.objects.filter(playlist=playlist_id)):
        settings.CURRENT_PLAYLIST.append(
            Composition(settings.BASE_DIR.__str__() + song.song_path.url,
                        i, song.song_path.url, song.pk))


def add_song_to_playlist(request):
    song_id, playlist_id = map(int, (request.GET['song_id'],
                                     request.GET['playlist_id']))
    song = Songs.objects.get(pk=song_id)
    playlist = Playlist.objects.get(pk=playlist_id)

    song.playlist.add(playlist)

    if playlist_id == settings.CURRENT_PLAYLIST.current_playlist_id:
        settings.CURRENT_PLAYLIST.append(Composition(settings.BASE_DIR.__str__() + song.song_path.url,
                                                     settings.CURRENT_PLAYLIST.last.data.song_number + 1,
                                                     song.song_path.url, song.pk))

    return HttpResponse(request)


def delete_song_from_playlist(request):
    song_id, playlist_id = map(int, (request.GET['song_id'],
                                     request.GET['playlist_id']))
    song = Songs.objects.get(pk=song_id)
    playlist = Playlist.objects.get(pk=playlist_id)

    song.playlist.remove(playlist)

    update_playlist(playlist_id)

    songs = Songs.objects.filter(playlist=playlist_id)
    song_list = []
    for i, song in enumerate(songs):
        song_list.append(Composition(settings.BASE_DIR.__str__() + song.song_path.url, i, song.song_path.url, song.pk))

    return HttpResponse(request)


def add_playlist(request):
    playlist_name = request.GET['playlist_name']
    Playlist.objects.create(title=playlist_name)


def delete_playlist(request):
    playlist_id = request.GET['playlist_id']
    if settings.CURRENT_PLAYLIST.current_playlist_id == playlist_id:
        utils.update_current_playlist()

    Playlist.objects.get(pk=request.GET['playlist_id']).delete()
    utils.update_playlists()

    return render(request, 'music_player/playlists.html')


def swap(request):
    direction, song_id = request.GET['direction'], int(request.GET['song_id'])
    if direction == 'up':
        if song_id == 0:
            prev_song_id = settings.CURRENT_PLAYLIST.length - 1
            settings.CURRENT_PLAYLIST.swap(song_id, prev_song_id)
        else:
            settings.CURRENT_PLAYLIST.swap(song_id, song_id - 1)
    elif direction == 'down':
        if song_id == settings.CURRENT_PLAYLIST.length - 1:
            next_song_id = 0
            settings.CURRENT_PLAYLIST.swap(song_id, next_song_id)
        else:
            settings.CURRENT_PLAYLIST.swap(song_id, song_id + 1)

    return HttpResponse(request)


def open_playlist(request):
    playlist = Playlist.objects.get(pk=request.GET['pl_id'])
    songs = Songs.objects.filter(playlist=playlist.pk)



    song_list = []
    for i, song in enumerate(songs):
        song_list.append(Composition(settings.BASE_DIR.__str__() + song.song_path.url, i, song.song_path.url, song.pk))

    return render(request, 'music_player/offcanvas_player.html', {'pp': song_list,
                                                                  'playlist_id': playlist.pk})


def update_playlists(request):
    utils.update_playlists()
    return render(request, 'music_player/playlists.html')


def encode_image_to_b64(byte_array):
    return b64encode(byte_array).decode()


def play_song(request):
    playlist = Playlist.objects.get(pk=request.GET['pl_id'])
    songs = Songs.objects.filter(playlist=playlist.pk)

    if settings.CURRENT_PLAYLIST.current_playlist_id != playlist.pk:
        utils.update_current_playlist()

        for i, song in enumerate(songs):
            settings.CURRENT_PLAYLIST.append(
                Composition(settings.BASE_DIR.__str__() + song.song_path.url,
                            i, song.song_path.url, song.pk))

        settings.CURRENT_PLAYLIST.current_playlist_id = playlist.pk

    settings.CURRENT_PLAYLIST.play_all(int(request.GET['song_number']))

    return JsonResponse({'song_path': settings.CURRENT_PLAYLIST.current.data.song_path,
                         'image': f'{encode_image_to_b64(settings.CURRENT_PLAYLIST.current.data.image)}',
                         'playlist_id': settings.CURRENT_PLAYLIST.current_playlist_id})


def next_song(request):
    settings.CURRENT_PLAYLIST.next_track()

    return JsonResponse(
        {'song_path': settings.CURRENT_PLAYLIST.current.data.song_path,
         'image': f'{encode_image_to_b64(settings.CURRENT_PLAYLIST.current.data.image)}'})


def prev_song(request):
    settings.CURRENT_PLAYLIST.previous_track()

    return JsonResponse(
        {'song_path': settings.CURRENT_PLAYLIST.current.data.song_path,
         'image': f'{encode_image_to_b64(settings.CURRENT_PLAYLIST.current.data.image)}'})
