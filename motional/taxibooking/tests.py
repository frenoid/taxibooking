from django.test import TestCase
from taxibooking.models import Car, Customer, Time
from . import views

 
class DistanceTests(TestCase):
	"""
	Test views.distance_between_two_points()
	"""
	def test_distance_between_two_points_1(self):
		self.assertEqual(views.distance_between_two_points(
			x1=0,x2=3,y1=0,y2=3), 6)

	def test_distance_between_two_points_2(self):
		self.assertEqual(views.distance_between_two_points(
			x1=1,x2=3,y1=1,y2=3), 4)

	def test_distance_between_two_points_3(self):
		self.assertEqual(views.distance_between_two_points(
			x1=0,x2=-3,y1=0,y2=-3), 6)



class CustomerCarTests(TestCase):
	"""
	Test views.is_customer_and_car_colocated()
	"""
	def test_is_customer_and_car_colocated_1(self):
		car_2 = Car(id=2, position_x=2, position_y=2, customer=None, booking_state='FREE')
		customer_2 = Customer(id=2, position_x=2, position_y=2, destination_x=5, destination_y=9)
		self.assertTrue(views.is_customer_and_car_colocated(customer=customer_2, car=car_2))

	def test_is_customer_and_car_colocated_2(self):
		car_3 = Car(id=3, position_x=-5, position_y=-3, customer=None, booking_state='FREE')
		customer_3 = Customer(id=3, position_x=-4, position_y=12, destination_x=3, destination_y=-7)
		self.assertFalse(views.is_customer_and_car_colocated(customer=customer_3, car=car_3))

	def test_is_car_at_customer_destination_1(self):
		customer_4 = Customer(id=4, position_x=2, position_y=-2, destination_x=8, destination_y=4)
		car_4 = Car(id=4, position_x=8, position_y=4, customer=None, booking_state='FREE')
		self.assertTrue(views.is_car_at_customer_destination(customer=customer_4, car=car_4))

	def test_is_car_at_customer_destination_2(self):
		car_1 = Car(id=1, position_x=0, position_y=0, customer=None, booking_state='FREE')
		customer_1 = Customer(id=1, position_x=0, position_y=0, destination_x=3, destination_y=3)
		self.assertFalse(views.is_car_at_customer_destination(customer=customer_1,car=car_1))


class CarMovementTests(TestCase):
	"""
	Test views.move_car_towards()
	"""
	def test_move_car_towards_1(self):
		car_1 = Car(id=1, position_x=0, position_y=0, customer=None, booking_state='FREE')
		did_move = views.move_car_towards(car=car_1, target_x=2, target_y=2)
		self.assertTrue(did_move)
		self.assertEqual(car_1.position_x, 1)
		self.assertEqual(car_1.position_y, 0)

	def test_move_car_towards_2(self):
		car_2 = Car(id=2, position_x=0, position_y=0, customer=None, booking_state='FREE')
		did_move = views.move_car_towards(car=car_2, target_x=0, target_y=2)
		self.assertTrue(did_move)
		self.assertEqual(car_2.position_x, 0)
		self.assertEqual(car_2.position_y, 1)

	def test_move_car_towards_3(self):
		car_3 = Car(id=3, position_x=0, position_y=0, customer=None, booking_state='FREE')
		did_move = views.move_car_towards(car=car_3, target_x=-4, target_y=0)
		self.assertTrue(did_move)
		self.assertEqual(car_3.position_x, -1)
		self.assertEqual(car_3.position_y, 0)

	def test_move_car_towards_4(self):
		car_4 = Car(id=4, position_x=0, position_y=0, customer=None, booking_state='FREE')
		did_move = views.move_car_towards(car=car_4, target_x=0, target_y=-4)
		self.assertTrue(did_move)
		self.assertEqual(car_4.position_x, 0)
		self.assertEqual(car_4.position_y, -1)

	def test_move_car_towards_5(self):
		car_5 = Car(id=5, position_x=0, position_y=0, customer=None, booking_state='FREE')
		did_move = views.move_car_towards(car=car_5, target_x=0, target_y=0)
		self.assertFalse(did_move)
		self.assertEqual(car_5.position_x, 0)
		self.assertEqual(car_5.position_y, 0)


class MoveCarsTests(TestCase):
	"""
	Test move_cars()
	"""
	def test_move_cars_1(self):
		customer_1 = Customer(id=1, position_x=4, position_y=4, destination_x=8, destination_y=8)
		customer_2 = Customer(id=2, position_x=3, position_y=3, destination_x=5, destination_y=-9)
		customer_1.save()
		customer_2.save()

		car_1 = Car(id=1, position_x=0, position_y=0, customer=None, booking_state='FREE')
		car_2 = Car(id=2, position_x=1, position_y=1, customer=customer_1, booking_state='ALLO')
		car_3 = Car(id=3, position_x=5, position_y=5, customer=customer_2, booking_state='INTR')
		car_1.save()
		car_2.save()
		car_3.save()

		# Expect only 2 cars to move
		cars = Car.objects.all()
		movements = views.move_cars(cars=cars)
		self.assertEqual(movements, 2)

		# Expect car 1 position to be unchanged
		car_1 = Car.objects.get(id=1)
		self.assertEqual(car_1.position_x, 0)
		self.assertEqual(car_1.position_y, 0)

		# Expect car 2 to move 1 right towards customer
		car_2 = Car.objects.get(id=2)
		self.assertEqual(car_2.position_x, 2)
		self.assertEqual(car_2.position_y, 1)

		# Expect car 3 to move 1 down towards customer destination
		car_3 = Car.objects.get(id=3)
		self.assertEqual(car_3.position_x, 5)
		self.assertEqual(car_3.position_y, 4)



class BookingStateTests(TestCase):
	"""
	Test update_car_booking_state()
	"""
	def test_update_car_booking_state(self):
		customer_1 = Customer(id=1, position_x=4, position_y=4, destination_x=8, destination_y=8)
		customer_2 = Customer(id=2, position_x=3, position_y=3, destination_x=5, destination_y=-9)
		customer_1.save()
		customer_2.save()

		car_1 = Car(id=1, position_x=0, position_y=0, customer=None, booking_state='FREE')
		car_2 = Car(id=2, position_x=4, position_y=4, customer=customer_1, booking_state='ALLO')
		car_3 = Car(id=3, position_x=5, position_y=-9, customer=customer_2, booking_state='INTR')
		car_1.save()
		car_2.save()
		car_3.save()

		# Expect only 2 cars to change state
		cars = Car.objects.all()
		customers = Customer.objects.all()
		state_changes = views.update_car_booking_state(cars=cars, customers=customers)
		self.assertEqual(state_changes, 2)

		# Expect car 1 to be in the FREE state and have no customer
		car_1 = Car.objects.get(id=1)
		self.assertEqual(car_1.booking_state, "FREE")
		self.assertEqual(car_1.customer, None)

		# Expect car 2 to be in the INTR state and have customer 1
		car_2 = Car.objects.get(id=2)
		self.assertEqual(car_2.booking_state, "INTR")
		self.assertEqual(car_2.customer, customer_1)

		# Exepect car 3 to be in the FREE state and have no customer
		car_3 = Car.objects.get(id=3)
		self.assertEqual(car_3.booking_state, "FREE")
		self.assertEqual(car_3.customer, None)

 
class AdvanceWorldTests(TestCase):
	"""
	Test advance_world()
	"""
	def test_advance_world(self):
		customer_1 = Customer(id=1, position_x=5, position_y=5, destination_x=-1, destination_y=-1)
		customer_2 = Customer(id=1, position_x=4, position_y=4, destination_x=3, destination_y=3)
		customer_1.save()
		customer_2.save()


		car_1 = Car(id=1, position_x=1, position_y=1, customer=None, booking_state='FREE')
		car_2 = Car(id=2, position_x=2, position_y=2, customer=customer_1, booking_state='ALLO')
		car_3 = Car(id=3, position_x=2, position_y=3, customer=customer_2, booking_state='INTR')
		car_1.save()
		car_2.save()
		car_3.save()

		time = Time(tick=0)
		time.save()

		new_tick = views.advance_world(cars=Car.objects.all(),
			customers=Customer.objects.all(),
			current_time=Time.objects.get(id=1))

		# Check positions of cars 1,2,3
		# car_1 does not move
		# booking_state remains in FREE
		car_1 = Car.objects.get(id=1)
		self.assertEqual(car_1.position_x, 1)
		self.assertEqual(car_1.position_y, 1)
		self.assertEqual(car_1.customer, None)
		self.assertEqual(car_1.booking_state, 'FREE')
		# car_2 moved 1 right to towards customer_1 source 
		# booking_state remains ALLO  
		car_2 = Car.objects.get(id=2)
		self.assertEqual(car_2.position_x, 3)
		self.assertEqual(car_2.position_y, 2)
		self.assertEqual(car_2.customer, customer_1)
		self.assertEqual(car_2.booking_state, 'ALLO')
		# car_3 moved 1 right to drop off customer_2 at destination 
		# booking_state changes from INTR to FREE
		car_3 = Car.objects.get(id=3)
		self.assertEqual(car_3.position_x, 3)
		self.assertEqual(car_3.position_y, 3)
		self.assertEqual(car_3.customer, None)
		self.assertEqual(car_3.booking_state, 'FREE')

		# Check that tick is incremented
		self.assertEqual(new_tick, 1)




class TestLowestDistance(TestCase):
	"""
	Test get_lowest_distance(), get_cars_of_x_distance_to_customer(), get_car_of_lowest_id()
	"""
	def test_get_lowest_distance(self):
		car_1 = Car(id=1, position_x=1, position_y=1, customer=None, booking_state='FREE')
		car_2 = Car(id=2, position_x=2, position_y=2, customer=None, booking_state='FREE')
		car_3 = Car(id=3, position_x=3, position_y=3, customer=None, booking_state='FREE')
		car_1.save()
		car_2.save()
		car_3.save()

		customer_1 = Customer(id=1, position_x=5, position_y=5, destination_x=1, destination_y=1)
		customer_1.save()


		lowest_distance = views.get_lowest_distance(customer=Customer.objects.get(id=1),
			cars=Car.objects.all())
		self.assertEqual(lowest_distance, 4)

	def test_get_cars_of_x_distance_to_customer(self):
		x_distance = 4
		car_1 = Car(id=1, position_x=1, position_y=1, customer=None, booking_state='FREE')
		car_2 = Car(id=2, position_x=2, position_y=2, customer=None, booking_state='FREE')
		car_3 = Car(id=3, position_x=3, position_y=3, customer=None, booking_state='FREE')
		car_1.save()
		car_2.save()
		car_3.save()

		customer_1 = Customer(id=1, position_x=5, position_y=5, destination_x=1, destination_y=1)
		customer_1.save()

		cars_of_x_distance = views.get_cars_of_x_distance_to_customer(x_distance=x_distance,
			customer=Customer.objects.get(id=1),
			cars=Car.objects.all())

		self.assertEqual(len(cars_of_x_distance), 1)
		self.assertEqual(cars_of_x_distance[0].id, 3)


	def test_get_car_of_lowest_id(self):
		car_1 = Car(id=1, position_x=1, position_y=1, customer=None, booking_state='FREE')
		car_2 = Car(id=2, position_x=2, position_y=2, customer=None, booking_state='FREE')
		car_3 = Car(id=3, position_x=3, position_y=3, customer=None, booking_state='FREE')
		car_1.save()
		car_2.save()
		car_3.save()

		lowest_id_car = views.get_car_of_lowest_id(cars=Car.objects.all())

		self.assertEqual(lowest_id_car.id ,1)


class TestNearestAvailableCar(TestCase):
	"""
	Test find_nearest_available_car()
	"""
	def test_find_nearest_available_car_1(self):
		car_1 = Car(id=1, position_x=0, position_y=0, customer=None, booking_state='FREE')
		car_2 = Car(id=2, position_x=0, position_y=0, customer=None, booking_state='FREE')
		car_3 = Car(id=3, position_x=0, position_y=0, customer=None, booking_state='FREE')
		car_1.save()
		car_2.save()
		car_3.save()

		customer_1 = Customer(id=1, position_x=1, position_y=0, destination_x=1, destination_y=1)
		customer_1.save()

		lowest_id_available_car = views.find_nearest_available_car(customer=Customer.objects.get(id=1),
			available_cars=Car.objects.filter(booking_state='FREE'))

		self.assertEqual(lowest_id_available_car.id, 1)

	def test_find_nearest_available_car_2(self):
		car_1 = Car(id=1, position_x=1, position_y=1, customer=None, booking_state='FREE')
		car_2 = Car(id=2, position_x=2, position_y=2, customer=None, booking_state='FREE')
		car_3 = Car(id=3, position_x=3, position_y=3, customer=None, booking_state='FREE')
		car_1.save()
		car_2.save()
		car_3.save()

		customer_1 = Customer(id=1, position_x=4, position_y=4, destination_x=9, destination_y=9)
		customer_1.save()

		lowest_id_available_car = views.find_nearest_available_car(customer=Customer.objects.get(id=1),
			available_cars=Car.objects.filter(booking_state='FREE'))

		self.assertEqual(lowest_id_available_car.id, 3)


class ResetCarsTests(TestCase):
	"""
	Test reset_cars()
	"""
	def test_reset_cars(self):
		car_1 = Car(id=1, position_x=0, position_y=0, customer=None, booking_state='FREE')
		car_2 = Car(id=2, position_x=4, position_y=4, customer=None, booking_state='ALLO')
		car_3 = Car(id=3, position_x=5, position_y=-9, customer=None, booking_state='INTR')
		car_1.save()
		car_2.save()
		car_3.save()

		cars = Car.objects.all()
		views.reset_cars(cars=cars)

		# Refresh the cars
		car_1 = Car.objects.get(id=1)
		self.assertEqual(car_1.booking_state, "FREE")
		self.assertEqual(car_1.customer, None)
		car_2 = Car.objects.get(id=2)
		self.assertEqual(car_2.booking_state, "FREE")
		self.assertEqual(car_2.customer, None)
		car_3 = Car.objects.get(id=3)
		self.assertEqual(car_3.booking_state, "FREE")
		self.assertEqual(car_3.customer, None)

 
class AssignCarTests(TestCase):
	"""
	Test assign_car_to_customer
	"""
	def test_assign_car_to_customer(self):
		car_1 = Car(id=1, position_x=0, position_y=0, customer=None, booking_state='FREE')
		car_1.save()

		customer_1 = Customer(id=1, position_x=4, position_y=4, destination_x=1, destination_y=1)
		customer_1.save()

		car = Car.objects.get(id=1)
		customer = Customer.objects.get(id=1)
		views.assign_car_to_customer(customer=customer, car=car)

		car = Car.objects.get(id=1)
		self.assertEqual(car.booking_state, 'ALLO')
		self.assertEqual(car.customer, customer)







