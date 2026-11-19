from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("/registration", views.register, name='registration'),
    path("list_events", views.list_events, name='list_events'),
    path("event/<int:event_id>", views.event, name='event'),
    path("register/<int:event_id>", views.register, name='register'),
    path("sobre", views.sobre, name='sobre'),
    path("add_event", views.add_event, name='add_event'),
]
