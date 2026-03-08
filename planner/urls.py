from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("plan/", views.plan_trip, name="plan_trip"),
    path("trip/<int:trip_id>/", views.trip_detail, name="trip_detail"),
   
    path("maps/", views.map_view, name="map"),
    
    path("cost/", views.cost_estimate, name="cost"),
    
    path("save-trip/", views.save_trip, name="save_trip"),
    path("my-trips/", views.my_trips, name="my_trips"),

 path("delete-trip/<int:trip_id>/", views.delete_trip, name="delete_trip"),
 path("guide/", views.guide, name="guide"),
    path("bookings/", views.bookings, name="bookings"),
 path("trip-preview/", views.trip_preview, name="trip_preview"),

]