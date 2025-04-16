from rest_framework import serializers
from .models import Customer, Movie, Hall, Seat, Ticket


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "name", "email", "phone"]


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title"]


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ["id", "name", "capacity"]


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ["id", "hall", "row", "number", "is_booked"]


class TicketSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    hall = HallSerializer()
    movie = MovieSerializer()
    seat_number = SeatSerializer()

    class Meta:
        model = Ticket
        fields = [
            "id",
            "customer",
            "hall",
            "date",
            "time",
            "movie",
            "seat_number",
            "price",
            "booking_date",
        ]

    def create(self, validated_data):
        customer_data = validated_data.pop("customer")
        movie_data = validated_data.pop("movie")
        hall_data = validated_data.pop("hall")
        seat_number_data = validated_data.pop("seat_number")

        # Create or get customer, movie, hall
        customer, _ = Customer.objects.get_or_create(**customer_data)
        movie, _ = Movie.objects.get_or_create(**movie_data)
        hall, _ = Hall.objects.get_or_create(**hall_data)

        # Get or create seat
        seat_number, _ = Seat.objects.get_or_create(
            hall=hall,
            row=seat_number_data["row"],
            number=seat_number_data["number"],
            defaults={"is_booked": False},
        )

        # Mark the seat as booked
        seat_number.is_booked = True
        seat_number.save()

        # Add them to validated_data for creating the ticket
        validated_data["customer"] = customer
        validated_data["movie"] = movie
        validated_data["hall"] = hall
        validated_data["seat_number"] = seat_number

        return super().create(validated_data)

    def delete(self, validated_data):
        customer_data = validated_data.pop("customer")
        movie_data = validated_data.pop("movie")
        hall_data = validated_data.pop("hall")
        seat_number_data = validated_data.pop("seat_number")

        # Create or get customer, movie, hall
        customer, _ = Customer.objects.get_or_create(**customer_data)
        movie, _ = Movie.objects.get_or_create(**movie_data)
        hall, _ = Hall.objects.get_or_create(**hall_data)
        seat_number, _ = Seat.objects.get_or_create(
            hall=hall,
            row=seat_number_data["row"],
            number=seat_number_data["number"],
            defaults={"is_booked": False},
        )

        # Mark the seat as booked
        seat_number.is_booked = True
        seat_number.save()
