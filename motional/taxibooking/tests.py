from django.test import TestCase
from taxibooking.models import Car, Customer, Time
from . import views

# Create your tests here.
class DistanceTests(TestCase):
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
	def test_is_customer_and_car_colocated_1(self):
		car_2 = Car(id=2, position_x=2, position_y=2, customer=None, booking_state='Free')
		customer_2 = Customer(id=2, position_x=2, position_y=2, destination_x=5, destination_y=9)
		self.assertTrue(views.is_customer_and_car_colocated(customer=customer_2, car=car_2))

	def test_is_customer_and_car_colocated_2(self):
		car_3 = Car(id=3, position_x=-5, position_y=-3, customer=None, booking_state='Free')
		customer_3 = Customer(id=3, position_x=-4, position_y=12, destination_x=3, destination_y=-7)
		self.assertFalse(views.is_customer_and_car_colocated(customer=customer_3, car=car_3))

	def test_is_car_at_customer_destination_1(self):
		customer_4 = Customer(id=4, position_x=2, position_y=-2, destination_x=8, destination_y=4)
		car_4 = Car(id=4, position_x=8, position_y=4, customer=None, booking_state='Free')
		self.assertTrue(views.is_car_at_customer_destination(customer=customer_4, car=car_4))

	def test_is_car_at_customer_destination_2(self):
		car_1 = Car(id=1, position_x=0, position_y=0, customer=None, booking_state='Free')
		customer_1 = Customer(id=1, position_x=0, position_y=0, destination_x=3, destination_y=3)
		self.assertFalse(views.is_car_at_customer_destination(customer=customer_1,car=car_1))




