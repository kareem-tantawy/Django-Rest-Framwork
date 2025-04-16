from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Ticket

@receiver(post_delete, sender=Ticket)
def unbook_seat_on_ticket_delete(sender, instance, **kwargs):
    seat = instance.seat_number
    seat.is_booked = False
    seat.save()
