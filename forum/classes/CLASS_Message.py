from django.db import models
#from ..models import Perso
from ..models import Jeu
from django.utils import timezone
from ..fonctions_base import *
#import datetime

class Message(models.Model):
	
	active = models.BooleanField(default=True)
	joueur = models.ForeignKey('Joueur', on_delete=models.CASCADE)
	joueurs_cible = models.ManyToManyField('Joueur', related_name = 'joueur_cible_message')
	titre = models.CharField(max_length=200)
	texte = models.TextField(verbose_name='')

	joueurs_affiche = models.ManyToManyField('Joueur', blank=True, related_name = 'joueur_affiche_message')
	joueurs_nonlu = models.ManyToManyField('Joueur', blank=True, related_name = 'joueur_non_lu')
	
	date_jeu = models.CharField(max_length=50, default='', blank=True)
	created_date = models.DateTimeField(default=timezone.now)
	
	
	def __str__(self):
		return self.created_date.strftime("%Y-%m-%d %H:%M")+' - '+self.joueur.nom+' - '+self.titre
		
	def save(self, *args, **kwargs):
		jeu = Jeu.objects.get(id = 1)
		T_date_jeu = jeu.convert_date(self.created_date)
		self.date_jeu = format_date_jeu(T_date_jeu,jeu.format_date)
		
		super().save()  # Call the "real" save() method.'''
		print("############# SAVE MESSAGE - "+str(timezone.now()))