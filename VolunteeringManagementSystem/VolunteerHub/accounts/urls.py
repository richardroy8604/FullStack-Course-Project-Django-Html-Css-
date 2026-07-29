from django.urls import path
from . import views

urlpatterns = [
    path("", views.accounts, name="accounts"),
    path("add-contact/", views.add_contact, name="add_contact"),
    
]