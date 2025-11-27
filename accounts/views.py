from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, PlayerRegistrationForm, OrganizerRegistrationForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.username}!')
                return redirect('profile')
            else:
                messages.error(request, 'Неверные учетные данные.')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки ниже.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def register_choice(request):
    return render(request, 'accounts/register_choice.html')

def register_player(request):
    if request.method == 'POST':
        form = PlayerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Автоматический вход после регистрации
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.email, password=raw_password)
            if user is not None:
                login(request, user)
            messages.success(request, 'Регистрация игрока успешно завершена!')
            return redirect('profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки ниже.')
    else:
        form = PlayerRegistrationForm()
    
    return render(request, 'accounts/register_player.html', {'form': form})

def register_organizer(request):
    if request.method == 'POST':
        form = OrganizerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Автоматический вход после регистрации
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.email, password=raw_password)
            if user is not None:
                login(request, user)
            messages.success(request, 'Регистрация организатора успешно завершена!')
            return redirect('profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки ниже.')
    else:
        form = OrganizerRegistrationForm()
    
    return render(request, 'accounts/register_organizer.html', {'form': form})

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Здесь должна быть логика восстановления пароля
        messages.success(request, 'Инструкции по восстановлению пароля отправлены на ваш email.')
        return redirect('login')
    
    return render(request, 'accounts/forgot_password.html')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})