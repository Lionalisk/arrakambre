from django.db import models
#from ..models import Perso
from ..models import Jeu
from django.utils import timezone
from ..fonctions_base import *
#import datetime

class Evenement(models.Model):
	active = models.BooleanField(default=True)
	titre = models.CharField(max_length=100)
	lieu = models.ManyToManyField('Lieu', related_query_name="lieu_event", blank=True)
	texte = models.TextField(verbose_name='')
	nom_info = models.CharField(verbose_name="Nom informatique (image) - si =='' : rien n'est associé ",max_length=30, default="", blank=True)
	
	dissimulation = models.SmallIntegerField(default=0)
	joueur_connaissant = models.ManyToManyField('Joueur', blank=True, related_name = 'joueur_know_event')
	persos_cible = models.ManyToManyField('Perso', blank=True, related_name = 'perso_cible_event')
	
	created_date = models.DateTimeField(default=timezone.now)
	date_publication = models.DateTimeField(default=timezone.now)
	date_jeu = models.CharField(max_length=50, default='', blank=True)
	
	
	def __str__(self):
		return self.titre
		
	def save(self, *args, **kwargs):
		jeu = Jeu.objects.get(id = 1)
		T_date_jeu = jeu.convert_date(self.created_date)
		self.date_jeu = format_date_jeu(T_date_jeu,jeu.format_date)
		
		
		super().save()  # Call the "real" save() method.'''
		print("############# SAVE POST - "+str(timezone.now()))