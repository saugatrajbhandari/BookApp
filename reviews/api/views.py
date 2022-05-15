from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from reviews.models import Book, Contributor, Publisher
from .serializer import BookSerailizer, ContributorSerializer, PublisherSerailizer


class BookModelViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerailizer
    queryset = Book.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ContributorView(generics.ListAPIView):
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()


class PublisherModelViewSet(viewsets.ModelViewSet):
    serializer_class = PublisherSerailizer
    queryset = Publisher.objects.all()