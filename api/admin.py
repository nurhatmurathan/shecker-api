from django.contrib import admin
from .models import *

admin.site.register(Fridge)
admin.site.register(Product)
admin.site.register(FridgeProduct)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Transaction)
