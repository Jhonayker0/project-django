"""
URL configuration for juskar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('', views.signIn, name='signIn'),
    path('postsignIn/', views.postsignIn, name='postsignIn'),
    path('signUp/', views.signUp, name="signup"),
    path('logout/', views.logout, name="logout"),
    path('postsignUp/', views.postsignUp, name='postsignUp'),
    path('reset/', views.reset, name='reset'),
    path('postReset/', views.postReset, name='postReset'),
    
    # Dashboards
    path('index/', views.cliente_dashboard, name='cliente_dashboard'),
    path('home/', views.home, name='home'),  # Mantener por compatibilidad
]