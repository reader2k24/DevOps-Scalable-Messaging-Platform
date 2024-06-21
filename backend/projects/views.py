from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm, UserRegistrationForm, MessageForm
from .models import Profile, Message
from django.contrib.auth import get_user_model

@login_required
def message_list(request):
    messages = Message.objects.filter(sender=request.user).order_by('-created_at')
    return render(request, 'message_list.html', {'messages': messages})

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    context = {
        'message': message,
    }
    return render(request, 'message_detail.html', context)

@login_required
def message_create(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('message_list')
    else:
        form = MessageForm()
    
    return render(request, 'message_form.html', {'form': form})

@login_required
def message_update(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('message_list')
    else:
        form = MessageForm(instance=message)
    
    return render(request, 'message_form.html', {'form': form})

@login_required
def message_delete(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    if request.method == 'POST':
        message.delete()
        return redirect('message_list')
    
    return render(request, 'message_confirm_delete.html', {'message': message})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            messages.success(request, 'Registration successful!')
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            if new_user is not None:
                login(request, new_user)
                return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'profile.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

User = get_user_model()

@login_required
def home(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message_content = form.cleaned_data['message']
            sender = request.user

            new_message = Message(subject=subject, message=message_content, sender=sender)
            new_message.save()

            messages.success(request, 'Message sent successfully!')
            return redirect('home')
    else:
        form = MessageForm()

    context = {
        'form': form,
    }
    return render(request, 'home.html', context)

def all_messages(request):
    messages = Message.objects.all()
    return render(request, 'all_messages.html', {'messages': messages})