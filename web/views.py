from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def home(request):
    return render(request, 'home.html')

def login_view(request):
    """Vista para iniciar sesión con email y contraseña"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.first_name or user.email}!')
                return redirect('home')
            else:
                messages.error(request, 'Contraseña incorrecta.')
        except User.DoesNotExist:
            messages.error(request, 'El usuario no existe.')
    
    return render(request, 'login.html')

def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.success(request, '¡Has cerrado sesión correctamente!')
    return redirect('home')

def signup_view(request):
    """Vista para registrarse (signup)"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name', '')
        
        # Validaciones
        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este correo ya está registrado.')
            return redirect('signup')
        
        if len(password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return redirect('signup')
        
        # Crear usuario
        user = User.objects.create_user(
            username=email.split('@')[0],  # Usar parte del email como username
            email=email,
            password=password,
            first_name=first_name
        )
        
        messages.success(request, '¡Cuenta creada exitosamente! Ahora inicia sesión.')
        return redirect('login')
    
    return render(request, 'signup.html')

def user_profile(request):
    return render(request, 'user.html')
