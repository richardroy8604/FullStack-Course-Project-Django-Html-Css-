from django.urls import path
from Inventory import views
urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_item, name='add_item'),
    path('update-stock/<int:item_id>/<str:action>/', views.update_stock, name='update_stock'),
    path('edit/', views.edit_item, name='edit_item'),
    path('update-product/<int:item_id>/', views.update_product, name='update_product'),
    path('delete-item/<int:item_id>/', views.delete_item, name='delete_item'),
]