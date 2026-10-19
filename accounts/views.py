from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from Events.models import Event

def homepage(request):
    return render(request,"homepage.html")

def dashboard(request):
     try:
          events=Event.objects.all()
         
     
          return render(
             request,
             "dashboard.html",
             {"events":events}
          )
     except Exception as e:
            messages.error(request,e)
     

def register(request):
     if request.method == "POST":
         username = request.POST["username"]
         password = request.POST["password"]
         email = request.POST["email"]

         try:
             User.objects.create_user( 
                 username=username,
                 password=password, 
                 email=email ) 
             messages.success(request,"Account created successfully")
             return redirect("login") 
         except Exception as e:
             messages.error(request,"The username already exists!") 
     return render(request, "register.html")

def login_view(request):
    if request.method =="POST":
         username = request.POST["username"]
         password = request.POST["password"]

         try:
             user=authenticate(
                 request,
                 username=username,
                 password=password
             )
             if user is not None:
                 login(request, user)
                 messages.success(request,"Login successful")
                 return redirect("dashboard")
             else:
                 messages.error(request,"invalid username or password")
                 return render(request,"login.html")
                 
         except Exception as e:
                      messages.error(request, f"login failed: {e}")

    return render(request,"login.html") 


             



      

# Create your views here.
