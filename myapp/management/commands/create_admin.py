
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import UserProfile
import pyrebase

class Command(BaseCommand):
    help = 'Crear un usuario administrador'

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, help='Nombre del administrador', required=True)
        parser.add_argument('--email', type=str, help='Email del administrador', required=True)
        parser.add_argument('--password', type=str, help='Contraseña del administrador', required=True)

    def handle(self, *args, **options):
        name = options['name']
        email = options['email']
        password = options['password']

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

        try:
            # Inicializar Firebase
            firebase = pyrebase.initialize_app(config)
            authe = firebase.auth()

            # Crear usuario en Firebase
            user_firebase = authe.create_user_with_email_and_password(email, password)
            firebase_uid = user_firebase['localId']

            # Crear usuario en Django
            django_user = User.objects.create_user(
                username=email,
                email=email,
                first_name=name,
                password=password,
                is_staff=True,  # Permitir acceso al panel de admin
                is_superuser=True  # Dar permisos de superusuario
            )

            # Actualizar perfil de usuario con rol de admin
            user_profile = UserProfile.objects.get(user=django_user)
            user_profile.firebase_uid = firebase_uid
            user_profile.role = 'admin'
            user_profile.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Administrador "{name}" creado exitosamente con email: {email}'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error al crear administrador: {str(e)}')
            )