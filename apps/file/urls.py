from django.urls import path
from .views import *

urlpatterns = [
    path('', download_file, name='home'),
    path('data/', read_file, name="data"),
]