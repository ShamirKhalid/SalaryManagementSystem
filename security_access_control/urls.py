from django.urls import path
from . import views

urlpatterns = [
    path('roles/', views.roles_view, name='roles'),
    path('permissions/', views.permissions_view, name='permissions'),
]
