from .models import User, Friendship
from .forms import UserForm, ChangePasswordForm, ChangeAvatarForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

# Create your views here.
def main(request):
    password_changed = 'password_changed' in request.GET
    avatar_changed = 'avatar_changed' in request.GET
    name_changed = 'name_changed' in request.GET
    friends_changed = 'friends_changed' in request.GET
    update_session_auth_hash(request, request.user)
    context = {
        'user': request.user,
        'password_changed': password_changed,
        'avatar_changed': avatar_changed,
        'name_changed': name_changed,
        'friends_changed': friends_changed,
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
    is_friend = False
    if request.user.is_authenticated:
        is_friend = Friendship.objects.filter(
            (Q(user1=request.user) & Q(user2=player)) |
            (Q(user1=player) & Q(user2=request.user))
		).exists()
    template = loader.get_template('details.html')
    context = {
            'player': player,
            'is_friend': is_friend,
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
    user_stats = User.objects.get(id=request.user.id)
    friends = Friendship.objects.filter(Q(user1=request.user) | Q(user2=request.user)).distinct()[:5]
    if request.method == 'POST':
        pwd_form = ChangePasswordForm(request.user, request.POST)
        avatar_form = ChangeAvatarForm(request.POST, request.FILES, instance=request.user)
        if 'change_password' in request.POST:
            if pwd_form.is_valid():
                pwd_form.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully')
                return redirect('/main?password_changed=true')
            else:
                messages.error(request, 'Error in password change form submission')

        elif 'change_avatar' in request.POST:
            # Handle avatar change form submission
            if avatar_form.is_valid():
                new_avatar = avatar_form.save(commit=False)
                print(f"New Avatar before deletion: {new_avatar.avatar.name}")
                if old_avatar and not old_avatar.name.endswith('default.png') and old_avatar.name != new_avatar.avatar.name:
                    default_storage.delete(old_avatar.name)
                avatar_form.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Avatar changed successfully')
                return redirect('/main?avatar_changed=true')
            else:
                print(f"Form errors: {avatar_form.errors}")
        elif 'change_name' in request.POST:
            # Aucun formulaire n'est nécessaire car vous récupérez directement les données du POST
            request.user.first_name = request.POST['first_name']
            request.user.last_name = request.POST['last_name']
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Name changed successfully')
            return redirect('/main?name_changed=true')
        else:
            messages.error(request, 'Invalid form submission')
            if avatar_form.is_valid():
                old_avatar = request.user.avatar
                if old_avatar and not old_avatar.name.endswith('default.png'):
                    old_avatar.delete()
                request.user.avatar = request.FILES['avatar']
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Avatar changed successfully')
                return redirect('/main?avatar_changed=true')
            else:
                messages.error(request, 'Error in avatar change form submission')
    else:
        pwd_form = ChangePasswordForm(request.user)
        avatar_form = ChangeAvatarForm(instance=request.user)
    return render(request, 'profile.html', {'pwd_form': pwd_form, 'avatar_form': avatar_form, 'user_stats': user_stats, 'friends': friends})


def handler404(request, exception):
    return render(request, '404.html', status=404)

def increment_game(request, player_id):
    player = get_object_or_404(User, id=player_id)
    player.total_pong_games += 1
    player.save()
    return HttpResponseRedirect(reverse('details', args=[player_id]))

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

def brique(request):
    # Your view logic here
    return render(request, 'brique.html')

def test(request):
    avatar_name = request.user.avatar.name if request.user.avatar else "No avatar uploaded"
    return render(request, 'test.html', {'avatar_name': avatar_name})

@login_required
def	check_login(request):
    return JsonResponse({'is_logged_in': request.user.is_authenticated})

@login_required
def add_friend(request, id):
    if request.method == 'POST':
        friend = get_object_or_404(User, id=id)
        # Vérifie si l'amitié existe déjà
        if not Friendship.objects.filter(user1=request.user, user2=friend).exists() and not Friendship.objects.filter(user1=friend, user2=request.user).exists():
            friendship = Friendship(user1=request.user, user2=friend)
            friendship.save()
            messages.success(request, f"You and {friend.username} are now friends.")
        else:
            messages.info(request, "You are already friends.")
        return redirect('/main?friends_changed=true', id=id)

@login_required
def remove_friend(request, id):
	if request.method == 'POST':
		friend = get_object_or_404(User, id=id)
		# Vérifie si l'amitié existe déjà
		if Friendship.objects.filter(user1=request.user, user2=friend).exists() or Friendship.objects.filter(user1=friend, user2=request.user).exists():
			Friendship.objects.filter(user1=request.user, user2=friend).delete()
			Friendship.objects.filter(user1=friend, user2=request.user).delete()
			messages.success(request, f"You and {friend.username} are no longer friends.")
		else:
			messages.info(request, "You are not friends.")
		return redirect('/main?friends_changed=true', id=id)

@csrf_exempt
def send_score_player_left(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		score_left = data['score']
		print(score_left)
		return JsonResponse({"status": "success"})
	return JsonResponse({"status": "invalid request"}, status=400)

@csrf_exempt
def send_score_player_right(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		score_right = data['score']
		print(score_right)
		return JsonResponse({"status": "success"})
	return JsonResponse({"status": "invalid request"}, status=400)

@csrf_exempt
def send_score_ai(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		score_right = data['score']
		print(score_AI)
		return JsonResponse({"status": "success"})
	return JsonResponse({"status": "invalid request"}, status=400)
