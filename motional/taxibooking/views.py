from django.shortcuts import render
from django.http import JsonResponse
from django.db.models.query import QuerySet
from taxibooking.models import Customer, Car, Time
import json

import logging


def distance_between_two_points(x1: int, x2: int, y1: int, y2: int) -> int:
	return abs(x1 - x2) + abs(y1 - y2)

def is_customer_and_car_colocated(customer: Customer, car: Car) -> bool:
	if customer.position_x == car.position_x and customer.position_y == car.position_y:
		return True

	return False

def is_car_at_customer_destination(customer: Customer, car: Car) -> bool:
	if customer.destination_x == car.position_x and customer.destination_y == car.position_y:
		return True

	return False


def move_car_towards(car: Car, target_x: int, target_y: int) -> bool:
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
				car.save()
				print(f"car {car.id} changed from INTR to FREE")
				state_changes += 1

	
	return state_changes


def advance_world(cars: QuerySet, customers: QuerySet, current_time: Time) -> int:
	movement_count = move_cars(cars=cars)
	state_change_count = update_car_booking_state(cars=cars, customers=customers)
	print(f"from tick {current_time.tick} to {current_time.tick + 1}")
	print(f"there were {movement_count} movements")
	print(f"there were {state_change_count} booking state changes")

	current_time.tick += 1
	current_time.save()

	return current_time.tick 

def find_nearest_available_car(customer: Customer, available_cars: QuerySet) -> Car:
	if len(available_cars) == 0:
		return None

	nearest_car = None
	largest_distance = 9999999999

	for car in available_cars:
		distance = distance_between_two_points(
			x1=customer.position_x,
			x2=car.position_x,
			y1=customer.position_y,
			y2=car.position_y)
		if distance < largest_distance:
			nearest_car = car

	return nearest_car

def reset_cars(cars: QuerySet) -> int:
	for car in cars:
		car.position_x, car.position_y = 0, 0
		car.customer = None
		car.booking_state = 'FREE'
		car.save()

	return len(cars)

def assign_car_to_customer(customer: Customer, car: Car) -> None:
	car.booking_state = 'ALLO'
	car.customer = customer
	car.save()

	return

def index(request):
	return JsonResponse({'health_check': "OK"})


# /api/book
def book(request):
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

	return JsonResponse({
		'car_id': nearest_car.id,
		'total_time': time_for_car_to_pickup_customer + time_from_source_to_destination
		})


# /api/tick
def tick(request):
	new_tick = advance_world(cars=Car.objects.all(),
		customers=Customer.objects.all(),
		current_time=Time.objects.all()[0])

	return JsonResponse({'new_tick': new_tick})


# /api/reset
def reset(request):
	cars = Car.objects.all()
	reset_cars(cars=cars)

	logging.info(f"Reset {len(cars)} cars")

	return JsonResponse({
		'view': 'reset',
		'cars_reset': len(cars)
		})