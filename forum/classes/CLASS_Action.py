from django.db import models
from django.db.models import Q
from ..models import Perso
from ..models import Lieu
from ..models import Jeu
from ..fonctions_base import *
from math import floor
#from datetime import timedelta

class Action(models.Model):

	active = models.BooleanField(default=True)
	MJ_only = models.BooleanField(default=False)
	nom = models.CharField(max_length=40, unique=True)
	nom_info = models.CharField(max_length=30, unique=True)
	#image = models.CharField(max_length=30, unique=True)
	description = models.TextField(default='', blank=True, null=True)
	description2 = models.TextField(default='', blank=True, null=True, verbose_name='description2 : se genere automatiquement')
	lock_description2 = models.BooleanField(default=False, verbose_name='si oui, description2 ne se genere pas automatiquement')
	regle_associe = models.ForeignKey('regle', blank=True, null=True ,on_delete=models.SET_NULL)
	texte_explicatif_choix = models.CharField(verbose_name = "Phrase qui va expliquer le choix", default='', blank=True , max_length=200)
	
	priorite = models.SmallIntegerField(default=1)
	categorie = models.ForeignKey('Categorie_action', default=1, blank=True, on_delete=models.SET_DEFAULT)
	action_parent = models.ForeignKey('self', blank=True, null=True ,on_delete=models.SET_NULL, verbose_name="Action parent : cette action se rattache en tant qu'option à une autre action")
	
	visible = models.BooleanField(default=True)
	OK_ds_post_action = models.BooleanField(default=False,verbose_name="OK_ds_post_action : si l'action n'est pas visible, on peut quand même accéder au formulaire par un autre lien")
	visible_ds_regles = models.BooleanField(default=True)
	delay = models.SmallIntegerField(verbose_name="temps pour réaliser l'action, en %",default=100)
	chance_reussite = models.SmallIntegerField(verbose_name="chance de réussite sur l'action, en %",default=100)
	
	post_only = models.BooleanField(default=False)
	appel_resultat = models.BooleanField(default=False,verbose_name="Appel un resultat auprès du MJ")
	est_deplacement = models.BooleanField(default=False)
	est_combat = models.BooleanField(default=False)
	programmable = models.BooleanField(default=True)
	annulable = models.BooleanField(default=True)
	#fonction_si_annulable = models.BooleanField(default=False,verbose_name="fonction_si_annulable : lance une fonction ANNULE_ lors de l'annulation de la commande de l'action")
	empechable = models.BooleanField(default=True)
	implique_objet = models.BooleanField(default=False,verbose_name="implique un objet")
	#dissimulable = models.BooleanField(default=True)
	interdit = models.BooleanField(default=False,verbose_name="interdit dans les lois d'arrakambre")
	options = models.BooleanField(default=False,verbose_name="a des options - Si oui, les actions lui rapportant doivent lui référer dans Action Parent. Les verifications de base se feront à partir de cette entité.")

	#CHAMPS DE RENSEIGNEMENT :
	post_OK = models.BooleanField(default=True)
	cible_perso = models.BooleanField(default=False)
	cible_persos = models.BooleanField(default=False)
	cible_perso_verbose = models.CharField(default='', blank=True, max_length=100)
	cible_lieu = models.BooleanField(default=False)
	cible_lieux = models.BooleanField(default=False)
	cible_lieu_verbose = models.CharField(default='', blank=True, max_length=100)
	cible_instant = models.BooleanField(default=False)
	cible_instant_verbose = models.CharField(default='', blank=True, max_length=100)
	cible_posture = models.BooleanField(default=False)
	cible_posture_verbose = models.CharField(default='', blank=True, max_length=100)
	cible_resultat = models.BooleanField(default=False)
	cible_resultat_verbose = models.CharField(default='', blank=True, max_length=100)
	#cible_action = models.BooleanField(default=False)
	champ_recherche1 = models.BooleanField(default=False)
	champ_recherche1_verbose = models.CharField(default='', blank=True, max_length=100)
	champ_recherche2 = models.BooleanField(default=False)
	champ_recherche2_verbose = models.CharField(default='', blank=True, max_length=100)
	champ_texte = models.BooleanField(default=False)
	champ_texte_verbose = models.CharField(default='', blank=True, max_length=100)

	#CONDITIONS :
	
	# 0:action possible quelque soit le cas ; 1: action possible si ce n'est pas le cas ; 2:action possible que si c'est le cas
	condition_cible_possible = models.BooleanField(verbose_name="OK seulement si au moins une cible est possible",default=False)
	condition_occupe = models.SmallIntegerField(default=1, choices=((0,'Peut etre fait si le perso est occupe ou non'),(1,"Ne peut etre fait que si le perso n'est pas occupe"),(2,'Ne peut être fait que si le perso est occupe')))
	condition_cache = models.SmallIntegerField(default=0, choices=((0,'Peut etre fait si le perso est caché ou non'),(1,"Ne peut etre fait que si le perso n'est pas caché"),(2,'Ne peut être fait que si le perso est caché')))
	condition_suit_perso = models.SmallIntegerField(default=1, choices=((0,"Peut etre fait si le perso suit quelqu'un ou non"),(1,"Ne peut etre fait que si le perso n'est pas en train de suivre quelqu'un"),(2,"Ne peut être fait que si le perso est en train de suivre quelqu'un")))
	condition_est_suivi = models.SmallIntegerField(default=0, choices=((0,"Peut etre fait si le perso a des accompagnants ou non"),(1,"Ne peut etre fait que si le perso n'a pas d'accompagnant"),(2,"Ne peut être fait que si le perso a des accompagnants")))
	
	condition_en_soin = models.SmallIntegerField(default=1, choices=((0,'Peut etre fait si le perso est en soin ou non'),(1,"Ne peut etre fait que si le perso n'est pas en soin"),(2,'Ne peut être fait que si le perso est en soin')))
	condition_prisonnier = models.SmallIntegerField(default=1, choices=((0,'Peut etre fait si le perso est prisonnier ou non'),(1,"Ne peut etre fait que si le perso n'est pas prisonnier"),(2,'Ne peut être fait que si le perso est prisonnier')))
	condition_geolier = models.SmallIntegerField(default=0, choices=((0,'Peut etre fait si le perso a un prisonnier ou non'),(1,"Ne peut etre fait que si le perso n'a pas de prisonnier"),(2,'Ne peut être fait que si le perso a un prisonnier')))
	condition_hote = models.SmallIntegerField(default=1, choices=((0,'Peut etre fait si le perso est un hote de lieu ou non'),(1,"Ne peut etre fait que si le perso n'est pas un hote de lieu"),(2,'Ne peut être fait que si le perso est un hote de lieu')))
	condition_gardes = models.SmallIntegerField(default=0, choices=((0,'Peut etre fait si le perso a des gardes ou non'),(1,"Ne peut etre fait que si le perso n'a pas de gardes"),(2,'Ne peut être fait que si le perso a des gardes')))
	condition_troupes = models.SmallIntegerField(default=0, choices=((0,'Peut etre fait si le perso a des troupes ou non'),(1,"Ne peut etre fait que si le perso n'a pas de troupes"),(2,'Ne peut être fait que si le perso a des troupes')))
	
	condition_en_combat = models.SmallIntegerField(default=1, choices=((0,'Peut etre fait si le perso est en combat ou non'),(1,"Ne peut etre fait que si le perso n'est pas en combat"),(2,'Ne peut être fait que si le perso est en combat')))
	condition_en_fuite = models.SmallIntegerField(default=1, choices=((0,'Peut etre fait si le perso est en fuite ou non'),(1,"Ne peut etre fait que si le perso n'est pas en fuite"),(2,'Ne peut être fait que si le perso est en fuite')))
	condition_en_duel = models.SmallIntegerField(default=1, choices=((0,'Peut etre fait si le perso est en duel ou non'),(1,"Ne peut etre fait que si le perso n'est pas en duel"),(2,'Ne peut être fait que si le perso est en duel')))
	
	condition_lieuferme = models.SmallIntegerField(default=0, choices=((0,'Peut etre fait si le lieu dans lequel est le perso est fermé ou non'),(1,"Ne peut etre fait que si le lieu dans lequel est le perso n'est pas fermé"),(2,'Ne peut etre fait que si le lieu dans lequel est le perso est fermé')))
	condition_lieu_propriete = models.SmallIntegerField(default=0, choices=((0,'Peut etre fait si le lieu dans lequel est le perso est la propriété de sa maison ou non'),(1,"Ne peut etre fait que si le lieu dans lequel est le perso n'est pas la propriété de sa maison"),(2,'Ne peut etre fait que si le lieu dans lequel est le perso est la propriété de sa maison')))
	condition_lieuQG = models.SmallIntegerField(default=0, choices=((0,'Peut etre fait si le lieu dans lequel est le perso est un QG ou non'),(1,"Ne peut etre fait que si le lieu dans lequel est le perso n'est pas un QG"),(2,'Ne peut etre fait que si le lieu dans lequel est le perso est un QG')))
	condition_lieu_espace = models.SmallIntegerField(default=0, choices=((0,'Peut etre fait si le lieu dans lequel est le perso est un grand espace ou non'),(1,"Ne peut etre fait que si le lieu dans lequel est le perso n'est pas un grand espace"),(2,'Ne peut etre fait que si le lieu dans lequel est le perso est un grand espace')))
	condition_lieu_agardes = models.SmallIntegerField(default=0, choices=((0,'Peut etre fait si le lieu dans lequel est le perso a des gardes ou non'),(1,"Ne peut etre fait que si le lieu dans lequel est le perso n'a pas de gardes"),(2,'Ne peut etre fait que si le lieu dans lequel est le perso a des gardes')))
	condition_lieu_atroupes = models.SmallIntegerField(default=0, choices=((0,'Peut etre fait si le lieu dans lequel est le perso a des troupes ou non'),(1,"Ne peut etre fait que si le lieu dans lequel est le perso n'a pas de troupes"),(2,'Ne peut etre fait que si le lieu dans lequel est le perso a des troupes')))

	PV_max = models.SmallIntegerField(default=10)
	PV_min = models.SmallIntegerField(default=1)
	
	condition_atelier = models.ForeignKey('Atelier', on_delete=models.SET_NULL, blank=True, null=True)
	condition_competence = models.ForeignKey('Competence', on_delete=models.SET_NULL, blank=True, null=True)
	condition_competence_necessaire = models.BooleanField(default=True)
	condition_atelier_ET_competence = models.BooleanField(default=False)
	condition_espece = models.ManyToManyField('Espece', blank=True, related_name = "espece_condition")
	
	#CONDITIONS CIBLE :
	
	cibleperso_PV_max = models.SmallIntegerField(default=10)
	cibleperso_PV_min = models.SmallIntegerField(default=1)
	cibleperso_soimeme = models.BooleanField(default=False, verbose_name = 'Cible Perso : peut être soi-même ?')
	cibleperso_eloigne = models.SmallIntegerField(default=1, verbose_name = 'Cible Perso : éloignée ?', choices=((0,'La cible peut être dans le même lieu ou non'),(1,"La cible doit être dans le même lieu"),(2,"La cible ne doit pas être dans le même lieu")))
	cibleperso_mm_secteur = models.SmallIntegerField(default=1, verbose_name = 'Cible Perso : dans le même secteur ?', choices=((0,'La cible peut être dans le même secteur ou non'),(1,"La cible doit être dans le même secteur"),(2,"La cible ne doit pas être dans le même secteur")))
	cibleperso_occupe = models.SmallIntegerField(default=0, verbose_name = 'Cible Perso : occupée ?', choices=((0,'La cible peut être occupée ou non'),(1,"Ne peut etre fait que si la cible n'est pas occupée"),(2,'Ne peut être fait que si la cible est occupée')))
	cibleperso_encombat = models.SmallIntegerField(default=0, verbose_name = 'Cible Perso : en combat ?', choices=((0,'La cible peut être en combat ou non'),(1,"La cible ne doit pas être en combat"),(2,"La cible doit être en combat")))
	cibleperso_prisonnier = models.SmallIntegerField(default=1, verbose_name = 'Cible Perso : prisonnier ?', \
				choices=((0,'La cible peut être prisonnier ou non'),(1,"La cible ne doit pas être prisonnier par un tiers"),(2,'La cible doit être prisonnier par un tiers'),\
				(3,'La cible ne doit pas être prisonnier par le perso acteur'),(4,'La cible doit être prisonnier par le perso acteur'),(5,'La cible ne doit pas être prisonnier du tout')))
	cibleperso_est_accompagnant = models.SmallIntegerField(default=1, verbose_name = 'Cible Perso : accompagne un autre perso ?', \
				choices=((0,'La cible peut accompagner un autre perso ou non'),(1,"La cible ne doit pas être en train d'accompagner un autre perso"),(2,"La cible doit être en train d'accompagner un autre perso"),\
						(3,"La cible ne doit pas être en train d'accompagner le perso"),(4,"La cible doit être en train d'accompagner ce perso")))
	cibleperso_est_leader = models.SmallIntegerField(default=0, verbose_name = 'Cible Perso : est en train de mener le perso ?', \
				choices=((0,'La cible peut être en train de mener le perso ou non'),(1,"La cible ne doit pas être en train de mener le perso"),(2,'La cible doit être en train de mener le perso'),\
						(3,"La cible ne doit pas être en train de mener quelqu'un"),(4,"La cible doit être en train de mener quelqu'un")))
	cibleperso_a_gardes = models.SmallIntegerField(default=0, verbose_name = 'Cible Perso : a des gardes ?', choices=((0,'La cible peut avoir des gardes ou non'),(1,"La cible ne doit pas avoir de gardes"),(2,'La cible doit avoir des gardes')))
	cibleperso_a_troupes = models.SmallIntegerField(default=0, verbose_name = 'Cible Perso : a des troupes ?', choices=((0,'La cible peut avoir des troupes ou non'),(1,"La cible ne doit pas avoir de troupes"),(2,'La cible doit avoir des troupes')))
	cibleperso_cache = models.SmallIntegerField(default=0, verbose_name = 'Cible Perso : est caché ?', choices=((0,'La cible peut être caché ou non'),(1,"La cible ne doit pas être cachée, même si repéré par joueur"),(2,'La cible doit être cachée, même si repérée par joueur')))
	cibleperso_espece = models.ManyToManyField('Espece', blank=True, related_name = "espece_cibleperso")
	
	ciblelieu_eloigne = models.SmallIntegerField(default=1, verbose_name = 'Cible Lieu : éloignée ?', choices=((0,'Le lieu cible peut être éloigné ou non'),(1,"Le lieu présent doit avoir un passage vers le lieu cible"),(2,"Le lieu présent ne doit pas avoir de passage vers le lieu cible")))
	ciblelieu_ferme = models.SmallIntegerField(default=1, verbose_name = 'Cible Lieu : est fermé ?', choices=((0,'Le lieu cible peut être fermé ou non'),(1,"Le lieu cible ne doit pas être fermé"),(2,"Le lieu cible doit être fermé")))
	ciblelieu_invite = models.SmallIntegerField(default=1, verbose_name = "Cible Lieu : le perso a le droit d'entrer ?", choices=((0,'Le lieu cible peut être fermé au perso ou non'),(1,"Le lieu cible ne doit pas être fermé au perso"),(2,"Le lieu cible doit être fermé au perso")))
	ciblelieu_espace = models.SmallIntegerField(default=1, verbose_name = 'Cible Lieu : est un espace ouvert ?', choices=((0,'Le lieu cible peut être un espace ouvert ou non'),(1,"Le lieu cible ne doit pas être un espace ouvert"),(2,"Le lieu cible doit être un espace ouvert")))
	ciblelieu_discret = models.SmallIntegerField(default=0, verbose_name = "Cible Lieu : est un lieu discret ?", choices=((0,'Le lieu cible peut être un lieu discret ou non'),(1,"Le lieu cible ne doit pas être un lieu discret"),(2,"Le lieu cible doit être un lieu discret")))
	ciblelieu_inconnu = models.SmallIntegerField(default=1, verbose_name = 'Cible Lieu : est inconnu ?', choices=((0,'Le lieu cible peut être un lieu inconnu ou non'),(1,"Le lieu cible ne doit pas être un lieu inconnu pour le joueur"),(2,"Le lieu cible doit être un lieu inconnu pour le joueur")))
	ciblelieu_secret = models.SmallIntegerField(default=0, verbose_name = 'Cible Lieu : est secret ?', choices=((0,'Le lieu cible peut être un lieu secret ou non'),(1,"Le lieu cible ne doit pas être un lieu secret pour le joueur"),(2,"Le lieu cible doit être un lieu secret pour le joueur")))
	ciblelieu_a_garde = models.SmallIntegerField(default=0, verbose_name = 'Cible Lieu : a des gardes ?', choices=((0,'Le lieu cible peut avoir des gardes ou non'),(1,"Le lieu cible ne doit pas avoir de gardes"),(2,"Le lieu cible doit avoir des gardes")))
	ciblelieu_a_troupe = models.SmallIntegerField(default=0, verbose_name = 'Cible Lieu : a des troupes ?', choices=((0,'Le lieu cible peut avoir des troupes ou non'),(1,"Le lieu cible ne doit pas avoir de troupes"),(2,"Le lieu cible doit avoir des troupes")))
	ciblelieu_proprietaire = models.SmallIntegerField(default=0, verbose_name = 'Cible Lieu : la maison du perso en est proprietaire ?', choices=((0,'Le lieu cible peut être la poprieté du perso ou non'),(1,"Le lieu cible ne doit pas être la poprieté du perso"),(2,"Le lieu cible doit être la poprieté du perso")))
	ciblelieu_QG = models.SmallIntegerField(default=0, verbose_name = "Cible Lieu : est le QG d'une maison ?", choices=((0,'Le lieu cible peut être un QG ou non'),(1,"Le lieu cible ne doit pas être un QG"),(2,"Le lieu cible doit être un QG")))
	
	
	#MSG
	
	msg_init = models.CharField(verbose_name = "Phrase de description lors du début de la commande (#perso# , #lieu# , #persos_cible# , #lieux_cible#)",default='', blank=True, null=True, max_length=200)
	msg_encours =  models.CharField(verbose_name = "Phrase d'information lorsque la commande est encours(#perso# , #lieu# , #persos_cible# , #lieux_cible#)",default='', blank=True, null=True, max_length=200)
	msg_fin = models.CharField(verbose_name = "Phrase de description lors de la fin de la commande (#perso# , #lieu# , #persos_cible# , #lieux_cible#)",default='', blank=True, null=True, max_length=200)
	
	
	#msg_resume = models.TextField(default='', blank=True, null=True)
	importance = models.SmallIntegerField(default=0)
	#msg_MJ = models.TextField(default='', blank=True, null=True)
	desc = models.TextField(verbose_name = "Phrase de description sur la commande vue par le perso acteur(#perso# , #lieu# , #persos_cible# , #lieux_cible#)",default='', blank=True, null=True)
	desc2 = models.TextField(verbose_name = "Phrase de description sur la commande vue par le perso cible(#perso# , #lieu# , #persos_cible# , #lieux_cible#)",default='', blank=True)
	
	def __str__(self):
		#return str(self.id)+' '+self.nom
		active = ""
		if not self.active : active = "-------------"
		visible = ""
		if not self.visible : visible = "X - "
		
		action_parent = ""
		if self.action_parent : action_parent = "("+self.action_parent.nom+") "
		
		return active+visible+action_parent+self.nom+' - '+self.nom_info+' - '+str(self.id)
		#return str(self.id)+'-'+active+visible+action_parent+self.nom+' - '+self.nom_info
		#return self.nom
		
	def get_nom(self):
		resultat = self.nom
		return resultat
	
		
	def save(self, *args, **kwargs):
		if not self.lock_description2 :
			jeu = Jeu.objects.get(id=1)
			
			self.description2 = self.description+'\n<div><img src="/static/forum/'+jeu.nom_info+'/img/separateur_h.png"></div>'
			
			if self.delay == 0 : txt_delai = "Instantané"
			else :
				
				delai = self.delay*jeu.base_delay/100
				delai_jeu_h = floor(delai/jeu.rapport_temps)
				delai_jeu_mn = int((delai-delai_jeu_h)*60)
				txt_delai = str(round(delai,2))+'H réelles ('+str(delai_jeu_h)+'H'+str(delai_jeu_mn)+' dans le temps du jeu)'
			
			competence_utile = 'Compétence : Aucune'
			if self.condition_competence : 
				if self.condition_atelier_ET_competence or self.condition_competence_necessaire : competence_utile = 'Compétence nécessaire : '+self.condition_competence.nom
				else : competence_utile = 'Compétence utilisée : '+self.condition_competence.nom
				
			T_cibles = []
			if self.cible_perso : T_cibles.append('Cible un personnage')
			elif self.cible_persos : T_cibles.append('Cible un ou ou plusieurs personnages')
			if self.cible_lieu : T_cibles.append('Cible un lieu')
			elif self.cible_lieux : T_cibles.append('Cible un ou ou plusieurs lieux')
			
			
			T_ajout = []
			if self.condition_atelier_ET_competence and self.condition_atelier : T_ajout.append("Action possible seulement dans les lieux le permettant")
			elif self.condition_atelier and self.condition_competence_necessaire and self.condition_competence :  T_ajout.append("Action possible seulement si le personnage possède la compétence OU qu'il est dans un lieu le permettant")
			
			if self.condition_occupe == 0 : T_ajout.append('Action possible même si le personnage est occupé')
			elif self.condition_occupe == 2 and self.condition_en_combat != 2 : T_ajout.append('Action possible seulement si le personnage est occupé')
			if self.condition_hote == 1 : T_ajout.append("Action impossible pour un hôte de lieu")
			elif self.condition_hote == 2 : T_ajout.append("Action réalisable seulement par l'hôte d'un lieu")
			if self.condition_en_combat == 0 : T_ajout.append("Action possible en combat")
			elif self.condition_en_combat == 2 : T_ajout.append("Action possible seulement en combat")
			#if self.condition_en_fuite == 0 : T_ajout.append("Action possible en fuite")
			#elif self.condition_en_fuite == 2 : T_ajout.append("Action possible seulement en fuite")
			if self.condition_cache == 1 : T_ajout.append("Action impossible si le personnage est dissimulé")
			elif self.condition_cache == 2 : T_ajout.append("Action possible seulement si le personnage est dissimulé")
			if self.condition_lieu_espace == 1 : T_ajout.append("Action possible seulement si le personnage est dans un espace restreint")
			elif self.condition_lieu_espace == 2 : T_ajout.append("Action possible seulement si le personnage est dans un Grand Espace")
			if self.condition_lieuferme == 1 : T_ajout.append("Action possible seulement si le personnage est dans un lieu ouvert")
			elif self.condition_lieuferme == 2 : T_ajout.append("Action possible seulement si le personnage est dans un lieu fermé")
			if self.condition_suit_perso == 0 : T_ajout.append("Action possible même si le personnage est en train d'accompagner quelqu'un")
			elif self.condition_suit_perso == 2 : T_ajout.append("Action possible seulement si le personnage est en train d'accompagner quelqu'un")
			
			if self.condition_est_suivi == 1 and self.condition_gardes == 1 and self.condition_troupes == 1 : T_ajout.append("Action impossible si le personnage est accompagné par d'autres persos, par des gardes ou par des troupes")
			elif self.condition_gardes == 1 and self.condition_troupes == 1 : T_ajout.append("Action impossible si le personnage est accompagné par des gardes ou par des troupes")
			else :
				if self.condition_est_suivi == 1 : T_ajout.append("Action impossible si le personnage est accompagné par d'autres persos")
				elif self.condition_est_suivi == 2 : T_ajout.append("Action possible seulement si le personnage est accompagné par d'autres persos")
				if self.condition_gardes == 1 : T_ajout.append("Action impossible si le personnage est accompagné de garde(s)")
				elif self.condition_gardes == 2 : T_ajout.append("Action possible seulement si le personnage est accompagné de garde(s)")
				if self.condition_troupes == 1 : T_ajout.append("Action impossible si le personnage est accompagné de troupe(s)")
				elif self.condition_troupes == 2 : T_ajout.append("Action possible seulement si le personnage est accompagné de troupe(s)")
			if self.PV_min>1 : T_ajout.append("Le personnage doit avoir au moins "+str(self.PV_min)+" pt(s) de vie pour réaliser cette action")
			if self.PV_max<3 : T_ajout.append("Le personnage doit avoir moins de "+str(self.PV_max+1)+" pt(s) de vie pour réaliser cette action")
			
			if self.cible_perso or self.cible_persos :
				if self.cibleperso_eloigne==0 and self.cibleperso_mm_secteur==0 : T_ajout.append("Le perso cible peut être dans lieu ou un secteur différent")
				elif self.cibleperso_mm_secteur==0 : T_ajout.append("Le perso cible peut être dans un secteur différent")
				elif self.cibleperso_mm_secteur==2 : T_ajout.append("Le perso cible doit être dans un secteur différent")
				elif self.cibleperso_eloigne==2 : T_ajout.append("Le perso cible doit être dans un lieu différent")
				
			if self.cible_lieu or self.cible_lieux :
				if self.ciblelieu_eloigne == 0 : T_ajout.append("Le lieu cible peut être éloigné")
				elif self.ciblelieu_eloigne == 2 : T_ajout.append("Le lieu cible doit être éloigné")
				if self.ciblelieu_espace == 1 : T_ajout.append("Le lieu cible doit être un espace restreint")
				elif self.ciblelieu_espace == 2 : T_ajout.append("Le lieu cible doit être un grand espace")
				if self.ciblelieu_discret == 1 : T_ajout.append("Le lieu cible ne doit pas être un lieu discret")
				elif self.ciblelieu_discret == 2 : T_ajout.append("Le lieu cible doit être un lieu discret")
				if self.ciblelieu_invite == 1 : T_ajout.append("Le lieu cible doit être ouvert pour le personnage")
				elif self.ciblelieu_invite == 2 : T_ajout.append("Le lieu cible doit être fermé pour le personnage")
				
			for cible in T_cibles : self.description2 = self.description2+'\n<div class="red">'+cible+'</div>'
			self.description2 = self.description2+'\n<div class="red">Délai : '+txt_delai+'</div><div class="red">'+competence_utile+'</div>'
			
			if len(T_ajout)>0:
				self.description2 = self.description2+'\n<div class="red">Conditions :</div><div><i>'+'</i></div><div><i>'.join(T_ajout)+'</i></div>'
		
		super().save()  # Call the "real" save() method.'''
		print("SAVE : "+str(self))
	
	def verif(self,perso):
		T_msg = []
		nom_acteur = perso.nom
		if perso.id==1 : 
			if self.MJ_only : T_msg = []
			else : T_msg = ["PERSO NONE"]
		else :
			if self.condition_occupe == 1 and perso.occupe and not perso.occupe.fini : T_msg.append("Pour réaliser cette action, "+nom_acteur+" ne doit pas être occupé")
			if self.condition_occupe == 2 and ((not perso.occupe) or perso.occupe.fini) : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être occupé")
			
			if self.condition_suit_perso == 1 and perso.leader_id : T_msg.append("Pour réaliser cette action, "+nom_acteur+" ne doit pas être en train de suivre quelqu'un")
			if self.condition_suit_perso == 2 and not perso.leader_id : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être en train de suivre quelqu'un")
			
			if self.condition_hote == 1 and perso.hote_id : T_msg.append("Pour réaliser cette action, "+nom_acteur+" ne doit pas être l'hote d'un lieu")
			if self.condition_hote == 2 and (not perso.hote_id ): T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être l'hote d'un lieu")
			
			if self.condition_en_combat == 1 and perso.en_combat : T_msg.append("Pour réaliser cette action, "+nom_acteur+" ne doit pas être en train de combattre")
			if self.condition_en_combat == 2 and (not perso.en_combat) : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être en train de combattre")
			
			if self.condition_en_fuite == 1 and perso.en_fuite : T_msg.append("Pour réaliser cette action, "+nom_acteur+" ne doit pas être en train de fuire")
			if self.condition_en_fuite == 2 and (not perso.en_fuite) : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être en train de fuire")
			
			if self.condition_en_duel == 1 and perso.en_combat and perso.occupe_id and perso.occupe.action.nom_info=='attaquer_duel' : T_msg.append("Pour réaliser cette action, "+nom_acteur+" ne doit pas être en train de faire un duel")
			if self.condition_en_duel == 2 and ((not perso.en_combat) or (not perso.occupe_id) or (perso.occupe_id and perso.occupe.action.nom_info!='attaquer_duel')) : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être en train de faire un duel")
			
			if self.condition_en_soin == 1 and perso.en_soin and not perso.occupe.fini : T_msg.append("Pour réaliser cette action, "+nom_acteur+" ne doit pas être en train d'être soigné")
			if self.condition_en_soin == 2 and (not perso.en_soin or perso.occupe.fini) : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être en train d'être soigné")
			
			if self.condition_prisonnier == 1 and perso.geolier : T_msg.append("Pour réaliser cette action, "+nom_acteur+" ne doit pas être prisonnier")
			if self.condition_prisonnier == 2 and (not perso.geolier) : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être prisonnier")
			
			if self.condition_geolier == 1 and Perso.objects.filter(geolier__id=self.id).exists() : T_msg.append("Pour réaliser cette action, "+nom_acteur+" ne doit pas avoir de prisonnier")
			if self.condition_geolier == 2 and (not Perso.objects.filter(geolier__id=self.id).exists()) : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit avoir un prisonnier")
			
			if self.condition_est_suivi == 1 and len(perso.perso_accompagne.all())>0 : T_msg.append("Pour réaliser cette action, "+nom_acteur+" ne doit pas être accompagné par d'autres personnages")
			if self.condition_est_suivi == 2 and len(perso.perso_accompagne.all())==0  : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être accompagné par d'autres personnages")
			
			if self.condition_espece.all() and not objet_ds_manytomany(perso.espece,self.condition_espece) :  T_msg.append("Pour réaliser cette action, "+nom_acteur+" ne doit pas être un "+perso.espece.nom)
			
			if perso.PV<self.PV_min : T_msg.append(nom_acteur+" est trop blessé pour réaliser cette action")
			if perso.PV>self.PV_max : T_msg.append(nom_acteur+" n'est pas assez blessé pour réaliser cette action")
			
			if self.condition_lieuferme == 1 and perso.lieu.ferme : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être dans un lieu ouvert")
			if self.condition_lieuferme == 2 and not perso.lieu.ferme : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être dans un lieu fermé")

			if self.condition_lieu_propriete == 1 and perso.lieu.hote and perso.maison == perso.lieu.maison() : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être dans un lieu qui n'est pas la propriété de sa maison")
			if self.condition_lieu_propriete == 2 and ((not perso.lieu.hote) or perso.maison != perso.lieu.maison()) : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être dans un lieu qui est la propriété de sa maison")

			if self.condition_lieuQG == 1 and perso.lieu.QG : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être dans un lieu qui n'est pas un QG")
			if self.condition_lieuQG == 2 and not perso.lieu.QG : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être dans un lieu qui est un QG")

			if self.condition_lieu_espace == 1 and perso.lieu.taille>1 : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être dans un lieu qui n'est pas un grand espace")
			if self.condition_lieu_espace == 2 and perso.lieu.taille<=1 : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être dans un lieu qui est un grand espace")

			if self.condition_lieu_agardes == 1 and perso.lieu.nbgarde>0 : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être dans un lieu qui n'a pas de gardes")
			if self.condition_lieu_agardes == 2 and perso.lieu.nbgarde==0 : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être dans un lieu qui a des gardes")

			if self.condition_lieu_atroupes == 1 and perso.lieu.nbtroupe>0 : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être dans un lieu qui n'a pas de troupes")
			if self.condition_lieu_atroupes == 2 and perso.lieu.nbtroupe==0 : _msg.append("Pour réaliser cette action, "+nom_acteur+" doit être dans un lieu qui a des troupes")
			
			if self.condition_gardes == 1 and perso.nbGardes>0 : T_msg.append("Pour réaliser cette action, "+nom_acteur+" ne doit pas avoir de gardes")
			if self.condition_gardes == 2 and perso.nbGardes==0 : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit avoir des gardes")

			if self.condition_troupes == 1 and perso.nbTroupes>0 : T_msg.append("Pour réaliser cette action, "+nom_acteur+" ne doit pas avoir de troupes")
			if self.condition_troupes == 2 and perso.nbTroupes==0 : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit avoir des troupes")
			
			#if not self.dissimulable and perso.dissimulation>0 : T_msg.append("Pour réaliser cette action, "+nom_acteur+" ne doit pas être caché")
			if self.condition_cache == 1 and perso.dissimulation>0 : T_msg.append("Pour réaliser cette action, "+nom_acteur+" ne doit pas être caché")
			if self.condition_cache == 2 and (perso.dissimulation==0) : T_msg.append("Pour réaliser cette action, "+nom_acteur+" doit être caché")


			cond_comp = True
			cond_atelier = True
			if (self.condition_competence_necessaire and self.condition_competence) and not perso.a_competence(self.condition_competence) : cond_comp = False
			if self.condition_atelier and not objet_ds_manytomany(self.condition_atelier,perso.lieu.atelier) : cond_atelier = False
			
			if (not cond_atelier) or (not cond_comp) :
				if self.condition_atelier_ET_competence : #or (not (self.condition_competence and self.condition_atelier)):
					if not cond_atelier : T_msg.append(nom_acteur+" doit avoir l'accés à un(e) "+self.condition_atelier.nom.upper()+" pour réaliser cette action")
					if not cond_comp : T_msg.append(nom_acteur+" doit avoir la competence "+self.condition_competence.nom.upper()+" pour réaliser cette action")
				else :
					if self.condition_atelier and self.condition_competence : T_msg.append(perso.nom+" doit avoir la competence "+self.condition_competence.nom.upper()+" ou avoir l'accés à un(e) "+self.condition_atelier.nom.upper()+" pour réaliser cette action")
					elif self.condition_atelier : T_msg.append(perso.nom+" doit avoir l'accés à un(e) "+self.condition_atelier.nom.upper()+" pour réaliser cette action")
					elif self.condition_competence : T_msg.append(perso.nom+" doit avoir la competence "+self.condition_competence.nom.upper()+" pour réaliser cette action")
		
		#if len(T_msg)>0 : print('\n'+self.nom+' - '+perso.nom+' impossible :\n	'+'\n	'.join(T_msg)+'\n')
		
		#if len(T_msg)>0 : verif = False
		#else : verif = True
		
		return T_msg
	
	def verif_perso_cible(self,perso,perso_cible):
		T_msg = []
		nom_acteur = perso.nom
		nom_cible = perso_cible.nom
		
		if self.cibleperso_eloigne == 1 and perso_cible.lieu != perso.lieu : T_msg.append("Pour subir cette action, "+nom_cible+" doit être dans le même lieu que "+nom_acteur)
		elif self.cibleperso_eloigne == 2 and perso_cible.lieu == perso.lieu : T_msg.append("Pour subir cette action, "+nom_cible+" ne doit pas être dans le même lieu que "+nom_acteur)
		
		#
		if self.cibleperso_mm_secteur == 1 and (perso_cible.secteur != perso.secteur or perso_cible.lieu != perso.lieu) : T_msg.append("Pour subir cette action, "+nom_cible+" doit être dans le même secteur que "+nom_acteur)
		elif self.cibleperso_mm_secteur == 2 and perso_cible.lieu == perso.lieu and perso_cible.secteur == perso.secteur : T_msg.append("Pour subir cette action, "+nom_cible+" ne doit pas être dans le même secteur que "+nom_acteur)
		
		if perso_cible.PV<self.cibleperso_PV_min : T_msg.append(nom_cible+" est trop blessé pour subir cette action")
		elif perso_cible.PV>self.cibleperso_PV_max : T_msg.append(nom_cible+" n'est pas assez blessé pour subir cette action")
		
		#
		if not self.cibleperso_soimeme and perso==perso_cible :  T_msg.append(nom_acteur+" ne peut pas subir lui/elle même subir cette action")
		
		if self.cibleperso_occupe == 1 and perso_cible.occupe_id and not perso_cible.occupe.fini : T_msg.append("Pour subir cette action, "+nom_cible+" ne doit pas être occupé")
		elif self.cibleperso_occupe == 2 and ((not perso_cible.occupe_id) or perso_cible.occupe.fini) : T_msg.append("Pour subir cette action, "+nom_cible+" doit être occupé")
		
		if self.cibleperso_encombat == 1 and perso_cible.en_combat: T_msg.append("Pour subir cette action, "+nom_cible+" ne doit pas être en train de combattre")
		elif self.cibleperso_encombat == 2 and (not perso_cible.en_combat) : T_msg.append("Pour subir cette action, "+nom_cible+" doit être en train de combattre")
		
		if self.cibleperso_prisonnier == 1 and perso_cible.geolier_id and perso_cible.geolier != perso : T_msg.append("Pour subir cette action, "+nom_cible+" ne doit pas être prisonnier par un tiers")
		elif self.cibleperso_prisonnier == 2 and (perso_cible.geolier == None or perso_cible.geolier==perso ): T_msg.append("Pour subir cette action, "+nom_cible+" cible doit être prisonnier d'un tiers")
		elif self.cibleperso_prisonnier == 3 and perso_cible.geolier == perso : T_msg.append("Pour subir cette action, "+nom_cible+" cible ne doit pas être le prisonnier de "+nom_acteur)
		elif self.cibleperso_prisonnier == 4 and perso_cible.geolier != perso : T_msg.append("Pour subir cette action, "+nom_cible+" cible doit être le prisonnier de "+nom_acteur)
		elif self.cibleperso_prisonnier == 5 and perso_cible.geolier != None : T_msg.append("Pour subir cette action, "+nom_cible+" cible ne doit pas être prisonnier par quelqu'un")
		
		#
		if self.cibleperso_est_accompagnant == 1 and perso_cible.leader_id : T_msg.append("Pour subir cette action, "+nom_cible+" ne doit pas être en train d'accompagner quelqu'un")
		elif self.cibleperso_est_accompagnant == 2 and (not perso_cible.leader_id) : T_msg.append("Pour subir cette action, "+nom_cible+" doit être en train d'accompagner quelqu'un")
		elif self.cibleperso_est_accompagnant == 3 and perso_cible.leader == perso : T_msg.append("Pour subir cette action, "+nom_cible+" ne doit pas être en train d'accompagner "+nom_acteur)
		elif self.cibleperso_est_accompagnant == 4 and perso_cible.leader != perso : T_msg.append("Pour subir cette action, "+nom_cible+" doit être en train d'accompagner "+nom_acteur)
		
		if self.cibleperso_est_leader == 1 and perso.leader == perso_cible : T_msg.append("Pour subir cette action, "+nom_cible+" ne doit pas être en train d'être accompagné par "+nom_acteur)
		elif self.cibleperso_est_leader == 2 and perso.leader != perso_cible : T_msg.append("Pour subir cette action, "+nom_cible+" doit être en train d'être accompagné par "+nom_acteur)
		elif self.cibleperso_est_leader == 3 and len(perso_cible.perso_accompagne.all())>0 : T_msg.append("Pour subir cette action, "+nom_cible+" ne doit pas être en train de mener quelqu'un")
		elif self.cibleperso_est_leader == 4 and len(perso_cible.perso_accompagne.all())==0 : T_msg.append("Pour subir cette action, "+nom_cible+" doit être en train de mener quelqu'un")
		
		if self.cibleperso_a_gardes == 1 and perso_cible.nbGardes>0 : T_msg.append("Pour subir cette action, "+nom_cible+" ne doit pas être accompagné de gardes")
		elif self.cibleperso_a_gardes == 2 and perso_cible.nbGardes==0 : T_msg.append("Pour subir cette action, "+nom_cible+" doit être accompagné de gardes")
		
		if self.cibleperso_a_troupes == 1 and perso_cible.nbTroupes>0 : T_msg.append("Pour subir cette action, "+nom_cible+" ne doit pas être accompagné de troupes")
		elif self.cibleperso_a_troupes == 2 and perso_cible.nbTroupes==0 : T_msg.append("Pour subir cette action, "+nom_cible+" doit être accompagné de troupes")
		
		if self.cibleperso_cache == 1 and perso_cible.dissimulation>0 : T_msg.append("Pour subir cette action, "+nom_cible+" ne doit pas être caché(e)")
		elif self.cibleperso_cache == 2 and perso_cible.dissimulation==0 : T_msg.append("Pour subir cette action, "+nom_cible+" doit être caché(e)")
		
		if self.cibleperso_espece.all() and not objet_ds_manytomany(perso_cible.espece,self.cibleperso_espece) :  T_msg.append("Pour subir cette action, "+nom_cible+" ne doit pas être un "+perso_cible.espece.nom)
		
		if perso_cible.dissimulation>0 and (not manytomany_ds_manytomany(perso.joueur,perso_cible.joueur)) and (not manytomany_ds_manytomany(perso.joueur,perso_cible.joueur_repere))  : T_msg.append("Pour subir cette action, "+nom_cible+" doit être visible au yeux de "+nom_acteur)
		
		
		verif = '\n'.join(T_msg)

		return T_msg
		
	
	def verif_lieu_cible(self,perso,lieu_cible):
		T_msg = []
		nom_lieu = lieu_cible.nom.lower()
		
		if self.ciblelieu_eloigne == 1 and not Lieu.objects.filter(id=perso.lieu.id).filter(passages=lieu_cible).exists() : T_msg.append("Pour subir cette action, "+nom_lieu+" ne doit pas être éloigné")
		elif self.ciblelieu_eloigne == 2 and lieu_cible == perso.lieu : T_msg.append("Pour subir cette action, "+nom_lieu+" doit être éloigné")
		
		if self.ciblelieu_ferme == 1 and lieu_cible.ferme : T_msg.append("Pour subir cette action, "+nom_lieu+" ne doit pas être fermé")
		elif self.ciblelieu_ferme == 2 and not lieu_cible.ferme : T_msg.append("Pour subir cette action, "+nom_lieu+" doit être fermé")

		if self.ciblelieu_invite == 1 and lieu_cible.ferme and not objet_ds_manytomany(perso,lieu_cible.perso_autorise) and (not perso.maison_id or perso.maison != lieu_cible.maison()) : T_msg.append("Pour subir cette action, "+nom_lieu+" ne doit pas être fermé pour "+perso.nom)
		elif self.ciblelieu_invite == 2 and (objet_ds_manytomany(perso,lieu_cible.perso_autorise) or not lieu_cible.ferme or (perso.maison_id and perso.maison==lieu_cible.maison())) : T_msg.append("Pour subir cette action, "+nom_lieu+" doit être fermé pour "+perso.nom)

		if self.ciblelieu_espace == 1 and lieu_cible.taille>1 : T_msg.append("Pour subir cette action, "+nom_lieu+" ne doit pas être un grand espace")
		elif self.ciblelieu_espace == 2 and lieu_cible.taille<=1 : T_msg.append("Pour subir cette action, "+nom_lieu+" doit être un grand espace")
		
		if self.ciblelieu_discret == 1 and lieu_cible.dissimulation>0 : T_msg.append("Pour subir cette action, "+nom_lieu+" ne doit pas être un lieu discret")
		elif self.ciblelieu_discret == 2 and lieu_cible.dissimulation==0 : T_msg.append("Pour subir cette action, "+nom_lieu+" doit être un lieu discret")
		
		if self.ciblelieu_inconnu == 1 and lieu_cible.inconnu and not manytomany_ds_manytomany(perso.joueur,lieu_cible.users_connaissants) : T_msg.append("Pour subir cette action, "+nom_lieu+" ne doit pas être inconnu du joueur")
		elif self.ciblelieu_inconnu == 2 and (manytomany_ds_manytomany(perso.joueur,lieu_cible.users_connaissants) or not lieu_cible.inconnu) : T_msg.append("Pour subir cette action, "+nom_lieu+" doit être inconnu du joueur")
		
		if self.ciblelieu_secret == 1 and lieu_cible.secret and not manytomany_ds_manytomany(perso.joueur,lieu_cible.users_connaissants_place) : T_msg.append("Pour subir cette action, "+nom_lieu+" ne doit pas être un lieu secret pour le joueur")
		elif self.ciblelieu_secret == 2 and (manytomany_ds_manytomany(perso.joueur,lieu_cible.users_connaissants_place) or not lieu_cible.secret) : T_msg.append("Pour subir cette action, "+nom_lieu+" doit être un lieu secret pour le joueur")

		if self.ciblelieu_a_garde == 1 and lieu_cible.nbGardes>0 : T_msg.append("Pour subir cette action, "+nom_lieu+" ne doit pas être occupé par des gardes")
		elif self.ciblelieu_a_garde == 2 and lieu_cible.nbGardes==0 : T_msg.append("Pour subir cette action, "+nom_lieu+" doit être occupé par des gardes")

		if self.ciblelieu_a_troupe == 1 and lieu_cible.nbTroupes>0 : T_msg.append("Pour subir cette action, "+nom_lieu+" ne doit pas être occupé par des troupes")
		elif self.ciblelieu_a_troupe == 2 and lieu_cible.nbTroupes==0 : T_msg.append("Pour subir cette action, "+nom_lieu+" doit être occupé par des troupes")


		if self.ciblelieu_proprietaire == 1 and (lieu_cible.maison() == perso.maison and perso.maison_id) : T_msg.append("Pour subir cette action, "+nom_lieu+" ne doit pas être la propriété de la Maison "+perso.maison.nom)
		elif self.ciblelieu_proprietaire == 2 and (lieu_cible.maison() != perso.maison or not perso.maison_id) : T_msg.append("Pour subir cette action, "+nom_lieu+" doit être la propriété de la Maison de "+perso.nom)

		if self.ciblelieu_QG == 1 and lieu_cible.QG : T_msg.append("Pour subir cette action, "+nom_lieu+" ne doit pas être un QG")
		elif self.ciblelieu_QG == 2 and not lieu_cible.QG : T_msg.append("Pour subir cette action, "+nom_lieu+" doit être un QG")
		#
		
		
		verif = '\n'.join(T_msg)

		return T_msg
		

	def recup_champs_cible(self):
		T_cible = []

		if self.cible_perso : 
			T_cible.append("cible_perso")
			T_cible.append(self.cible_perso_verbose)
		if self.cible_persos : 
			T_cible.append("cible_persos")
			T_cible.append(self.cible_perso_verbose)
		if self.cible_lieu : 
			T_cible.append("cible_lieu")
			T_cible.append(self.cible_lieu_verbose)
		if self.cible_lieux : 
			T_cible.append("cible_lieux")
			T_cible.append(self.cible_lieu_verbose)
			
		if self.cible_resultat : 
			T_cible.append("cible_resultat")
			T_cible.append(self.cible_resultat_verbose)
			
		if self.cible_posture : 
			T_cible.append("cible_posture")
			T_cible.append(self.cible_posture_verbose)
			
		if self.cible_heure : 
			T_cible.append("cible_heure")
			T_cible.append(self.cible_heure_verbose)
		if self.champ_recherche1 : 
			T_cible.append("champ_recherche1")
			T_cible.append(self.champ_recherche1_verbose)
		if self.champ_recherche2 : 
			T_cible.append("champ_recherche2")
			T_cible.append(self.champ_recherche2_verbose)
		if self.champ_texte : 
			T_cible.append("champ_texte")
			T_cible.append(self.champ_texte_verbose)

		if self.post_only : T_cible.append("post_obligatoire")

		return T_cible
		
	def return_html_desc(self):
		jeu = Jeu.objects.get(id=1)
		html = '<img src="/static/forum/'+jeu.nom_info+'/img/separateur_h.png">'
		
		contenu_description = self.description2
		if self.regle_associe and self.regle_associe.id != self.id : 
			
			contenu_description = contenu_description.replace('#regle#',self.regle_associe.desc())
			
		regle = jeu.regle_index
		contenu_description = regle.conversion_regle(contenu_description)
		html = html+'<div id=action_'+str(self.id)+' class=desc_action style=\"padding:15px\">'+'<div class=texte_base>'+contenu_description+'</div></div>'
		html= html + '<img src="/static/forum/'+jeu.nom_info+'/img/separateur_h.png">'
		
		
		return html
	
	
