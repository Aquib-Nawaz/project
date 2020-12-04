from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from pyfcm import FCMNotification
from .models import User, Classes
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


def index(request):

    # Authenticated users view their inbox
    user = request.user
    if request.user.is_authenticated:
        return render(request, "Dashboard/index.html", {"classes":user.teach_classes.all()})

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password) 

        # Check if authentication successful
        if user is not None and user.role != "student":
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "Dashboard/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "Dashboard/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "Dashboard/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.role = "pending"
            user.save()
        except IntegrityError:
            return render(request, "Dashboard/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Dashboard/register.html")

@api_view(['POST'])
def register_student(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

@api_view(['POST'])
def login_student(request):
    username = request.data["username"]
    password = request.data["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None and user.role=="student":
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_token(request):
    username = request.data["username"]
    try:
        user = User.objects.get(username=username)
        user.token = request.data["token"]
        user.save()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_classes(request):
    pass
        
@login_required(login_url="login")
def notification(request):
    user = request.user
    if request.method == "POST":
        push_service = FCMNotification(api_key="AAAARFVNDDc:APA91bETk2utEMjEJB7k9QE51q5RfqM-PfLCtWICq413mkvR1nP_PV8wwpfRxBbgPiULysbycpMv_LBh9MSRfzGYaX4EBV7mCSA9sKVfxZ_ommvAW3qoLvj3JnpWrRB6PI5eZiGgOa2X")
        #registration_id = "cl9OOak3RlKO7LX5m7h4LP:APA91bGRf8vw6iXrLwusy5PNagoAR04UHUo4RYXkGm_35pS7_vbNH2pAaeCI-HCpXW6JW0gvsVYfEz-Hr6gWZELqX7rB-2hsffeFOEAFZ9d57lsfMKYsQeDr5MmzhEaKbZXxX0IWPKJ7"
        registration_ids = []
        id = request.POST["class_group"]
        try:
            cl = user.teach_classes.get(pk=id)
        except:
            raise Http404
        students = cl.students.all()
        for s in students:
            if s.token is not None:
                registration_ids.append(s.token)
        print (registration_ids)
        message_title = request.POST["topic"]
        message_body = request.POST["body"]
        result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
        print (result)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render (request, "Dashboard/notification.html", {"classes":user.teach_classes.all()})

@login_required(login_url="login")
def pending_instructor(request):
    try:
        users = User.objects.filter(role="pending")
    except:
        raise Http404
    return render (request, "Dashboard/add_instructor.html", {"users": users})

@login_required(login_url="login")
def add_instructor(request, id):
    user = request.user
    if user.is_staff:
        try:
            use = User.objects.get(pk=id)
        except:
            raise Http404("Requsested user not found")
        use.role = "instructor"
        use.save()
    return HttpResponseRedirect(reverse("pending_instructor"))

@login_required(login_url="login")    
def delete_instructor(request, id):
    user = request.user
    if user.is_staff:
        try:
            User.objects.get(pk=id).delete()
        except:
            raise Http404("Requsested user not found")
        
    return HttpResponseRedirect(reverse("pending_instructor"))

@login_required(login_url="login")
def add_class(request):
    if request.method == "GET":
        return render (request, "Dashboard/class.html")
    if request.method == "POST":
        title = request.POST["title"]
        cl = Classes.objects.create(name=title, instructor=request.user)
        cl.save()
        return HttpResponseRedirect(reverse("index"))

@login_required(login_url="login")
def class_view(request, id):
    user = request.user

    try:
        cl = user.teach_classes.get(pk=id)
        return render (request, 'Dashboard/class_view.html', {"students":User.objects.filter(role='student').exclude(in_classes = cl),"class":cl, "notifications":cl.class_notification.all()})
    except:
        raise Http404

@login_required(login_url="login")
def add_student(request, id):
    user = request.user
    try:
        cl = user.teach_classes.get(pk=id)
        print(cl)
        cl.students.add(User.objects.get(pk=request.POST["student"]))
        cl.save()
    except:
        raise Http404
    return HttpResponseRedirect(reverse("class_view", args=[id]))
