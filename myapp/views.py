from django.shortcuts import render
import pyrebase
from django.http import HttpResponse

# Create your views here.
def hello_world(request):
    return render(request, 'index.html')

def about(request):
    return HttpResponse("This is the about page.")

# LOGIN AND SIGNUP PAGE

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
# Initialising database,auth and firebase for further use 
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

def signIn(request):
    return render(request,"Login.html")
def home(request):
    return render(request,"Home.html")

def postsignIn(request):
    email=request.POST.get('email')
    pasw=request.POST.get('pass')
    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,pasw)
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request,"Login.html",{"message":message})
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request,"Home.html",{"email":email})

def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request,"Login.html")

def signUp(request):
    return render(request,"Registration.html")

def postsignUp(request):
     email = request.POST.get('email')
     passs = request.POST.get('pass')
     name = request.POST.get('name')
     try:
        # creating a user with the given email and password
        user=authe.create_user_with_email_and_password(email,passs)
        uid = user['localId']
        idtoken = request.session['uid']
        print(uid)
     except:
        return render(request, "Registration.html")
     return render(request,"Login.html")