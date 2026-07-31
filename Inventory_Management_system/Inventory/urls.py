from django.urls import path
from Inventory import views
urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_item, name='add_item'),
]