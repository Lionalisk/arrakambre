from django.db import models

class Competence(models.Model):
	nom = models.CharField(max_length=40, unique=True)
	description = models.TextField(default='', blank=True, null=True)
	categorie =
	priorite = 
	
	def __str__(self):
		return self.nom