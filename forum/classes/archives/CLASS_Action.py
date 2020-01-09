from django.db import models

class Action(models.Model):
	
	nom = models.CharField(max_length=40, unique=True)
	nom_info = models.CharField(max_length=30, unique=True)
	image = models.CharField(max_length=30, unique=True)
	description = models.TextField(default='', blank=True, null=True)
	priorite = models.SmallIntegerField(default=1)
	#categorie = 
	PA = models.SmallIntegerField(default=1)
	delay = models.SmallIntegerField(default=1) # en minute
	
	condition_sante =
	condition_situation = 
	condition_lieu = competences_utiles = models.ManyToManyField('Lieu')
	
	action_parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
	is_objet = models.BooleanField(default=False)
	is_lieu = models.BooleanField(default=False)
	empechable = models.BooleanField(default=True)
	dissimulable = models.BooleanField(default=True)
	interdit = models.BooleanField(default=False)
	
	cible_perso = models.BooleanField(default=False)
	cible_persos = models.BooleanField(default=False)
	cible_lieu = models.BooleanField(default=False)
	cible_lieux = models.BooleanField(default=False)
	cible_heure = models.BooleanField(default=False)
	cible_action = models.BooleanField(default=False)
	champ_recherche1 = models.BooleanField(default=False)
	champ_recherche2 = models.BooleanField(default=False)
	champ_texte = models.BooleanField(default=False)
	
	msg = models.TextField(default='', blank=True, null=True)
	msg_resume = models.TextField(default='', blank=True, null=True)
	signal_MJ = models.SmallIntegerField(default=0)
	msg_MJ = models.TextField(default='', blank=True, null=True)
	
	competences_utiles = models.ManyToManyField('Competence')
	
	def __str__(self):
		return self.nom