from django.db import models
from django.utils import timezone
#from ..models import Loi
from ..models import Competence, Charge
from ..fonctions_base import *

class Maison(models.Model):
	#user = models.ForeignKey(auth.User)
	active = models.BooleanField(default=True)
	priorite = models.SmallIntegerField(default=9)
	nom = models.CharField(max_length=40, unique=True)
	description = models.TextField(default='', blank=True, null=True)
	background = models.TextField(default='', blank=True, null=True)
	nom_info = models.CharField(max_length=20, blank=True, default='')
	institutions = models.TextField(blank=True, default='')
	dieu = models.CharField(max_length=40, blank=True, default='')
	embleme = models.CharField(max_length=40, blank=True, default='')
	suzerain = models.CharField(max_length=40, blank=True, default='')
	senateur = models.ForeignKey('Perso', blank=True, null=True, on_delete=models.SET_NULL, related_name=('senateur'))
	
	bonus_competence_categorie1 = models.ForeignKey('Categorie_competence', blank=True, null=True, on_delete=models.SET_NULL, related_name=('bonus_competence_categorie1'))
	bonus_competence1 = models.ForeignKey('Competence', blank=True, null=True, on_delete=models.SET_NULL, related_name=('bonus_competence1'))
	bonus_competence_categorie2 = models.ForeignKey('Categorie_competence', blank=True, null=True, on_delete=models.SET_NULL, related_name=('bonus_competence_categorie2'))
	bonus_competence2 = models.ForeignKey('Competence', blank=True, null=True, on_delete=models.SET_NULL, related_name=('bonus_competence2'))
	
	prestige = models.SmallIntegerField(default=100)
	pct_prestige = models.SmallIntegerField(default=0, verbose_name='pct_prestige : valeur temporaire et auto')
	influence = models.SmallIntegerField(default=0, verbose_name='influence : valeur temporaire et auto')
	nb_voix_senat = models.SmallIntegerField(default=0, verbose_name='nb_voix_senat : valeur temporaire et auto')
	
	def __str__(self):
		return self.nom
		
	def save(self):
		
		#self.influence = self.get_influence()
		#self.nb_voix_senat = self.get_pct_influence()
		'''
		# sauvegarde des lois en cours pour les mettre a jour
		qst_lois_encours = Loi.objects.filter(active=True)
		for loi_encours in qst_lois_encours :
			if objet_ds_manytomany(self,loi_encours.maison_a_vote):
				loi_encours.save()
		'''
		#senateur
		charge_senateur = Charge.objects.get(nom_info='senateur')
		if self.senateur :
			qst_senateurs = charge_senateur.perso_charge.filter(maison=self).exclude(id=self.senateur.id).all()
			for senateur in qst_senateurs :
				senateur.charge = None
				senateur.save()
			if not self.senateur.charge == charge_senateur :
				self.senateur.charge = charge_senateur
				self.senateur.save()
		else : 
			qst_senateurs = charge_senateur.perso_charge.filter(maison=self).all()
			for senateur in qst_senateurs :
				print(senateur)
				senateur.charge = None
				senateur.save()
				
			
		super().save()  # Call the "real" save() method.
		
	def get_pct_prestige(self):
		resultat = 0
		if self.get_OK_pr_senat() :
			prestige_total = 0
			qst_all_maison = Maison.objects.all()
			for maison in qst_all_maison:
				if maison.get_OK_pr_senat():
					prestige_total = prestige_total + maison.prestige
			resultat = int(round(float(self.prestige*100/prestige_total)))
		
		return resultat
	
	def get_influence(self):
		resultat = 0
		if self.senateur and self.active :
			bonus_aura = 0
			bonus_charge = 0
			comp_aura = Competence.objects.get(nom_info='aura')
			lieu_senat = self.senateur.charge.lieu
			qst_persos = self.persos_maison.filter(active=True).filter(hote__isnull=True).filter(lieu=lieu_senat).filter(PV__gt=0).all()
			for perso in qst_persos :
				bonus_aura = bonus_aura + perso.valeur_competence(comp_aura)
				if perso.charge :
					bonus_charge = bonus_charge + perso.charge.influence
			
			resultat = self.get_pct_prestige() + bonus_aura + bonus_charge
		return resultat
		
	def get_pct_influence(self):
		resultat = 0
		if self.get_OK_pr_senat() :
			influence_total = 0
			qst_all_maison = Maison.objects.all()
			for maison in qst_all_maison:
				if maison.get_OK_pr_senat():
					influence_total = influence_total + maison.get_influence()
			resultat = int(round(float(self.get_influence()*100/influence_total)))
		
		return resultat
		
	def get_OK_pr_senat(self):
		r = True
		if not self.active : r=False
		if not self.senateur : r= False
		return r
		