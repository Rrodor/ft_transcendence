import datetime
import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Manager, Max

# Create your models here.

class User(AbstractUser):
    date_joined = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=2, default='en')
    total_pong_games = models.IntegerField(default=0)
    pong_victories = models.IntegerField(default=0)
    pong_defeats = models.IntegerField(default=0)
    pong_points_for = models.IntegerField(default=0)
    pong_points_against = models.IntegerField(default=0)
    pong_wl_ratio = models.FloatField(default=0)
    pong_points_ratio = models.FloatField(default=0)
    pong_average_for = models.FloatField(default=0)
    pong_average_against = models.FloatField(default=0)
    pong_victories_percentage = models.FloatField(default=0)
    pong_defeats_percentage = models.FloatField(default=0)
    brick_games = models.IntegerField(default=0)
    brick_points = models.IntegerField(default=0)
    brick_average = models.FloatField(default=0)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True, null=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_in_game = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_pong_defeats = self.pong_defeats
        self._original_pong_victories = self.pong_victories

    def __str__(self):
        return f"{self.id} {self.email}"

    def calculate_percentages(self):
        total_games = self.pong_victories + self.pong_defeats
        if total_games > 0:
            self.pong_victories_percentage = (self.pong_victories / total_games) * 100
            self.pong_defeats_percentage = (self.pong_defeats / total_games) * 100
        else:
            self.pong_victories_percentage = 0
            self.pong_defeats_percentage = 0

    def save(self, *args, **kwargs):
        if self.username == 'user':
            super().save(*args, **kwargs)
            self.username = 'user' + str(self.id)
        if self.pong_defeats != self._original_pong_defeats or self.pong_victories != self._original_pong_victories:
            self.calculate_percentages()
        super().save(*args, **kwargs)
        self._original_pong_defeats = self.pong_defeats
        self._original_pong_victories = self.pong_victories

    def are_friends(self, user):
        return Friendship.objects.filter(user1=self, user2=user).exists() or Friendship.objects.filter(user1=user, user2=self).exists()

    def is_online(self):
        return self.last_activity > timezone.now() - datetime.timedelta(minutes=5)

class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    is_pending = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user1', 'user2']

    def __str__(self):
        return f"{self.user1} is friend with {self.user2}"
    
class GameRecord(models.Model):
    PONG = 'PONG'
    BRICK = 'BRICK'
    PONGT = 'PONGTOURNAMENT'
    GAME_CHOICES = [
        (PONG, 'Pong'),
        (BRICK, 'Brick'),
        (PONGT, 'Pong Tournament')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='game_records')
    game_type = models.CharField(max_length=14, choices=GAME_CHOICES)
    score_left = models.IntegerField(null=True, blank=True)
    score_right = models.IntegerField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} played {self.get_game_type_display()}"
    
    def save(self, *args, **kwargs):
        if self.game_type == 'PONG':
            if self.score_left is None or self.score_right is None:
                raise ValidationError('Pong game must have both scores')
            self.score = None
        elif self.game_type == 'BRICK':
            if self.score is None:
                raise ValidationError('Brick game must have a score')
            self.score_left = None
            self.score_right = None

        super().save(*args, **kwargs)

class TournamentManager(Manager):
    def get_tournament_with_most_players(self):
        tournaments = self.filter(nb_players__lt=8)
        tournament = tournaments.order_by('-nb_players').first()
        return tournament
    
    def get_user_tournament(self, user):
        return self.filter(players=user).first()
    
    def get_user_match(self, user):
        tournaments = self.filter(is_active=True, players=user)
        for tournament in tournaments:
            # Récupérer les matchs de l'utilisateur dans le tournoi
            matches = tournament.matches.filter(
                models.Q(participant1__user=user) | models.Q(participant2__user=user),
                score_participant1__isnull=True,
                score_participant2__isnull=True
            )
            if matches.exists():
                return matches.first()
        return None

class Tournament(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_started = models.BooleanField(default=False)
    nb_players = models.IntegerField(default=0)
    players = models.ManyToManyField(User, through='Participant', related_name='tournaments')
    quarters = models.JSONField(default=list)
    semis = models.JSONField(default=list)
    final = models.IntegerField(null=True, blank=True)
    objects = TournamentManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_initial_matches(self):
        if not self.pk:
            raise ValueError("Tournament must be saved before creating matches")

        quarter_final_matches = [Match(tournament=self, round=1, pos='top' if i < 2 else 'bottom') for i in range(4)]
        semi_final_matches = [Match(tournament=self, round=2) for _ in range(2)]
        final_match = [Match(tournament=self, round=3)]

        Match.objects.bulk_create(quarter_final_matches + semi_final_matches + final_match)

    def add_participant(self, user):
        used_seeds = Participant.objects.filter(tournament=self).values_list('seed', flat=True)
        all_seeds = list(range(1, 9))
        unused_seeds = [seed for seed in all_seeds if seed not in used_seeds]
        seed = random.choice(unused_seeds)
        Participant.objects.create(user=user, tournament=self, seed=seed)
        self.nb_players += 1
        self.save()
        if self.nb_players == 8:
            self.generate_matches()
    
    def remove_participant(self, user):
        participant = Participant.objects.get(user=user, tournament=self)
        participant.delete()
        self.nb_players -= 1
        self.save()

    def generate_matches(self):
        if self.nb_players != 8:
            raise ValidationError('Tournament must have 8 players')

        self.matches.all().delete()
        self.create_initial_matches()

        # Récupérer les matchs vides et ajouter les participants
        quarters_matches = self.get_matches_by_round(1)
        participants = list(self.participants.all())
        random.shuffle(participants)

        for match, participant_pair in zip(quarters_matches, zip(participants[::2], participants[1::2])):
            match.participant1, match.participant2 = participant_pair
            match.save()
        self.is_started = True

    def get_matches_by_round(self, round_number):
        return self.matches.filter(round=round_number)
    
    def delete_tournament(self):
        self.matches.all().delete()
        self.delete()


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='participants')
    seed = models.IntegerField()

class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    participant1 = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='matches_as_player1', null=True)
    participant2 = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='matches_as_player2', null=True)
    score_participant1 = models.IntegerField(null=True, blank=True)
    score_participant2 = models.IntegerField(null=True, blank=True)
    winner = models.ForeignKey(Participant, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_matches')
    round = models.IntegerField(default=1)
    POS_CHOICES = [
        ('top', 'Top'),
        ('bottom', 'Bottom'),
    ]
    pos = models.CharField(max_length=6, choices=POS_CHOICES, null=True, blank=True)

    def save(self, *args, **kwargs):
        updating_winner = self.pk is not None and (self.score_participant1 is not None and self.score_participant2 is not None)
        super().save(*args, **kwargs)

        if updating_winner:
            self.winner = self.participant1 if self.score_participant1 > self.score_participant2 else self.participant2
            print("winner :")
            print(self.winner.user.username)
            super().save(*args, **kwargs)

            if self.round == 1:  # Match de quart de finale
                next_round = self.round + 1
                next_matches = Match.objects.filter(tournament=self.tournament, round=next_round)
                
                for next_match in next_matches:
                    if next_match.pos is None:
                        next_match.pos = self.pos
                        next_match.save()
                    if not next_match.participant1:
                        next_match.participant1 = self.winner
                        next_match.save()
                        break
                    elif not next_match.participant2:
                        next_match.participant2 = self.winner
                        next_match.save()
                        break

            else:
                next_round = self.round + 1
                next_matches = Match.objects.filter(tournament=self.tournament, round=next_round)
                for next_match in next_matches:
                    if not next_match.participant1:
                        next_match.participant1 = self.winner
                        next_match.save()
                        break
                    elif not next_match.participant2:
                        next_match.participant2 = self.winner
                        next_match.save()
                        break
                