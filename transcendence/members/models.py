from django.db import models

class Member(models.Model):
	firstname = models.CharField(max_length=255)
	lastname = models.CharField(max_length=255)
	phone = models.IntegerField(null=True)
	joined_date = models.DateField(null=True)

	def __str__(self):
		return f"{self.firstname} {self.lastname}"
# Create your models here.

class Player(models.Model):
	email = models.CharField(max_length=255)
	name = models.CharField(max_length=255, default='user')
	password = models.CharField(max_length=255)
	joined_date = models.DateField(null=True)

	def save(self, *args, **kwargs):
		if self.name == 'user':
			super().save(*args, **kwargs)  # Call the "real" save() method to get an ID.
			self.name = 'user' + str(self.id)  # Update the name with the ID.
		super().save(*args, **kwargs)  # Call the "real" save() method.

	def __str__(self):
		return f"{self.id} {self.email}"
