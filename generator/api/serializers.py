from rest_framework import serializers
from generator.models import Band, Song, BandMember

class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Band
        fields = ['id', 'band_name']

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'band', 'title', 'artist', 'bpm', 'is_encore', 'song_key', 'is_slow_song']

class BandMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = BandMember
        fields = ['id', 'band', 'first_name', 'last_name', 'email', 'instrument']