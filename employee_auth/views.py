# employee_auth/views.py

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from .forms import EmployeeRegistrationForm, EmployeeLoginForm, EmployeePasswordResetForm, EmployeeSetPasswordForm

def employee_register(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_login')
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'employee_auth/register.html', {'form': form})

def employee_login(request):
    if request.method == 'POST':
        form = EmployeeLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('employee_portal:portal_home')
    else:
        form = EmployeeLoginForm()
    return render(request, 'employee_auth/login.html', {'form': form})

def employee_logout(request):
    logout(request)
    return redirect('employee_login')

def employee_password_reset(request):
    if request.method == 'POST':
        form = EmployeePasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "employee_auth/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': get_current_site(request).domain,
                        'site_name': 'SMS Administration',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    send_mail(subject, email, 'dannymacharia5074@gmail.com', [user.email], fail_silently=False)
                return redirect("employee_password_reset_done")
    else:
        form = EmployeePasswordResetForm()
    return render(request, 'employee_auth/password_reset.html', {'form': form})

def employee_password_reset_confirm(request):
    if request.method == 'POST':
        form = EmployeeSetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_password_reset_complete')
    else:
        form = EmployeeSetPasswordForm(user=request.user)
    return render(request, 'employee_auth/password_reset_confirm.html', {'form': form})

def employee_password_reset_done(request):
    return render(request, 'employee_auth/password_reset_done.html')

def employee_password_reset_complete(request):
    return render(request, 'employee_auth/password_reset_complete.html')
