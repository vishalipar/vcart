from django.urls import path 
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('category/', views.prod_detail, name='prod_detail'),
    
]
