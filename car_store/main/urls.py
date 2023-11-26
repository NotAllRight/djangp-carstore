from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='home'),
	path('catalog', views.catalog, name='catalog'),
	path('about', views.about, name='about'),
	path('contacts', views.contacts, name='contacts'),
	path('car/<int:car_id>/', views.car, name='car'),
	path('sub_app/<int:car_id>/', views.sub_app, name='sub_app'),
]