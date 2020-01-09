from django.db import models

class Competence(models.Model):
	active = models.BooleanField(default=True)
	nom = models.CharField(max_length=40, unique=True)
	nom_info = models.CharField(max_length=40, unique=True, null=True)
	description = models.TextField(default='', blank=True, null=True)
	
	categorie_classement = models.ForeignKey('Categorie_competence', null=True, blank=True, on_delete=models.SET_NULL, related_name = 'categorie_classement')
	categorie = models.ManyToManyField('Categorie_competence', blank=True, related_name = 'categorie')
	
	priorite = models.SmallIntegerField(default=0)
	
	def __str__(self):
		return self.nom