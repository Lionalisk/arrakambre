from django.db import models
#from django.utils import timezone
#Importation des classes
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
#import os
from .fonctions_base import *



class Sante(models.Model):
	nom = models.CharField(max_length=30, unique=True)
	PV = models.SmallIntegerField(default=0, unique=True)
	image = models.CharField(max_length=30)
	
	def __str__(self):
		return self.nom

class Categorie_competence(models.Model):
	nom = models.CharField(max_length=30, unique=True)
	description = models.TextField(null=True, blank=True)
	priorite = models.SmallIntegerField(default=0)
	
	def __str__(self):
		return self.nom


class Atelier(models.Model):
	nom = models.CharField(max_length=30, unique=True)
	description = models.TextField(null=True, blank=True)
	
	def __str__(self):
		return self.nom

class Espece(models.Model):
	nom = models.CharField(max_length=30, unique=True)
	description = models.TextField(null=True, blank=True)
	
	def __str__(self):
		return self.nom
		
class Mois(models.Model):
	nom = models.CharField(max_length=30, unique=True)
	description = models.TextField(null=True, blank=True)
	numero = models.SmallIntegerField(verbose_name="numero du mois dans l'année", default=1, validators=[MinValueValidator(1)])
	
	def __str__(self):
		return self.nom

class Categorie_action(models.Model):
	nom = models.CharField(max_length=30, unique=True)
	description = models.TextField(null=True, blank=True)
	priorite = models.SmallIntegerField(default=1)
	
	def __str__(self):
		return self.nom
		

class Categorie_combat(models.Model):
	nom = models.CharField(max_length=30, unique=True)
	nom_info = models.CharField(max_length=30, null=True)
	description = models.TextField(null=True, blank=True)
	priorite = models.SmallIntegerField(default=1)
	
	def __str__(self):
		return self.nom

class Comportement_intervention(models.Model):
	active = models.BooleanField(default=True)
	nom = models.CharField(max_length=60, unique=True)
	nom_info = models.CharField(max_length=30, null=True)
	description = models.TextField(null=True, blank=True)
	priorite = models.SmallIntegerField(default=1)
	OK_hote = models.BooleanField(default=False)
	OK_perso = models.BooleanField(default=False)
	
	def __str__(self):
		return self.nom
		
class Charge(models.Model):
	active = models.BooleanField(default=True)
	nom = models.CharField(max_length=30, unique=True)
	nom_F = models.CharField(max_length=30, blank=True, null=True)
	nom_info = models.CharField(max_length=30, null=True)
	description = models.TextField(null=True, blank=True)
	priorite = models.SmallIntegerField(default=1)
	lieu = models.ForeignKey('Lieu', blank=True, null=True ,on_delete=models.SET_NULL, verbose_name="lieu : charge relie a ce lieu", related_name="charge")
	
	influence = models.SmallIntegerField(default=1)
	bonus_aura = models.SmallIntegerField(default=1)
	
	gardes = models.BooleanField(default=False, verbose_name="Peut recevoir des gardes de son lieu, mais ne peut pas en donner à un autre perso")
	troupes = models.BooleanField(default=False, verbose_name="Peut recevoir des troupes de son lieu, mais ne peut pas en donner à un autre perso")
	
	def __str__(self):
		return self.nom
		
	def titre(self,perso):
		titre = self.nom
		if self.nom_F and self.nom_F != '' and not perso.genre : titre = self.nom_F
		return titre
		
from .classes.CLASS_Jeu import *
from .classes.CLASS_Effet import *	
from .classes.CLASS_ObjetPerso import *	
from .classes.CLASS_Langage import *
from .classes.CLASS_Competence import *
from .classes.CLASS_Posture import *
from .classes.CLASS_Objet import *
from .classes.CLASS_Maison import *
from .classes.CLASS_Loi import *
from .classes.CLASS_Joueur import *
from .classes.CLASS_Commande import *
from .classes.CLASS_Perso import *
from .classes.CLASS_Message import *
from .classes.CLASS_Post import *
from .classes.CLASS_Lieu import *
from .classes.CLASS_Action import *
from .classes.CLASS_Resultat import *
from .classes.CLASS_Evenement import *
from .classes.CLASS_Regle import *	
from .classes.CLASS_Background import *	

