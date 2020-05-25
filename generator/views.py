from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
# Create your views here.
import random
import math
from .models import Band, BandMember, Song

#function to find a list songs in the next possible song_key
def sort_by_key(list_of_songs, num_songs, start_key):
    key = chr(ord(start_key)+1)
    songs_added = []
    while len(songs_added) != num_songs:
        if key == 'H':
            key = 'A'
        if len(list(filter(lambda song: song.song_key == key, list_of_songs))) > 0:
            if len(songs_added) == 0:
                songs_added.append(list(filter(lambda song: song.song_key == key, list_of_songs))[0])
                list_of_songs.remove(songs_added[-1])
            else:
                if songs_added[-1].song_key != key:
                    songs_added.append(list(filter(lambda song: song.song_key == key, list_of_songs))[0])
                    list_of_songs.remove(songs_added[-1])
        key = chr(ord(key)+1)
    return songs_added 


class IndexView(generic.ListView):
    template_name = 'generator/index.html'
    context_object_name = 'band_list'

    def get_queryset(self):
        """Returns ordered first 5 persons by pk."""
        return Band.objects.all()

class BandSongsView(generic.ListView):
    template_name = 'generator/bandsongs.html'
    context_object_name = 'context'

    def get_queryset(self):
        self.band = get_object_or_404(Band, id=self.kwargs['band_id'])
        # return Song.objects.filter(band=self.band)
        return {
            "songs": Song.objects.filter(band=self.band),
            "band": self.band
        }


#TODO seperate into two setlists - choose opening songs for both sets
#generate setlist from indexview by clicking on the band 

class SetlistView(generic.ListView):
    template_name = 'generator/setlist.html'
    context_object_name = 'setlists'

    def get_queryset(self):
        num_songs = self.kwargs['num_songs']
        num_slow_songs = self.kwargs['num_slow_songs']
        num_encores = self.kwargs['num_encores']
        start_song = list(Song.objects.filter(title=self.kwargs['start_song']))
        start_song_key = Song.objects.values_list('song_key', flat=True).get(title=self.kwargs['start_song'])
        self.band = get_object_or_404(Band, id=self.kwargs['band_id'])
        shuffled_songs = sorted(Song.objects.filter(band=self.band).exclude(title=self.kwargs['start_song']).order_by('id')[:], key=lambda x: random.random())
    
        setlist_1_length = math.floor(num_songs / 2)
        setlist_2_length = math.ceil(num_songs / 2)

        list_of_slow_songs = list(filter(lambda song: song.is_slow_song == True and song.is_encore == False, shuffled_songs))
        list_of_songs = list(filter(lambda song: song.is_encore == False and song.is_slow_song == False, shuffled_songs))
        list_of_encores = list(filter(lambda song: song.is_encore == True, shuffled_songs))

        slow_songs = sort_by_key(list_of_slow_songs, num_slow_songs, start_song_key)
        set_1_songs = sort_by_key(list_of_songs, (setlist_1_length - num_slow_songs - 1), slow_songs[-1].song_key)
        setlist_1 = start_song + slow_songs + set_1_songs

        set_2_songs = sort_by_key(list_of_songs, (setlist_2_length - num_encores), set_1_songs[-1].song_key)
        encores = sort_by_key(list_of_encores, num_encores, set_2_songs[-1].song_key)
        setlist_2 = set_2_songs + encores
        print(setlist_1)
        print(setlist_2)
        return {
            "setlist1": setlist_1,
            "setlist2": setlist_2
            }


class GenerateView(generic.ListView):
    template_name = 'generate.html'
    context_object_name = 'context'

    def get_queryset(self):
        self.band = get_object_or_404(Band, id=self.kwargs['band_id'])
        return {
            "songs": Song.objects.filter(band=self.band),
            "band": self.band
        }