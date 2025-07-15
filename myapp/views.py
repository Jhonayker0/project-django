from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib import messages
from django.http import HttpResponse
import pyrebase
from .models import UserProfile

# Configuración de Firebase
config = {
    'apiKey': "AIzaSyAAu_mi1_gVhWM2U1DdJ_NWld5oMjek6G4",
    'authDomain': "juskar-f1d75.firebaseapp.com",
    'projectId': "juskar-f1d75",
    'storageBucket': "juskar-f1d75.firebasestorage.app",
    'messagingSenderId': "59544486270",
    'appId': "1:59544486270:web:b53ad5285b9f930c98f32f",
    'measurementId': "G-3YLEEHTDLQ",
    "databaseURL": "",
}

# Inicializar Firebase
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

def signIn(request):
    return render(request, "index.html")

def home(request):
    return render(request, "Home.html")

def index(request):
    # Página para clientes
    return render(request, "index.html")

def postsignIn(request):
    email = request.POST.get('email')
    pasw = request.POST.get('pass')
    
    try:
        # Autenticar con Firebase
        user_firebase = authe.sign_in_with_email_and_password(email, pasw)
        firebase_uid = user_firebase['localId']
        
        # Buscar usuario en Django por email
        try:
            django_user = User.objects.get(email=email)
            user_profile = UserProfile.objects.get(user=django_user)
            
            # Actualizar firebase_uid si no existe
            if not user_profile.firebase_uid:
                user_profile.firebase_uid = firebase_uid
                user_profile.save()
            
            # Autenticar usuario en Django
            django_user.backend = 'django.contrib.auth.backends.ModelBackend'
            django_login(request, django_user)
            
            # Guardar session de Firebase
            session_id = user_firebase['idToken']
            request.session['uid'] = str(session_id)
            request.session['firebase_uid'] = firebase_uid
            
            # Redirigir según el rol
            if user_profile.is_admin():
                return redirect('/admin/')
            else:
                return redirect('cliente_dashboard')
                
        except User.DoesNotExist:
            message = "Usuario no encontrado en el sistema. Por favor regístrate primero."
            return render(request, "Login.html", {"message": message})
        except UserProfile.DoesNotExist:
            message = "Perfil de usuario no encontrado. Contacta al administrador."
            return render(request, "Login.html", {"message": message})
            
    except Exception as e:
        message = "Credenciales inválidas. Por favor verifica tus datos."
        return render(request, "Login.html", {"message": message})

def logout(request):
    try:
        del request.session['uid']
        del request.session['firebase_uid']
    except:
        pass
    django_logout(request)
    return render(request, "Login.html")

def signUp(request):
    return render(request, "Registration.html")

def postsignUp(request):
    email = request.POST.get('email')
    passs = request.POST.get('pass')
    name = request.POST.get('name')
    
    try:
        # Crear usuario en Firebase
        user_firebase = authe.create_user_with_email_and_password(email, passs)
        firebase_uid = user_firebase['localId']
        
        # Crear usuario en Django
        django_user = User.objects.create_user(
            username=email,  # Usar email como username
            email=email,
            first_name=name,
            password=passs
        )
        
        # Crear perfil de usuario con rol de cliente
        user_profile = UserProfile.objects.get(user=django_user)
        user_profile.firebase_uid = firebase_uid
        user_profile.role = 'cliente'  # Por defecto cliente
        user_profile.save()
        
        message = "Usuario registrado exitosamente. Puedes iniciar sesión ahora."
        return render(request, "Login.html", {"message": message})
        
    except Exception as e:
        message = "Error al registrar usuario. El email puede estar ya en uso."
        return render(request, "Registration.html", {"message": message})

def reset(request):
    return render(request, "Reset.html")

def postReset(request):
    email = request.POST.get('email')
    try:
        authe.send_password_reset_email(email)
        message = "Un email para restablecer la contraseña ha sido enviado exitosamente"
        return render(request, "Reset.html", {"msg": message})
    except:
        message = "Algo salió mal. Por favor verifica que el email esté registrado"
        return render(request, "Reset.html", {"msg": message})

def cliente_dashboard(request):
    """Vista para el dashboard de clientes"""
    if not request.user.is_authenticated:
        return redirect('signIn')
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile.is_cliente():
            return redirect('/admin/')
    except UserProfile.DoesNotExist:
        return redirect('signIn')
    
    return render(request, "index.html", {"user": request.user})