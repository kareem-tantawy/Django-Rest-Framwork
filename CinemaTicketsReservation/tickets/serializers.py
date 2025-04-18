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
        fields = ["id", "name", "capacity", "is_in_service"]


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ["id", "hall", "row", "number", "is_booked"]

    def validate(self, data):
        hall = data.get("hall") or (self.instance.hall if self.instance else None)

        if hall and not hall.is_in_service:
            raise serializers.ValidationError(
                "Cannot add or modify seats in an inactive hall."
            )

        return data


class TicketSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

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

    def validate(self, data):
        hall = data.get("hall")
        seat = data.get("seat_number")

        if not hall:
            raise serializers.ValidationError("Hall is required.")

        if not hall.is_in_service:
            raise serializers.ValidationError(
                "Sorry! this hall is currently out of service, try another hall"
            )

        if not seat:
            raise serializers.ValidationError("Seat number is required.")

        if seat.hall != hall:
            raise serializers.ValidationError(
                "This hall hasn't any seats with this location."
            )

        if seat.is_booked:
            raise serializers.ValidationError("This seat is already booked.")

        return data

    def create(self, validated_data):
        customer_data = validated_data.pop("customer")

        customer, created = Customer.objects.get_or_create(
            name=customer_data.get("name"),
            email=customer_data.get("email"),
            phone=customer_data.get("phone"),
        )

        validated_data["customer"] = customer

        # Mark the seat as booked
        seat = validated_data["seat_number"]
        seat.is_booked = True
        seat.save()

        # Add them to validated_data for creating the ticket
        return super().create(validated_data)
