from django.db import models

class Maison(models.Model):
	#user = models.ForeignKey(auth.User)
	nom = models.CharField(max_length=40, unique=True)
	description = models.TextField(default='')
	influence = models.SmallIntegerField(default=100)
	prestige = models.SmallIntegerField(default=100)
	
	def __str__(self):
		return self.nom