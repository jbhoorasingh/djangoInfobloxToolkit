from django.urls import path
from . import views

urlpatterns = [
    path('create-new-network/', views.CreateNewNetwork.as_view(), name='create_new_network'),
]