from django.db import models
from ..models import Objet_perso
from ..fonctions_base import txt_liste,manytomany_ds_manytomany

class Resultat(models.Model):
	
	active = models.BooleanField(default=True)
	
	action = models.ForeignKey('Action', on_delete=models.SET_DEFAULT, default=29 , related_name=('resultat_type'))
	priorite = models.SmallIntegerField(default=1,verbose_name="priorite : ponderation si choix aléatoire d'un resultat dans une liste (ex : rumeur)") 
	# echec : cas de competence trop faible uniquement pour "examiner"
	echec = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name=('resultat_echec'),verbose_name="echec : si echec possible (avec chance_reussite<100 ou competence trop faible), peut amener a cet autre resultat")
	#chance_reussite = models.SmallIntegerField(default=100,verbose_name="chance_reussite : si reussi --> cf texte si réussite, si raté --> cf texte")
	competence = models.ForeignKey('Competence', on_delete=models.SET_NULL, blank=True, null=True , related_name=('resultat_copetence'), verbose_name="competence : si blank, prend la compétence associée à l'action")
	valeur_competence = models.SmallIntegerField(default=0, blank=True)
	nom = models.CharField(verbose_name="Titre du resultat",max_length=30, null=True)
	description = models.TextField(verbose_name="Description MJ",default='', blank=True, null=True)
	texte = models.TextField(verbose_name="Texte",default='', blank=False, null=True)
	#texte_reussite = models.TextField(verbose_name="Texte si reussite",default='', blank=True, null=True)
	
	lieu = models.ForeignKey('Lieu', on_delete=models.SET_NULL, blank=True, null=True, related_name=('lieu_recherche'))
	cle1 = models.CharField(verbose_name="Clé 1 - ';' sépare les entités ",max_length=300, blank=True, null=True)
	cle2 = models.CharField(verbose_name="Clé 2 - ';' sépare les entités ",max_length=300, blank=True, null=True)
	cle_date = models.CharField(verbose_name="Clé Date",max_length=100, blank=True, null=True)
	obj_necessaire = models.ForeignKey('Objet', on_delete=models.SET_NULL, blank=True, null=True, related_name=('necessaire_pr_resultat'), verbose_name="obj_necessaire : sans cet objet, le resultat n'est pas trouvable")
	obj_prioritaire = models.BooleanField(default=True,verbose_name="obj_prioritaire :  si obj_necessaire : si le perso a l'objet, alors ce résultat sera prioritaire sur d'autres --> le resultat ne peut pas être répétable")
	obj_importance = models.SmallIntegerField(default=1, choices=((0,"suffisant pour avoir le résultat, mais n'est pas nécessaire"),(1,"Nécessaire pour avoir le résultat, mais n'est pas suffisant"),(2,"Nécessaire et suffisant pour avoir le résultat")))
	
	public = models.BooleanField(default=False, verbose_name="la découverte se fait par un message public")
	repetable = models.BooleanField(default=False, verbose_name="est répétable : re-découvrable une 2e fois par un joueur qui connait déjà ce résultat")
	unique = models.BooleanField(default=False, verbose_name="est unique : n'est pas re-découvrable une 2e fois même par un perso différent")
	fini = models.BooleanField(default=False, verbose_name="est unique et a déjà été découvert")
	users_connaissants = models.ManyToManyField('Joueur', blank=True, related_name = 'connaissants_resultat')
	
	passage_trouve = models.ForeignKey('Lieu', on_delete=models.SET_NULL, blank=True, null=True, related_name=('passage_trouve'))
	#objet_trouve = models.ManyToManyField('Objet', blank=True, related_name=('objet_trouve'))
	effet_recu = models.ForeignKey('Effet', on_delete=models.SET_NULL, blank=True, null=True, related_name=('effet_trouve'))
	resultat_trouve = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name=('resultat_pour_le_trouver'))
	perso_trouve = models.ForeignKey('Perso', on_delete=models.SET_NULL, blank=True, null=True, related_name=('perso_trouve'))
	attaquer_par = models.ForeignKey('Perso', on_delete=models.SET_NULL, blank=True, null=True, related_name=('attaquer_par'))
	modif_PV = models.SmallIntegerField(default=0, blank=True)
	modif_gardes = models.SmallIntegerField(default=0, blank=True)
	modif_troupes = models.SmallIntegerField(default=0, blank=True)
	add_resultat = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name=('resultat_additionnel'))
	
	commande_suivante = models.ForeignKey('Commande', on_delete=models.SET_NULL, blank=True, null=True, related_name=('commande_suivante'))
	
	possible_pour_tous = models.BooleanField(default=True, verbose_name="possible_pour_tous : si False, alors juste les joueurs ci-dessous peuvent être concerné par ce resultat")
	users_possible = models.ManyToManyField('Joueur', blank=True, related_name = 'peut_avoir_resultat') # liste des personnes qui peuvent avoir ce resultat
	
	
	def __str__(self):
		decouvertes = self.return_decouverte()
		active = ''
		if not self.active : active = '----------- '
		return active+self.lieu.nom+' - '+self.action.nom+'  -  ' +self.nom +' ---> '+decouvertes
		
		
	def save(self, *args, **kwargs):
		if self.action :
			if not self.action.appel_resultat and not self.action.cible_resultat:
				self.active = False
		if self.obj_necessaire and obj_prioritaire : self.repetable = False
		
		if self.add_resultat :
			if self.add_resultat in self.resultat_additionnel.all():self.add_resultat=None
			chance_reussite = 100
			
		if self.valeur_competence<1 : self.valeur_competence = 1
		
		if self.add_resultat : self.active=False
		if self.id and self.resultat_echec.count()>0 : self.active=False
		
		super().save()
	
	def T_decouverte(self):
		T_resultat = []
		if self.effet_recu : T_resultat.append(self.passage_trouve.nom)
		if self.passage_trouve : T_resultat.append(self.passage_trouve.nom)
		T_obj = []
		for objet in self.tresor.all() :
			T_obj.append(objet.obj.nom)
		T_resultat.append(','.join(T_obj))
		if self.perso_trouve : T_resultat.append(self.perso_trouve.nom)
		if self.modif_PV!=0 : 
			indic='+'
			if self.modif_PV<0 : indic = '-'
			T_resultat.append('PV:'+indic+str(self.modif_PV))
		if self.modif_PV!=0 : 
			indic='+'
			if self.modif_gardes<0 : indic = '-'
			T_resultat.append('Gardes:'+indic+str(self.modif_gardes))
		if self.modif_troupes!=0 : 
			indic='+'
			if self.modif_troupes<0 : indic = '-'
			T_resultat.append('Troupe:'+indic+str(self.modif_troupes))
		return T_resultat
		
	def return_decouverte(self):
		T_resultat = self.T_decouverte()
		return '-'.join(T_resultat)
		
	def return_decouverte2(self):
		T_resultat = self.T_decouverte()
		return '/n'.join(T_resultat)
	
	def return_have_key(self):
		resultat = False
		if (self.cle1 and self.cle1!='') or (self.cle2 and self.cle2!='') or (self.cle_date and self.cle_date!='') : resultat = True
		return resultat
	
	def return_objet_trouve_liste(self):
		T_obj = []
		for objet in self.objet_trouve() :
			T_obj.append(objet.obj)
		return txt_liste(self.tresor.all())
		
	def objet_trouve(self):
		return self.tresor.filter(active=True).filter(obj__active=True).all()
		
	def verif_resultat_cible(self,perso):
		T_verif = []
		
		if not self.repetable and manytomany_ds_manytomany(perso.joueur,self.users_connaissants) : T_verif.append("Le joueur connait déjà ce résultat")
		if self.unique and self.fini and not manytomany_ds_manytomany(perso.joueur,self.users_connaissants) : T_verif.append("Ce résultat a déjà été trouvé par un autre joueur")
		if not self.possible_pour_tous and not manytomany_ds_manytomany(perso.joueur,self.users_possible) : T_verif.append("Ce joueur ne peux pas trouver ce résultat")
		if perso.PV<=0 : T_verif.append("Le perso n'est plus en état pour trouver ce résultat")
		if not self.echec and self.action.nom_info!="examiner" :
			T_reussite = self.verif_reussite_resultat(perso)
			if len(T_reussite) >0 : T_verif.append("Une réussite (competence et/ou objet nécessaire) est nécessaire pour avoir ce résultat")
		
		return T_verif
		
	def verif_reussite_resultat(self,perso):
		T_verif = []
		
		if self.obj_necessaire and self.obj_importance!=0 and not perso.a_type_objet(self.obj_necessaire) : T_verif.append("Pour trouver ce résultat, il faut un certain type d'objet que le perso ne possède pas")
		if self.competence and self.valeur_competence>perso.valeur_competence(self.competence) : 
			echec_competence = True
			if self.obj_necessaire and self.obj_importance!=1 and perso.a_type_objet(self.obj_necessaire) : echec_competence = False
			if echec_competence : T_verif.append("Pour trouver ce résultat, le perso doit avoir au moins "+str(self.valeur_competence)+" dans la compétence "+self.competence.nom)
		
		return T_verif
		
		
	def get_users_connaissants(self):
		T=[]
		for j in self.users_connaissants.all():T.append(j.nom)
		if len(T)>0 : T[-1]='et '+T[-1]
		txt = ", ".join(T)
		return txt
		
	def echec_utile(self):
		resultat=False
		if self.competence and self.valeur_competence>0 : resultat=True
		if self.obj_necessaire and self.obj_importance !=0 : resultat=True
		return resultat
		
	def one_resultat_possible(self):
		resultat = False
		if self.action.nom_info=='examiner' : resultat = True
		return resultat
	
	def get_resultat_additionnel(self):
		return self.resultat_additionnel.filter(active=False).filter(fini=False).all()
		
	def trouve_obj(self,obj):
		etat = 1
		if obj.reparable : etat = 2
		
		o = Objet_perso.objects.create(\
		resultat = self, \
		obj = obj, \
		etat=etat)