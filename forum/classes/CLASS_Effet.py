from django.db import models
from django.utils import timezone
from datetime import timedelta
from ..models import Jeu

class Effet(models.Model):
	active = models.BooleanField(default=True)
	niv_priorite = models.SmallIntegerField(default=1)
	nom = models.CharField(max_length=30,unique=True)
	nom_visible = models.CharField(max_length=30, null=True, blank=True)
	effet_visible = models.BooleanField(default=False)
	classe = models.CharField(max_length=100, blank=True,default = "",choices=(('potion','potion'),('benediction','benediction'),('malediction','malediction'),('poison','poison'),('charme','charme'),('maladie','maladie'),('','divers')))
	negatif = models.BooleanField(default=False)
	support = models.CharField(max_length=100,blank=True,default = "",choices=(('perso','perso'),('arme','arme'),('armure','armure'),('','divers')))
	
	special = models.CharField(max_length=120,blank=True)
	competence_bonifie = models.ForeignKey('Competence', null=True, blank=True, on_delete=models.SET_NULL, related_name = 'effet_comp_bonus')
	val_competence_bonifie = models.SmallIntegerField(default=0)
	posture_bonifie = models.ForeignKey('Posture', null=True, blank=True, on_delete=models.SET_NULL, related_name = 'effet_posture_bonus')
	val_posture_bonifie = models.SmallIntegerField(default=0)
	bonus_combat = models.SmallIntegerField(default=0)
	bonus_PV = models.SmallIntegerField(default=0)
	bonus_PA = models.SmallIntegerField(default=0)
	bonus_PC = models.SmallIntegerField(default=0)
	bonus_PE = models.SmallIntegerField(default=0)
	bonus_protection = models.SmallIntegerField(default=0)
	bonus_defense = models.SmallIntegerField(default=0)
	bonus_dommage = models.SmallIntegerField(default=0)
	
	delai = models.SmallIntegerField(default=100)
	infini = models.BooleanField(default=False)
	fonction_suivant = models.CharField(max_length=30,null=True, blank=True, verbose_name="fonction_suivant : lance la fonction a la fin du delai. si Null, l'effet s'arrete")
	
	
	
	def __str__(self):
		classe = ""
		support = " - sur artefact"
		active = ""
		if self.classe != "" : classe = self.classe+' - '
		if self.support != "" : support = ' - sur '+self.support
		if not self.active : active = "X "
		return active+classe+self.nom+support
		
	def save(self):
		
		if not self.nom_visible : self.nom_visible = self.nom
		if self.bonus_PV and not self.fonction_suivant : self.fonction_suivant = "guerison"
		if self.special : self.special = self.special.replace(',',';')
		super().save()
		
	def priorite(self):
		return self.niv_priorite
		
	
	
class Effet_perso(models.Model):
	
	perso = models.ForeignKey('Perso', null=True, blank=True, on_delete=models.SET_NULL, related_name = 'effet_perso')
	objet = models.ForeignKey('Objet_perso', null=True, blank=True, on_delete=models.SET_NULL, related_name = 'effet_objet')
	eft = models.ForeignKey('Effet', on_delete=models.CASCADE, related_name = 'perso_effet')
	objet_initial = models.ForeignKey('Objet_perso', null=True, blank=True, on_delete=models.SET_NULL, related_name = 'effet_obj') 
	
	valeur = models.SmallIntegerField(default=1)
	special = models.CharField(max_length=120,blank=True, null=True)
	
	date_debut = models.DateTimeField(default=timezone.now)
	date_fin = models.DateTimeField(default=timezone.now)
	infini = models.BooleanField(default=False)
	
	fini = models.BooleanField(default=False)
	commence = models.BooleanField(default=False)
	erreur = models.BooleanField(default=False)
	
	def __str__(self):
		#return str(self.id)
		nom_support = ''
		if self.objet : nom_support = self.objet.obj.nom +'/'+ self.objet.perso.nom_origine
		if self.perso : nom_support = self.perso.nom_origine
		return nom_support+' - '+self.eft.nom
		
	def save(self, *args, **kwargs):
		
		now = timezone.now()
		jeu = Jeu.objects.get(id=1)
		
		if self.objet_initial:
			if self.infini and not self.objet_initial.obj.effet.infini :
				self.date_fin = now+timedelta(hours=float(jeu.base_delay)*(self.objet_initial.obj.effet.delai/100))
				self.infini = False
			self.valeur = self.objet_initial.valeur
			if not self.special : self.special = self.objet_initial.obj.special
		else :
			if not self.eft.infini : 
				self.date_fin = now+timedelta(hours=float(jeu.base_delay)*(self.eft.delai/100))
				self.infini=False
				
		
		if self.infini : 
			#self.fini = False
			self.date_fin = timezone.now()+timedelta(days=3650)
			
		if self.erreur : self.fini = True
		if now>=self.date_debut : self.commence = True
			
		if self.eft.infini : self.infini = True
		
			
		
		super().save()
		
		if self.eft.nom=='doppelganger' and self.commence and not self.perso.doppelganger and not self.fini :
			if self.special : n = self.special
			else : n = self.perso.nom_info
			self.perso.transforme(n)
		
			self.perso.save()
		
	def nom(self):
		if self.objet_initial : resultat = self.objet_initial.obj.nom
		else : resultat = self.eft.nom_visible
		return resultat
	


		