from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Band(models.Model):
    band_name = models.CharField(max_length=40)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.band_name

class Song(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    artist = models.CharField(max_length=20)
    bpm = models.IntegerField()
    is_encore = models.BooleanField('encore', default=False)
    song_key = models.CharField(max_length=5)
    is_slow_song = models.BooleanField('slow song', default=False)

    def __str__(self):
        return self.title

class BandMember(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    instrument = models.CharField(max_length=20)

    def __str__(self):
        return ('{} {}'.format(self.first_name, self.last_name))









