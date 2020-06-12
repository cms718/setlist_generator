from django.urls import path, include
from . import views

#Change URL paths here:

urlpatterns = [
    path('generate_setlist', views.generate_setlist)
]
