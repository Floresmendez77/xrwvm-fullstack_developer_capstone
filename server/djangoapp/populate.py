from .models import CarMake, CarModel


def initiate():
    car_make_data = [
        {"name": "NexaAuto", "description": "Popular car manufacturer of compact cars"},
        {"name": "Elegran Motors", "description": "American car manufacturer of luxury vehicles"},
        {"name": "Bluewave", "description": "Reliable manufacturer known for durability"},
        {"name": "Sunrise Autoworks", "description": "German manufacturer of luxury and sports cars"},
        {"name": "Trailridge Motors", "description": "Japanese manufacturer known for reliability"},
    ]

    car_models_data = [
        {"name": "Sentinel", "type": "SEDAN", "year": 2021, "make": "NexaAuto", "dealer_id": 1},
        {"name": "Ridgeback", "type": "SUV", "year": 2022, "make": "NexaAuto", "dealer_id": 2},
        {"name": "Aventis", "type": "SEDAN", "year": 2020, "make": "Elegran Motors", "dealer_id": 3},
        {"name": "Vantage GT", "type": "COUPE", "year": 2023, "make": "Elegran Motors", "dealer_id": 4},
        {"name": "Marina", "type": "WAGON", "year": 2019, "make": "Bluewave", "dealer_id": 5},
        {"name": "Coastline", "type": "SUV", "year": 2022, "make": "Bluewave", "dealer_id": 6},
        {"name": "Falcon Sport", "type": "COUPE", "year": 2023, "make": "Sunrise Autoworks", "dealer_id": 7},
        {"name": "Horizon", "type": "SEDAN", "year": 2021, "make": "Sunrise Autoworks", "dealer_id": 8},
        {"name": "Summit", "type": "SUV", "year": 2020, "make": "Trailridge Motors", "dealer_id": 9},
        {"name": "Pioneer", "type": "SEDAN", "year": 2022, "make": "Trailridge Motors", "dealer_id": 10},
    ]

    makes = {}
    for data in car_make_data:
        car_make, _ = CarMake.objects.get_or_create(
            name=data["name"],
            defaults={"description": data["description"]},
        )
        makes[data["name"]] = car_make

    for data in car_models_data:
        CarModel.objects.get_or_create(
            car_make=makes[data["make"]],
            name=data["name"],
            defaults={
                "type": data["type"],
                "year": data["year"],
                "dealer_id": data["dealer_id"],
            },
        )