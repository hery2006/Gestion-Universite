from django.urls import path
from .views import *
urlpatterns=[
    path('verificator/0/25',EnregistrementGodUser,name='GodUser')
]