# employee_auth/backends.py

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

from employee_management.models import Employee


class EmployeeBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            employee = Employee.objects.get(email=username)
            if employee.user.check_password(password):
                return employee.user
        except Employee.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
