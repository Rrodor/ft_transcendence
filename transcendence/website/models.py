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

	def are_friends(self, user):
		return Friendship.objects.filter(user1=self, user2=user).exists() or Friendship.objects.filter(user1=user, user2=self).exists()

class Friendship(models.Model):
	user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
	user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ['user1', 'user2']

	def __str__(self):
		return f"{self.user1} is friend with {self.user2}"