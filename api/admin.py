from django.contrib import admin

from .models import Room, Movie, Ticket

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'movie_count')

class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'room', 'sold_tickets_count', 'remaining_tickets_count', 'tickets_sold_out')
    list_display_links = ('name',)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('movie', 'quantity')
    list_display_links = ('movie',)

admin.site.register(Room, RoomAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Ticket, TicketAdmin)
