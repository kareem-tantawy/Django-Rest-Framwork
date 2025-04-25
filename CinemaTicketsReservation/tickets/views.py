from django.shortcuts import render
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from .models import Customer, Movie, Seat, Ticket, Hall
from .serializers import (
    CustomerSerializer,
    MovieSerializer,
    HallSerializer,
    SeatSerializer,
    TicketSerializer,
)


@api_view(["GET", "POST"])
def customer_list_create(request):
    if request.method == "GET":
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def customer_update_delete(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def movie_list_create(request):
    if request.method == "GET":
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def movie_update_delete(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def hall_list_create(request):
    if request.method == "GET":
        halls = Hall.objects.all()
        serializer = HallSerializer(halls, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = HallSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def hall_update_delete(request, pk):
    try:
        hall = Hall.objects.get(pk=pk)
    except Hall.DoesNotExist as e:
        return Response({"error": "Hall not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = HallSerializer(hall)
        return Response(serializer.data)

    elif request.method in ["PUT", "PATCH"]:
        old_status = hall.is_in_service
        serializer = HallSerializer(hall, data=request.data, partial=True)
        if serializer.is_valid():
            updated_hall = serializer.save()
            if old_status and not updated_hall.is_in_service:
                Ticket.objects.filter(hall=hall).delete()
                hall.seat_set.update(is_booked="False")
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        hall.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def seat_list_create(request):
    if request.method == "GET":
        seats = Seat.objects.all()
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = SeatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def seat_update_delete(request, pk):
    try:
        seat = Seat.objects.get(pk=pk)
    except Seat.DoesNotExist as e:
        return Response({"error": "Seat not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = SeatSerializer(seat)
        return Response(serializer.data)
    elif request.method in ["PUT", "PATCH"]:
        serializer = SeatSerializer(seat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        seat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def ticket_list_create(request):
    if request.method == "GET":
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def ticket_update_delete(request, pk):
    try:
        ticket = Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)
    elif request.method in ["PUT", "PATCH"]:
        partial = request.method == "PATCH"
        serializer = TicketSerializer(ticket, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        seat = ticket.seat_number
        seat.is_booked = False
        seat.save()
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class generics_tickets_list(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

class viewsets_tickets(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"message":"Successfull logged out"}, status=status.HTTP_200_OK)

