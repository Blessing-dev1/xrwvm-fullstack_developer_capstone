# server/djangoapp/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
import logging, json


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
        # Even if logout fails, still redirect to login
    return redirect('djangoapp:login')

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration` view to handle sign up request
# @csrf_exempt
# def registration(request):
# ...

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
