from django import forms
from django.db.models import Q
#from .models import Post
from .models import *
from .fonctions import define_cible_perso,define_cible_lieu,define_cible_posture,define_cible_resultat
from django.utils import timezone

#class PostForm(forms.ModelForm):

class MJDonneEffet(forms.Form):

	effet_maladie_cible = forms.ModelChoiceField(queryset=Effet.objects.filter(active=True), empty_label="---------------", label="Maladie : ", required=False)
	effet_potion_cible = forms.ModelChoiceField(queryset=Effet.objects.filter(active=True), empty_label="---------------", label="Effet de Potion : ", required=False)
	effet_poison_cible = forms.ModelChoiceField(queryset=Effet.objects.filter(active=True), empty_label="---------------", label="Effet de Poison : ", required=False)
	effet_divers_cible = forms.ModelChoiceField(queryset=Effet.objects.filter(active=True), empty_label="---------------", label="Effet divers : ", required=False)
	
	def __init__(self,qst_effet):
		super().__init__()
		
		qst_effet_maladie_cible = qst_effet.filter(classe="maladie")
		qst_effet_potion_cible = qst_effet.filter(classe="potion")
		qst_effet_poison_cible = qst_effet.filter(classe="poison")
		qst_effet_divers_cible = qst_effet.exclude(classe="maladie").exclude(classe="potion").exclude(classe="poison").order_by('classe')
		
		self.fields['effet_maladie_cible'].queryset = qst_effet_maladie_cible
		self.fields['effet_potion_cible'].queryset = qst_effet_potion_cible
		self.fields['effet_poison_cible'].queryset = qst_effet_poison_cible
		self.fields['effet_divers_cible'].queryset = qst_effet_divers_cible
		
		
	
class MJDonneEffet2(forms.Form):

	effet_maladie_cible = forms.ModelChoiceField(queryset=Effet.objects.filter(active=True), empty_label="---------------", label="Maladie : ", required=False)
	effet_potion_cible = forms.ModelChoiceField(queryset=Effet.objects.filter(active=True), empty_label="---------------", label="Effet de Potion : ", required=False)
	effet_poison_cible = forms.ModelChoiceField(queryset=Effet.objects.filter(active=True), empty_label="---------------", label="Effet de Poison : ", required=False)
	effet_divers_cible = forms.ModelChoiceField(queryset=Effet.objects.filter(active=True), empty_label="---------------", label="Effet divers : ", required=False)

class MJDonneObjet(forms.Form):

	arme_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Arme : ", required=False)
	armure_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Armure : ", required=False)
	potion_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Potion : ", required=False)
	parchemin_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Parchemin : ", required=False)
	rituel_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Rituel : ", required=False)
	obj_quete_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Objet de quête : ", required=False)
	divers_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Objet divers : ", required=False)
	
	
	def __init__(self,qst_obj):
		super().__init__()
		qst_arme_cible = qst_obj.filter(classe="arme")
		qst_armure_cible = qst_obj.filter(classe="armure")
		qst_potion_cible = qst_obj.filter(Q(classe="potion") | Q(classe="poison"))
		qst_parchemin_cible = qst_obj.filter(classe="parchemin")
		qst_rituel_cible = qst_obj.filter(classe="rituel")
		qst_quete_cible = qst_obj.filter(classe="quete")
		qst_divers_cible = qst_obj.exclude(classe="arme").exclude(classe="armure").exclude(classe="potion").exclude(classe="parchemin").exclude(classe="rituel").exclude(classe="quete").order_by('classe')
		
		self.fields['arme_cible'].queryset = qst_arme_cible
		self.fields['armure_cible'].queryset = qst_armure_cible
		self.fields['potion_cible'].queryset = qst_potion_cible
		self.fields['parchemin_cible'].queryset = qst_parchemin_cible
		self.fields['rituel_cible'].queryset = qst_rituel_cible
		self.fields['obj_quete_cible'].queryset = qst_quete_cible
		self.fields['divers_cible'].queryset = qst_divers_cible
		
		
		
	
class MJDonneObjet2(forms.Form):
	arme_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Arme : ", required=False)
	armure_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Armure : ", required=False)
	potion_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Potion : ", required=False)
	parchemin_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Parchemin : ", required=False)
	rituel_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Rituel : ", required=False)
	obj_quete_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Objet de quête : ", required=False)
	divers_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Objet divers : ", required=False)
	
	effet_maladie_cible = forms.ModelChoiceField(queryset=Effet.objects.filter(active=True), empty_label="---------------", label="Maladie : ", required=False)
	effet_potion_cible = forms.ModelChoiceField(queryset=Effet.objects.filter(active=True), empty_label="---------------", label="Effet de Potion : ", required=False)
	effet_poison_cible = forms.ModelChoiceField(queryset=Effet.objects.filter(active=True), empty_label="---------------", label="Effet de Poison : ", required=False)
	effet_divers_cible = forms.ModelChoiceField(queryset=Effet.objects.filter(active=True), empty_label="---------------", label="Effet divers : ", required=False)


class ModifResultat(forms.Form):
	nom = forms.CharField(max_length=200,required=True)
		#add_resultat = forms.ModelChoiceField(queryset=Resultat.objects.none(), empty_label="---------------", label="", required=False)
		#possible_pour_tous = forms.BooleanField(initial=True, required=False)
		#priorite = forms.IntegerField(required=False)
	action = forms.ModelChoiceField(queryset=Action.objects.all(), empty_label="---------------", label="", required=False)
	
	texte = forms.CharField(widget=forms.Textarea({'cols': '200', 'rows': '10'}), required=True)
		#description_MJ = forms.CharField(widget=forms.Textarea({'cols': '200', 'rows': '10'}), required=False)
	
	competence = forms.ModelChoiceField(queryset=Competence.objects.all(), empty_label="---------------", label="competence", required=False)
		#valeur_competence = forms.IntegerField(required=False)
		#chance_reussite = forms.IntegerField(required=False)
		#echec = forms.ModelChoiceField(queryset=Resultat.objects.none(), empty_label="---------------", label="", required=False)
	
	cle1 = forms.CharField(max_length=300,required=False)
	cle2 = forms.CharField(max_length=300,required=False)
		#cle_date = forms.CharField(max_length=100,required=False)
	obj_necessaire = forms.ModelChoiceField(queryset=Objet.objects.all(), empty_label="---------------", label="", required=False)
		#obj_importance = forms.ChoiceField(choices=((0,"suffisant pour avoir le résultat, mais n'est pas nécessaire"),(1,"Nécessaire pour avoir le résultat, mais n'est pas suffisant"),(2,"Nécessaire et suffisant pour avoir le résultat")), required=False)
		#obj_prioritaire = forms.BooleanField(initial=False, required=False)
	
		#public = forms.BooleanField(initial=False, required=False)
		#unique = forms.BooleanField(initial=True, required=False)
		#repetable = forms.BooleanField(initial=True, required=False)
	
	passage_trouve = forms.ModelChoiceField(queryset=Lieu.objects.all(), empty_label="---------------", label="", required=False)
	perso_trouve = forms.ModelChoiceField(queryset=Perso.objects.all(), empty_label="---------------", label="", required=False)
	effet_recu = forms.ModelChoiceField(queryset=Effet.objects.all(), empty_label="---------------", label="", required=False)
		#attaquer_par = forms.ModelChoiceField(queryset=Perso.objects.all(), empty_label="---------------", label="", required=False)
		#modif_PV = forms.IntegerField(initial=0, required=False)
		#modif_gardes = forms.IntegerField(initial=0, required=False)
		#modif_troupes = forms.IntegerField(initial=0, required=False)
	
	arme_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Arme : ", required=False)
	armure_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Armure : ", required=False)
	potion_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Potion : ", required=False)
	parchemin_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Parchemin : ", required=False)
	rituel_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Rituel : ", required=False)
	obj_quete_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Objet de quête : ", required=False)
	divers_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Objet divers : ", required=False)
	
	resultat_trouve = forms.ModelChoiceField(queryset=Resultat.objects.all(), empty_label="---------------", label="", required=False)
	
	
	def __init__(self,resultat):
		super().__init__()
		lieu = resultat.lieu
		qst_obj = Objet.objects.filter(active=True).order_by('nom')
		self.fields['passage_trouve'].queryset = Lieu.objects.filter(active=True).filter(secret=True).filter(lieu=lieu).order_by('priorite')
		self.fields['perso_trouve'].queryset = Perso.objects.filter(active=True).exclude(dissimulation=0).filter(lieu=lieu)
			#self.fields['add_resultat'].queryset = Resultat.objects.filter(active=True).filter(lieu=lieu).order_by('nom')
		qst_action = Action.objects.filter(active=True).filter(appel_resultat=True).order_by('categorie__priorite','priorite')
		self.fields['competence'].queryset = Competence.objects.filter(active=True).order_by('nom')
			#self.fields['echec'].queryset = Resultat.objects.filter(lieu=lieu).order_by('nom')
		self.fields['resultat_trouve'].queryset = Resultat.objects.filter(active=True).filter(possible_pour_tous=False).filter(lieu=lieu).order_by('nom')
		self.fields['obj_necessaire'].queryset =  Objet.objects.filter(active=True).filter(classe='quete').order_by('nom')
		self.fields['effet_recu'].queryset = Effet.objects.filter(active=True).exclude(support='divers').order_by('classe','nom')
		
		qst_action2 = qst_action
		for action in qst_action:
			action_OK = True
			if action.condition_atelier and (not action.condition_competence or action.condition_atelier_ET_competence) and not action.condition_atelier in resultat.lieu.atelier.all() : action_OK = False
			if (action.nom_info == 'explorer' and resultat.lieu.taille==1) or (action.nom_info == 'fouiller' and resultat.lieu.taille>1): action_OK = False
			if not action_OK : qst_action2 = qst_action2.exclude(id=action.id)
		self.fields['action'].queryset = qst_action2
		
		
		self.fields['arme_cible'].queryset = qst_obj.filter(classe="arme")
		self.fields['armure_cible'].queryset = qst_obj.filter(classe="armure")
		self.fields['potion_cible'].queryset = qst_obj.filter(Q(classe="potion") | Q(classe="poison"))
		self.fields['parchemin_cible'].queryset = qst_obj.filter(classe="parchemin")
		self.fields['rituel_cible'].queryset = qst_obj.filter(classe="rituel")
		self.fields['obj_quete_cible'].queryset = qst_obj.filter(classe="quete")
		self.fields['divers_cible'].queryset = qst_obj.exclude(classe="arme").exclude(classe="armure").exclude(classe="potion").exclude(classe="parchemin").exclude(classe="rituel").exclude(classe="quete").order_by('classe')
		
		self.fields['nom'].initial = resultat.nom
			#self.fields['add_resultat'].initial = resultat.add_resultat
		self.fields['texte'].initial = resultat.texte
		self.fields['cle1'].initial = resultat.cle1
		self.fields['cle2'].initial = resultat.cle2
		self.fields['obj_necessaire'].initial = resultat.obj_necessaire
		self.fields['effet_recu'].initial = resultat.effet_recu
		self.fields['passage_trouve'].initial = resultat.passage_trouve
		self.fields['perso_trouve'].initial = resultat.perso_trouve
		self.fields['competence'].initial = resultat.competence
		self.fields['action'].initial = resultat.action
		self.fields['resultat_trouve'].initial = resultat.resultat_trouve
		
		
class ModifResultat2(forms.Form):
	nom = forms.CharField(max_length=200,required=True)
		#add_resultat = forms.ModelChoiceField(queryset=Resultat.objects.none(), empty_label="---------------", label="", required=False)
		#possible_pour_tous = forms.BooleanField(initial=True, required=False)
		#priorite = forms.IntegerField(required=False)
	action = forms.ModelChoiceField(queryset=Action.objects.all(), empty_label="---------------", label="", required=False)
	
	texte = forms.CharField(widget=forms.Textarea({'cols': '200', 'rows': '10'}), required=True)
		#description_MJ = forms.CharField(widget=forms.Textarea({'cols': '200', 'rows': '10'}), required=False)
	
	competence = forms.ModelChoiceField(queryset=Competence.objects.all(), empty_label="---------------", label="competence", required=False)
		#valeur_competence = forms.IntegerField(required=False)
		#chance_reussite = forms.IntegerField(required=False)
		#echec = forms.ModelChoiceField(queryset=Resultat.objects.none(), empty_label="---------------", label="", required=False)
	
	cle1 = forms.CharField(max_length=300,required=False)
	cle2 = forms.CharField(max_length=300,required=False)
		#cle_date = forms.CharField(max_length=100,required=False)
	obj_necessaire = forms.ModelChoiceField(queryset=Objet.objects.all(), empty_label="---------------", label="", required=False)
		#obj_importance = forms.ChoiceField(choices=((0,"suffisant pour avoir le résultat, mais n'est pas nécessaire"),(1,"Nécessaire pour avoir le résultat, mais n'est pas suffisant"),(2,"Nécessaire et suffisant pour avoir le résultat")), required=False)
		#obj_prioritaire = forms.BooleanField(initial=False, required=False)
	
		#public = forms.BooleanField(initial=False, required=False)
		#unique = forms.BooleanField(initial=True, required=False)
		#repetable = forms.BooleanField(initial=True, required=False)
	
	passage_trouve = forms.ModelChoiceField(queryset=Lieu.objects.all(), empty_label="---------------", label="", required=False)
	perso_trouve = forms.ModelChoiceField(queryset=Perso.objects.all(), empty_label="---------------", label="", required=False)
	effet_recu = forms.ModelChoiceField(queryset=Effet.objects.all(), empty_label="---------------", label="", required=False)
		#attaquer_par = forms.ModelChoiceField(queryset=Perso.objects.all(), empty_label="---------------", label="", required=False)
		#modif_PV = forms.IntegerField(initial=0, required=False)
		#modif_gardes = forms.IntegerField(initial=0, required=False)
		#modif_troupes = forms.IntegerField(initial=0, required=False)
	
	arme_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Arme : ", required=False)
	armure_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Armure : ", required=False)
	potion_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Potion : ", required=False)
	parchemin_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Parchemin : ", required=False)
	rituel_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Rituel : ", required=False)
	obj_quete_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Objet de quête : ", required=False)
	divers_cible = forms.ModelChoiceField(queryset=Objet.objects.filter(active=True), empty_label="---------------", label="Objet divers : ", required=False)
	
	resultat_trouve = forms.ModelChoiceField(queryset=Resultat.objects.all(), empty_label="---------------", label="", required=False)
	
class LierResultat(forms.Form):
	nom = forms.CharField(max_length=200,required=True)
	texte = forms.CharField(widget=forms.Textarea({'cols': '200', 'rows': '10'}), required=True)
	public = forms.BooleanField(initial=False, required=False)
	unique = forms.BooleanField(initial=True, required=False)
	passage_trouve = forms.ModelChoiceField(queryset=Lieu.objects.none(), empty_label="---------------", label="", required=False)
	objet_trouve = forms.ModelMultipleChoiceField(queryset=Objet.objects.filter(active=True),label="---------------", required=False)
	effet_recu = forms.ModelChoiceField(queryset=Effet.objects.none(), empty_label="---------------", label="", required=False)
	perso_trouve = forms.ModelChoiceField(queryset=Perso.objects.none(), empty_label="---------------", label="", required=False)
	#attaquer_par = forms.ModelChoiceField(queryset=Perso.objects.all(), empty_label="---------------", label="", required=False)
	modif_PV = forms.IntegerField(initial=0, required=False)
	modif_gardes = forms.IntegerField(initial=0, required=False)
	modif_troupes = forms.IntegerField(initial=0, required=False)
	resultat_trouve = forms.ModelChoiceField(queryset=Resultat.objects.none(), empty_label="---------------", label="", required=False)
	
	def __init__(self,commande):
		super().__init__()
		self.fields['passage_trouve'].queryset = Lieu.objects.filter(active=True).filter(secret=True).filter(lieu=commande.lieu).exclude(users_connaissants_place=commande.joueur)
		self.fields['perso_trouve'].queryset = Perso.objects.filter(active=True).exclude(dissimulation=0).filter(lieu=commande.lieu).exclude(joueur_repere=commande.joueur)
		self.fields['resultat_trouve'].queryset = Resultat.objects.filter(active=True).filter(possible_pour_tous=False).filter(lieu=lieu).exclude(users_possible=commande.joueur).order_by('nom')
		self.fields['effet_recu'].queryset = Effet.objects.filter(active=True).exclude(support='divers').order_by('classe','nom')
		self.fields['objet_trouve'].queryset = Objet.objects.filter(active=True).order_by('classe','nom')
		

class LierResultat2(forms.Form):
	nom = forms.CharField(max_length=200,required=True)
	texte = forms.CharField(widget=forms.Textarea({'cols': '200', 'rows': '10'}), required=True)
	public = forms.BooleanField(initial=False, required=False)
	unique = forms.BooleanField(initial=True, required=False)
	passage_trouve = forms.ModelChoiceField(queryset=Lieu.objects.none(), empty_label="---------------", label="", required=False)
	objet_trouve = forms.ModelMultipleChoiceField(queryset=Objet.objects.filter(active=True),label="---------------", required=False)
	effet_recu = forms.ModelChoiceField(queryset=Effet.objects.none(), empty_label="---------------", label="", required=False)
	perso_trouve = forms.ModelChoiceField(queryset=Perso.objects.none(), empty_label="---------------", label="", required=False)
	#attaquer_par = forms.ModelChoiceField(queryset=Perso.objects.all(), empty_label="---------------", label="", required=False)
	modif_PV = forms.IntegerField(initial=0, required=False)
	modif_gardes = forms.IntegerField(initial=0, required=False)
	modif_troupes = forms.IntegerField(initial=0, required=False)
	resultat_trouve = forms.ModelChoiceField(queryset=Resultat.objects.none(), empty_label="---------------", label="", required=False)

	
class EnvoieMsg(forms.Form):

	texte = forms.CharField(widget=forms.Textarea({'cols': '200', 'rows': '10'}), required=True)
	persos_cible = forms.ModelMultipleChoiceField(queryset=Joueur.objects.all(),label="Joueurs cible", required=True)
	titre = forms.CharField(max_length=200,required=True)
	
	def __init__(self,qst_persos_cible,qst_cible_default,texte_default,titre_default):
		super().__init__()
		self.fields['persos_cible'].queryset = qst_persos_cible
		if len(qst_persos_cible)==1:
			self.fields['persos_cible'].initial = qst_persos_cible[0]
		if len(qst_cible_default)>0 :
			self.fields['persos_cible'].initial = qst_cible_default
		if texte_default != '' : self.fields['texte'].initial = texte_default
		if titre_default != '' : self.fields['titre'].initial = titre_default

		
class EnvoieMsg2(forms.Form):

	texte = forms.CharField(widget=forms.Textarea({'cols': '200', 'rows': '10'}), required=True)
	persos_cible = forms.ModelMultipleChoiceField(queryset=Joueur.objects.all(), label="Joueurs cible", required=True)
	titre = forms.CharField(max_length=200,required=True)	

class PostForm(forms.Form):

	texte = forms.CharField(widget=forms.Textarea({'cols': '200', 'rows': '10' }), required=False)
	
	option_action = forms.ModelChoiceField(queryset=Action.objects.none(),empty_label=None, label="Options :", required=False)
	
	perso_cible = forms.ModelChoiceField(queryset=Perso.objects.all(), empty_label="---------------", label="", required=False)
	persos_cible = forms.ModelMultipleChoiceField(queryset=Perso.objects.all(),label="Personnages cible", required=False)#widget=forms.CheckboxSelectMultiple
	
	lieu_cible = forms.ModelChoiceField(queryset=Lieu.objects.all(), empty_label="---------------", label="", required=False)
	lieux_cible = forms.ModelMultipleChoiceField(queryset=Lieu.objects.all(),label="Lieux cible", required=False)
	
	posture_cible = forms.ModelChoiceField(queryset=Posture.objects.all(), empty_label="---------------", label="", required=False)
	
	resultat_cible = forms.ModelChoiceField(queryset=Resultat.objects.all(), empty_label="---------------", label="", required=False)

	minute_cible = forms.IntegerField(required=False)
	heure_cible = forms.IntegerField(required=False)
	jour_cible = forms.IntegerField(required=False)
	mois_cible = forms.ModelChoiceField(queryset=Mois.objects.all(), empty_label="---------------", label="", required=False)
	annee_cible = forms.IntegerField(required=False)
	
	champ_recherche1 = forms.CharField(max_length=100,required=False)
	champ_recherche2 = forms.CharField(max_length=100,required=False)
	
	champ_texte = forms.CharField(widget=forms.Textarea({'cols': '70', 'rows': '3'}), required=False)
	
	def __init__(self,perso,lieu,action,T_date_jeu,commande_edit):
		super().__init__()
		
		if perso.id == 1 : perso.lieu = lieu
		
		#self.fields['minute_cible'].initial = T_date_jeu[0]
		#self.fields['heure_cible'].initial = T_date_jeu[1]
		self.fields['jour_cible'].initial = T_date_jeu[2]
		self.fields['mois_cible'].initial = T_date_jeu[3]
		self.fields['annee_cible'].initial = T_date_jeu[4]
		
		qst_perso_cible = define_cible_perso(action,perso)
		qst_lieu_cible = define_cible_lieu(action,perso)
		qst_posture_cible = define_cible_posture(action,perso)
		qst_resultat_cible = define_cible_resultat(action,perso)
		
		self.fields['perso_cible'].queryset = qst_perso_cible.order_by('-hote','maison','priorite')
		self.fields['lieu_cible'].queryset = qst_lieu_cible.order_by('priorite')
		self.fields['persos_cible'].queryset = qst_perso_cible.order_by('-hote','maison','priorite')
		self.fields['lieux_cible'].queryset = qst_lieu_cible.order_by('priorite')
		self.fields['posture_cible'].queryset = qst_posture_cible.order_by('priorite')
		self.fields['resultat_cible'].queryset = qst_resultat_cible.order_by('priorite')

		if action.post_only : self.fields['texte'].required = True
		if commande_edit : self.fields['texte'].initial = commande_edit.texte_post
		if action.cible_perso : 
			self.fields['perso_cible'].required = True
			if commande_edit : self.fields['perso_cible'].initial = commande_edit.persos_cible.all()[0]
		if action.cible_persos : 
			self.fields['persos_cible'].required = True
			if commande_edit : self.fields['persos_cible'].initial = commande_edit.persos_cible.all()
		if action.cible_lieu : 
			self.fields['lieu_cible'].required = True
			if commande_edit : self.fields['lieu_cible'].initial = commande_edit.lieux_cible.all()[0]
		if action.cible_lieux : 
			self.fields['lieux_cible'].required = True
			if commande_edit : self.fields['lieux_cible'].initial = commande_edit.lieux_cible.all()
		if action.cible_posture : 
			self.fields['posture_cible'].required = True
		if action.cible_resultat : 
			self.fields['resultat_cible'].required = True
			if commande_edit : self.fields['resultat_cible'].initial = commande_edit.resultat_cible
			
		#if action.champ_recherche1 : self.fields['champ_recherche1'].required = True
		#if action.champ_recherche2 : self.fields['champ_recherche2'].required = True
		if action.champ_texte : 
			self.fields['champ_texte'].required = True
			if commande_edit : self.fields['champ_texte'].initial = commande_edit.champ_texte
		if action.cible_instant :
			
			jeu = Jeu.objects.get(id = 1)
			T_date_jeu = jeu.convert_date(timezone.now())
			
			#self.fields['minute_cible'].required = True
			#self.fields['heure_cible'].initial = 3
			#self.fields['jour_cible'].initial = T_date_jeu[2]
			#self.fields['mois_cible'].initial = T_date_jeu[3]
			#self.fields['annee_cible'].required = True
		
		if action.cible_perso_verbose != '' : 
			self.fields['perso_cible'].label = action.cible_perso_verbose
			self.fields['persos_cible'].label = action.cible_perso_verbose
		
		if action.cible_lieu_verbose != '' : 
			self.fields['lieu_cible'].label = action.cible_lieu_verbose
			self.fields['lieux_cible'].label = action.cible_lieu_verbose
		
		if action.cible_posture_verbose != '' : 
			self.fields['posture_cible'].label = action.cible_posture_verbose
			
		if action.cible_resultat_verbose != '' : 
			self.fields['resultat_cible'].label = action.cible_resultat_verbose

		if action.champ_recherche1_verbose != '' : 
			self.fields['champ_recherche1'].label = action.champ_recherche1_verbose
			
		if action.champ_recherche2_verbose != '' : 
			self.fields['champ_recherche2'].label = action.champ_recherche2_verbose
			
		if action.champ_texte_verbose != '' : 
			self.fields['champ_texte'].label = action.champ_texte_verbose
		
		#qst_option_action = Action.objects.filter(Q(action_parent=action) | Q(id=action.id)).order_by('action_parent__nom','priorite')
		qst_option_action = Action.objects.filter(active=True).filter(action_parent=action).order_by('priorite')
		for option_action in qst_option_action :
			T_verif = option_action.verif(perso)
			if len(T_verif)!=0:
				qst_option_action = qst_option_action.exclude(id=option_action.id)
				print('\n'+perso.nom+' - '+option_action.nom+' impossible :\n---'+'\n---'.join(T_verif))

		if qst_option_action.count()>0 : 
			qst1 = Action.objects.filter(id=action.id)
			self.fields['option_action'].required = True
			self.fields['option_action'].queryset = qst_option_action
			


class PostForm2(forms.Form): # UNE STRICTE COPY DE POSTFORM, mais SANS INIT

	texte = forms.CharField(widget=forms.Textarea({'cols': '200', 'rows': '10' }), required=False)
	
	option_action = forms.ModelChoiceField(queryset=Action.objects.none(),empty_label=None, label="Options :", required=False)
	
	perso_cible = forms.ModelChoiceField(queryset=Perso.objects.all(), empty_label="---------------", label="", required=False)
	persos_cible = forms.ModelMultipleChoiceField(queryset=Perso.objects.all(),label="Personnages cible", required=False)#widget=forms.CheckboxSelectMultiple
	
	lieu_cible = forms.ModelChoiceField(queryset=Lieu.objects.all(), empty_label="---------------", label="", required=False)
	lieux_cible = forms.ModelMultipleChoiceField(queryset=Lieu.objects.all(),label="Lieux cible", required=False)
	
	posture_cible = forms.ModelChoiceField(queryset=Posture.objects.all(), empty_label="---------------", label="", required=False)
	
	resultat_cible = forms.ModelChoiceField(queryset=Resultat.objects.all(), empty_label="---------------", label="", required=False)

	minute_cible = forms.IntegerField(required=False)
	heure_cible = forms.IntegerField(required=False)
	jour_cible = forms.IntegerField(required=False)
	mois_cible = forms.ModelChoiceField(queryset=Mois.objects.all(), empty_label="---------------", label="", required=False)
	annee_cible = forms.IntegerField(required=False)
	
	champ_recherche1 = forms.CharField(max_length=100,required=False)
	champ_recherche2 = forms.CharField(max_length=100,required=False)
	
	champ_texte = forms.CharField(widget=forms.Textarea({'cols': '70', 'rows': '3'}), required=False)