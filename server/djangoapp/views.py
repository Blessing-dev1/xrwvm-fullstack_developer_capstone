from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
import logging, json
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

logger = logging.getLogger(__name__)

@csrf_exempt
def login_user(request):
    try:
        payload = json.loads(request.body)
        username = payload['userName']
        password = payload['password']
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Login payload error: {e}")
        return JsonResponse({"error": "Invalid request data"}, status=400)

    try:
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        else:
            return JsonResponse({"userName": username, "status": "Failed"}, status=401)
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        return JsonResponse({"error": "Server error"}, status=500)

def logout_view(request):
    try:
        logout(request)
    except Exception as e:
        logger.error(f"Logout error: {e}")
    return redirect('djangoapp:login')

def initiate():
    toyota = CarMake.objects.create(name="Toyota", description="Reliable Japanese brand.")
    honda = CarMake.objects.create(name="Honda", description="Popular compact vehicles.")

    CarModel.objects.create(car_make=toyota, dealer_id=1, name="Corolla", type="SEDAN", year=2020)
    CarModel.objects.create(car_make=toyota, dealer_id=2, name="RAV4", type="SUV", year=2021)
    CarModel.objects.create(car_make=honda, dealer_id=3, name="Civic", type="SEDAN", year=2022)
    CarModel.objects.create(car_make=honda, dealer_id=4, name="CR-V", type="SUV", year=2023)

def get_cars(request):
    if CarMake.objects.count() == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    cars = [{"CarModel": cm.name, "CarMake": cm.car_make.name} for cm in car_models]
    return JsonResponse({"CarModels": cars})

# ✅ REPLACED /fetchDealers with /djangoapp/get_dealers
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/djangoapp/get_dealers"
    else:
        endpoint = f"/djangoapp/get_dealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

# ✅ REPLACED /fetchDealer with /djangoapp/get_dealer
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/djangoapp/get_dealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# ✅ REPLACED /fetchReviews with /djangoapp/get_reviews
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/djangoapp/get_reviews/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail.get('review', ''))
            review_detail['sentiment'] = response.get('label', 'unknown')
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

@csrf_exempt
def add_review(request):
    if not request.user.is_anonymous:
        try:
            data = json.loads(request.body)
            response = post_review(data)
            return JsonResponse({"status": 200, "result": response})
        except Exception as e:
            logger.error(f"Error posting review: {e}")
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
