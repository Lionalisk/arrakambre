
from django.db import models
from ..fonctions_base import *

class Posture(models.Model):
	active = models.BooleanField(default=True)
	nom = models.CharField(max_length=100, unique=True)
	nom_info = models.CharField(max_length=100, unique=True)
	description = models.TextField(default='', blank=True)
	description2 = models.TextField(null=True, blank=True, verbose_name='description2 : se genere automatiquement')
	lock_description2 = models.BooleanField(default=False, verbose_name='si oui, description2 ne se genere pas automatiquement')
	
	categorie_combat = models.ForeignKey('Categorie_combat', on_delete=models.SET_NULL, blank=True, null=True)
	bonus = models.SmallIntegerField(default=0)
	commpetence_bonus = models.ForeignKey('Competence', verbose_name="Apporte comme bonus la valeur de cette competence", on_delete=models.SET_NULL, blank=True, null=True)
	multiplie_comp_bonus = models.SmallIntegerField(default=1)
	posture_neutralise = models.ForeignKey('self', verbose_name="Posture neutralisée par cette posture", on_delete=models.SET_NULL, blank=True, null=True, related_name=('posture_neutralisee'))
	
	choix_defaut = models.BooleanField(default=True, verbose_name="Peut être une posture par défaut")
	choix_attaque = models.BooleanField(default=False, verbose_name="Peut être une posture choisie lors de l'attaque")
	PV_max = models.SmallIntegerField(default=10)
	PV_min = models.SmallIntegerField(default=1)
	condition_espece = models.ManyToManyField('Espece', blank=True, related_name = "espece_condition_posture", verbose_name = "Condition d'espèce pour adopter cette Posture")
	condition_hote = models.SmallIntegerField(default=1, choices=((0,'Peut etre fait si le perso est un hote de lieu ou non'),(1,"Ne peut etre fait que si le perso n'est pas un hote de lieu"),(2,'Ne peut être fait que si le perso est un hote de lieu')))
	condition_cache = models.SmallIntegerField(default=0, choices=((0,'Peut etre fait si le perso est caché ou non'),(1,"Ne peut etre fait que si le perso n'est pas caché"),(2,'Ne peut être fait que si le perso est caché')))
	
	priorite = models.SmallIntegerField(default=1)
	
	

	def __str__(self):
		a = ''
		if not self.active : a = 'X '
		
		return a+self.categorie_combat.nom+' - '+self.nom
		
	def save(self, *args, **kwargs):
		if not self.lock_description2 :
			#jeu = Jeu.objects.get(id=1)
			
			if self.description : description2 = self.description+'\n'#<div><img src="/static/forum/'+jeu.nom_info+'/img/separateur_h.png"></div>'
			else : description2=''
			T_ajout = []
			
			if self.bonus>0 : bonus = ' + '+str(self.bonus)
			elif self.bonus<0 : bonus = str(self.bonus).replace('-',' - ')
			else : bonus=''
			
			if self.commpetence_bonus :
				multi = ''
				if self.multiplie_comp_bonus>0 : multi = '*'+str(self.multiplie_comp_bonus)
				T_ajout.append("<div class='red'><i>"+'Bonus : '+self.commpetence_bonus.nom + multi + bonus+"</i></div>")
			
			else :
				if bonus == '' : txt_bonus = ''
				else : T_ajout.append("<div class='red'><i>"+bonus.replace(' + ','Bonus : + ').replace(' - ','Malus : - ')+"</i></div>")
				
			if self.posture_neutralise :
				T_ajout.append("<div class='red'><i>Neutralise la Posture de l'adversaire : "+self.posture_neutralise.nom+'</i></div>')
			
			if self.choix_defaut : T_ajout.append('<div><i>Peut être une Posture par défaut</i></div>')
			if self.choix_attaque : T_ajout.append("<div><i>Peut être choisi en option lors de l'action d'attaque</i></div>")
			if self.PV_max<3 : T_ajout.append("<div><i>Possible qu'avec moins de "+str(self.PV_max)+" PV</i></div>")
			if self.PV_min!=1 : 
				if self.PV_min>1 : T_ajout.append("<div><i>Possible qu'avec au moins "+str(self.PV_min)+" PV</i></div>")
			
			self.description2 = description2
			if len(T_ajout)>0:
				self.description2 = self.description2+'\n'+''.join(T_ajout)+''
			
			
			
		super().save()  # Call the "real" save() method.

				
	def verif_posture_cible(self,perso):
		T_verif = []
		
		if perso.PV<self.PV_min : T_verif.append(" n'est pas en assez bonne santé pour adopter cette posture de combat")
		if perso.PV>self.PV_max : T_verif.append(" n'est pas blessé pour adopter cette posture de combat")
		if perso.dissimulation>0 and self.condition_cache == 1 : T_verif.append(" ne doit pas être dissimulé pour adopter cette posture de combat")
		if perso.dissimulation==0 and self.condition_cache == 2 : T_verif.append(" doit être caché pour adopter cette posture de combat")
		if perso.hote and self.condition_hote == 1 : T_verif.append("Le gardien d'un lieu ne peut pas adopter cette posture de combat")
		if not perso.hote and self.condition_hote == 2 : T_verif.append("Il faut être le gardien d'un lieu pour adopter cette posture de combat")
		if not objet_ds_manytomany(perso.espece,self.condition_espece) and len(self.condition_espece.all())>0 : T_verif.append("Un "+perso.especenom+" ne peut adopter cette posture de combat")
		if self.categorie_combat != perso.posture.categorie_combat : T_verif.append("La posture "+self.nom+" est incompatible avec ce type de combat ("+perso.posture.categorie_combat.nom+")")
		
		return T_verif