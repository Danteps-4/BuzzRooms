from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Room, Topic, Message, Profile
from .forms import RoomForm, ProfileForm, TopicForm


# Create your views here.
def login_page(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password does not exist")
    
    context = {"page": page}
    return render(request, "base/login_register.html", context)

def register_user(request):
    page = "register"

    if request.user.is_authenticated:
        return redirect("home")
    
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error ocurred during registration")

    context = {"page": page, "form": form}
    return render(request, "base/login_register.html", context)

def logout_user(request):
    logout(request)
    return redirect("home")


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | 
                                Q(name__icontains=q) | 
                                Q(description__icontains=q))
    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    room_count = rooms.count()
    context = {"rooms": rooms, "topics": topics, "rooms_count": room_count, "room_messages": room_messages}
    return render(request, "base/home.html", context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by("-created")
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("room", pk=room.id)

    context = {"room": room, "room_messages": room_messages, "participants": participants}
    return render(request, "base/room.html", context)

def profile(request, pk):
    user = User.objects.get(id=pk) 
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {"user": user, "rooms": rooms, "room_messages": room_messages, "topics": topics}
    return render(request, "base/profile.html", context)

@login_required
def update_user(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile", pk=profile.user.id)
    else:
        form = ProfileForm(instance=profile, user=request.user)
        context = {"form": form}
        return render(request, "base/update_user.html", context)

@login_required
def create_room(request, name):
    if name == "room":
        form = RoomForm()
        if request.method == "POST":
            form = RoomForm(request.POST)
            if form.is_valid():
                room = form.save(commit=False)
                room.host = request.user
                room.save()
                return redirect("home")
    else:
        form = TopicForm()
        if request.method == "POST":
            form = TopicForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("home")
    
    title = "room" if name == "room" else "topic"
    context = {"form": form, "title": title}
    return render(request, "base/room_form.html", context)

@login_required
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return redirect("home")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "base/room_form.html", context)

@login_required
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return redirect("home")

    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": room})

@login_required
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return redirect("home")

    if request.method == "POST":
        message.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": room})

def topics_page(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    topics = Topic.objects.filter(name__icontains=q)
    context = {"topics": topics}
    return render(request, "base/topics.html", context)

def activity_page(request):
    room_messages = Message.objects.all()
    context = {"room_messages": room_messages}
    return render(request, "base/activity.html", context)