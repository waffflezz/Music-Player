from django.contrib import admin


from .models import Songs, Playlist
# Register your models here.


@admin.register(Songs)
class SongsAdmin(admin.ModelAdmin):
    list_display = ('id', 'song_path')


admin.site.register(Playlist)
