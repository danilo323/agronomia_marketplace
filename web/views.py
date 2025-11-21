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
from django.contrib.auth.decorators import login_required
from django.db import models, IntegrityError
from django.contrib.auth.models import User
import re
from django.contrib.auth import update_session_auth_hash

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
            # Debugging: check whether the stored hash matches the provided password
            try:
                pw_ok = user.check_password(password)
            except Exception:
                pw_ok = None
            print(f"[LOGIN] attempt email={email!r} user_id={user.id} check_password={pw_ok}")
            user = authenticate(request, username=user.username, password=password)
            print(f"[LOGIN] authenticate returned: {user}")
            
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
        
        # Crear usuario: usar el email completo como username para evitar colisiones
        try:
            user = User.objects.create_user(
                username=email,  # usar el email completo como username (más único)
                email=email,
                password=password,
                first_name=first_name
            )
        except IntegrityError as e:
            messages.error(request, f'Error al crear la cuenta: {e}')
            return redirect('signup')

        messages.success(request, '¡Cuenta creada exitosamente! Ahora inicia sesión.')
        return redirect('login')
    
    return render(request, 'signup.html')


def user_profile(request):
    
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
        
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        # ----------------------------------------------------
        # A)  LÓGICA DE CAMBIO DE CONTRASEÑA
        # ---------------------------------------------------
        if form_type == 'password_change':
            current_password = request.POST.get('current-password')
            new_password = request.POST.get('new-password')
            confirm_password = request.POST.get('confirm-password')
            
            # Validación de contraseñas omitida por brevedad
            if not request.user.check_password(current_password):
                messages.error(request, 'La contraseña actual es incorrecta.')
            elif new_password != confirm_password:
                messages.error(request, 'La nueva contraseña y la confirmación no coinciden.')
            else:
                #  Solo modificamos y guardamos el campo de contraseña
                request.user.set_password(new_password)
                request.user.save()

                # Actualizar sesión para evitar logout inmediato
                update_session_auth_hash(request, request.user)

                # Verificar que la nueva contraseña funciona (no registrar la contraseña)
                try:
                    reauth = authenticate(request, username=request.user.username, password=new_password)
                    if reauth is None:
                        # Si no se pudo re-autenticar, informar y escribir un log mínimo
                        print(f"[WARN] password_change: re-authentication failed for user id={request.user.id}")
                        messages.warning(request, 'La contraseña fue actualizada, pero no se pudo verificar automáticamente. Intenta iniciar sesión de nuevo.')
                    else:
                        messages.success(request, 'Contraseña actualizada con éxito.')
                except Exception as ex:
                    print(f"[ERROR] password_change: exception during re-authentication for user id={request.user.id}: {ex}")
                    messages.success(request, 'Contraseña actualizada con éxito.')
            
            return redirect('user') 

        # ----------------------------------------------------
        # B)  LÓGICA DE ACTUALIZACIÓN DE DATOS DE PERFIL
        # ----------------------------------------------------
        else:
            username_data = request.POST.get('username')
            full_name_data = request.POST.get('full-name') 
            email_data = request.POST.get('email')
            
            # --- Validaciones Mínimas para NOT NULL ---
            is_valid = True
            
            # 1. Validación NOT NULL: Asegurarse de que el username no esté vacío
            if not username_data or username_data.strip() == "":
                messages.error(request, 'El nombre de usuario no puede estar vacío.')
                is_valid = False
            
            # 2. Validación de Nombre Completo y Split
            if full_name_data: 
                full_name_parts = full_name_data.split(' ')
                first_name_data = full_name_parts[0] if full_name_parts else ''
                last_name_data = ' '.join(full_name_parts[1:]) if len(full_name_parts) > 1 else ''
            else:
                 first_name_data = ''
                 last_name_data = ''

            
            if is_valid:
                try:
                    # Actualizar todos los campos de información
                    request.user.username = username_data
                    request.user.first_name = first_name_data
                    request.user.last_name = last_name_data
                    request.user.email = email_data
                    request.user.save()
                    
                    # Actualizar la foto de perfil 
                    foto_perfil = request.FILES.get('profile_picture')
                    if foto_perfil:
                        profile.profile_picture = foto_perfil
                        profile.save()
                    
                    messages.success(request, ' Perfil actualizado con éxito.')
                    return redirect('user') 
                
                except Exception as e:
                    # Esto captura errores como violaciones de unicidad de username/email
                    messages.error(request, f' Error al guardar en la base de datos: {e}')
                    return redirect('user')
            
            # Si is_valid es False, redirige para mostrar el error de validación
            return redirect('user')
            
    # Para la solicitud GET
    context = {
        'user': request.user,
        'profile': profile,
    }
    return render(request, 'user.html', context)