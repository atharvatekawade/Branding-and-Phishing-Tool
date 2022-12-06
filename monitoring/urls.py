from django.urls import path
from . import views

urlpatterns = [
    path('',views.scan),
    path('sim/',views.similar),
]