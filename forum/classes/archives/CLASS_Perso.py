from django.db import models
from forum.classes.CLASS_Lieu import *
from forum.classes.CLASS_Objet import *

class Perso(models.Model):
	#user = models.ForeignKey(auth.User)
	lieu = models.ForeignKey(Lieu, null=True, on_delete=models.DO_NOTHING, related_name=('localisation'))
	nom = models.CharField(max_length=30, unique=True)
	genre = models.BooleanField(default=True)
	maison = models.ForeignKey(Maison, null=True, on_delete=models.DO_NOTHING)
	titre = models.CharField(max_length=50, default='')
	description = models.TextField(default='')
	image = models.CharField(max_length=40,default='perso_none.jpg')
	
	PA_MAX = models.SmallIntegerField(default=0)		# Pt d'Action
	PA = models.SmallIntegerField(default=0)
	PVA_MAX = models.PositiveIntegerField(default=0) 	# Pt de Vie Armure
	PVA = models.SmallIntegerField(default=0)
	PV_MAX = models.PositiveIntegerField(default=3)
	PV = models.SmallIntegerField(default=3)
	etat_sante = models.CharField(max_length=30,choices=(('MORT','Mort'),('INC','Inconscient'),('BLESSE2','Gravement Blesse'),('BLESSE1','Blesse'),('OK','En bonne sante')))
	situation = models.CharField(max_length=30,choices=(('PRISONNIER','Prisonnier(e)'),('COMBAT','En situation de combat')))
	dissimulation = models.SmallIntegerField(default=0)
	
	accompagnants = models.ManyToManyField('self', blank=True)
	prisonnier = models.ForeignKey('self', null=True, on_delete=models.DO_NOTHING)
	nbGardes = models.SmallIntegerField(default=0)
	nbTroupes = models.SmallIntegerField(default=0)
	
	apparence_combat = models.CharField(max_length=100,choices=(('AC0','Parait particulierement faible'),('AC1','Sait se defendre'),('AC2','A l\'air assez puissant'),('AC3','Dangereux')))
	arme = models.ForeignKey(Objet, null=True, on_delete=models.DO_NOTHING, related_name="arme")
	armure = models.ForeignKey(Objet, null=True, on_delete=models.DO_NOTHING, related_name="armure")
	en_main = models.ManyToManyField(Objet, related_name="en_main")
	
	attaque_melee = models.SmallIntegerField(default=0, editable=False)
	attaque_duel = models.SmallIntegerField(default=0, editable=False)
	defense_melee = models.SmallIntegerField(default=0, editable=False)
	defense_duel = models.SmallIntegerField(default=0, editable=False)
	initiative = models.SmallIntegerField(default=0, editable=False)
	
	Objets = models.ManyToManyField(Objet, related_name="objets")
	volume_MAX = models.SmallIntegerField(default=5)
	#competences = 
	

	def __str__(self):
		return self.nom