from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.name}'

class Movie(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.title}'

class Hall(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    
    def __str__(self):
        return f'{self.name}'

class Seat(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    row = models.IntegerField()
    number = models.IntegerField()
    is_booked = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Hall: {self.hall.name}, Row: {self.row}, Seat: {self.number}'

class Ticket(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat_number = models.ForeignKey(Seat, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ticket for {self.movie.title} on {self.date} at {self.time}'