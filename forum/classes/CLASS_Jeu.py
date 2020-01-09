from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import timedelta
from math import *
from ..models import Mois

class Jeu(models.Model):

	nom = models.CharField(verbose_name="Nom de la partie",max_length=30, unique=True)
	description = models.TextField(null=True, blank=True)
	nom_info = models.CharField(verbose_name="Nom informatique - lien vers static",max_length=30, unique=True)
	base_delay = models.DecimalField(verbose_name="Délai pour une action courante, en heures", default=1, max_digits=6, decimal_places=4)
	delay_suppr = models.DecimalField(verbose_name="Temps avant de supprimer une action finie, en jours", default=4, max_digits=4, decimal_places=2)
	defense_assault_max = models.SmallIntegerField(verbose_name="Valeur maximale de la defense d'un lieu standard",default=5)
	
	#calendrier
	date_initiale = models.DateTimeField(verbose_name="Date réelle initiale", default=timezone.now)
	
	heure_jeu_init = models.SmallIntegerField(verbose_name="Date jeu initiale : heure",default=1, validators=[MinValueValidator(0),MaxValueValidator(23)])
	jour_jeu_init = models.SmallIntegerField(verbose_name="Date jeu initiale : jour",default=1, validators=[MinValueValidator(1)])
	mois_jeu_init = models.ForeignKey(Mois,verbose_name="Date jeu initiale : mois", default = 1, on_delete=models.SET_DEFAULT)
	annee_jeu_init = models.SmallIntegerField(verbose_name="Date jeu initiale : année", default=99)
	jour_par_mois = models.SmallIntegerField(verbose_name="Nombre de jour par mois", default=31, validators=[MinValueValidator(1)])
	mois_par_an = models.SmallIntegerField(verbose_name="Nombre de mois par an", default=12, validators=[MinValueValidator(1)])
	
	format_date = models.CharField(verbose_name="Phrase de description de la date <minute><heure><jour><mois><annee>", max_length=40, default = "<heure>h<minute>, <jour> jour <mois>")
	rapport_temps = models.DecimalField(verbose_name="Combien d'heures réelles pour une heure de jeu ?", default=1, max_digits=4, decimal_places=2)
	
	nb_heure_jour = models.SmallIntegerField(verbose_name="Nombre d'heures de jour", default=10)
	nb_heure_nuit = models.SmallIntegerField(verbose_name="Nombre d'heures de nuit", default=10)
	
	delai_edit = models.SmallIntegerField(verbose_name="Delai laisser pour éditer son post en minute", default=5)
	delai_refresh = models.SmallIntegerField(verbose_name="Delai entre chaque rafrachissement automatique, en minute", default=0)
	
	lock_onload = models.BooleanField(default=False,verbose_name="param temporaire pour empecher le thread d'onload en même temps qu'un refresh manuel - A LAISSER DECOCHE !")
	regle_index = models.ForeignKey('Regle', default = 1, on_delete=models.SET_DEFAULT)
	
	def __str__(self):
		return self.nom
		
		
	def save(self):
		if self.jour_jeu_init>self.jour_par_mois : self.jour_jeu_init = self.jour_par_mois
		
		num_mois = self.mois_jeu_init.numero
		if num_mois > self.mois_par_an :
			num_mois = self.mois_par_an
			if self.mois_jeu_init == Mois.objects.get(numero=num_mois).exist() :
				self.mois_jeu_init = Mois.objects.get(numero=num_mois)
			else : self.mois_jeu_init = Mois.objects.get(id=1)
		
		if self.nb_heure_jour+self.nb_heure_nuit>24 : self.nb_heure_nuit = 24-self.nb_heure_jour
		
		#now = timezone.now()
		#print(now)

		super().save()
	
	
	def convert_date(self,date):
		#date_now = timezone.now
		
		delta_date = date - self.date_initiale
		delta_heure = delta_date.seconds/3600 + delta_date.days*24
		
		delta_heure_jeu_float = delta_heure / float(self.rapport_temps)
		delta_heure_jeu = floor(delta_heure_jeu_float)
		
		minute_jeu = floor((delta_heure_jeu_float - delta_heure_jeu)*60)
		heure_jeu = self.heure_jeu_init + delta_heure_jeu
		jour_jeu = self.jour_jeu_init
		ordre_mois_jeu = self.mois_jeu_init.numero
		anne_jeu = self.annee_jeu_init
		
		while heure_jeu>23 :
			heure_jeu = heure_jeu-24
			jour_jeu = jour_jeu+1
			
		while heure_jeu<0 :
			heure_jeu = heure_jeu+24
			jour_jeu = jour_jeu-1
			
		while jour_jeu>self.jour_par_mois :
			jour_jeu = jour_jeu - self.jour_par_mois
			ordre_mois_jeu = ordre_mois_jeu+1
		
		while jour_jeu<0 :
			jour_jeu = jour_jeu + self.jour_par_mois
			ordre_mois_jeu = ordre_mois_jeu-1
			
		while ordre_mois_jeu>self.mois_par_an :
			ordre_mois_jeu = ordre_mois_jeu - self.mois_par_an
			anne_jeu = anne_jeu+1
		
		while ordre_mois_jeu<0 :
			ordre_mois_jeu = ordre_mois_jeu + self.mois_par_an
			anne_jeu = anne_jeu-1
			
		mois_jeu = Mois.objects.get(numero = ordre_mois_jeu)
		if not mois_jeu : mois_jeu =  Mois.objects.get(id = 1)
		
		T_resultat = [minute_jeu,heure_jeu,jour_jeu,mois_jeu,anne_jeu]
		
		return T_resultat
	
	def convert_date_inverse(self,T_date_jeu):
		
		nb_annee_jeu_deroule = T_date_jeu[4]-self.annee_jeu_init
		nb_mois_jeu_deroule = T_date_jeu[3].numero-self.mois_jeu_init.numero + nb_annee_jeu_deroule*self.mois_par_an
		nb_jours_jeu_deroule = T_date_jeu[2]-self.jour_jeu_init + nb_mois_jeu_deroule*self.jour_par_mois
		nb_heures_jeu_deroule = T_date_jeu[1]-self.heure_jeu_init + nb_jours_jeu_deroule*24
		nb_minutes_jeu_deroule = T_date_jeu[0]-1 + nb_heures_jeu_deroule*60
		
		nb_secondes_jeu_deroule = nb_minutes_jeu_deroule*60
		delta_secondes = int(nb_secondes_jeu_deroule * self.rapport_temps)
		
		date = self.date_initiale + timedelta(seconds=delta_secondes)
		return date
	
	def moment_journee(self,heure_jeu):
		
		resultat = 'erreur'
		
		h_debut_jour = ceil(13-(self.nb_heure_jour/2))
		#if h_debut_jour<0 : h_debut_jour = 24-h_debut_jour
		
		h_fin_jour = ceil(13+(self.nb_heure_jour/2))
		if h_fin_jour>23 : h_fin_jour = h_debut_jour-24
		
		h_debut_nuit = ceil(1-(self.nb_heure_nuit/2))
		if h_debut_nuit<0 : h_debut_nuit = h_debut_nuit+24
		
		h_fin_nuit =ceil(1+(self.nb_heure_nuit/2))
		#if h_fin_nuit>23 : h_fin_nuit = h_fin_nuit-24
		
		h_inter = ceil((24-h_debut_jour-h_debut_nuit)/2)
		
		h_debut_soir = h_fin_jour
		h_fin_soir = h_fin_jour+h_inter
		if h_fin_soir>23 : h_fin_soir=h_fin_soir-24
		
		h_debut_matin = h_debut_jour-h_inter
		if h_debut_matin<0 : h_debut_matin = h_debut_matin+24
		h_fin_matin = h_debut_jour
		
		if est_ds_heures(heure_jeu,h_debut_jour,h_fin_jour) : resultat = 'jour'
		elif est_ds_heures(heure_jeu,h_debut_nuit,h_fin_nuit) : resultat = 'nuit'
		elif h_inter>0 and est_ds_heures(heure_jeu,h_debut_soir,h_fin_soir) : resultat = 'soir'
		elif h_inter>0 and est_ds_heures(heure_jeu,h_debut_matin,h_fin_matin) : resultat = 'matin'
		
		return resultat
		
	
