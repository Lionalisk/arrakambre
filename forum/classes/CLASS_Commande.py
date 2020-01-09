from django.db import models
from datetime import timedelta
from ..models import Jeu
#from ..fonctions_actions import *
from ..fonctions_base import *
from django.utils import timezone

#import datetime

class Commande(models.Model):
	joueur = models.ForeignKey('Joueur', on_delete=models.SET_NULL, blank=True, null=True)
	perso = models.ForeignKey('Perso', on_delete=models.CASCADE, blank=True, null=True, related_name="commande_perso")
	action = models.ForeignKey('Action', on_delete=models.CASCADE, null=True)
	lieu = models.ForeignKey('Lieu', on_delete=models.SET_NULL, blank=True, null=True)
	post = models.ForeignKey('Post', on_delete=models.SET_NULL, blank=True, null=True)
	active = models.BooleanField(default=True)
	
	commande_precede = models.ForeignKey('self', verbose_name="Commande précédent le lancement", on_delete=models.CASCADE, blank=True, null=True, related_name = 'commande_enclenche')
	commande_parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name = 'commande_associe')
	resultat = models.ForeignKey('Resultat', null=True, blank=True, on_delete=models.SET_NULL, related_name = 'resultat')
	
	texte_post = models.TextField(blank=True, null=True, default = '')
	persos_cible = models.ManyToManyField('Perso', blank=True, related_name = 'persos_cible')
	lieux_cible = models.ManyToManyField('Lieu', blank=True, related_name = 'lieux_cible')
	objet = models.ForeignKey('Objet_perso', on_delete=models.SET_NULL, null=True, blank=True)
	resultat_cible = models.ForeignKey('Resultat', null=True, blank=True, related_name = 'resultat_cible', on_delete=models.CASCADE)
	num = models.SmallIntegerField(default=0)
	champ_recherche1 = models.CharField(max_length=100, default='', blank=True, null=True)
	champ_recherche2 = models.CharField(max_length=100, default='', blank=True, null=True)
	champ_texte = models.TextField(blank=True, null=True, default = '')
	instant_heure = models.SmallIntegerField(default=0, null=True, blank=True)
	instant_jour = models.SmallIntegerField(default=1, null=True, blank=True)
	instant_mois = models.ForeignKey('Mois', on_delete=models.SET_NULL, null=True, blank=True,default=1)
	
	
	chance_reussite = models.SmallIntegerField(default=100)
	bonus_reussite = models.SmallIntegerField(default=0)
	jet = models.SmallIntegerField(default=0)
	jet_opposition = models.SmallIntegerField(default=0)
	
	dissimulation = models.SmallIntegerField(default=0)
	joueur_connaissant = models.ManyToManyField('Joueur', blank=True, related_name = 'joueur_know_commande')
	#txt_joueurs_connaissant = models.TextField(default='', blank=True, null=True , editable=False)
	
	fini = models.BooleanField(default=False)
	commence = models.BooleanField(default=False)
	erreur = models.BooleanField(default=False)
	
	no_result = models.BooleanField(default=False)
	
	created_date = models.DateTimeField(default=timezone.now)
	date_debut = models.DateTimeField(default=timezone.now)
	date_fin = models.DateTimeField(default=timezone.now)
	date_jeu_fin = models.CharField(max_length=50, default='', blank=True)
	T_date_jeu_fin = models.CharField(max_length=50, default='', blank=True)

	desc = models.TextField(default='', blank=True, null=True)
	
	#def __init__(self):



	def __str__(self):
		#return self.created_date.strftime("%Y-%m-%d %H:%M")+' - '+self.lieu.nom+'-'+self.perso.nom+' - '+self.action.nom+' - '+self.date_validation.strftime("%Y-%m-%d %H:%M")
		etat = "ATTENTE"
		if self.commence : etat = "START"
		if self.fini : etat = "END"
		if self.erreur : etat = "ERREUR"
		
		if self.perso.lieu : nom_lieu = self.perso.nom
		else : nom_lieu=''
		return str(self.id)+" "+etat+" : "+self.date_debut.strftime("%d/%m - %H:%M")+' - '+nom_lieu+' - '+self.perso.nom+' - '+self.action.nom+' - '+self.date_fin.strftime("%d/%m - %H:%M")
		#return self.date_debut.strftime("%d/%m - %H:%M")+' - '+self.desc+' - '+self.date_validation.strftime("%d/%m - %H:%M")
		
	def save(self, *args, **kwargs):
		jeu = Jeu.objects.get(id = 1)
		
		if not self.champ_recherche1 : self.champ_recherche1=""
		if not self.champ_recherche2 : self.champ_recherche2=""
		
		if self.fini : self.commence = True
		if self.erreur : 
			self.commence = True
			self.fini = True
		
		#libere tous les persos occupes par cette commande si celle ci est fini
		if self.fini :
			persos_occupes = self.commande_perso.all()
			for p in persos_occupes :
				p.occupe = None
				p.en_combat = False
				p.en_soin = False
				p.save()
		
		if self.perso and not self.lieu : self.lieu = self.perso.lieu
		
		if self.commande_parent : self.dissimulation = self.commande_parent.dissimulation
		if self.dissimulation==0 and self.lieu and (self.lieu.ferme or self.lieu.dissimulation>0) : self.dissimulation=1
		
		if self.chance_reussite>100 : self.chance_reussite=100
		if self.chance_reussite<0 : self.chance_reussite=0
		
		if self.commande_precede and not self.active :
			self.date_debut = self.commande_precede.date_fin
			self.date_fin = self.date_debut + timedelta(hours=float(jeu.base_delay)*(self.action.delay/100))
		
		
		T_date_jeu = jeu.convert_date(self.date_fin)
		self.date_jeu_fin = format_date_jeu(T_date_jeu,jeu.format_date)
		self.T_date_jeu_fin = format_T_date_jeu(T_date_jeu)
		
		
		if not self.lieu : self.lieu = self.perso.lieu
		
		if self.post and self.post.lieu != self.lieu :
			self.post.lieu = self.lieu
			self.post.save()
		
		if self.resultat_cible and not self.resultat : self.resultat = self.resultat_cible
		
		super().save()  # Call the "real" save() method.'''
		print("############# SAVE COMMANDE num "+str(self.id)+" - "+str(self.date_fin))#+str(timezone.now()))
		#print('----------------'+self.objet.obj.nom)
	
	def delete(self):
		
		persos_occupes = self.commande_perso.all()
		for p in persos_occupes :
			p.occupe = None
			p.en_combat = False
			p.en_soin = False
			p.save()
		super().delete()
	
	def return_persos_cible(self):
		T_cible = self.persos_cible.all()
		if len(T_cible)==0 : resultat = ""
		elif len(T_cible)==1 : resultat = T_cible[0].nom
		else : 
			T_resultat = []
			for p in T_cible:
				T_resultat.append(p.nom)
			resultat = ', '.join(T_resultat[:-1])+' et '+T_resultat[-1]
		
		return resultat
		
		
	def return_lieux_cible(self):
		T_cible = self.lieux_cible.all()
		if len(T_cible)==0 : resultat = ""
		elif len(T_cible)==1 : resultat = T_cible[0].nom
		else : 
			T_resultat = []
			for p in T_cible:
				T_resultat.append(p.nom)
			resultat = ', '.join(T_resultat[:-1])+' et '+T_resultat[-1]
		
		return resultat
		
	def return_resultat_cible(self):
		resultat = ""
		if self.resultat_cible : resultat = self.resultat_cible.nom
		return resultat
		
	def return_objet_implique(self):
		resultat = ""
		if self.objet :
			resultat = self.objet.nom
		
	def return_date_created(self):
		return self.created_date.strftime("%H:%M - %d/%m")
		
	def return_date_debut(self):
		return self.date_debut.strftime("%H:%M - %d/%m")
		
	def return_date_fin(self):
		return self.date_fin.strftime("%H:%M - %d/%m")
		
	def return_succes(self):
		resultat = True
		if self.chance_reussite and self.jet :
			if (self.jet + self.jet_opposition) <= (self.chance_reussite + self.bonus_reussite):
				resultat = True #succes
			else :
				resultat = False #echec
		return resultat
		
	def return_proba_succes(self):
		resultat = ""
		if self.chance_reussite and self.jet :
			resultat = str((self.jet + self.jet_opposition))+'/'+ str((self.chance_reussite + self.bonus_reussite))

		return resultat
		
	def return_recap(self):
		champ1 = champ2 = ""
		if self.champ_recherche1 : champ1 = self.champ_recherche1
		if self.champ_recherche2 : champ2 = self.champ_recherche2
		T_cibles = [self.return_objet_implique(),self.return_persos_cible(),self.return_lieux_cible(),self.return_resultat_cible(),champ1,champ2]
		resultat = self.perso.nom+' - '+self.action.nom+' - '
		for cible in T_cibles :
			if cible and cible != '' : resultat = resultat+str(cible)+' / '
		resultat = resultat + ' - Fin: '+self.date_jeu_fin
		return resultat.replace(' -  - ',' - ').replace(' /  - ',' - ')
		
	def make_fail(self):
		if self.chance_reussite and self.jet :
			if (self.jet + self.jet_opposition) <= (self.chance_reussite + self.bonus_reussite):
				difference = 100 - (self.chance_reussite + self.bonus_reussite - self.jet_opposition )
				if difference<1 : difference=1
				self.jet = (self.chance_reussite + self.bonus_reussite) + de(difference)
				
				if self.jet >100 : self.jet = 100
				
				self.save()
				
	def make_success(self):
		if self.chance_reussite and self.jet :
			
			if (self.jet + self.jet_opposition) >(self.chance_reussite + self.bonus_reussite):
				
				difference = (self.chance_reussite + self.bonus_reussite - self.jet_opposition)
				if difference<1 : difference=1
				self.jet = de(difference)
				
				if self.jet <1 : self.jet = 1
				
				self.save()
				
	def validation(self):
		self.active = True
		self.date_debut = timezone.now()
		jeu = Jeu.objects.get(id = 1)
		timedelta_delay = timedelta(hours=float(jeu.base_delay)*(self.action.delay/100))
		self.date_fin = self.date_debut+timedelta_delay
		self.save()
	
	def annulation(self):
		if self.post : self.post.delete()
		self.delete()
		
	def pause(self):
		self.active = False
		self.save()
		
	def play(self):
		self.active = True
		jeu = Jeu.objects.get(id = 1)
		self.date_debut = timezone.now() + timedelta(seconds=60*jeu.delai_edit)
		timedelta_delay = timedelta(hours=float(jeu.base_delay)*(self.action.delay/100))
		self.date_fin = self.date_debut+timedelta_delay
		self.save()