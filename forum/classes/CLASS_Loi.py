from django.db import models
from ..models import Jeu, Maison, Competence
from ..fonctions_base import *
from django.utils import timezone
from datetime import timedelta
from math import *

class Loi(models.Model):
	#user = models.ForeignKey(auth.User)
	nom = models.CharField(max_length=100)#, unique=True)
	lieu = models.ForeignKey('Lieu', on_delete=models.SET_NULL, blank=True, null=True)
	#description = models.TextField(default='', blank=True, null=True)
	post = models.ForeignKey('Post', on_delete=models.CASCADE, blank=True, null=True)
	perso = models.ForeignKey('Perso', on_delete=models.CASCADE, blank=True, null=True)
	maison = models.ForeignKey('Maison', on_delete=models.SET_NULL, blank=True, null=True)
	joueur = models.ForeignKey('Joueur', on_delete=models.SET_NULL, blank=True, null=True)
	commande = models.ForeignKey('Commande', on_delete=models.SET_NULL, blank=True, null=True)
	
	#votes = models.SmallIntegerField(default=0)
	
	valide = models.BooleanField(default=False)
	active = models.BooleanField(default=True)
	
	created_date = models.DateTimeField(default=timezone.now)
	date_validation = models.DateTimeField(default=timezone.now)
	date_fin = models.DateTimeField(default=timezone.now)
	
	date_jeu_fin = models.CharField(max_length=50, default='', blank=True)
	date_jeu_validation = models.CharField(max_length=50, default='', blank=True)
	
	maison_a_vote = models.ManyToManyField('Maison', blank=True, related_name=('maison_vote'))
	
	def __str__(self):
		return self.nom
		
	
	def save(self, *args, **kwargs):
		
		jeu = Jeu.objects.get(id = 1)
		T_date_jeu_fin = jeu.convert_date(self.date_fin)
		T_date_jeu_validation = jeu.convert_date(self.date_validation)
		self.date_jeu_fin = format_date_jeu(T_date_jeu_fin,jeu.format_date)
		self.date_jeu_validation = format_date_jeu(T_date_jeu_validation,jeu.format_date)
		
		self.maison = self.perso.maison
		
		
		if timezone.now() >= self.date_fin and self.active and not self.valide :
			if self.get_nb_votes() > 50:
				self.valide = True
				if self.date_validation < self.created_date + timedelta(seconds=5) :
					self.date_validation = timezone.now()
			
			else : self.active = False
		self.date_fin = self.commande.date_fin
		
		super().save()  # Call the "real" save() method.'''
		print('-------------SAVE LOI')
		
	def return_senateur_vote(self):
		T_resultat = []
		for m in self.maison_a_vote.all() :
			T_resultat.append(m.senateur.nom)
		if len(T_resultat)>1 : resultat = ', '.join(T_resultat[:-1])+' et '+T_resultat[-1]
		elif len(T_resultat)==1 : resultat = T_resultat[0]
		else : resultat = 'aucun'
		return resultat
		
	def get_nb_votes(self):
		lieu_senat = self.lieu
		comp_aura = Competence.objects.get(nom_info='aura')
		
		prestige_total = 0
		prestige_vote = 0
		qst_all_maison = Maison.objects.all()
		for maison in qst_all_maison:
			if maison.get_OK_pr_senat():
				prestige_total = prestige_total + maison.prestige
				if maison in self.maison_a_vote.all() : prestige_vote = prestige_vote + maison.prestige
		
		print(str(prestige_vote)+'-'+str(prestige_total))
		influence_vote = int(round(float(prestige_vote*100/prestige_total)))
		influence_total = 100
		
		for perso in lieu_senat.persos_presents.all() :
			if perso.influence_OK() :
				influence_perso = perso.valeur_competence(comp_aura)
				if perso.charge : influence_perso = influence_perso + perso.charge.influence
				influence_total = influence_total + influence_perso
				if perso.maison in self.maison_a_vote.all() :
					influence_vote = influence_vote + influence_perso
		
		pct_influence = int(round(float(influence_vote*100/influence_total)))
		return pct_influence
		