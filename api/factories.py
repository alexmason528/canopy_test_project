import factory

from .models import Room, Movie, Ticket

class RoomFactory(factory.DjangoModelFactory):
    class Meta:
        model = Room

    name = factory.Sequence(lambda n: 'Room %s' % n)
    capacity = factory.Sequence(lambda n: n * 10)


class MovieFactory(factory.DjangoModelFactory):
    class Meta:
        model = Movie
    
    name = factory.Sequence(lambda n: 'Movie %s' % n)
    start_time = factory.Sequence(lambda n: '%s:00:00' % (n * 2))
    end_time = factory.Sequence(lambda n: '%s:00:00' % (n + 1) * 2)
    room = factory.SubFactory(RoomFactory)


class TicketFactory(factory.DjangoModelFactory):
    class Meta:
        model = Ticket
    
    movie = factory.SubFactory(MovieFactory)
    quantity = 1
