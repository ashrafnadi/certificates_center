from django.urls import path
from . import views

app_name = "graduates"

urlpatterns = [
    path("", views.index, name="index"),
    path('graduates/', views.graduate_list, name='graduate_list'),
]
