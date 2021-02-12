from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('book', views.book, name='book'),
	path('tick', views.tick, name='tick'),
	path('reset', views.reset, name='reset')
]