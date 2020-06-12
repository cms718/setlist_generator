import random
import math
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.views import generic
from rest_framework import viewsets
from .api.serializers import BandSerializer, SongSerializer, BandMemberSerializer
from .models import Band, BandMember, Song
# Create your views here.

#TODO change to include major and minor keys
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

#TODO add default params and error handling
def generate_setlist(request):
    try:
        num_songs = int(request.GET['numSongs'])
        num_slow_songs = int(request.GET['numSlowSongs'])
        num_encores = int(request.GET['numEncores'])
        set_one_opener = request.GET['setOneOpener']
        start_song = list(Song.objects.filter(title=set_one_opener))
        set_two_opener = request.GET['setTwoOpener']
        start_song_two = list(Song.objects.filter(title=set_two_opener))
        #ID is hardcoded for TEST BAND
        band = get_object_or_404(Band, id=4)
        band_members = BandMember.objects.filter(band=band)
        shuffled_songs = sorted(Song.objects.filter(band=band).exclude(title=set_one_opener).exclude(title=set_two_opener).order_by('id')[:], key=lambda x: random.random())
        start_song_key = Song.objects.values_list('song_key', flat=True).get(title=set_one_opener)
        set_two_start_key = Song.objects.values_list('song_key', flat=True).get(title=set_two_opener)

        setlist_1_length = math.floor(num_songs / 2)
        setlist_2_length = math.ceil(num_songs / 2)

        #need to make list because filter is not subscriptable
        list_of_slow_songs = list(filter(lambda song: song.is_slow_song == True and song.is_encore == False, shuffled_songs))
        list_of_songs = list(filter(lambda song: song.is_encore == False and song.is_slow_song == False, shuffled_songs))
        list_of_encores = list(filter(lambda song: song.is_encore == True, shuffled_songs))

        slow_songs = sort_by_key(list_of_slow_songs, num_slow_songs, start_song_key)
        set_1_songs = sort_by_key(list_of_songs, (setlist_1_length - num_slow_songs - 1), slow_songs[-1].song_key)
        setlist_1 = start_song + slow_songs + set_1_songs

        set_2_songs = sort_by_key(list_of_songs, (setlist_2_length - num_encores - 1), set_two_start_key)
        encores = sort_by_key(list_of_encores, num_encores, set_2_songs[-1].song_key)
        setlist_2 = start_song_two + set_2_songs + encores

        reserve_songs = [song for song in shuffled_songs if song not in setlist_1 if song not in setlist_2]

        responses = {
            'band': BandSerializer(band).data,
            'setlist_one': list(map(lambda song: SongSerializer(song).data, setlist_1)),
            'setlist_two': list(map(lambda song: SongSerializer(song).data, setlist_2)),
            'band_members': list(map(lambda member: BandMemberSerializer(member).data, band_members)),
            'reserve_songs': list(map(lambda song: SongSerializer(song).data, reserve_songs))
        }
        return JsonResponse(responses)

    except Band.DoesNotExist:
        return HttpResponse(status=404)
    