from django.db import models
from ..models import Jeu
from ..fonctions_base import *
from ..models import Perso,Lieu,Maison

class Background(models.Model):
	active = models.BooleanField(default=True)
	priorite = models.SmallIntegerField(default=1)
	nom = models.CharField(max_length=30)
	parent = models.ForeignKey('self', blank=True, null=True ,on_delete=models.SET_NULL, verbose_name="Categorie de règle parent", related_name="enfant")
	nom_info = models.CharField(max_length=30, null=True)
	description = models.TextField(null=True, blank=True)
	
	
	def __str__(self):
		retour = self.nom
		if self.parent_id : retour = str(self.parent)+' - '+self.nom
		return retour
		
	def desc(self):
		html = self.description
		return html
		
	
	def enfants(self):
		qst_resultat = self.enfant.all().order_by('priorite')
		return qst_resultat
		