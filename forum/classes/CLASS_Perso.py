from math import ceil,floor
from django.db import models
from django.utils import timezone
from django.db.models import Q
from ..models import Jeu, Sante, Competence, Charge, Posture, Commande, Objet_perso, Effet_perso, Categorie_competence, Langage
from datetime import timedelta

from ..fonctions_base import *

class Perso(models.Model):
	
	active = models.BooleanField(default=True)
	joueur = models.ManyToManyField('Joueur', blank=True, related_name='persos')
	nom = models.CharField(max_length=30)
	nom_origine = models.CharField(max_length=30, null=True, blank=True)
	genre = models.BooleanField(verbose_name='Le personnage est un homme ?', default=True)
	espece = models.ForeignKey('Espece', default=1, null=True, on_delete=models.SET_NULL, related_name=('espece'))
	maison = models.ForeignKey('Maison', null=True, blank=True, on_delete=models.SET_NULL, related_name='persos_maison')
	rejete = models.BooleanField(default=False,verbose_name="rejete : Est il rejeté de sa maison ?")
	titre = models.CharField(max_length=50, default='', blank=True)
	charge = models.ForeignKey('Charge', null=True, blank=True, on_delete=models.SET_NULL, related_name='perso_charge')
	description = models.TextField(default='', blank=True, null=True)
	background = models.TextField(default='', blank=True, null=True)
	nom_info = models.CharField(max_length=40, default='perso_none')
	
	priorite =  models.SmallIntegerField(default=1)
	priorite_temp = models.SmallIntegerField(default=1)
	hote = models.ForeignKey('Lieu', null=True, on_delete=models.CASCADE, blank=True, related_name = 'hote')
	
	lieu = models.ForeignKey('Lieu', null=True, blank=True, on_delete=models.SET_NULL, related_name=('persos_presents'))
	secteur = models.SmallIntegerField(default=1)
	
	occupe =  models.ForeignKey('Commande', null=True, blank=True, on_delete=models.SET_NULL, related_name=('commande_perso'))
	last_commande = models.ForeignKey('Commande', null=True, blank=True, on_delete=models.SET_NULL, related_name=('last_commande_perso'))
	desc_occupe = models.TextField(default='', blank=True)
	
	vivant = models.BooleanField(default=True)
	prisonnier = models.BooleanField(default=False)
	en_combat = models.BooleanField(default=False)
	en_soin = models.BooleanField(default=False)
	en_fuite = models.BooleanField(default=False)
	
	geolier = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, blank=True, verbose_name='De qui le perso est prisonnier', related_name=('perso_prisonnier')) #
	leader = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, blank=True, verbose_name='Qui le perso est en train de suivre', related_name=('perso_accompagne')) #
	ds_groupe_temporaire = models.BooleanField(default=False)
	espionne = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, blank=True, verbose_name="Qui le perso est en train d'espionner", related_name=('espions'))
	
	protection = models.SmallIntegerField(default=2)
	defense = models.SmallIntegerField(default=4)
	aura = models.SmallIntegerField(default=0)
	PC = models.SmallIntegerField(default=0)			# Pt de concentration
	#PA_MAX = models.PositiveIntegerField(default=0) 	# Pt d'Armure
	PA = models.SmallIntegerField(default=0)
	PE_MAX = models.PositiveIntegerField(default=0) 	# Pt d'Esquive
	PE = models.PositiveIntegerField(default=0) 
	PV_MAX = models.PositiveIntegerField(default=3)		# Pt de vie
	PV = models.SmallIntegerField(default=3)
	etat_sante = models.ForeignKey('Sante', null=True, on_delete=models.SET_NULL, default=1)
	#situation = models.CharField(max_length=30,choices=(('','RAS'),('Accompagnant','Accompagnant'),('Prisonnier(e)','Prisonnier(e)'),('En situation de combat','En situation de combat')), default= '', blank=True)
	dissimulation = models.SmallIntegerField(default=0)
	joueur_repere = models.ManyToManyField('Joueur', blank=True, related_name = 'joueur_repere')

	#perso_accompagnants = models.ManyToManyField('self', blank=True)
	nbGardes = models.SmallIntegerField(default=0)
	#nbGardes_MAX = models.SmallIntegerField(default=0)
	nbTroupes = models.SmallIntegerField(default=0)
	#nbTroupes_MAX = models.SmallIntegerField(default=0)
	gardes_MAX = models.SmallIntegerField(default=0)
	troupes_MAX = models.SmallIntegerField(default=0)
	accompagnants_MAX = models.SmallIntegerField(default=0)
	
	#etat d'esprit
	persos_deja_provoques = models.ManyToManyField('self', related_name="persos_qui_a_provoque", blank=True)
	accepte_duel = models.BooleanField(default=False)
	comportement_intervention = models.ForeignKey('Comportement_intervention', default=1, on_delete=models.SET_DEFAULT)
	
	volume_MAX = models.SmallIntegerField(default=5)
	
	classe_principale = models.ForeignKey('Categorie_competence', null=True, on_delete=models.SET_NULL, related_name=('classe_principale'), default=1)
	classe_secondaire = models.ForeignKey('Categorie_competence', null=True, on_delete=models.SET_NULL, related_name=('classe_secondaire'), default=2)
	comp_niv1 = models.ManyToManyField('Competence', related_name="comp_niv1", blank=True)
	comp_niv2 = models.ManyToManyField('Competence', related_name="comp_niv2", blank=True)
	comp_niv3 = models.ManyToManyField('Competence', related_name="comp_niv3", blank=True)
	comp_niv4 = models.ManyToManyField('Competence', related_name="comp_niv4", blank=True)
	langage = models.ManyToManyField('Langage', related_name="langage_persos", blank=True,verbose_name="langage : Langages connus en plus du commun")
	
	posture = models.ForeignKey('Posture', null=True, blank=True, on_delete=models.SET_NULL, related_name=('posture_perso'))
	posture_defaut_duel = models.ForeignKey('Posture', on_delete=models.SET_DEFAULT, related_name=('posture_def_duel'), default=8)
	posture_defaut_melee = models.ForeignKey('Posture', on_delete=models.SET_DEFAULT, related_name=('posture_def_melee'), default=6)
	
	doppelganger = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, blank=True, verbose_name='doppelganger : Si Doppelganger, copie du perso original', related_name=('perso_original')) #
	#info_signature = models.TextField(default='', blank=True, null=True)

	def __str__(self):
		resultat = self.get_nom()
		if self.hote : resultat = self.get_nom()+' ('+self.hote.nom+')'
		return resultat

	def save(self, *args, **kwargs):
		#print(self.nom)
		
		#doppelganger
		if self.doppelganger :
			if not self.effets().filter(eft__nom="doppelganger").filter(commence=True).filter(fini=False).exists() : self.doppelganger = None
		if self.doppelganger and self.nom_origine and self.nom != self.doppelganger.nom : self.nom = self.doppelganger.nom
		
		self.priorite_temp = self.get_priorite()
		if not self.id: self.nom_origine = self.nom
		elif not self.doppelganger and self.nom_origine and self.nom!=self.nom_origine : self.nom=self.nom_origine
		
		#
		
		PA_MAX = self.PA_MAX()
		self.gardes_MAX = self.get_gardes_MAX()
		self.troupes_MAX = self.get_troupes_MAX()
		self.accompagnants_MAX = self.get_accompagnants_MAX()
		
		if self.PC<0 : self.PC=0
		if self.PV<0 and self.vivant :  self.PV = 0
		if not self.vivant :  self.PV = -1
		if self.PV >=0 : self.vivant = True
		if self.PV > self.PV_MAX : self.PV = self.PV_MAX
		if self.PA < 0 : self.PA=0
		if self.PA > PA_MAX : self.PVA = PVA_MAX
		if self.PC < 0 : self.PC=0
		if self.nbGardes > self.gardes_MAX : self.nbGardes = self.gardes_MAX
		if self.nbGardes < 0 : self.nbGardes = 0
		if self.nbTroupes > self.troupes_MAX : self.nbTroupes = self.troupes_MAX
		if self.nbTroupes < 0 : self.nbTroupes = 0
		
		if self.hote : self.lieu = self.hote
		
		if self.PV<=0 :
			if self.occupe_id and self.occupe.perso == self :
				self.occupe.erreur = True
				self.occupe.desc = self.get_nom() +" ne peut plus réaliser l'action car il est inconscient ou mort"
				self.occupe.save()
				self.occupe = None
			self.en_combat = False
			
			for accompagnant in self.perso_accompagne.all():
				accompagnant.leader=None
				accompagnant.save()
				
			if self.hote :
				self.nbGardes = 0
				self.nbTroupes = 0
		
		self.etat_sante = Sante.objects.get(PV = self.PV)
		
		#espionne
		if self.occupe and self.occupe.action.nom_info == 'espionner':
			if not self.espionne : self.espionne = self.occupe.persos_cible.all()[0]
		elif self.espionne : self.espionne = None
		
		#secteur
		if self.lieu :
			if self.secteur<1 or self.secteur>self.lieu.taille : self.secteur = de(self.lieu.taille)
		
		#Charge :
		if self.maison and self.maison.senateur and self.maison.senateur==self and not self.rejete == self : self.charge = Charge.objects.get(nom_info="senateur")
		elif self.charge and self.charge.nom_info == 'senateur' : self.charge = None
		
		comp_senateur = Competence.objects.get(nom_info='senateur')
		if self.charge :
			if self.genre : self.titre = self.charge.nom
			else : self.titre = self.charge.nom_F
			if self.charge.nom_info == 'senateur' and not self.a_competence(comp_senateur) : self.modifie_competence(comp_senateur,1)
			elif self.charge.nom_info != 'senateur' and self.a_competence(comp_senateur) : self.modifie_competence(comp_senateur,0)
		else :
			if self.a_competence(comp_senateur) : self.modifie_competence(comp_senateur,0)
			if self.titre != '':
				for charge in Charge.objects.filter(active=True):
					if self.titre == charge.nom or self.titre == charge.nom_F : 
						self.titre=''
						break
		
		#liberation de prisonnier ou des suiveurs
		if self.PV<=0 or self.en_fuite or self.prisonnier or not self.vivant :
			qst_prisonniers = Perso.objects.filter(geolier=self)
			for prisonnier in qst_prisonniers :
				prisonnier.geolier = None
				prisonnier.prisonnier = False
				prisonnier.save()
				
			qst_suiveurs = Perso.objects.filter(leader=self)
			for suiveur in qst_suiveurs :
				suiveur.leader = None
				suiveur.save()
		
		
		if self.occupe_id : self.last_commande = self.occupe
		if self.occupe_id and self.occupe.fini : self.occupe = None
		if not self.occupe_id : 
			self.en_soin = False
			self.en_combat = False
			self.en_fuite = False
			self.posture = None
		
		if self.occupe_id and not self.occupe.action.est_combat :
			self.en_combat = False
			self.posture = None
		
		'''if self.dissimulation == 0 : 
			self.joueur_repere.clear()
			self.en_fuite = False'''
		
		'''if self.dissimulation > 0 :
			comp_dissimulation = Competence.objects.get(nom_info='dissimulation')
			if comp_dissimulation :
				valeur_dissimulation = self.valeur_competence(comp_dissimulation)
				if self.lieu.dissimulation == 0 :
					if self.dissimulation>=10 :
						self.dissimulation = valeur_dissimulation
				else : 
					self.dissimulation = valeur_dissimulation + 10'''
				
		if self.leader_id :
			save_leader = False
			if self.leader.dissimulation != 0:
				self.leader.dissimulation = 0
				save_leader = True
			if self.nbTroupes>0 and self.leader.nbTroupes<=0 :
				self.nbTroupes = self.nbTroupes-1
				self.leader.nbTroupes = 1
				save_leader = True
				
			if self.leader.en_combat : self.en_combat = True
			else : self.en_combat = False
			if self.leader.en_fuite or self.leader.PV<=0 or self.leader.prisonnier : self.leader = None
			
			if self.leader.lieu == self.lieu and self.leader.secteur == self.secteur :
				if self.occupe and self.occupe.action.nom_info=='sedeplacer_suivre' :
					if not self.leader.occupe or (self.leader.occupe and not self.leader.occupe.action.est_deplacement and self.leader.occupe.lieux_cible.all()[0]!=self.occupe.lieux_cible.all()[0]):
						self.occupe.delete()
						self.occupe=None
						self.last_commande = None
			else :
				if self.occupe_id and self.occupe.action.nom_info == "sedeplacer_suivre" and self.occupe.lieux_cible.all()[0] == leader.lieu and self.occupe.persos_cible.all()[0] == self.leader : a=0
				elif (not self.occupe_id) and self.last_commande.action.nom_info == "sedeplacer_suivre" and self.last_commande.lieux_cible.all()[0] == self.leader.lieu and self.last_commande.persos_cible.all()[0] == self.leader : a=0
				else : self.leader = None
				
			
			if save_leader : self.leader.save()
			
			
		else : self.ds_groupe_temporaire = False
			
		if self.geolier_id :
			if self.geolier.dissimulation != 0:
				self.geolier.dissimulation = 0
				self.geolier.save()
			self.prisonnier = True
		else :
			self.prisonnier = False
		
		if self.id and self.lieu and self.lieu.inconnu : 
			for j in self.joueur.all():
				if not objet_ds_manytomany(j,self.lieu.users_connaissants) :
					self.lieu.users_connaissants.add(j)
					if not objet_ds_manytomany(j,self.lieu.users_connaissants_place) :
						self.lieu.users_connaissants_place.add(j)
					self.lieu.save()
		
		qst_prisonniers = Perso.objects.filter(geolier__isnull=False).filter(geolier__id=self.id)
		qst_accompagnants = Perso.objects.filter(leader__isnull=False).filter(leader__id=self.id)
		
		for accompagnant in qst_accompagnants :
			save_accompagnant = False
			if accompagnant.nbTroupes>=0 and self.nbTroupes<=0 :
				accompagnant.nbTroupes = accompagnant.nbTroupes-1
				self.nbTroupes = 1
				save_accompagnant = True
			if accompagnant.lieu != self.lieu or accompagnant.secteur != self.secteur :
				if accompagnant.occupe_id and accompagnant.occupe.action.nom_info == "sedeplacer_suivre" and accompagnant.occupe.lieux_cible.all()[0] == self.lieu and accompagnant.occupe.persos_cible.all()[0] == self : a=0
				else : 
					accompagnant.leader=None
					save_accompagnant = True
			if save_accompagnant : accompagnant.save()
					
					
		for prisonnier in qst_prisonniers :
			if prisonnier.lieu != self.lieu or prisonnier.secteur != self.secteur:
				prisonnier.lieu = self.lieu
				prisonnier.secteur = self.secteur
				prisonnier.save()
		
		info_signature = ''
		T_elts_accompagne = []
		if self.nbGardes>0 : T_elts_accompagne.append("est escorté par "+str(self.nbGardes)+" gardes")
		if self.nbTroupes>0 : T_elts_accompagne.append("mène "+str(self.nbGardes)+" troupes")
		if qst_accompagnants : T_elts_accompagne.append("est accompagné par "+txt_liste(qst_accompagnants))
		if len(T_elts_accompagne)>0 :
			info_signature = info_signature + self.get_nom() +" "+("\n."+pronom(self.genre).capitalize()+" ").join(T_elts_accompagne)
		self.info_signature = info_signature
		
		if self.occupe_id :
			if self != self.occupe.perso and self.occupe.action.desc2!='' and self.occupe.persos_cible : 
				texte = self.occupe.action.desc2
				if self.occupe.perso.dissimulation>0 : texte = texte.replace('#perso#','Inconnu')
			else :
				texte = self.occupe.action.desc
			self.desc_occupe = traduction_msg(texte,self.occupe)
		
		if not self.en_combat and (not self.leader or not self.leader.en_combat) and self.PA<PA_MAX : self.PA = PA_MAX
		
		#print('#######2 : '+str(timezone.now()))
		super().save()
		print("############# SAVE PERSO "+self.nom+" - "+str(timezone.now()))
	
	
	
	def get_nom(self):
		resultat = self.nom
		if self.doppelganger : resultat = self.doppelganger.nom
		return resultat
		
	def get_nom_info(self):
		resultat = self.nom_info
		if self.doppelganger : resultat = self.doppelganger.nom_info
		return resultat
	
	def get_genre(self):
		resultat = self.genre
		if self.doppelganger : resultat = self.doppelganger.genre
		return resultat
		
	def get_maison(self):
		resultat = self.maison
		if self.doppelganger : resultat = self.doppelganger.maison
		return resultat
		
	def get_priorite(self):
		perso = self
		if self.doppelganger : perso = self.doppelganger
		if perso.maison : priorite_maison = (perso.maison.priorite)*100
		else : priorite_maison = 0
		resultat = perso.priorite + priorite_maison
		return resultat
		
	def get_titre(self):
		resultat = self.titre
		if self.doppelganger : resultat = self.doppelganger.titre
		return resultat
		
	def get_charge(self):
		resultat = self.charge
		if self.doppelganger : resultat = self.doppelganger.charge
		return resultat
		
	def get_description(self):
		resultat = self.description
		if self.doppelganger : resultat = self.doppelganger.description
		return resultat
	
	def get_classe_principale(self):
		resultat = self.classe_principale
		if self.doppelganger : resultat = self.doppelganger.classe_principale
		return resultat
		
	def get_classe_secondaire(self):
		resultat = self.classe_secondaire
		if self.doppelganger : resultat = self.doppelganger.classe_secondaire
		return resultat
		
	def get_classe_tertiaire(self):
		classe_principale = self.get_classe_principale()
		classe_secondaire = self.get_classe_secondaire()
		resultat = Categorie_competence.objects.exclude(id=classe_principale.id).exclude(id=classe_secondaire.id).all()[0]
		return resultat
		
	def get_liste_competence3(self):
		perso = self
		if self.doppelganger : perso = self.doppelganger
		T_resultat = []
		for c in perso.comp_niv3.all() : T_resultat.append(c)
		for c in perso.comp_niv4.all() : T_resultat.append(c)
		return T_resultat
	
	def get_aura(self):
		perso = self
		if self.doppelganger : perso = self.doppelganger
		competence = Competence.objects.filter(nom_info="aura").all()[0]
		resultat = perso.valeur_competence(competence)
		return resultat
	
	def signature(self):
		info_signature = ''
		T_elts_accompagne = []
		nb_gardes = self.NB_GARDES_GROUPE()
		nb_troupe = self.NB_TROUPES_GROUPE()
		qst_accompagnants = self.perso_accompagne.all()
		
		if nb_gardes>0 : T_elts_accompagne.append("est escorté par "+str(nb_gardes)+" gardes")
		if nb_troupe>0 : T_elts_accompagne.append("mène "+str(nb_troupe)+" troupes")
		if qst_accompagnants : T_elts_accompagne.append("est accompagné par "+txt_liste(qst_accompagnants))
		if len(T_elts_accompagne)>0 :
			info_signature = info_signature + self.get_nom() +" "+(".\n"+pronom(self.genre).capitalize()+" ").join(T_elts_accompagne)+'.'
		return info_signature
	
	def listejoueur(self):
		T_resultat = []
		T_joueur = self.joueur.all()
		for joueur in T_joueur :
			T_resultat.append(joueur.nom)
		return ', '.join(T_resultat)
	
	def image(self):
		
		nom_img = self.get_nom_info()
		resultat = 'persos/'+nom_img
		
		if resultat[-4:]!='.jpg': resultat = resultat+'.jpg'
		if self.hote and (nom_img == 'perso_none' or nom_img == self.hote.image) : 
			resultat = 'lieu/'+self.hote.image
			if resultat[-4:]!='.jpg': resultat = resultat+'.jpg'
		return resultat
	
	def nom_sous_image(self):
		indic = ''
		if self.dissimulation>0 : indic = ' (caché)'
		elif self.geolier : indic = ' (prisonnier)'
		elif self.leader : indic = ' (accompagne - '+self.leader.get_nom()+')'
		resultat = self.get_nom()+indic+' - '+self.etat_sante.nom
		if self.hote : resultat = self.hote.nom +' '+indic+ ' - ' +self.get_nom()
		return resultat
	
	def objets(self):
		qst_objets = self.objet.filter(active=True).exclude(etat=0)
		return qst_objets
		
	def a_objet(self,objet):
		resultat = False
		qst_obj = self.objets().filter(id=objet.id)
		if len(qst_obj)>0 : resultat = True
		return resultat
		
	def a_type_objet(self,obj):
		resultat = False
		qst_obj = self.objets().filter(obj=obj)
		if len(qst_obj)>0 : resultat = True
		return resultat
		
	def cb_type_objet(self,obj):
		qst_obj = self.objets().filter(obj=obj)
		resultat = 0
		if obj.cumulable :
			if len(qst_obj)==0 : resultat = -1
			else :
				for o in qst_obj :
					resultat = resultat+o.etat
		else :
			for o in qst_obj : resultat = resultat+1
		
		return resultat
	
	def trouve_obj(self,obj):
		etat = 1
		if obj.reparable : etat = 2
		
		o = Objet_perso.objects.create(\
		perso = self, \
		obj = obj, \
		etat=etat)
	
	def prend_effet(self,eft):
		
		if eft.support=="perso" :
			#evite le cumule de differents effets du meme type
			valide=True
			
			if eft.classe == '': 
				for effet in self.effets().filter(eft=eft):
					if effet.eft.priorite() <= eft.priorite() and effet.eft.priorite()<100 : 
						effet.fini=True
						effet.save()
					else : valide = False
					
			if eft.classe != '':
				for effet in self.effets().filter(eft__classe=eft.classe):
					if effet.eft.priorite() <= eft.priorite() : 
						effet.fini=True
						effet.save()
					else : valide = False
					
			if valide :
				e = Effet_perso.objects.create(\
				perso = self, \
				eft = eft, \
				infini=True)
				print(e)
				return e
			else : return False
			
		elif eft.support=="amure" :
			armure = self.armure()
			if armure : return armure.prend_effet(eft)
			else : return False
			
		elif eft.support=="ame" :
			arme = self.arme()
			if arme : return arme.prend_effet(eft)
			else : return False
	
	def arme(self):
		resultat = None
		qst_arme = self.objets().filter(obj__classe='arme').filter(porte=True).exclude(etat=1)
		if len(qst_arme)>0 : 
			arme_possede = qst_arme.all()[0]
			resultat = arme_possede
		return resultat
		
	def armure(self):
		resultat = None
		qst_armure = self.objets().filter(obj__classe='armure').filter(porte=True).exclude(etat=1).all()
		if len(qst_armure)>0 : 
			armure_possede = qst_armure.all()[0]
			resultat = armure_possede
		return resultat
	
	
	def PA_MAX(self):
		resultat = 0
		if self.armure() : 
			resultat = self.armure().armure_valeur1()
			
		T_effets = self.effets()
		for effet in T_effets :
			resultat = resultat + (effet.eft.bonus_PA*effet.valeur)
				
		return resultat
		
	def NIV_PROTECTION(self):
		resultat = self.protection + self.valeur_protection_bonus()
		if self.armure() : resultat = resultat + self.armure().obj.valeur2
		return resultat
		
	def BONUS_DENOMINATEUR_DOMMAGE(self):
		resultat = self.defense + self.valeur_defense_bonus()
		if self.armure() : resultat = resultat + self.armure().obj.valeur3
		return resultat
	
	def valeur_competence_brut(self,competence):
		valeur=0
		if self.id:
			if objet_ds_manytomany(competence,self.comp_niv4) : valeur=4
			elif objet_ds_manytomany(competence,self.comp_niv3) : valeur=3
			elif objet_ds_manytomany(competence,self.comp_niv2) : valeur=2
			elif objet_ds_manytomany(competence,self.comp_niv1) : valeur=1
				
		#print(competence.nom+'-'+str(valeur))
		return valeur
	
	def effets(self):
		#now = timezone.now()
		return self.effet_perso.filter(eft__active=True).filter(fini=False).filter(commence=True).filter(eft__support='perso').all()
	
	def T_all_effets(self):
		now = timezone.now()
		arme = self.arme()
		armure = self.armure()
		T_effets = []
		for e in self.effet_perso.filter(fini=False).filter(commence=True).filter(date_debut__lt=now).filter(date_fin__gt=now).filter(eft__support='perso').all() : T_effets.append(e)
		if arme :
			for e in arme.effet_objet.filter(fini=False).filter(commence=True).filter(date_debut__lt=now).filter(date_fin__gt=now).filter(eft__support='arme').all() : T_effets.append(e)
		if armure :
			for e in armure.effet_objet.filter(fini=False).filter(commence=True).filter(date_debut__lt=now).filter(date_fin__gt=now).filter(eft__support='armure').all() : T_effets.append(e)
		# les objets portes par le perso qui peuvent avoir des effets
		for o in self.objets().filter(porte=True).filter(obj__classe='artefact').filter(obj__effet_si_porte=True).exclude(obj__effet=None).all() : 
			T_e = o.effet_objet.filter(fini=False).filter(commence=True).filter(date_debut__lt=now).filter(date_fin__gt=now).all()
			for e in T_e :
				if not e in T_effets : T_effets.append(e)
			
		return T_effets
	
	def valeur_competence_bonus(self,competence):
		
		T_effets = self.T_all_effets()
		valeur = 0
		for effet in T_effets :
			if effet.eft.competence_bonifie and effet.eft.competence_bonifie == competence :
				valeur = valeur + (effet.eft.val_competence_bonifie*effet.valeur)
		
		return valeur
		
	def valeur_combat_bonus(self):

		T_effets = self.effets()
		valeur = 0
		for effet in T_effets :
			valeur = valeur + (effet.eft.bonus_combat*effet.valeur)
			
		return valeur
		
	def valeur_protection_bonus(self):

		T_effets = self.effets()
		valeur = 0
		for effet in T_effets :
			valeur = valeur + (effet.eft.bonus_protection*effet.valeur)
			
		return valeur
		
	def valeur_defense_bonus(self):

		T_effets = self.effets()
		valeur = 0
		for effet in T_effets :
			valeur = valeur + (effet.eft.bonus_defense*effet.valeur)
			
		return valeur
	
	
	def valeur_dommage_bonus(self):

		T_effets = self.effets()
		valeur = 0
		for effet in T_effets :
			valeur = valeur + (effet.eft.bonus_dommage*effet.valeur)
			
		return valeur
	
	def valeur_competence_str(self,competence_nom_info):
		valeur = False
		competence = Competence.objects.get(nom_info = competence_nom_info)
		if competence : valeur = self.valeur_competence(competence)
		return valeur
		
	
	def valeur_competence(self,competence):
		valeur = self.valeur_competence_brut(competence)
		valeur = valeur + self.valeur_competence_bonus(competence)
				
		#print(competence.nom+'-'+str(valeur))
		return valeur
		
	def a_competence(self,competence):
		val_comp = self.valeur_competence(competence)
		if val_comp>0 : return True
		else : return False
	
	def modifie_competence(self,competence,valeur):
		T_valeurCompetence = [self.comp_niv1,self.comp_niv2,self.comp_niv3,self.comp_niv4]
		a=0
		while a<len(T_valeurCompetence):
			if valeur == a+1 : T_valeurCompetence[a].add(competence)
			else : T_valeurCompetence[a].remove(competence)
			a=a+1
	
	
	def sortie_competence(self):
		qst_competence = Competence.objects.filter(active=True).order_by('categorie_classement__priorite','priorite')
		T_categorie = []
		for competence in qst_competence :
			if not competence.categorie_classement in T_categorie : T_categorie.append(competence.categorie_classement)
		
		TTT_resultat = []
		a=0
		for categorie in T_categorie:
			if categorie : nom_categorie = categorie.nom
			else : nom_categorie=''
			TTT_resultat.append([nom_categorie,[]])
			for competence in qst_competence :
				if categorie == competence.categorie_classement :
					TTT_resultat[a][1].append([competence,self.valeur_competence_brut(competence),self.valeur_competence_bonus(competence)])
			a=a+1
		return TTT_resultat
		#[ ["COMBAT",[["Officier",0,bonus],["Melee","2",bonus],["Escrime","1",bonus]]] , [] .... ]
	
	def valeur_concentration(self):
		competence = Competence.objects.get(nom_info="concentration")
		return self.valeur_competence(competence)
	
	def get_langage(self):
		if self.id == 1 : 
			T_resultat = Langage.objects.filter(active=True).exclude(id=1).all()
		else :
			T_resultat = self.langage.filter(active=True).exclude(id=1).all()
		return T_resultat.order_by('priorite')
	
	
	def get_langage_parle(self):
		qst_langage = self.get_langage()
		if self.id == 1 : return qst_langage
		else : return qst_langage.filter(est_parle=True).all()
	
	def connait_langage(self,langage):
		resultat = False
		if langage in self.langage.all(): resultat = True
		return resultat
	
	def VALEUR_DUEL_brut(self):
		val_competence_duel = self.valeur_competence(Competence.objects.get(nom_info='duel'))
		return val_competence_duel*2
		
	def VALEUR_MELEE_brut(self):
		val_competence_melee = self.valeur_competence(Competence.objects.get(nom_info='melee'))
		return val_competence_melee*2
		
	def VALEUR_ARME_MELEE(self):
		val_arme = 0
		arme = self.arme()
		if arme : val_arme = (arme.arme_valeur1() + arme.obj.valeur2)
		return val_arme
		
	def VALEUR_ARME_DUEL(self):
		val_arme = 0
		arme = self.arme()		
		if arme : val_arme = arme.arme_valeur1()
		return val_arme
	
	def VALEUR_FRAPPE_MELEE_GROUPE(self):
		valeur = self.VALEUR_FRAPPE_MELEE()
		
		comp_officier = Competence.objects.get(nom_info='officier')
		val_officier = self.valeur_competence(comp_officier)
		max_accompagnant_au_combat = val_officier+2
		
		nb_accompagnants = 0
		for accompagnant in self.perso_accompagne.order_by("?").all():
			if accompagnant.PV>0 :
				nb_accompagnants = nb_accompagnants +1
				if nb_accompagnants > max_accompagnant_au_combat : break
				else : valeur = valeur + accompagnant.VALEUR_FRAPPE_MELEE()
		return valeur
			
	
	def VALEUR_FRAPPE_MELEE(self):
		#val_competence_duel = self.valeur_competence(Competence.objects.get(nom_info='duel'))
		val_competence_melee = self.VALEUR_MELEE_brut()
		bonus_garde = self.nbGardes
		val_arme = self.VALEUR_ARME_MELEE()
		bonus_effet_objet = self.valeur_combat_bonus()
		
		return val_competence_melee + bonus_garde + val_arme + bonus_effet_objet
		
		
	def VALEUR_FRAPPE_DUEL(self):
		val_competence_duel = self.VALEUR_DUEL_brut()
		val_arme = self.VALEUR_ARME_DUEL()
		bonus_effet_objet = self.valeur_combat_bonus()
		malus_blesse = 0
		if self.PV==1 and self.PV_MAX>=2 : malus_blesse = -2
		
		return val_competence_duel + val_arme + malus_blesse + bonus_effet_objet
		
	def VALEUR_FRAPPE_BATAILLE(self):
		val_competence_strategie = self.valeur_competence(Competence.objects.get(nom_info='strategie'))	
		return val_competence_strategie*2
	
	def MALUS_DENOMINATEUR_DOMMAGE(self):
		resultat = 0 + self.valeur_dommage_bonus()
		if self.arme() : resultat = resultat + self.arme().obj.valeur3
		return resultat
	
	def NB_TROUPES_GROUPE(self):
		valeur = self.nbTroupes
		
		max_accompagnant_au_combat = self.accompagnants_MAX
		
		nb_accompagnants = 0
		for accompagnant in self.perso_accompagne.all():
			if accompagnant.PV>0 and accompagnant.nbTroupes>0 :
				nb_accompagnants = nb_accompagnants + 1
				if nb_accompagnants > max_accompagnant_au_combat : break
				else : valeur = valeur + accompagnant.nbTroupes
		return valeur
		
	def NB_GARDES_GROUPE(self):
		valeur = self.nbGardes
		
		max_accompagnant_au_combat = 2#self.accompagnants_MAX
		
		nb_accompagnants = 0
		for accompagnant in self.perso_accompagne.all():
			if accompagnant.PV>0 and accompagnant.nbGardes>0 :
				nb_accompagnants = nb_accompagnants + 1
				if nb_accompagnants > max_accompagnant_au_combat : break
				else : valeur = valeur + accompagnant.nbGardes
		return valeur
	
	def BONUS_POSTURE(self,adversaire):
		valeur_posture = 0
		if self.posture :
			if adversaire.posture and adversaire.posture.posture_neutralise != self.posture :
				
				valeur_posture = self.posture.bonus + self.valeur_competence(self.posture.commpetence_bonus)*self.posture.multiplie_comp_bonus
				
				if self.posture.nom_info=="defense_lieu" and self.hote==self.lieu :
					valeur_posture = valeur_posture + self.lieu.defense_assault
				
				if self.posture.nom_info=="backstab" and self.valeur_competence(self.posture.commpetence_bonus)>1 : 
					valeur_posture = valeur_posture + adversaire.nbGardes
			
		return valeur_posture
	
	def DETECTION_BACKSTAB(self,adversaire):
		if adversaire.posture and adversaire.posture.nom_info == "backstab" :
			comp_backstab = Competence.objects.get(nom_info=='embuscade')
			comp_detection = Competence.objects.get(nom_info=='detection')
			
			valeur_detection = self.valeur_competence(comp_detection)
			for accompagnant in self.perso_accompagne.all():
				val_detection_accompagnant = accompagnant.valeur_competence(comp_detection)
				if valeur_detection<val_detection_accompagnant : valeur_detection=val_detection_accompagnant
			
			#Detection du Backstab --> le perso perd sa posture speciale
			if not (adversaire.valeur_competence(comp_backstab) - valeur_detection)*2+de(10)>6 :
				adversaire.posture = Posture.objects.get(nom_info=='combat')
				adversaire.save()
	
	def ENCAISSE_GROUPE(self,n,special):
		nb_accompagnant = len(self.perso_accompagne.all())
		# Le Perso Leader ne sera jamais touche tant qu'il a des accompagnants
		if nb_accompagnant==0 : self.ENCAISSE(n,special)
		else :
			if 'cible' in special : self.ENCAISSE(n,special)
			else :
				jet = de(nb_accompagnant)
				self.perso_accompagne.all()[jet].ENCAISSE(n,special)
	
		
	
	def ENCAISSE(self,dommage,special):
		
		init_nbGardes = self.nbGardes
		init_PE = self.PE
		init_PV = self.PV
		init_PA = self.PA

		niv_protection = self.NIV_PROTECTION()
		
		T_phrase = []
		
		if dommage>0 or self.dissimulation>0 :
			n = dommage
			self.dissimulation = 0
			if self.posture and self.posture.nom_info == 'backstab':
				self.posture = Posture.objects.get(nom_info='combat')
			
			if 'feu' in special : n = n*2  
			
			if self.nbGardes >= n and not'cible' in special : 
				self.nbGardes = self.nbGardes-n
			else :
				
				if not 'cible' in special :
					n = n-self.nbGardes
					self.nbGardes = 0
				
				if 'feu' in special : n = int(math.ceil(float(n/2)))
				
				if self.PE >= n : self.PE = self.PE-n
				else :
					n = n-self.PE
					self.PE = 0
					
					if 'perforant' in special : n = n*2
					
					if self.PA >= n and not 'sans_armure' in special : self.PA = self.PA-n
					else :
						if not 'sans_armure' in special :
							n = n-self.PA
							self.PA = 0
						
						if 'perforant' in special : n = int(math.ceil(float(n/2)))
						
						
						self.PV = self.PV-int(math.ceil(float(n/niv_protection)))							
							
						if 'poison' in special : self.PV = 0
							
						if self.PV<0 : self.PV = 0
			
			phrase = ''
			
			if init_nbGardes != self.nbGardes : T_phrase.append(str(init_nbGardes-self.nbGardes)+" garde(s)")
			if init_PE != self.PE : T_phrase.append(str(init_PE-self.PE)+" Point(s) d'Esquive")
			if init_PA != self.PA : T_phrase.append(str(init_PA-self.PA)+" Point(s) d'Armure")
			if init_PV != self.PV : T_phrase.append(str(init_PV-self.PV)+" Point(s) de Vie")
			
			if len(T_phrase)>0 :
				if len(T_phrase)==1 : et = ''
				else : et = ' et '
				phrase = self.get_nom()+" perd "+', '.join(T_phrase[:-1])+ et +T_phrase[-1]
			
			
			self.save()
			
			return phrase
	
	
	def ENCAISSE_TROUPE_GROUPE(self,n):
		nb_accompagnant = len(self.perso_accompagne.all())
		# Le Perso Leader ne sera jamais touche tant qu'il a des accompagnants
		if nb_accompagnant==0 : self.ENCAISSE_TROUPE(n,special)
		else :
			jet = de(nb_accompagnant)
			self.perso_accompagne.all()[jet].ENCAISSE_TROUPE(n,special)
			
	
	def ENCAISSE_TROUPE(self,n):
		
		if n>0 :
			if n>self.nbTroupes : n = self.nbTroupes
			self.nbTroupes = self.nbTroupes-n
			
			if n>1 : s='s'
			else : s=''
			phrase = self.get_nom()+' perd '+str(n)+' troupe'+s
			
			if self.nbTroupes == 0 :
				if self.leader : 
					self.PV=0
					self.leader=None
					phrase = self.get_nom()+' perd toutes ses troupes et tombe inconscient dans la bataille'
				else : 
					self.PV=1
					phrase = self.get_nom()+' perd toutes ses troupes et se retrouve grièvement blessé dans la bataille'
			
			self.save()
			
			
			return phrase
	
	
	def get_gardes_MAX(self):
		comp_officier = Competence.objects.get(nom_info='officier')
		comp_aura = Competence.objects.get(nom_info='aura')
		val_officier = self.valeur_competence(comp_officier)
		val_aura = self.valeur_competence(comp_aura)
		
		if self.hote : resultat = 3 + val_officier*2 + val_aura
		else : resultat = 2 + val_officier + val_aura
		return resultat
		
	def get_troupes_MAX(self):
		comp_officier = Competence.objects.get(nom_info='officier')
		#comp_aura = Competence.objects.get(nom_info='aura')
		val_officier = self.valeur_competence(comp_officier)
		#val_aura = self.valeur_competence(comp_aura)
		
		resultat = 2 + val_officier*2
		return resultat
		
	def get_accompagnants_MAX(self):
		comp_officier = Competence.objects.get(nom_info='officier')
		comp_aura = Competence.objects.get(nom_info='aura')
		val_officier = self.valeur_competence(comp_officier)
		val_aura = self.valeur_competence(comp_aura)
		
		resultat = 2 + val_officier + val_aura
		return resultat
		
	def commande_attente(self):
		resultat = None
		if self.id!=1 :
			if len(self.commande_perso.all())>0:
				T_commande_perso = self.commande_perso.all()
				last_commande = T_commande_perso[len(T_commande_perso)-1]
				if last_commande.active and not last_commande.commence and not last_commande.fini and last_commande.date_debut<timezone.now()+timedelta(seconds=10*60) and last_commande.commande_precede == None :
					resultat = last_commande
		#print(resultat)
		return resultat
		
	def last_commande_programme(self):
		resultat = None
		last_commande = self.occupe
		
		while last_commande :
			resultat = last_commande
			if Commande.objects.filter(commande_precede=last_commande).filter(commence=False).filter(fini=False).exists() :
				last_commande = Commande.objects.get(commande_precede=resultat)
			else : last_commande = None
		return resultat
		
	def dernier_lieu_programme(self):
		resultat = self.lieu
		last_commande = self.occupe
		while last_commande :
			if last_commande.action.est_deplacement and last_commande.lieux_cible :
				resultat = last_commande.lieux_cible.all()[0]
			if Commande.objects.filter(commande_precede=last_commande).filter(commence=False).filter(fini=False).exists() :
				last_commande = Commande.objects.get(commande_precede=last_commande)
			else : last_commande = None
			#print(last_commande)
				
		return resultat
		
	def lieu_cible_connu(self):
		resultat = True
		last_lieu = self.dernier_lieu_programme()
		if last_lieu.inconnu :# and last_lieu.maison != self.maison :
			resultat = False
			for j in self.joueur.all():
				if j in last_lieu.users_connaissants.all() :
					resultat = True
					break
		return resultat
		
	def liste_commandes_programmes(self):
		T_resultat = []
		last_commande = self.occupe
		
		while last_commande :
			resultat = last_commande
			if Commande.objects.filter(commande_precede=last_commande).filter(commence=False).filter(fini=False).exists() :
				last_commande = Commande.objects.get(commande_precede=resultat)
				T_resultat.append(last_commande)
			else : last_commande = None
		T_resultat.reverse()
		return T_resultat
		
	def suiveurs(self):
		T_resultat = []
		for accompagnant in self.perso_accompagne.all():
			T_resultat.append(accompagnant)
		for prisonnier in self.perso_prisonnier.all():
			T_resultat.append(prisonnier)
		#qst_commande_espionnage = Commande.objects.filter(action__nom_info='espionner').filter(active=True).filter(commence=True).filter(fini=False).filter(persos_cible=perso).filter(perso__lieu=lieu)
		#qst_espions = Perso.objects.filter(active=True).filter(occupe__action__nom_info=True)
		
		return T_resultat
		
	def transforme(self,nom_info_cible):
		perso_cible = Perso.objects.filter(nom_info=nom_info_cible).all()[0]
		if perso_cible : self.doppelganger=perso_cible
		else : self.doppelganger=self
		print(self.doppelganger)
		self.save()
	
	def bouton_objet_OK(self):
		resultat = True
		if self.PV<=0 : resultat = False
		return resultat
	
	def get_espions(self):
		return self.espions.filter(active=True).filter(lieu=self.lieu).all()
	
	def vol_OK(self,joueur):
		resultat = False
		qst_espions_du_perso = self.get_espions()
		for espion in qst_espions_du_perso :
			if joueur in espion.joueur.all() :
				resultat = True
				break
		return resultat
		
	def influence_OK(self):
		r = True
		if not self.active : r = False
		elif self.PV<1 : r = False
		elif self.geolier : r = False
		elif self.en_combat : r = False
		elif self.en_fuite : r = False
		elif self.doppelganger : r = False
		return r