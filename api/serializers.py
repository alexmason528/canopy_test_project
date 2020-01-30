from rest_framework import serializers

from .constants import *
from .models import Room, Movie, Ticket


class RepresentSerializerMixin(object):
    def to_representation(self, obj):
        return self.Meta.representation_serializer(obj).data


class RoomMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        

class RoomSerializer(serializers.ModelSerializer):
    current_playing_movie = RoomMovieSerializer()

    class Meta:
        model = Room
        fields = ('id', 'name', 'capacity', 'current_playing_movie')


class MovieReadSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    remaining_tickets = serializers.IntegerField(source='remaining_tickets_count')

    class Meta:
        model = Movie
        fields = '__all__'


class MovieCreateSerializer(RepresentSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        representation_serializer = MovieReadSerializer

    def validate(self, data):
        start_time = data['start_time']
        end_time = data['end_time']
        room = data['room']
 
        if start_time > end_time:
            raise serializers.ValidationError(WRONG_DURATION)

        if Movie.objects.filter(start_time__lte=start_time, end_time__gte=end_time, room=room).exists():
            raise serializers.ValidationError(MOVIE_EXIST)

        if Movie.objects.filter(start_time__lte=start_time, end_time__gte=end_time, room=room).exists():
            raise serializers.ValidationError(MOVIE_EXIST)

        return data


class TicketReadSerializer(serializers.ModelSerializer):
    movie = MovieReadSerializer()

    class Meta:
        model = Ticket
        fields = '__all__'


class TicketCreateSerializer(RepresentSerializerMixin, serializers.ModelSerializer):
    def validate(self, data):
        movie = data['movie']
        quantity = data['quantity']

        if movie.tickets_sold_out:
            raise serializers.ValidationError(SOLD_OUT)

        if movie.remaining_tickets_count < quantity:
            raise serializers.ValidationError(INSUFFICIENT_TICKETS)

    class Meta:
        model = Ticket
        fields = '__all__'
        representation_serializer = TicketReadSerializer
