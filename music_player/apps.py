from django.apps import AppConfig


class MusicPlayerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'music_player'

    def ready(self):
        from .utils import update_playlists
        update_playlists()
