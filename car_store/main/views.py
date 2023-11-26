from django.shortcuts import render
from .models import Car, SoldCar
from .forms import ApplicationForm
from django.db import IntegrityError

# Create your views here.
def index(request):
	cars = Car.objects.all()
	cars = [{
		'id': car.pk,
		'title': car.title,
  		'img': car.img,
		'year': car.year,
		'price': (f"{car.price:_}" + " $").replace("_", " ") if car.price is not None else 'No price',
        'is_sold': car.is_sold} 
	for car in cars if not car.is_sold]
	return render(request, 'main/index.html', {'cars': cars[:9]})


def catalog(request):
	cars = Car.objects.order_by("-id")
	cars = [{
		'id': car.pk,
		'title': car.title,
  		'img': car.img,
		'year': car.year,
		'price': (f"{car.price:_}" + " $").replace("_", " ") if car.price is not None else 'No price',
        'is_sold': car.is_sold} 
	for car in cars]
      
	sold_cars = SoldCar.objects.order_by("-id")
	sold_cars = [{
			'id': sold_car.car.pk,
			'title': sold_car.car.title,
			'img': sold_car.car.img,
			'year': sold_car.car.year,
			'price': (f"{sold_car.car.price:_}" + " $").replace("_", " ") if sold_car.car.price is not None else 'No price',
			'is_sold': sold_car.car.is_sold} 
	for sold_car in sold_cars]
	return render(request, 'main/catalog.html', {'cars': cars, 'sold_cars': sold_cars})


def about(request):
	return render(request, 'main/about.html')


def contacts(request):
	return render(request, 'main/contacts.html')


def car(request, car_id):
	car = Car.objects.get(pk = car_id)
	car = {
		'id': car.pk,
		'title': car.title,
  		'img': car.img,
		'year': car.year,
		'color': car.color,
		'coloration': car.coloration,
		'kilometrage': car.kilometrage,
		'condition': car.condition,
		'price': car.price,
        'is_sold': car.is_sold,
		'header_price': (f"{car.price:_}" + " $").replace("_", " ") if car.price is not None else 'No price'
	}
	return render(request, 'main/car.html', {'car': car})


def sub_app(request, car_id):
    car = Car.objects.get(pk=car_id)
    error_message = None

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            try:
                application = form.save(commit=False)
                application.car = car
                application.save()

            except IntegrityError:
                error_message = 'An application with such data already exists.'
                return render(request, 'main/submit_application_page.html', {'car': car, 'form': form, 'error_message': error_message})

        car = {
            'id': car.pk,
            'title': car.title,
            'img': car.img,
            'year': car.year,
            'color': car.color,
            'coloration': car.coloration,
            'kilometrage': car.kilometrage,
            'condition': car.condition,
            'price': car.price,
            'header_price': (f"{car.price:_}" + " $").replace("_", " ") if car.price is not None else 'No price'
        }

        return render(request, 'main/car.html', {'car': car})
    else:
        form = ApplicationForm()

    return render(request, 'main/submit_application_page.html', {'car': car, 'form': form, 'error_message': error_message})