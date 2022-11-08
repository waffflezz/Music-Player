from django.db import models


def get_main_playlist():
    return Playlist.objects.filter(title='all_songs')


# Create your models here.
class Songs(models.Model):
    song_path = models.FileField(upload_to="songs/%Y/%m/%d/")
    playlist = models.ManyToManyField('Playlist', default=get_main_playlist)
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", default="default.jpg")


class Playlist(models.Model):
    title = models.CharField(max_length=40)

    def __str__(self):
        return self.title

