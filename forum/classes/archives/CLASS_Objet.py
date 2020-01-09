from django.db import models

class Objet(models.Model):
	
	nom = models.CharField(max_length=30,unique=True)
	description = models.TextField(default='', blank=True)
	#classe = models.CharField(max_length=100,choices=(('','arme'),('','armure'),('','potion'),('','parchemin'),('','artefact'),('','objet de quete'),('','divers')))
	one_use = models.BooleanField(default = False)
	arme_OK = models.BooleanField(default = False)
	armure_OK = models.BooleanField(default = False)
	en_main_OK = models.BooleanField(default = False)
	
	bonus_attaque_duel = models.SmallIntegerField(default=0)
	bonus_defense_duel = models.SmallIntegerField(default=0)
	bonus_defense_melee = models.SmallIntegerField(default=0)
	bonus_attaque_melee = models.SmallIntegerField(default=0)
	bonus_initiative = models.SmallIntegerField(default=0)
	bonus_PA = models.SmallIntegerField(default=0)
	niveau_armurerie = models.SmallIntegerField(default=0)
	solidite = models.SmallIntegerField(default=1)
	
	niveau_sorcellerie = models.SmallIntegerField(default=0)
	niveau_alchimie = models.SmallIntegerField(default=0) # pour sa creation s'il sagit 
	pouvoir = models.CharField(max_length=30, default='', blank=True)
	puissance = models.SmallIntegerField(default=1)
	volume = models.SmallIntegerField(default=1)
	
	bonus_officier = models.SmallIntegerField(default=0)
	bonus_soins = models.SmallIntegerField(default=0)
	bonus_regeneration = models.SmallIntegerField(default=0)
	bonus_concentration = models.SmallIntegerField(default=0)
	bonus_aura = models.SmallIntegerField(default=0)
	bonus_savoir = models.SmallIntegerField(default=0)
	bonus_fouille = models.SmallIntegerField(default=0)
	bonus_enquete = models.SmallIntegerField(default=0)
	bonus_intrusion = models.SmallIntegerField(default=0)
	bonus_dissimulation = models.SmallIntegerField(default=0)
	bonus_fuite = models.SmallIntegerField(default=0)
		
	def __str__(self):
		return self.nom