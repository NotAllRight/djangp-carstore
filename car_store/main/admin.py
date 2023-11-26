from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Car, SoldCar, Application


# Register your models here.
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('car', 'name')
    list_filter = ('car__title',)
    search_fields = ('car__title',)
    ordering = ('car__title',)


class CarAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_sold')
    search_fields = ('title',)
    
    def response_change(self, request, obj):
        # Перенаправляем на редактирование соответствующего объекта в SoldCar, если is_sold=True
        if '_saveasnew' not in request.POST and obj.is_sold:
            sold_car = SoldCar.objects.get_or_create(car=obj)[0]
            url = reverse('admin:main_soldcar_change', args=[sold_car.id])
            return HttpResponseRedirect(url)
        return super().response_change(request, obj)


class SoldCarAdmin(admin.ModelAdmin):
    list_display = ('car', 'owner_name')
    search_fields = ('car__title',)


admin.site.register(Car, CarAdmin)
admin.site.register(SoldCar, SoldCarAdmin)
admin.site.register(Application, ApplicationAdmin)