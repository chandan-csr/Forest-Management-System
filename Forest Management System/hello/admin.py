from asyncio import transports
from django.contrib import admin
from hello.models import Forest,Product,Haulier,customer,Visitors_pass

# Register your models here.
admin.site.register(Forest)
admin.site.register(Product)
admin.site.register(Haulier)
admin.site.register(customer)
admin.site.register(Visitors_pass)