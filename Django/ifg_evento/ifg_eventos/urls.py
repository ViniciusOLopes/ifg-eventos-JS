from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("/registration", views.register, name='registration'),
    path("list_events", views.list_events, name='list_events'),
    path("event/<int:event_id>", views.event, name='event'),
]
