from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", views.viewsets_tickets)

urlpatterns = [
    path("customers/", views.customer_list_create),
    path("customers/<int:pk>", views.customer_update_delete),
    path("movies/", views.movie_list_create),
    path("movies/<int:pk>", views.movie_update_delete),
    path("halls/", views.hall_list_create),
    path("halls/<int:pk>", views.hall_update_delete),
    path("seats/", views.seat_list_create),
    path('seats/<int:pk>', views.seat_update_delete),
    path("tickets/", views.ticket_list_create),
    path("tickets/<int:pk>", views.ticket_update_delete),
    path("tickets/generics/", views.generics_tickets_list.as_view()),
    path("tickets/viewsets/", include(router.urls)),
]
