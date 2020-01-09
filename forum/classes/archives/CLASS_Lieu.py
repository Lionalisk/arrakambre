from django.db import models
from forum.models import Maison
from forum.classes.CLASS_Perso import *

print('BBBB')
class Lieu(models.Model):
	nom = models.CharField(max_length=100, unique=True)
	description = models.TextField(default='')
	image = models.CharField(max_length=40, default = 'lieu_none.jpg')
	maison = models.ForeignKey(Maison, verbose_name="Maison", null=True, on_delete=models.SET_NULL, blank=True)
	passages = models.ManyToManyField('self', blank=True)
	lieu_parent = models.ForeignKey('self', verbose_name="Lieu", null=True, on_delete=models.DO_NOTHING, blank=True)
	dissimulation = models.SmallIntegerField(default=0)
	defense_garde = models.SmallIntegerField(default=0)
	defense_assault = models.SmallIntegerField(default=0)
	defense_intrusion = models.SmallIntegerField(default=0)
	perso_autorise = models.ManyToManyField('Perso', blank=True, related_name = 'persos_autorises') # liste des personnes autorisees par le maitre des lieux a entrer
	secret = models.BooleanField(default=False)
	proprietaire = models.ForeignKey('Perso', null=True, on_delete=models.SET_NULL, blank=True, related_name = 'proprietaire')
	#action =

	def __str__(self):
		return self.nom