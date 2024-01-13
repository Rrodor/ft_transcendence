from .models import User, Friendship, GameRecord
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
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import activate

import json

# Create your views here.
def main(request):
    password_changed = 'password_changed' in request.GET
    avatar_changed = 'avatar_changed' in request.GET
    name_changed = 'name_changed' in request.GET
    friends_changed = 'friends_changed' in request.GET
    game_changed = 'game_changed' in request.GET
    update_session_auth_hash(request, request.user)
    context = {
        'user': request.user,
        'password_changed': password_changed,
        'avatar_changed': avatar_changed,
        'name_changed': name_changed,
        'friends_changed': friends_changed,
        'game_changed': game_changed,
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
    user_stats = User.objects.get(id=id)
    is_friend = False
    is_pending = False
    latest_games = GameRecord.objects.filter(user=player).order_by('-date')[:5]
    if request.user.is_authenticated:
        is_friend = Friendship.objects.filter(
            ((Q(user1=request.user) & Q(user2=player)) |
            (Q(user1=player) & Q(user2=request.user))) &
            Q(is_confirmed=True)
        ).exists()
        is_pending = Friendship.objects.filter(
            (Q(user1=request.user) & Q(user2=player)) |
            (Q(user1=player) & Q(user2=request.user))
        ).exists()
    template = loader.get_template('details.html')
    context = {
            'player': player,
            'is_friend': is_friend,
            'is_pending': is_pending,
            'user_stats': user_stats,
            'latest_games': latest_games,
    }
    return (HttpResponse(template.render(context, request)))

def register(request):
    if request.user.is_authenticated and request.user.language == 'sp':
        messages.error(request, 'Ya se ha autentificado')
        return redirect('/')
    elif request.user.is_authenticated and request.user.language == 'fr':
        messages.error(request, 'Vous etes deja connecte')
        return redirect('/')
    elif request.user.is_authenticated and request.user.language == 'en':
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
    if request.user.is_authenticated and request.user.language == 'sp':
        messages.error(request, 'Ya se ha autentificado')
        return redirect('/')
    elif request.user.is_authenticated and request.user.language == 'fr':
        messages.error(request, 'Vous êtes déjà connecté')
        return redirect('/')
    elif request.user.is_authenticated and request.user.language == 'en':
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
    friends = Friendship.objects.filter((Q(user1=request.user) | Q(user2=request.user)) & Q(is_confirmed=True) & ~Q(is_pending=True)
).distinct()[:5]
    pending_friends = Friendship.objects.filter(Q(user2=request.user, is_pending=True)).distinct()[:5]
    latest_games = GameRecord.objects.filter(user=request.user).order_by('-date')[:5]
    friends_changed = 'friends_changed' in request.GET
    avatar_changed = 'avatar_changed' in request.GET
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
                return redirect('/profile?avatar_changed=true')
            else:
                print(f"Form errors: {avatar_form.errors}")
        elif 'change_name' in request.POST:
            # Aucun formulaire n'est nécessaire car vous récupérez directement les données du POST
            request.user.first_name = request.POST['first_name']
            request.user.last_name = request.POST['last_name']
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Name changed successfully')
            return redirect('/profile?name_changed=true')
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
                return redirect('/profile?avatar_changed=true')
            else:
                messages.error(request, 'Error in avatar change form submission')
    else:
        pwd_form = ChangePasswordForm(request.user)
        avatar_form = ChangeAvatarForm(instance=request.user)
    context = {
        'pwd_form': pwd_form,
        'avatar_form': avatar_form,
        'user_stats': user_stats,
        'friends': friends,
        'pending_friends': pending_friends,
        'friends_changed': friends_changed,
        'avatar_changed': avatar_changed,
        'latest_games': latest_games,
    }
    return render(request, 'profile.html', context)

@login_required
def add_friend(request, id):
    if request.method == 'POST':
        friend = get_object_or_404(User, id=id)
        if not Friendship.objects.filter(user1=request.user, user2=friend).exists():
            friendship = Friendship(user1=request.user, user2=friend, is_confirmed=False, is_pending=False)
            friendship.is_pending = True
            friendship.save()
            messages.success(request, f"Friend request sent to {friend.username}.")
        else:
            messages.info(request, "Friend request already sent or you are already friends.")
        return redirect('/main?friends_changed=true', id=id)

@login_required
def accept_friend_request(request, id):
    if request.method == 'POST':
        friendship = get_object_or_404(Friendship, user1_id=id, user2=request.user, is_confirmed=False)
        friendship.is_confirmed = True
        friendship.is_pending = False
        friendship.save()
        messages.success(request, f"You are now friends with {friendship.user1.username}.")
        return redirect('/profile?friends_changed=true', id=id)

@login_required
def decline_friend_request(request, id):
    if request.method == 'POST':
        friendship = get_object_or_404(Friendship, user1_id=id, user2=request.user, is_confirmed=False)
        friendship.delete()
        messages.success(request, f"You declined {friendship.user1.username}'s friend request.")
        return redirect('/profile?friends_changed=true', id=id)

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
        return redirect('/profile?friends_changed=true', id=id)

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

def pong_welcome(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to play Pong')
        return redirect('/login')
    context = {
        'user_id': request.user.id,
    }
    # Your view logic here
    return render(request, 'pong_welcome.html', context)

def two_players(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to play Pong')
        return redirect('/login')
    context = {
        'user_id': request.user.id,
        'is_ai': 0,
    }
    # Your view logic here
    return render(request, 'pong_two_players.html', context)

def vs_ai(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to play Pong')
        return redirect('/login')
    context = {
        'user_id': request.user.id,
        'is_ai': 1,
    }
    # Your view logic here
    return render(request, 'pong_two_players.html', context)

def end_game(request):
    game_changed = 'game_changed' in request.GET
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to play Pong')
        return redirect('/login')
    context = {
        'user_id': request.user.id,
        'game_changed': game_changed,
    }
    messages.success(request, 'Game ended, see you soon!')
    return redirect('/main?game_changed=true')


@csrf_exempt
def	sendscore(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data['userId']
        score_left = data['scoreLeft']
        score_right = data['scoreRight']
        try:
            user = User.objects.get(id=user_id)
            user.total_pong_games += 1
            if score_left > score_right:
                user.pong_victories += 1
            else:
                user.pong_defeats += 1
            user.pong_wl_ratio = user.pong_victories / user.pong_defeats if user.pong_defeats > 0 else user.pong_victories
            user.pong_points_for += score_left
            user.pong_points_against += score_right
            user.pong_points_ratio = user.pong_points_for / user.pong_points_against if user.pong_points_against > 0 else user.pong_points_for
            user.pong_average_for = user.pong_points_for / user.total_pong_games
            user.pong_average_against = user.pong_points_against / user.total_pong_games
            user.save()
            game_record = GameRecord(user=user, game_type=GameRecord.PONG, score_left=score_left, score_right=score_right)
            game_record.save()

            return JsonResponse({"status": "Score updated successfully"})
        except User.DoesNotExist:
            return JsonResponse({"status": "User not found"}, status=404)

    return JsonResponse({"status": "Invalid request"}, status=400)

def brique(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to play Casse-Brique')
        return redirect('/login')
    # Your view logic here
    return render(request, 'brique.html')

def test(request):
    avatar_name = request.user.avatar.name if request.user.avatar else "No avatar uploaded"
    return render(request, 'test.html', {'avatar_name': avatar_name})

@login_required
def	check_login(request):
    return JsonResponse({'is_logged_in': request.user.is_authenticated})

@csrf_exempt
def send_score_ai(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        score_right = data['score']
        print(score_AI)
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "invalid request"}, status=400)

def change_language(request):
    if request.method == 'POST':
        language_code = request.POST.get('language_code', '')
        activate(language_code)
        request.user.language = language_code
        request.user.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'error_page.html', {'error_message': 'Invalid request.'})
