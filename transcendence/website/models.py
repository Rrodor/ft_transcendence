import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError

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
	GAME_CHOICES = [
		(PONG, 'Pong'),
		(BRICK, 'Brick'),
	]
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='game_records')
	game_type = models.CharField(max_length=10, choices=GAME_CHOICES)
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