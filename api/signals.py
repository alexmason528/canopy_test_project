from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from rest_framework import exceptions

from .constants import *
from .models import Movie, Ticket


@receiver(pre_save, sender=Ticket)
def pre_save_ticket(sender, **kwargs):
    ticket = kwargs['instance']

    if ticket.movie.tickets_sold_out:
        raise exceptions.ValidationError({ 'details': SOLD_OUT })

    if ticket.movie.remaining_tickets_count < ticket.quantity:
        raise exceptions.ValidationError({ 'details': INSUFFICIENT_TICKETS })


@receiver(pre_save, sender=Movie)
def pre_save_movie(sender, **kwargs):
    movie = kwargs['instance']

    if movie.start_time >= movie.end_time:
        raise exceptions.ValidationError({ 'details': WRONG_DURATION })

    if Movie.objects.filter(start_time__lte=movie.start_time, end_time__gte=movie.start_time, room=movie.room).exists():
        raise exceptions.ValidationError({ 'details': MOVIE_EXIST })

    if Movie.objects.filter(start_time__lte=movie.end_time, end_time__gte=movie.end_time, room=movie.room).exists():
        raise exceptions.ValidationError({ 'details': MOVIE_EXIST })
