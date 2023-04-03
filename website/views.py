from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, AddRecord
from .models import Record


def home(request):
    records = Record.objects.all()

    # Login Part
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Auth
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in!')
        else:
            messages.error(request, 'Error')

        return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out!')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You Have Successfully Registered!')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})


def user_record(request, pk):
    if request.user.is_authenticated:
        personal_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'personal_record': personal_record})
    else:
        messages.error(request, 'You must be logged in!')
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        record.delete()
        messages.success(request, 'Record deleted successfuly!')
        return redirect('home')
    else:
        messages.error(request, 'You must be logged in!')
        return redirect('home')


def add_record(request):
    if request.user.is_authenticated:
        form = AddRecord(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, 'Record added...')
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in!')
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        form = AddRecord(request.POST or None, instance=record)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Record updated...')
                return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in!')
        return redirect('home')
