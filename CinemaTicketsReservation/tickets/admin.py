from django.contrib import admin
from .models import Customer, Movie, Hall, Ticket, Seat

admin.site.register(Customer)
admin.site.register(Movie)
admin.site.register(Seat)
admin.site.register(Hall)
admin.site.register(Ticket)
