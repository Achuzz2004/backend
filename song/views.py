from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter
from user.models import Customer
from .models import Playlist, Song, Genre,ListeningHistory
from .serializers import (
    PlayListSerializer, SongSerializer, SongDetailSerializer, GenreSummarySerializer, GenreSerializer
)
from .serializers import PlayListDetailSerializer
from .recommendations import reccomend_for_user
# Create your views here.

class PlaylistListAV(ListCreateAPIView):
    queryset = Playlist.objects.filter(hide=False)
    serializer_class = PlayListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title']
    
class PlaylistDetailAV(RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.filter(hide=False)
    serializer_class = PlayListDetailSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title']
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    
class SongListAV(ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title']
class SongDetailAV(RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongDetailSerializer
    filter_backends =  [SearchFilter]
    search_fields = ['title']
    
# generate genre list and detail class view
class GenreListAV(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSummarySerializer
    
class GenreDetailAV(RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    
class SuggestedSongsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        try:
            customer = user.customer  # ✅ Use lowercase 'customer'
        except Customer.DoesNotExist:
            return Response({"detail": "Only customers can get song recommendations."}, status=400)

        recommended_songs = reccomend_for_user(customer, Song, ListeningHistory)

        data = [
            {
                "id": s.id,
                "title": s.title,
                "image": request.build_absolute_uri(s.image.url) if s.image else None,
                "audio": request.build_absolute_uri(s.audio.url) if s.audio else None,  # ✅ Fix here
                "duration": s.duration,
                "artists": [
                    {
                        "id": artist.id,
                        "first_name": artist.user.first_name,
                        "last_name": artist.user.last_name
                    }
                    for artist in s.artists.all()
                ],
                "genres": [genre.title for genre in s.genres.all()]
            }
            for s in recommended_songs
        ]

        return Response(data)

#class AddSongToPlaylistView(generics.CreateAPIView):
 #   serializer_class = PlaylistSongsSerializer