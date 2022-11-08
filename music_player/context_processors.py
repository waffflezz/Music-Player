from django.conf import settings


def playlists(request):
    return {'PLAYLISTS': settings.PLAYLISTS,
            'CURRENT_PLAYLIST': settings.CURRENT_PLAYLIST}
