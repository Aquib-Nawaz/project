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

from .models import User


def index(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "Dashboard/index.html")

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
        if user is not None:
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
        role = request.POST.get("role", None)
        if role == None:
            return render(request, "Dashboard/register.html", {
                "message": "Role must be chosen"
            })
        if password != confirmation:
            return render(request, "Dashboard/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.role = role
            user.save()
        except IntegrityError:
            return render(request, "Dashboard/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Dashboard/register.html")
@login_required(login_url="login")
def notification(request):
	if request.method == "POST":
		pass
	else:
		return render (request, "Dashboard/notification.html", {})

@login_required(login_url="login")
def pending_instructor(request):
    try:
        users = User.objects.filter(role="pending")
    except:
        pass
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

