# authentication/views.py
# authentication/views.py
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from SalaryManagementSystem import settings
from .forms import UserLoginForm, ForgotPasswordForm, UserRegistrationForm
import logging

from .models import CustomUser

logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            logger.debug(f"Attempting to authenticate user: {username}")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                logger.debug(f"Authentication successful for user: {username}")
                login(request, user)
                messages.success(request, 'You have successfully logged in.')
                return redirect('dashboard')  # Replace with your actual dashboard URL
            else:
                logger.error(f"Authentication failed for user: {username}")
                messages.error(request, 'Invalid username or password.')
        else:
            logger.error("Invalid form submission")
            messages.error(request, 'Invalid form submission.')
    else:
        form = UserLoginForm()
    return render(request, 'authentication/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created. You can now log in.')
            return redirect('login')  # Replace with your actual login URL
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})

def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = CustomUser.objects.get(email=email)
                new_password = CustomUser.objects.make_random_password()
                user.set_password(new_password)
                user.save()
                send_mail(
                    'Your new password',
                    f'Your new password is {new_password}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Your password has been reset. Check your email for the new password.')
                return redirect('login')  # Replace with your actual login URL
            except CustomUser.DoesNotExist:
                messages.error(request, 'User with this email does not exist.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'authentication/forgot_password.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')  # Replace with your actual login URL
