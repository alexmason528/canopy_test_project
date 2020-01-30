from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=256)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    @property
    def movie_count(self):
        return self.movies.count()

    @property
    def current_playing_movie(self):
        current_time = datetime.now()

        movie_filter = self.movies.filter(start_time__lte=current_time, end_time__gte=current_time)

        if movie_filter.exists():
            return movie_filter.first()
        
        return None


class Movie(models.Model):
    name = models.CharField(max_length=256)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='movies')

    def __str__(self):
        return '%s (%s) : %s - %s' % (self.name, self.room, self.start_time, self.end_time)

    @property
    def sold_tickets_count(self):
        return self.tickets.aggregate(models.Sum('quantity')).get('quantity__sum') or 0

    @property
    def remaining_tickets_count(self):
        return self.room.capacity - self.sold_tickets_count

    @property
    def tickets_sold_out(self):
        return self.remaining_tickets_count == 0


class Ticket(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='tickets')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return  '%s - %s : %s' % (self.movie.room, self.movie.name, self.quantity)
