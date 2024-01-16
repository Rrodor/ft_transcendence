from .models import User, Friendship, GameRecord, Tournament, Participant, Match
from .forms import UserForm, ChangePasswordFormEn, ChangePasswordFormFr, ChangePasswordFormSp, ChangeAvatarFormEn, ChangeAvatarFormFr, ChangeAvatarFormSp
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.test import RequestFactory
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import activate
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import check_password
from django.db import connection

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
    if request.user.is_authenticated:
        request.user.is_in_game = False
        request.user.save()
    return render(request, 'main.html', context)

def players(request):
    all_users = User.objects.all().values()
    template = loader.get_template('players.html')
    context = {
        'all_users': all_users,
    }
    if request.user.is_authenticated:
        request.user.is_in_game = False
        request.user.save()
    return HttpResponse(template.render(context, request))

def details(request, id):
    player = User.objects.get(id=id)
    user_stats = User.objects.get(id=id)
    is_friend = False
    is_pending = False
    latest_games = GameRecord.objects.filter(user=player).order_by('-date')[:5]
    latest_brick_score = list(GameRecord.objects.filter(user=player, game_type=GameRecord.BRICK).order_by('-date').values_list('score', flat=True)[:5])
    if request.user.is_authenticated:
        request.user.is_in_game = False
        request.user.save()
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
            'latest_brick_score': latest_brick_score,
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
                return redirect('/main?password_changed=true')
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
    latest_brick_score = list(GameRecord.objects.filter(user=request.user, game_type=GameRecord.BRICK).order_by('-date').values_list('score', flat=True)[:5])
    friends_changed = 'friends_changed' in request.GET
    avatar_changed = 'avatar_changed' in request.GET
    friends_info = []
    for friendship in friends:
        friend = friendship.user1 if friendship.user1 != request.user else friendship.user2
        friends_info.append({
            'friend': friend,
            'is_in_game': friend.is_in_game
        })
    request.user.is_in_game = False
    request.user.save()
    if request.method == 'POST':
        if request.user.language == 'en':
            pwd_form = ChangePasswordFormEn(request.user, request.POST)
            avatar_form = ChangeAvatarFormEn(request.POST, request.FILES, instance=request.user)
        elif request.user.language == 'fr':
            pwd_form = ChangePasswordFormFr(request.user, request.POST)
            avatar_form = ChangeAvatarFormFr(request.POST, request.FILES, instance=request.user)
        elif request.user.language == 'sp':
            pwd_form = ChangePasswordFormSp(request.user, request.POST)
            avatar_form = ChangeAvatarFormSp(request.POST, request.FILES, instance=request.user)
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
        if request.user.language == 'en':
            pwd_form = ChangePasswordFormEn(request.user)
            avatar_form = ChangeAvatarFormEn(instance=request.user)
        elif request.user.language == 'fr':
            pwd_form = ChangePasswordFormFr(request.user)
            avatar_form = ChangeAvatarFormFr(instance=request.user)
        elif request.user.language == 'sp':
            pwd_form = ChangePasswordFormSp(request.user)
            avatar_form = ChangeAvatarFormSp(instance=request.user)
    context = {
        'pwd_form': pwd_form,
        'avatar_form': avatar_form,
        'user_stats': user_stats,
        'friends': friends,
        'pending_friends': pending_friends,
        'friends_changed': friends_changed,
        'avatar_changed': avatar_changed,
        'latest_games': latest_games,
        'friends_info': friends_info,
        'latest_brick_score': latest_brick_score,
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
    request.user.is_in_game = False
    request.user.save()
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
        'match': 0,
    }
    request.user.is_in_game = True
    request.user.save()
    # Your view logic here
    return render(request, 'pong_two_players.html', context)

def vs_ai(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to play Pong')
        return redirect('/login')
    context = {
        'user_id': request.user.id,
        'is_ai': 1,
        'match': 0,
    }
    request.user.is_in_game = True
    request.user.save()
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
    request.user.is_in_game = False
    request.user.save()
    messages.success(request, 'Game ended, see you soon!')
    return redirect('/main?game_changed=true')

@csrf_exempt
def adjustPlayerPongScores(user_id, score_left, score_right):
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
    except User.DoesNotExist:
        return JsonResponse({"status": "User not found"}, status=404)

@csrf_exempt
def	sendscore(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data['userId']
        score_left = data['scoreLeft']
        score_right = data['scoreRight']
        try:
            adjustPlayerPongScores(user_id, score_left, score_right)
            return JsonResponse({"status": "Score updated successfully"})
        except User.DoesNotExist:
            return JsonResponse({"status": "User not found"}, status=404)

    return JsonResponse({"status": "Invalid request"}, status=400)

def brique(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to play Casse-Brique')
        return redirect('/login')
    context = {
        'user_id': request.user.id,
    }
    request.user.is_in_game = True
    request.user.save()
    # Your view logic here
    return render(request, 'brique.html', context)

@csrf_exempt
def sendscore_brique(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data['userId']
        score = data['score']
        try:
            user = User.objects.get(id=user_id)
            user.brick_games += 1
            user.brick_points += score
            user.brick_average = user.brick_points / user.brick_games
            user.save()
            game_record = GameRecord(user=user, game_type=GameRecord.BRICK, score=score)
            game_record.save()
            return JsonResponse({"status": "Score updated successfully"})
        except User.DoesNotExist:
            return JsonResponse({"status": "User not found"}, status=404)

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

def tournament(request):
    is_in_tournament = False
    nb_players = 0
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to play Pong')
        return redirect('/login')
    tournament = Tournament.objects.get_user_tournament(request.user)
    if not tournament:
        tournament = Tournament.objects.get_tournament_with_most_players()
    if not tournament:
        active = False
        matches = []
    else:
        active = True
        nb_players = tournament.nb_players
        if request.user in tournament.players.all():
            is_in_tournament = True
        matches = tournament.matches.all()
        tournament.participants.all().order_by('seed')
        print("nb_players: ", tournament.nb_players)
        for participant in tournament.participants.all():
            print(participant.user.username, participant.seed)
        round_1_matches = tournament.get_matches_by_round(1)
        for match in round_1_matches:
            participant1_username = match.participant1.user.username if match.participant1 else 'TBD'
            participant2_username = match.participant2.user.username if match.participant2 else 'TBD'
            print(f"R1 : {participant1_username} vs {participant2_username}")
        round_2_matches = tournament.get_matches_by_round(2)
        for match in round_2_matches:
            participant1_username = match.participant1.user.username if match.participant1 else 'TBD'
            participant2_username = match.participant2.user.username if match.participant2 else 'TBD'
            print(f"R2 : {participant1_username} vs {participant2_username}")
        round_3_matches = tournament.get_matches_by_round(3)
        for match in round_3_matches:
            participant1_username = match.participant1.user.username if match.participant1 else 'TBD'
            participant2_username = match.participant2.user.username if match.participant2 else 'TBD'
            print(f"R3 : {participant1_username} vs {participant2_username}")

    context = {
        'user_id': request.user.id,
        'active': active,
        'tournament': tournament,
        'is_in_tournament': is_in_tournament,
        'nb_players': nb_players,
        'matches': matches,
    }
    # Your view logic here
    return render(request, 'pong_tournament.html', context)

def create_tournament(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to play Pong')
        return redirect('/login')
    tournament = Tournament.objects.get_tournament_with_most_players()
    if tournament is None:
        tournament = Tournament.objects.create()
    tournament.is_active = True
    tournament.add_participant(request.user)
    tournament.save()
    print(tournament.players.all())
    return redirect('/pong/tournament')

def join_tournament(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to play Pong')
        return redirect('/login')
    tournament = Tournament.objects.get_tournament_with_most_players()
    if tournament is None or tournament.nb_players == 8:
        messages.error(request, 'No tournament available')
        return redirect('/pong/tournament')
    tournament.add_participant(request.user)
    tournament.save()
    return redirect('/pong/tournament')

def leave_tournament(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to play Pong')
        return redirect('/login')
    tournament = Tournament.objects.get_user_tournament(request.user)
    if tournament is None:
        messages.error(request, 'No tournament available')
        return redirect('/pong/tournament')
    if request.user not in tournament.players.all():
        messages.error(request, 'You are not in the tournament')
        return redirect('/pong/tournament')
    tournament.remove_participant(request.user)
    tournament.save()
    if tournament.nb_players == 0:
        tournament.delete()
    return redirect('/pong/tournament')

def play_match(request, match_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to play Pong')
        return redirect('/login')
    match = get_object_or_404(Match, id=match_id)
    if request.user not in [match.participant1.user, match.participant2.user]:
        messages.error(request, 'You are not in the match')
        return redirect('/pong/tournament')
    player1_id = match.participant1.user.id
    player2_id = match.participant2.user.id
    context = {
        'user_id': request.user.id,
        'is_ai': 0,
        'player1_id': player1_id,
        'player2_id': player2_id,
        'match_id': match_id,
        'match': 1,
    }
    match.participant1.user.is_in_game = True
    match.participant1.user.save()
    match.participant2.user.is_in_game = True
    match.participant2.user.save()
    return render(request, 'pong_match.html', context)


@csrf_exempt
@require_POST
def verify_password(request):
    password = request.POST.get('password')
    match_id = request.POST.get('match_id')
    opponent_id = request.POST.get('opponent_id')
    User = get_user_model()

    try:
        opponent = User.objects.get(id=opponent_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Opponent not found'})

    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Match not found'})

    if check_password(password, opponent.password):
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Incorrect password'})

@csrf_exempt
def sendmatchscore(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        match_id = data['match_id']
        score_left = data['scoreLeft']
        score_right = data['scoreRight']
        try:
            match = Match.objects.get(id=match_id)
        except Match.DoesNotExist:
            return JsonResponse({"status": "Match not found"}, status=404)
        User = get_user_model()
        player_left = User.objects.get(id=match.participant1.user.id)
        player_right = User.objects.get(id=match.participant2.user.id)
        try:
            adjustPlayerPongScores(player_left.id, score_left, score_right)
            adjustPlayerPongScores(player_right.id, score_right, score_left)
            match.score_participant1 = score_left
            match.score_participant2 = score_right
            match.save()
            if match.round == 3:
                if score_left > score_right:
                    messages.success(request, f"{player_left.username} won the tournament!")
                    game_record = GameRecord(user=player_left, game_type=GameRecord.PONGT, score_left=100, score_right=0)
                else:
                    messages.success(request, f"{player_right.username} won the tournament!")
                    game_record = GameRecord(user=player_right, game_type=GameRecord.PONGT, score_left=100, score_right=0)
                game_record.save()
                tournament = Tournament.objects.get_user_tournament(request.user)
                tournament.delete_tournament()
            return JsonResponse({"status": "Score updated successfully"})
        except User.DoesNotExist:
            return JsonResponse({"status": "User not found"}, status=404)


def force_create(request):
    Tournament.objects.all().delete()
    Match.objects.all().delete()
    create_tournament(request)
    factory = RequestFactory()
    request = factory.get('/')
    name = {
        'test01': 'test01',
        'test03': 'test03',
        'test02': 'test02',
        'rrodor': 'rrodor',
        'aramon': 'aramon',
        'test00': 'test00',
    }
    for username in name:
        request.user = User.objects.get(username=username)
        join_tournament(request)
    return redirect('/pong/tournament')

def generate(request):
    tournament = Tournament.objects.get_user_tournament(request.user)
    tournament.create_initial_matches()
    tournament.generate_matches()
    return redirect('/pong/tournament')