from django.contrib import admin
from django.urls import path
from django.urls import register_converter

from ena.views import dashboard, redirect_index
from ena import converters

register_converter(converters.ThreeLetterCountryConverter, 'lll')

urlpatterns = [
    path("ena/", redirect_index, name="to_ena"),
    path("days=<int:days_range>", dashboard, name="dashboardENA"),
    path("days=<int:days_range>&country=<str:country_names>", dashboard, name="dashboardENA"),
    path("days=<int:days_range>/country=<lll:country_names>", dashboard, name="dashboardENA"),
]
