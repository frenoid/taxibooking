from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def index(request):
	return JsonResponse({
		'health_check': "OK",
		'view': 'index'
		})

def book(request):
	return JsonResponse({
		'health_check': "OK",
		'view': 'book'
		})


def tick(request):
	return JsonResponse({
		'health_check': "OK",
		'view': 'tick'
		})


def reset(request):
	return JsonResponse({
		'health_check': "OK",
		'view': 'reset'
		})