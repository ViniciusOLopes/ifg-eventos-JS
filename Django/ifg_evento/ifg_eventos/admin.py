from django.contrib import admin
from .models import Event, Registration , Student

# Register your models here.

admin.site.register(Student)
admin.site.register(Event)
admin.site.register(Registration)
