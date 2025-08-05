from django.contrib import admin
from .models import Genre, Playlist, Song

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'color')
    search_fields = ('title',)
    list_filter = ('color',)

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')
    search_fields = ('title', 'author__user__username')
    list_filter = ('author',)

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_artists', 'get_genres')
    search_fields = ('title', 'artists__user__username')
    list_filter = ('genres',)

    def get_artists(self, obj):
        return ", ".join([artist.user.username for artist in obj.artists.all()])
    get_artists.short_description = 'Artists'

    def get_genres(self, obj):
        return ", ".join([genre.title for genre in obj.genres.all()])
    get_genres.short_description = 'Genres'
