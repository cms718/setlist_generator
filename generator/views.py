from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
# Create your views here.
import random
from .models import Band, BandMember, Song

class IndexView(generic.ListView):
    template_name = 'generator/index.html'
    context_object_name = 'band_list'

    def get_queryset(self):
        """Returns ordered first 5 persons by pk."""
        return Band.objects.all()

class BandSongsView(generic.ListView):
    template_name = 'generator/bandsongs.html'
    context_object_name = 'song_list'

    def get_queryset(self):
        self.band = get_object_or_404(Band, id=self.kwargs['band_id'])
        return Song.objects.filter(band=self.band)


#TODO seperate into two setlists - choose opening songs for both sets - apply the key logic based on starting songs key
#change slow_songs from BPM based to a attribute or method is_dance_song. 
#generate setlist from indexview by clicking on the band 

class SetlistView(generic.ListView):
    template_name = 'generator/setlist.html'
    context_object_name = 'setlist'

    def get_queryset(self):
        num_songs = self.kwargs['num_songs']
        num_slow_songs = self.kwargs['num_slow_songs']
        num_encores = self.kwargs['num_encores']
        start_song = list(Song.objects.filter(title=self.kwargs['start_song']))
        self.band = get_object_or_404(Band, id=self.kwargs['band_id'])
        shuffled_songs = sorted(Song.objects.filter(band=self.band).exclude(title=self.kwargs['start_song']).order_by('id')[:], key=lambda x: random.random())
    
        setlist = []
        slow_songs = list(filter(lambda song: song.is_slow() and song.is_encore == False, shuffled_songs))[:num_slow_songs]
        songs = list(filter(lambda song: song.is_encore == False and song not in slow_songs, shuffled_songs))[:num_songs]
        encores = list(filter(lambda song: song.is_encore == True, shuffled_songs))[:num_encores]


        setlist = start_song + slow_songs + songs + encores
        return setlist