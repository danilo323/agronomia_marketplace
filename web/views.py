from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Profile
from django.db import IntegrityError
import re
from django.contrib.auth import update_session_auth_hash


# ----------------------------------------------
# 🟩 HOME
# ----------------------------------------------
def home(request):
    return render(request, 'home.html')


# ----------------------------------------------
# 🟩 LOGIN
# ----------------------------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)

            if user:
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.first_name or user.email}!')
                return redirect('home')
            else:
                messages.error(request, 'Contraseña incorrecta.')

        except User.DoesNotExist:
            messages.error(request, 'El usuario no existe.')

    return render(request, 'login.html')


# ----------------------------------------------
# 🟩 LOGOUT
# ----------------------------------------------
def logout_view(request):
    logout(request)
    messages.success(request, '¡Has cerrado sesión correctamente!')
    return redirect('home')


# ----------------------------------------------
# 🟩 SIGNUP
# ----------------------------------------------
def signup_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name', '')

        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este correo ya está registrado.')
            return redirect('signup')

        if len(password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return redirect('signup')

        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name
            )
        except IntegrityError:
            messages.error(request, 'Error al crear la cuenta.')
            return redirect('signup')

        messages.success(request, '¡Cuenta creada exitosamente!')
        return redirect('login')

    return render(request, 'signup.html')


# ================================================================
# 🟩 PERFIL DE USUARIO — CORREGIDO COMPLETAMENTE
# ================================================================
@login_required
def user_profile(request):

    # Crear perfil si no existe
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        # ----------------------------------------------------
        # A) CAMBIO DE CONTRASEÑA
        # ----------------------------------------------------
        if form_type == "password_change":
            current_password = request.POST.get("current-password")
            new_password = request.POST.get("new-password")
            confirm_password = request.POST.get("confirm-password")

            if not request.user.check_password(current_password):
                messages.error(request, "La contraseña actual es incorrecta.")
                return redirect("user")

            if new_password != confirm_password:
                messages.error(request, "Las contraseñas no coinciden.")
                return redirect("user")

            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)

            messages.success(request, "Contraseña actualizada correctamente.")
            return redirect("user")

        # ----------------------------------------------------
        # B) ACTUALIZACIÓN DE DATOS + FOTO DE PERFIL
        # ----------------------------------------------------
        elif form_type == "profile_update":

            username_data = request.POST.get("username")
            full_name_data = request.POST.get("full-name")
            email_data = request.POST.get("email")

            # Validación simple
            if not username_data:
                messages.error(request, "El nombre de usuario no puede estar vacío.")
                return redirect("user")

            # Separar nombre completo
            if full_name_data:
                parts = full_name_data.strip().split(" ")
                first_name = parts[0]
                last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
            else:
                first_name = ""
                last_name = ""

            try:
                # Guardar datos del usuario
                request.user.username = username_data
                request.user.first_name = first_name
                request.user.last_name = last_name
                request.user.email = email_data
                request.user.save()

                # Guardar foto si viene en el formulario
                foto = request.FILES.get("profile_picture")
                if foto:
                    profile.profile_picture = foto

                profile.save()

                messages.success(request, "Perfil actualizado con éxito.")
                return redirect("user")

            except Exception as e:
                messages.error(request, f"Error al actualizar el perfil: {e}")
                return redirect("user")

    # GET — mostrar perfil
    return render(request, "user.html", {
        "profile": profile
    })
