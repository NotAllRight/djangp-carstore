from django.db import models


# Create your models here.
class Car(models.Model):
	title = models.CharField('Name', max_length=100)
	img = models.FileField(upload_to='images/', verbose_name='', default='images/no_image.png')
	year = models.PositiveIntegerField('Year', null=True)
	color = models.CharField('Color', max_length=50,
							choices=[("white", "White"),("black", "Black"),("gray","Gray"),
									 ("brown","Brown"),("green", "Green"),("yellow", "Yellow"),
									 ("red","Red"),("orange","Orange"),("blue","Blue"),
									 ("pink","Pink"),("purple","Purple")], null=True)
	coloration = models.CharField('Coloration', max_length=10, choices=[("yes", "Yes"), ("no", "No")], null=True)
	kilometrage = models.PositiveIntegerField('Kilometrage', null=True)
	condition = models.CharField('Condition', max_length=25, choices=[("broken", "Broken"), ("not broken", "Not Broken")], null=True)
	price = models.PositiveIntegerField('Price')
	is_sold = models.BooleanField(default=False)

	def __str__(self):
		return self.title
	

class SoldCar(models.Model):
    car = models.OneToOneField('Car', on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=100)
    owner_phone = models.CharField(max_length=10)
	
    def __str__(self):
        return self.car.title

class Application(models.Model):
	car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='applications')
	name = models.CharField(max_length=100)
	phone = models.CharField(max_length=10)
	message = models.TextField()
	
	class Meta:
		unique_together = ['car', 'name', 'phone']

	def __str__(self):
		return f"Application for {self.car.title} - {self.name}"


