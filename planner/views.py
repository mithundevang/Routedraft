

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from datetime import datetime
from .models import Review, Trip, DayPlan, Attraction, Hotel, Booking, TripImage
from .utils import get_coordinates, get_attractions, distribute_days
from django.conf import settings
import requests
import json

from .models import Trip, DayPlan, Attraction, Hotel, Booking
from .utils import get_coordinates, get_attractions, distribute_days







# ================= HOME =================
def home(request):
    return render(request, "home.html")


# ================= PLAN TRIP =================
@login_required
def plan_trip(request):

    if request.method == "POST":

        action = request.POST.get("action")

        # ===================================
        # 🌍 SMART EXPLORER (Google Maps)
        # ===================================
        from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def plan_trip(request):

    if request.method == "POST":

        action = request.POST.get("action")

        # =====================================
        # 🤖 NORMAL AI TRIP PLANNER
        # =====================================
        if action == "normal":

            destination = request.POST.get("destination")
            request.session["latest_destination"] = destination
            
            budget = request.POST.get("budget")
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")

            if not destination or not budget or not start_date or not end_date:
                return render(request, "plan.html", {
                    "error": "All fields are required."
                })

            budget = int(budget)

            try:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.strptime(end_date, "%Y-%m-%d")
                days = (end - start).days

                if days <= 0:
                    return render(request, "plan.html", {
                        "error": "End date must be after start date."
                    })

            except:
                return render(request, "plan.html", {
                    "error": "Invalid date selection."
                })
                
            request.session["latest_destination"] = destination
            request.session["latest_budget"] = budget
            request.session["latest_days"] = days
            
            
            

            lat, lon = get_coordinates(destination)

            if not lat or not lon:
                return render(request, "plan.html", {
                    "error": "Destination not found."
                })

            attractions = get_attractions(lat, lon)

            if not attractions:
                return render(request, "plan.html", {
                    "error": "No attractions found."
                })

            itinerary = distribute_days(attractions, days)
            request.session["planned_places"] = attractions

           

            return render(request, "itinerary.html", {
                "destination": destination,
                "budget": budget,
                "days": days,
                "itinerary": itinerary
            })
            
           
        

        # =====================================
        # 🌍 SMART EXPLORER (Google Maps)
        # =====================================
        elif action == "advanced":

            city = request.POST.get("city")
            
            request.session["map_mode"] = "explorer"
            
            
            
            
            request.session["latest_destination"] = city
            budget = request.POST.get("budget")
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            

            if not city or not budget or not start_date or not end_date:
                return render(request, "plan.html", {
                    "error": "All fields are required."
                })

            budget = int(budget)

            try:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.strptime(end_date, "%Y-%m-%d")
                days = (end - start).days

                if days <= 0:
                    return render(request, "plan.html", {
                        "error": "End date must be after start date."
                    })

            except:
                return render(request, "plan.html", {
                    "error": "Invalid date selection."
                })
                
                   
            request.session["latest_destination"] = city
            request.session["latest_budget"] = budget
            request.session["latest_days"] = days
                
                # ✅ ADD THIS ONLY
           

            # Budget based suggestion
            if budget <= 5000:
                place_type = "nearby nature places waterfalls temples"
            elif budget <= 20000:
                place_type = "hill stations beaches wildlife parks"
            else:
                place_type = "top tourist attractions island trips adventure"

            # Days based suggestion
            if days <= 2:
                place_count = "top 10"
            elif days <= 5:
                place_count = "top 20"
            else:
                place_count = "top 30"

            search_query = f"{city} {place_count} {place_type}"
            google_maps_url = f"https://www.google.com/maps/search/{search_query}"

            return render(request, "plan.html", {
    "google_maps_url": google_maps_url
})

    return render(request, "plan.html")
#---------------------Trip_details---------------------



@login_required
def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    attractions = Attraction.objects.filter(trip=trip)

    return render(request, "trip_detail.html", {
        "trip": trip,
        "attractions": attractions
    })








# ================= BOOKINGS =================
@login_required
def bookings(request):
    user_bookings = Booking.objects.filter(user=request.user)
    return render(request, "bookings.html", {
        "bookings": user_bookings
    })


# ================= MAP VIEW =================
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
import json
from .models import Trip


@login_required
def map_view(request):

    destination = request.session.get("latest_destination")
    planned_places = request.session.get("planned_places", [])
    mode = request.session.get("map_mode")

    places = []

    # -----------------------------
    # SMART EXPLORER MODE
    # -----------------------------
    if mode == "explorer" and destination:

        geo_url = f"https://nominatim.openstreetmap.org/search?q={destination}&format=json&limit=1"
        headers = {"User-Agent": "TripPlannerApp"}

        try:
            response = requests.get(geo_url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                if data:
                    lat = float(data[0]["lat"])
                    lon = float(data[0]["lon"])

                    places = [{
                        "name": destination,
                        "lat": lat,
                        "lng": lon
                    }]

        except:
            places = []

        return render(request, "map.html", {
            "places": json.dumps(places),
            "route": json.dumps([]),
            "destination": destination,
            "explorer_mode": True
        })

    # -----------------------------
    # SMART PLANNER MODE
    # -----------------------------
    if not destination:
        return redirect("plan_trip")

    for p in planned_places:
        places.append({
            "name": p["name"],
            "lat": float(p["lat"]),
            "lng": float(p["lon"])
        })

    return render(request, "map.html", {
        "places": json.dumps(places),
        "route": json.dumps([]),
        "destination": destination,
        "explorer_mode": False
    })
# ================= COST ESTIMATION =================
@login_required
def cost_estimate(request):

    trip_id = request.session.get("current_trip_id")

    # 🔥 fallback to planned trip session
    if not trip_id:

        destination = request.session.get("latest_destination")
        days = request.session.get("latest_days")

        if not destination or not days:
            return render(request, "cost.html", {"trip": None})

        avg_hotel_per_night = 80
        hotel_cost = avg_hotel_per_night * days

        food_per_day = 30
        food_cost = food_per_day * days

        attraction_cost = 100
        travel_cost = 50

        total = hotel_cost + food_cost + attraction_cost + travel_cost

        hotel_percent = (hotel_cost / total) * 100 if total else 0
        food_percent = (food_cost / total) * 100 if total else 0
        attraction_percent = (attraction_cost / total) * 100 if total else 0
        travel_percent = (travel_cost / total) * 100 if total else 0

        # 🔥 create temporary trip object so template still works
        class TempTrip:
            def __init__(self, destination, days):
                self.destination = destination
                self.days = days

        trip = TempTrip(destination, days)

        return render(request, "cost.html", {
            "trip": trip,
            "hotel_cost": hotel_cost,
            "food_cost": food_cost,
            "attraction_cost": attraction_cost,
            "travel_cost": travel_cost,
            "total": total,
            "hotel_percent": hotel_percent,
            "food_percent": food_percent,
            "attraction_percent": attraction_percent,
            "travel_percent": travel_percent,
        })

    trip = get_object_or_404(Trip, id=trip_id, user=request.user)

    avg_hotel_per_night = 80
    hotel_cost = avg_hotel_per_night * trip.days

    food_per_day = 30
    food_cost = food_per_day * trip.days

    attraction_count = Attraction.objects.filter(trip=trip).count()
    attraction_cost = 15 * attraction_count

    travel_km = attraction_count * 5
    travel_cost = travel_km * 0.5

    total = hotel_cost + food_cost + attraction_cost + travel_cost

    hotel_percent = (hotel_cost / total) * 100 if total else 0
    food_percent = (food_cost / total) * 100 if total else 0
    attraction_percent = (attraction_cost / total) * 100 if total else 0
    travel_percent = (travel_cost / total) * 100 if total else 0

    return render(request, "cost.html", {
        "trip": trip,
        "hotel_cost": hotel_cost,
        "food_cost": food_cost,
        "attraction_cost": attraction_cost,
        "travel_cost": travel_cost,
        "total": total,
        "hotel_percent": hotel_percent,
        "food_percent": food_percent,
        "attraction_percent": attraction_percent,
        "travel_percent": travel_percent,
    })

# ================= SIGNUP =================
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})


# ================= AUTO GUIDE =================
from django.conf import settings
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='login')
def guide(request):
    
    
   

    city = request.session.get("latest_destination")

    if not city:
        return render(request, "guide.html", {
            "error": "Please plan a trip first."
        })

    try:

        # ===============================
        # WEATHER API (FORECAST 4 DAYS)
        # ===============================
        weather_url = (
            f"https://api.weatherapi.com/v1/forecast.json"
            f"?key={settings.WEATHER_API_KEY}&q={city}&days=4&aqi=yes"
        )

        response = requests.get(weather_url, timeout=10)

        if response.status_code != 200:
            raise Exception("Weather API failed")

        data = response.json()

        if "current" not in data:
            raise Exception("Invalid weather data")

        # ========================
        # CURRENT WEATHER
        # ========================
        temperature = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        icon = data["current"]["condition"]["icon"]
        feels_like = data["current"]["feelslike_c"]
        humidity = data["current"]["humidity"]
        wind_kph = data["current"]["wind_kph"]
        local_time = data["location"]["localtime"]
        country = data["location"]["country"]
        uv_index = data["current"]["uv"]

        # ========================
        # 4 DAY FORECAST
        # ========================
        forecast = []

        for day in data["forecast"]["forecastday"]:
            forecast.append({
                "date": day["date"],
                "temp": day["day"]["avgtemp_c"],
                "condition": day["day"]["condition"]["text"],
                "icon": day["day"]["condition"]["icon"]
            })

        # ========================
        # SMART WEATHER ANALYSIS
        # ========================
        if temperature >= 35:
            weather_advice = "Extreme heat expected. Avoid afternoon travel."
            dressing_tip = "Light cotton clothes, sunscreen, sunglasses."
            travel_score = 5

        elif temperature <= 10:
            weather_advice = "Cold weather conditions."
            dressing_tip = "Jackets, thermal wear."
            travel_score = 6

        elif "rain" in condition.lower():
            weather_advice = "Rain likely. Plan indoor activities."
            dressing_tip = "Umbrella, waterproof shoes."
            travel_score = 7

        else:
            weather_advice = "Excellent weather for outdoor exploration."
            dressing_tip = "Comfortable casual wear."
            travel_score = 9

        # ========================
        # SEASON TIP
        # ========================
        season_tip = (
            f"This is a great time to visit {city}."
            if 18 <= temperature <= 30
            else f"Check seasonal tourism trends before visiting {city}."
        )

        # ========================
        # TRANSPORT GUIDE
        # ========================
        transport_guide = [
            f"Public buses operate across {city}.",
            "Metro services available (if applicable).",
            "Ride-sharing apps like Uber/Ola available.",
            "Car & bike rentals available."
        ]

        # ========================
        # FOOD RECOMMENDATIONS
        # ========================
        best_foods = [
            f"Famous street food in {city}",
            "Local traditional dishes",
            "Top-rated restaurants",
            "Popular cafes"
        ]

        # ========================
        # BUDGET TIP
        # ========================
        avg_daily_budget = 50
        budget_tip = f"Estimated daily budget in {city}: ${avg_daily_budget} - ${avg_daily_budget + 30}"

        # ========================
        # ACCOMMODATION
        # ========================
        accommodation_tip = "Budget to premium hotels available depending on location."

        # ========================
        # PACKING LIST
        # ========================
        packing_list = [
            "Valid ID / Passport",
            "Comfortable walking shoes",
            "Power bank",
            "Weather appropriate clothing",
            "Basic medicines"
        ]

        # ========================
        # SAFETY
        # ========================
        safety_index = "Tourist Friendly Area"

        emergency_map = {
            "India": "Police: 100 | Ambulance: 108 | Emergency: 112",
            "United States": "Emergency: 911",
            "United Kingdom": "Emergency: 999",
            "France": "Police: 17 | Ambulance: 15 | Fire: 18",
            "Japan": "Police: 110 | Ambulance: 119",
            "Australia": "Emergency: 000",
            "Canada": "Emergency: 911",
            "Germany": "Police: 110 | Emergency: 112",
            "Singapore": "Police: 999 | Ambulance: 995"
        }

        currency_map = {
            "India": "Indian Rupee (INR)",
            "United States": "US Dollar (USD)",
            "United Kingdom": "British Pound (GBP)",
            "France": "Euro (EUR)",
            "Germany": "Euro (EUR)",
            "Japan": "Japanese Yen (JPY)",
            "Australia": "Australian Dollar (AUD)",
            "Canada": "Canadian Dollar (CAD)",
            "Singapore": "Singapore Dollar (SGD)"
        }

        emergency_numbers = emergency_map.get(country, "Emergency: 112")
        currency_info = currency_map.get(country, f"Local currency used in {country}")

        # ========================
        # SUMMARY
        # ========================
        summary = (
            f"{city}, {country} currently has {condition.lower()} weather "
            f"with {temperature}°C. Travel comfort score: {travel_score}/10."
        )

    except Exception:
        return render(request, "guide.html", {
            "error": "Unable to fetch guide information at the moment."
        })

    # ========================
    # CONTEXT
    # ========================
    context = {

        "city": city,
        "country": country,

        "temperature": temperature,
        "condition": condition,
        "icon": icon,
        "feels_like": feels_like,
        "humidity": humidity,
        "wind_kph": wind_kph,
        "local_time": local_time,
        "uv_index": uv_index,

        "forecast": forecast,

        "weather_advice": weather_advice,
        "dressing_tip": dressing_tip,
        "season_tip": season_tip,

        "transport_guide": transport_guide,
        "best_foods": best_foods,

        "budget_tip": budget_tip,
        "accommodation_tip": accommodation_tip,

        "packing_list": packing_list,

        "safety_index": safety_index,
        "emergency_numbers": emergency_numbers,
        "currency_info": currency_info,

        "summary": summary,
        "travel_score": travel_score
    }

    return render(request, "guide.html", context)


# =========================
# TRIP PREVIEW PAGE
# =========================
import requests
from django.shortcuts import render

def trip_preview(request):

    # get destination from session
    destination = request.session.get("latest_destination",)

    url = "https://api.unsplash.com/search/photos"

    params = {
        "query": destination,
        "client_id": "klxgVTRNu6IbFX6SQYlCfbQgq4s0adqT8ZRzQJKOCzg",
        "per_page": 8
    }

    images = []

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if "results" in data:
            for img in data["results"]:
                images.append({
                    "url": img["urls"]["regular"],
                    "title": img["alt_description"] or destination
                })
        else:
            print("Unsplash Error:", data)

    except Exception as e:
        print("API Error:", e)
        
    request.session["preview_images"] = images
    
    return render(request, "trip_preview.html", {
        "destination": destination,
        "images": images
    })
    
def my_trips(request):

    trips = Trip.objects.filter(user=request.user)

    return render(request, "my_trips.html", {
        "trips": trips
    })  
    
def save_trip(request):

    destination = request.session.get("latest_destination")
    budget = request.session.get("latest_budget")
    days = request.session.get("latest_days")
    images = request.session.get("preview_images")

    if not destination:
        return redirect("plan")

    trip = Trip.objects.create(
        user=request.user,
        destination=destination,
        budget=budget,
        days=days
    )

    if images:
        for img in images:
            TripImage.objects.create(
                trip=trip,
                image_url=img["url"],
                title=img["title"]
            )

    return redirect("my_trips")


from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    trip.delete()
    return redirect("my_trips")