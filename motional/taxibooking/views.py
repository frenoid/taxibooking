from django.shortcuts import render
from django.http import JsonResponse
from django.db.models.query import QuerySet
from django.views.decorators.csrf import csrf_exempt
from taxibooking.models import Customer, Car, Time
from typing import List
import json

import logging


def distance_between_two_points(x1: int, x2: int, y1: int, y2: int) -> int:
	"""
	Return the taxicab distance between 2 points (x1, y1) and (x2, y2)
	"""
	return abs(x1 - x2) + abs(y1 - y2)

def is_customer_and_car_colocated(customer: Customer, car: Car) -> bool:
	"""
	Determine if a customer and a car are at the same coordinates
	"""
	if customer.position_x == car.position_x and customer.position_y == car.position_y:
		return True

	return False

def is_car_at_customer_destination(customer: Customer, car: Car) -> bool:
	"""
	Determine if a car is at the destination of a customer
	"""
	if customer.destination_x == car.position_x and customer.destination_y == car.position_y:
		return True

	return False


def move_car_towards(car: Car, target_x: int, target_y: int) -> bool:
	"""
	Given a target location (x,y), move the car 1 distance towards it
	Car moves in the x-axis first, until car_x = target_x
	Then car moves in the y-axis, until car_y = target_y
	"""
	print(f"car {car.id} at ({car.position_x}, {car.position_y}) to move to destination ({target_x}, {target_y})")

	# Car is to the right of target
	if car.position_x > target_x:
		car.position_x -= 1
		car.save()
		print(f"car {car.id} moved 1 left")
		return True
	# Car is to the left of target
	elif car.position_x < target_x:
		car.position_x += 1
		car.save()
		print(f"car {car.id} moved 1 right")
		return True
	# Car is to the up of target
	elif car.position_y > target_y:
		car.position_y -= 1
		car.save()
		print(f"car {car.id} moved 1 down")
		return True
	# Car is to the down of target
	elif car.position_y < target_y:
		car.position_y += 1
		car.save()
		print(f"car {car.id} moved 1 up")
		return True


	return False

# Move cars
def move_cars(cars: QuerySet) -> int:
	"""
	Move all cars on the map, according to their state
	1) FREE -> Don't move
	2) ALLO -> Move towards customer
	3) INTR -> Move towards customer destination
	"""
	logging.info("Move cars")
	movements = 0
	for car in cars:
		did_move = False
		if car.booking_state == "FREE":
			pass
		elif car.booking_state == "ALLO":
			did_move = move_car_towards(car=car,
				target_x=car.customer.position_x,
				target_y=car.customer.position_y)
		elif car.booking_state == "INTR":
			did_move = move_car_towards(car=car,
				target_x=car.customer.destination_x,
				target_y=car.customer.destination_y)

		if did_move:
			movements += 1

	return movements


# Change car booking state
def update_car_booking_state(cars: QuerySet, customers: QuerySet) -> int:
	"""
	Update the booking_state of all cars, depending on their previous state and position
	1) FREE cars -> no change
	2) ALLO cars -> if they have reached customer source, change their state to INTR
	3) INTR cars -> if they have reached customer destination, change their state to FREE
	"""
	state_changes = 0
	for car in cars:
		print(f"car {car.id} is in {car.booking_state} state")

		if car.booking_state == "FREE":
			pass

		elif car.booking_state == "ALLO":
			if is_customer_and_car_colocated(car=car, customer=car.customer):
				car.booking_state = "INTR"
				car.save()
				print(f"car {car.id} changed from ALLO to INTR")
				state_changes += 1

		elif car.booking_state == "INTR":
			if is_car_at_customer_destination(car=car, customer=car.customer):
				car.booking_state = "FREE"
				car.customer = None
				car.save()
				print(f"car {car.id} changed from INTR to FREE")
				state_changes += 1

	
	return state_changes


def advance_world(cars: QuerySet, customers: QuerySet, current_time: Time) -> int:
	"""
	Advance time and simulate car and passenger actions
	1) Move cars to customers or customer destinations
	2) Update car states
	3) Increment time
	"""
	movement_count = move_cars(cars=cars)
	state_change_count = update_car_booking_state(cars=cars, customers=customers)
	print(f"from tick {current_time.tick} to {current_time.tick + 1}")
	print(f"there were {movement_count} movements")
	print(f"there were {state_change_count} booking state changes")

	current_time.tick += 1
	current_time.save()

	return current_time.tick 

def get_lowest_distance(customer: Customer, cars: QuerySet) ->  int:
	"""
	Return the lowest distance between a Customer and QuerySet[Car]
	"""
	distances = []

	for car in cars:
		distance = distance_between_two_points(
			x1=customer.position_x,
			x2=car.position_x,
			y1=customer.position_y,
			y2=car.position_y)
		distances.append(distance)

	distances.sort()

	return distances[0]


def get_cars_of_x_distance_to_customer(x_distance: int, customer: Customer, cars: QuerySet) -> List[Car]:
	"""
	Return the list of Car which are a certain distnace(x_distance) from a customer source 
	"""
	x_distance_cars = []

	for car in cars:
		distance_of_car_from_customer = distance_between_two_points(
			x1=customer.position_x,
			x2=car.position_x,
			y1=customer.position_y,
			y2=car.position_y)
		if distance_of_car_from_customer == x_distance:
			x_distance_cars.append(car)

	return x_distance_cars

def get_car_of_lowest_id(cars: QuerySet) -> Car:
	"""
	Return the Car with the lowest id from a QuerySet[Car]
	"""
	nearest_car_with_lowest_id, lowest_car_id = None, 999999999
	for car in cars:
		if car.id < lowest_car_id:
			nearest_car_with_lowest_id, lowest_car_id = car, car.id

	return nearest_car_with_lowest_id


def find_nearest_available_car(customer: Customer, available_cars: QuerySet) -> Car:
	"""
	Return the Car which is
	1) available AND
	2) nearest to the customer AND
	3) lowest car id
	"""
	if len(available_cars) == 0:
		return None

	# Find the list of cars with the lowest distance to customer
	lowest_distance = get_lowest_distance(customer=customer, cars=available_cars)
	nearest_cars = get_cars_of_x_distance_to_customer(x_distance=lowest_distance, customer=customer, cars=available_cars)
	nearest_car_of_lowest_id = get_car_of_lowest_id(cars=nearest_cars)

	return nearest_car_of_lowest_id


def reset_cars(cars: QuerySet) -> int:
	"""
	Return all Car to their state
	1) location (0,0)
	2) state 'FREE'
	3) customer None
	"""
	if len(cars) != 3:
		Cars.objects.all().delete()
		car_1 = Car(id=1, position_x=0, position_y=0, customer=None, booking_state='FREE')
		car_1.save()
		car_2 = Car(id=2, position_x=0, position_y=0, customer=None, booking_state='FREE')
		car_2.save()
		car_3 = Car(id=3, position_x=0, position_y=0, customer=None, booking_state='FREE')
		car_3.save()

	for car in cars:
		car.position_x, car.position_y = 0, 0
		car.customer = None
		car.booking_state = 'FREE'
		car.save()

	return len(cars)

def assign_car_to_customer(customer: Customer, car: Car) -> None:
	"""
	Allocate a car to a customer
	1) Car booking state becomes 'ALLO'
	2) Car customer field is references the customer
	"""
	car.booking_state = 'ALLO'
	car.customer = customer
	car.save()

	print(f"car {car.id} was assigned to customer {customer.id}")

	return

@csrf_exempt
def index(request):
	"""
	used for health checks
	"""
	return JsonResponse({'health_check': "OK"})


@csrf_exempt
def book(request):
	"""
	given a customer of source (x1,y1) and destination (x2,y2)
	return the nearest car id and the total time needed for the car to
	1) pick up the customer
	2) send the customer to their destination

    expects a json in the request body of
	 {
	  "source": {
	    "x": x1,
	    "y": y1
	  },
	  "destination": {
	    "x": x2,
	    "y": y2
	  }
	}

	returns a json in the response body of
	{
	  "car_id": id,
	  "total_time": t
	}
	"""
	body = json.loads(request.body)
	customer = Customer(position_x=int(body['source']['x']),
		position_y=int(body['source']['y']),
		destination_x=int(body['destination']['x']),
		destination_y=int(body['destination']['y']))
	customer.save()

	nearest_car = find_nearest_available_car(
		customer=customer,
		available_cars=Car.objects.filter(booking_state='FREE'))
	assign_car_to_customer(car=nearest_car, customer=customer)
	time_for_car_to_pickup_customer = distance_between_two_points(
		x1=customer.position_x,
		x2=nearest_car.position_x,
		y1=customer.position_y,
		y2=nearest_car.position_y
		)
	time_from_source_to_destination = distance_between_two_points(
		x1=customer.position_x,
		x2=customer.destination_x,
		y1=customer.position_y,
		y2=customer.destination_y
		)

	return JsonResponse(data={
		'car_id': nearest_car.id,
		'total_time': time_for_car_to_pickup_customer + time_from_source_to_destination
		}, safe=True)


@csrf_exempt
def tick(request):
	"""
	Move time forward and causes cars to move, pick up customers, drop off customers, and change state
	"""
	new_tick = advance_world(cars=Car.objects.all(),
		customers=Customer.objects.all(),
		current_time=Time.objects.all()[0])

	return JsonResponse(data={'new_tick': new_tick})


@csrf_exempt
def reset(request):
	"""
	Return all cars to their original state
	"""
	cars = Car.objects.all()
	reset_cars(cars=cars)

	logging.info(f"Reset {len(cars)} cars")

	return JsonResponse(data={
		'view': 'reset',
		'cars_reset': len(cars)
		})