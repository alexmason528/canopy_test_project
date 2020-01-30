from django.conf.urls import url, include

from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()

router.register(r'room', RoomViewSet)
router.register(r'movie', MovieViewSet)
router.register(r'ticket', TicketViewSet)
router.register(r'theater-playing-movies', TheaterPlayingMovieViewSet, basename='theater-playing-movie')

urlpatterns = [
    url(r'', include(router.urls)),
]
