import logging
import json

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .restapis import (
    get_dealers_from_cf,
    get_dealer_by_id_from_cf,
    get_dealer_reviews_from_cf,
    post_review,
    analyze_review_sentiments,
)

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}
    if user is not None:
        login(request, user)
        response_data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(response_data)


def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    username_exist = False
    try:
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        logger.debug("%s is a new user", username)

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})

    return JsonResponse({"userName": username, "error": "Already Registered"})


def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_dealers_from_cf(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})
    endpoint = f"/fetchDealer/{dealer_id}"
    dealership = get_dealer_by_id_from_cf(endpoint, dealer_id)
    return JsonResponse({"status": 200, "dealer": dealership})


def get_dealer_reviews(request, dealer_id):
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})
    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_dealer_reviews_from_cf(endpoint)
    for review_detail in reviews:
        response = analyze_review_sentiments(review_detail.get('review', ''))
        review_detail['sentiment'] = response.get('sentiment') if response else None
    return JsonResponse({"status": 200, "reviews": reviews})


@csrf_exempt
def add_review(request):
    if request.user.is_anonymous:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
    data = json.loads(request.body)
    try:
        post_review(data)
        return JsonResponse({"status": 200})
    except Exception:
        return JsonResponse({"status": 401, "message": "Error posting review"})


def get_cars(request):
    count = CarMake.objects.count()
    if count == 0:
        from .populate import initiate
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {"CarModel": cm.name, "CarMake": cm.car_make.name}
        for cm in car_models
    ]
    return JsonResponse({"CarModels": cars})