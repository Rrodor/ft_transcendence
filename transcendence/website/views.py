from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import User
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from .forms import UserForm, ChangePasswordForm, ChangeAvatarForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import default_storage

# Create your views here.
def main(request):
    password_changed = 'password_changed' in request.GET
    context = {
        'user': request.user,
        'password_changed': password_changed,
    }
    return render(request, 'main.html', context)

def players(request):
    all_users = User.objects.all().values()
    template = loader.get_template('players.html')
    context = {
        'all_users': all_users,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    player = User.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
            'player': player,
    }
    return (HttpResponse(template.render(context, request)))

def register(request):
    if request.user.is_authenticated:
        messages.error(request, 'You are already logged in')
        return redirect('/')
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Account created successfully')
                return redirect('/')
            else:
                messages.error(request, 'Error in user authentication')
        else:
            messages.error(request, 'Error in form submission')
    else:
        form = UserForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        messages.error(request, 'You are already logged in')
        return redirect('/')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                 login(request, user)
            else:
                 messages.error(request, 'Error in user authentication')
            return redirect('/')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You are not logged in')
        return redirect('/')
    logout(request)
    return redirect('/')

from django.contrib import messages

def profile(request):
    old_avatar = request.user.avatar
    print(f"Old Avatar before deletion: {old_avatar.name}")
    if request.method == 'POST':
        pwd_form = ChangePasswordForm(request.user, request.POST)
        avatar_form = ChangeAvatarForm(request.POST, request.FILES, instance=request.user)
        if 'change_password' in request.POST:
            # Handle password change form submission
            if pwd_form.is_valid():
                pwd_form.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully')
                return redirect('/main?password_changed=true')
            else:
                messages.error(request, 'Error in password change form submission')
        elif 'change_avatar' in request.POST:
            # Handle avatar change form submission
            print(f"Avatar before form validation: {request.user.avatar}")
            if avatar_form.is_valid():
                new_avatar = avatar_form.save(commit=False)
                print(f"New Avatar before deletion: {new_avatar.avatar.name}")
                if old_avatar and not old_avatar.name.endswith('default.png') and old_avatar.name != new_avatar.avatar.name:
                    default_storage.delete(old_avatar.name)
                    print(f"Old Avatar after deletion: {old_avatar.name}")
                avatar_form.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Avatar changed successfully')
                return redirect('/main?avatar_changed=true')
            else:
                print(f"Form errors: {avatar_form.errors}")
        else:
            messages.error(request, 'Invalid form submission')
    else:
        pwd_form = ChangePasswordForm(request.user)
        avatar_form = ChangeAvatarForm(instance=request.user)
    return render(request, 'profile.html', {'pwd_form': pwd_form, 'avatar_form': avatar_form})


def handler404(request, exception):
    return render(request, '404.html', status=404)

def increment_victory(request, player_id):
    player = get_object_or_404(User, id=player_id)
    player.pong_victories += 1
    player.save()
    return HttpResponseRedirect(reverse('details', args=[player_id]))

def increment_defeat(request, player_id):
    player = get_object_or_404(User, id=player_id)
    player.pong_defeats += 1
    player.save()
    return HttpResponseRedirect(reverse('details', args=[player_id]))

def decrement_victory(request, player_id):
    player = get_object_or_404(User, id=player_id)
    if (player.pong_victories > 0):
        player.pong_victories -= 1
    player.save()
    return HttpResponseRedirect(reverse('details', args=[player_id]))

def decrement_defeat(request, player_id):
    player = get_object_or_404(User, id=player_id)
    if (player.pong_defeats > 0):
        player.pong_defeats -= 1
    player.save()
    return HttpResponseRedirect(reverse('details', args=[player_id]))

def resetWL(request, player_id):
    player = get_object_or_404(User, id=player_id)
    player.pong_victories = 0
    player.pong_defeats = 0
    player.save()
    return HttpResponseRedirect(reverse('details', args=[player_id]))

def pong(request):
    # Your view logic here
    return render(request, 'pong.html')

def test(request):
    avatar_name = request.user.avatar.name if request.user.avatar else "No avatar uploaded"
    return render(request, 'test.html', {'avatar_name': avatar_name})
