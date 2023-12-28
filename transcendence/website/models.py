from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
	date_joined = models.DateTimeField(auto_now_add=True)
	total_pong_games = models.IntegerField(default=0)
	pong_victories = models.IntegerField(default=0)
	pong_defeats = models.IntegerField(default=0)
	pong_victories_percentage = models.FloatField(default=0)
	pong_defeats_percentage = models.FloatField(default=0)
	avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True, null=True)

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