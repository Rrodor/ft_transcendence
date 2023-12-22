from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
	date_joined = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"{self.id} {self.email}"
	def save(self, *args, **kwargs):
		if self.username == 'user':
			super().save(*args, **kwargs)  # Call the "real" save() method to get an ID.
			self.username = 'user' + str(self.id)  # Update the name with the ID.
		super().save(*args, **kwargs)  # Call the "real" save() method.
