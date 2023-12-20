from django.urls import path
from . import views

from django.conf.urls import handler500

handler500 = 'weather_app.views.custom_500'

urlpatterns = [
    path('', views.index, name='index'),
]