from datetime import datetime

from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from .models import Room, Movie, Ticket

from .serializers import (
    RoomSerializer, RoomMovieSerializer,
    MovieCreateSerializer, MovieReadSerializer,
    TicketCreateSerializer, TicketReadSerializer,
)

class CreateReadViewSetMixin(object):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.read_serializer_class
        return self.create_serializer_class


class RoomViewSet(CreateModelMixin, ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class MovieViewSet(CreateReadViewSetMixin, CreateModelMixin, ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    read_serializer_class = MovieReadSerializer
    create_serializer_class = MovieCreateSerializer


class TicketViewSet(CreateReadViewSetMixin, CreateModelMixin, ReadOnlyModelViewSet):
    queryset = Ticket.objects.all()
    read_serializer_class = TicketReadSerializer
    create_serializer_class = TicketCreateSerializer


class TheaterPlayingMovieViewSet(ListModelMixin, GenericViewSet):
    serializer_class = MovieReadSerializer

    def get_queryset(self):
        current_time = datetime.now()

        return Movie.objects.filter(start_time__lte=current_time, end_time__gte=current_time).all()
