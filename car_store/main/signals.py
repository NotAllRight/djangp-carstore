from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Car, SoldCar, Application


@receiver(pre_save, sender=Car)
def handle_car_pre_save(sender, instance, **kwargs):
    # Обработка события перед сохранением Car
    if instance.pk:
        # Если Car уже существует (не новый объект)
        original_car = Car.objects.get(pk=instance.pk)
        if original_car.is_sold and not instance.is_sold:
            # Если машина была продана и теперь не продается, удаляем запись из SoldCar
            sold_car = SoldCar.objects.filter(car=instance).first()
            if sold_car:
                with transaction.atomic():
                    sold_car.delete()


@receiver(post_save, sender=SoldCar)
def handle_sold_car_save(sender, instance, **kwargs):
    # Обработка события сохранения SoldCar
    with transaction.atomic():
        if instance.car and instance.car.is_sold:
            # Если машина продана, удаляем заявки с таким же названием машины
            Application.objects.filter(car__title=instance.car.title).delete()
