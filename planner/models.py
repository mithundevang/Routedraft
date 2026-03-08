from time import timezone

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profiles/", blank=True)

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interest = models.CharField(max_length=100)
    budget_range = models.IntegerField(default=1000)
    last_destination = models.CharField(max_length=200, blank=True)

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.CharField(max_length=200)
    budget = models.IntegerField()
    days = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class DayPlan(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    day_number = models.IntegerField()
    content = models.TextField()

class Attraction(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    lat = models.FloatField()
    lon = models.FloatField()

class Hotel(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price_per_night = models.IntegerField(default=80)
    lat = models.FloatField()
    lon = models.FloatField()

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.FloatField()

class Review(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    
class TripImage(models.Model):

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField()
    title = models.CharField(max_length=200, blank=True)