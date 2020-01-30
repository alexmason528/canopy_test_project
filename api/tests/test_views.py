from datetime import datetime, timedelta

from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from api.constants import *
from api.factories import RoomFactory, MovieFactory, TicketFactory

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()


class RoomViewSetTestCase(ViewTestCase):
    def test_room_create_success(self):
        room_data = {'name': 'Room 1', 'capacity': 500}
        response = self.client.post('/api/room/', room_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], room_data['name'])

    def test_room_create_fail_with_missing_param(self):
        room_data = {'name': 'Room 1'}
        response = self.client.post('/api/room/', room_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_room_list_success(self):
        room_count = 2
        for i in range(0, room_count):
            RoomFactory()

        response = self.client.get('/api/room/', format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), room_count)


class MovieViewSetTestCase(ViewTestCase):
    def test_movie_create_success(self):
        room = RoomFactory()
        movie_data = {
            'name': 'Movie 1',
            'start_time': '11:00:00',
            'end_time':'13:00:00',
            'room': room.id
        }
        response = self.client.post('/api/movie/', movie_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], movie_data['name'])
        self.assertEqual(response.data['room']['name'], room.name)

    def test_movie_create_fail_with_missing_param(self):
        movie_data = {
            'name': 'Movie 1',
        }
        response = self.client.post('/api/movie/', movie_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_movie_create_fail_with_invalid_show_time(self):
        room = RoomFactory()
        movie_data = {
            'name': 'Movie 1',
            'start_time': '13:00:00',
            'end_time':'10:00:00',
            'room': room.id,
        }
        response = self.client.post('/api/movie/', movie_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['non_field_errors'][0]), WRONG_DURATION)

    def test_movie_create_fail_with_movie_exist(self):
        room = RoomFactory()
        MovieFactory(name='Movie 1', start_time='10:00:00', end_time='12:00:00', room=room)

        movie_data = {
            'name': 'Movie 2',
            'start_time': '09:00:00',
            'end_time':'11:00:00',
            'room': room.id,
        }
        response = self.client.post('/api/movie/', movie_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['non_field_errors'][0]), MOVIE_EXIST)

        movie_data = {
            'name': 'Movie 2',
            'start_time': '11:00:00',
            'end_time':'13:00:00',
            'room': room.id
        }
        response = self.client.post('/api/movie/', movie_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['non_field_errors'][0]), MOVIE_EXIST)

    def test_movie_list_success(self):
        MovieFactory(start_time='14:00:00', end_time='16:00:00')

        response = self.client.get('/api/movie/', format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TicketViewSetTestCase(ViewTestCase):
    def test_ticket_create_success(self):
        movie = MovieFactory(name='Movie 1', start_time='10:00:00', end_time='12:00:00')

        ticket_data = {'movie': movie.id, 'quantity': 1}
        response = self.client.post('/api/ticket/', ticket_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['quantity'], ticket_data['quantity'])

    def test_ticket_create_fail_with_missing_param(self):
        ticket_data = {'quantity': 1}
        response = self.client.post('/api/ticket/', ticket_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ticket_create_fail_with_sold_out(self):
        room = RoomFactory(capacity=10)
        movie = MovieFactory(start_time='10:00:00', end_time='12:00:00', room=room)
        TicketFactory(quantity=10, movie=movie)

        ticket_data = {'quantity': 1, 'movie': movie.id}
        response = self.client.post('/api/ticket/', ticket_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['non_field_errors'][0]), SOLD_OUT)

    def test_ticket_create_fail_with_insufficient_tickets(self):
        room = RoomFactory(capacity=10)
        movie = MovieFactory(start_time='10:00:00', end_time='12:00:00', room=room)
        TicketFactory(quantity=5, movie=movie)

        ticket_data = {'quantity': 10, 'movie': movie.id}
        response = self.client.post('/api/ticket/', ticket_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['non_field_errors'][0]), INSUFFICIENT_TICKETS)

    def test_ticket_list_success(self):
        movie = MovieFactory(name='Movie 1', start_time='10:00:00', end_time='12:00:00')
        ticket_count = 2
        for i in range(0, ticket_count):
            TicketFactory(movie=movie)

        response = self.client.get('/api/ticket/', format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), ticket_count)


class TheaterPlayingMovieViewSet(ViewTestCase):
    def test_playing_movie_list_success(self):
        room1 = RoomFactory()
        room2 = RoomFactory()

        current_time = datetime.now()

        movie1 = MovieFactory(room=room1, start_time=current_time, end_time=current_time + timedelta(hours=2))

        movie2 = MovieFactory(room=room1, start_time=current_time, end_time=current_time + timedelta(hours=2))

        movie3 = MovieFactory(room=room1, start_time=current_time - timedelta(hours=5), end_time=current_time - timedelta(hours=3))

        response = self.client.get('/api/theater-playing-movies/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
