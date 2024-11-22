# security_access_control/views.py

from django.shortcuts import render
from .models import Role, Permission

def roles_view(request):
    roles = Role.objects.all()
    return render(request, 'security_access_control/roles.html', {'roles': roles})

def permissions_view(request):
    permissions = Permission.objects.all()
    return render(request, 'security_access_control/permissions.html', {'permissions': permissions})
