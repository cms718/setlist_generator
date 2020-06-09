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
        return Band.objects.all()

class BandSongsView(generic.ListView):
    template_name = 'generator/bandsongs.html'
    context_object_name = 'context'

    def get_queryset(self):
        self.band = get_object_or_404(Band, id=self.kwargs['band_id'])
        return {
            "songs": Song.objects.filter(band=self.band),
            "band": self.band
        }


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
        return {
            "setlist1": setlist_1,
            "setlist2": setlist_2
            }

################################################--FIGURING OUT SERIALIZERS---#################################################
@csrf_exempt
def band_list(request):
    """
    List all Bands, or create a new Band.
    """
    if request.method == 'GET':
        bands = Band.objects.all()
        serialized_bands = BandSerializer(bands, many=True)
        return JsonResponse(serialized_bands.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BandSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def band_detail(request, band_id):
    """
    Retrieve, update or delete a band.
    """
    try:
        band = Band.objects.get(id=band_id)
        songs = Song.objects.filter(band=band_id)
        band_members = BandMember.objects.filter(band=band_id)
    except Band.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        responses = {
            'band': BandSerializer(band).data,
            'songs': list(map(lambda song: SongSerializer(song).data, songs)),
            'band_members': list(map(lambda member: BandMemberSerializer(member).data, band_members))
        }
        return JsonResponse(responses)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BandSerializer(band, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        band.delete()
        return HttpResponse(status=204)

def generate_setlist(request):
    try:
        num_songs = int(request.GET['numSongs'])
        num_slow_songs = int(request.GET['numSlowSongs'])
        num_encores = int(request.GET['numEncores'])
        set_one_opener = request.GET['setOneOpener']
        start_song = list(Song.objects.filter(title=set_one_opener))
        set_two_opener = request.GET['setTwoOpener']
        start_song_two = list(Song.objects.filter(title=set_two_opener))
        #ID is hardcoded
        band = get_object_or_404(Band, id=4)
        band_members = BandMember.objects.filter(band=band)
        shuffled_songs = sorted(Song.objects.filter(band=band).order_by('id')[:], key=lambda x: random.random())
        start_song_key = Song.objects.values_list('song_key', flat=True).get(title=set_one_opener)
        set_two_start_key = Song.objects.values_list('song_key', flat=True).get(title=set_two_opener)

        setlist_1_length = math.floor(num_songs / 2)
        setlist_2_length = math.ceil(num_songs / 2)

        list_of_slow_songs = list(filter(lambda song: song.is_slow_song == True and song.is_encore == False, shuffled_songs))
        list_of_songs = list(filter(lambda song: song.is_encore == False and song.is_slow_song == False, shuffled_songs))
        list_of_encores = list(filter(lambda song: song.is_encore == True, shuffled_songs))

        #need to make list because filter is not subscriptable
        slow_songs = sort_by_key(list_of_slow_songs, num_slow_songs, start_song_key)
        set_1_songs = sort_by_key(list_of_songs, (setlist_1_length - num_slow_songs - 1), slow_songs[-1].song_key)
        setlist_1 = start_song + slow_songs + set_1_songs

        set_2_songs = sort_by_key(list_of_songs, (setlist_2_length - num_encores - 1), set_two_start_key)
        encores = sort_by_key(list_of_encores, num_encores, set_2_songs[-1].song_key)
        setlist_2 = start_song_two + set_2_songs + encores

        responses = {
            'band': BandSerializer(band).data,
            'setlist_one': list(map(lambda song: SongSerializer(song).data, setlist_1)),
            'setlist_two': list(map(lambda song: SongSerializer(song).data, setlist_2)),
            'band_members': list(map(lambda member: BandMemberSerializer(member).data, band_members))
        }
        return JsonResponse(responses)

    except Band.DoesNotExist:
        return HttpResponse(status=404)
    