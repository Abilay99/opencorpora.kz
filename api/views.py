from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, generics
from main.models import Corpora, Genres
from .serializers import CorporaSerializer, GenresSerializer
from rest_framework.pagination import PageNumberPagination


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def corpora(request):
    if request.method == 'GET':
        corpora = Corpora.objects.all().order_by('-id')[:10]
        serializer = CorporaSerializer(corpora, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def genres(request):
    if request.method == 'GET':
        genres = Genres.objects.all().order_by('-id')[:5]
        serializer = GenresSerializer(genres, many=True)
        return Response(serializer.data)