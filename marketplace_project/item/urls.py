from django.urls import path
from . import views

app_name = 'item'

urlpatterns = [
    path('', views.items, name="items"),
    path('newitem/', views.newItem, name="new"),
    path('<int:pk>', views.detailPage, name="detail"),
    path('<int:pk>/delete/', views.deleteItem, name="delete"),
    path('<int:pk>/edit/', views.edit, name="edit")
]
