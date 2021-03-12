from django.urls import path
from rate_my_walk import views

app_name = 'rate_my_walk'

urlpatterns = [
    path('', views.index, name='index'),
]