from django.contrib import admin
from django.urls import path
from .views import core

urlpatterns = [
    path('', core),
]