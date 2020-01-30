from datetime import datetime, timedelta

from django.test import TestCase

from api.factories import RoomFactory, MovieFactory, TicketFactory

class RoomModelTestCase(TestCase):
    def setUp(self):
        self.room = RoomFactory()

    def test_str(self):
        self.assertEqual(str(self.room), self.room.name)
    
    def test_movie_count(self):
        movie_count = 2
        for i in range(0, movie_count):
            MovieFactory(room=self.room)

        self.assertEqual(self.room.movie_count, movie_count)

    def test_current_playing_movie(self):
        self.assertEqual(self.room.current_playing_movie, None)

        current_time = datetime.now()
        MovieFactory(room=self.room, start_time=current_time, end_time=current_time + timedelta(hours=2))
        self.assertNotEqual(self.room.current_playing_movie, None)
        self.assertEqual(self.room.movie_count, 1)


class MovieModelTestCase(TestCase):
    def setUp(self):
        self.movie = MovieFactory()
        self.ticket_count = 10

        for i in range(0, self.ticket_count):
            TicketFactory(movie=self.movie)

    def test_str(self):
        movie = self.movie
        self.assertEqual(str(movie), '%s (%s) : %s - %s' % (movie.name, movie.room, movie.start_time, movie.end_time))

    def test_sold_tickets_count(self):
        self.assertEqual(self.movie.sold_tickets_count, self.ticket_count)

    def test_remaining_tickets_count(self):
        self.assertEqual(self.movie.remaining_tickets_count, self.movie.room.capacity - self.ticket_count)

    def test_tickets_sold_sout(self):
        self.assertEqual(self.movie.tickets_sold_out, (self.movie.room.capacity - self.ticket_count) == 0)


class TicketTestCase(TestCase):
    def setUp(self):
        self.ticket = TicketFactory()

    def test_str(self):
        ticket = self.ticket
        movie = ticket.movie

        self.assertEqual(str(ticket), '%s - %s : %s' % (movie.room, movie.name, ticket.quantity))
