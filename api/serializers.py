from rest_framework import serializers

from main.models import Corpora, Genres

class CorporaSerializer(serializers.ModelSerializer):
    genre = serializers.SerializerMethodField()
    def get_genre(self, obj):
        return obj.genre.kz
    class Meta:
        model = Corpora
        fields = ('id', 'title', 'text', 'lemmas', 'morphanaliz', 'genre', 'keywords', 'annotation', 'url')

class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('id', 'rus', 'kz', 'en')