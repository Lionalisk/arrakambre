from django.utils import timezone
from datetime import timedelta
from django.http import *
from django.db.models import Q

from .models import *



from .fonctions_base import *
from .fonctions_actions import *
from math import *


def reset(option):
	
	if option!='MAJlieux' :
		print("		Suppression des Posts")
		if option == "all": qst_posts = Post.objects.all()
		else : qst_posts = Post.objects.filter(lock=False)
		
		for post in qst_posts :
			post.delete()
		
		print("		Suppression des Commandes")
		qst_commande = Commande.objects.all()
		for commande in qst_commande :
			commande.delete()
		
		print("		Suppression des Messages")
		qst_message = Message.objects.all()
		for msg in qst_message :
			msg.delete()
		
		print("		MAJ des PERSOS")
		qst_perso = Perso.objects.filter(active=True)
		for perso in qst_perso :
			print(perso.nom)
			perso.occupe = None
			perso.desc_occupe = ""
			perso.prisonnier = False
			#perso.en_combat = False
			#perso.en_soin = False
			#perso.en_fuite = False
			perso.geolier = None
			perso.leader = None
			#perso.PC = 0
			#perso.PV = 3
			#perso.PE = 0
			#perso.dissimulation = 0
			perso.joueur_repere.clear()
			perso.persos_deja_provoques.clear()
			#perso.accepte_duel = False
			
			perso.save()
		
	MAJlieux()
	

def MAJlieux():
	print("		MAJ des LIEUX")
	qst_lieux = Lieu.objects.all()
	for lieu in qst_lieux :
		print(lieu.nom)
		lieu.ferme = False
		lieu.users_connaissants.clear()
		lieu.users_connaissants_place.clear()
		lieu.save()
		qst_perso_connaissant = Perso.objects.filter(active=True)
		if lieu.hote.count()>=1 : 
			print(lieu.hote.all()[0].nom)
			maison = lieu.hote.all()[0].maison
			qst_perso_connaissant = qst_perso_connaissant.filter(Q(lieu=lieu) | Q(maison=maison))
		else : qst_perso_connaissant = qst_perso_connaissant.filter(lieu=lieu)
		for p in qst_perso_connaissant :
			for j in p.joueur.all():
				if not objet_ds_manytomany(j,lieu.users_connaissants) :
					lieu.users_connaissants.add(j)				

def MAJregles():
	
	#Bonus de compétences des maisons
	tableau_bonus_maison = Tableau.objects.get(nom_info="competence_bonus_maison")
	
	qst_maison = Maison.objects.filter(active=True).order_by('priorite')
	
	T_contenu = ['- Maison#Orientation Principale#Bonus']
	for maison in qst_maison:
		if maison.bonus_competence_categorie1_id and maison.bonus_competence1_id :
			ligne = maison.nom+'#'+maison.bonus_competence_categorie1.nom+'#+1 en '+maison.bonus_competence1.nom
			T_contenu.append(ligne)
		if maison.bonus_competence_categorie2_id and maison.bonus_competence2_id :
			ligne2 = maison.nom+'#'+maison.bonus_competence_categorie2.nom+'#+1 en '+maison.bonus_competence2.nom
			T_contenu.append(ligne2)
	tableau_bonus_maison.description = '\n- '.join(T_contenu)
	tableau_bonus_maison.save()
	
	#Liste des compétences
	tableau_competences = Tableau.objects.get(nom_info="liste_compétence")
	
	qst_competence = Competence.objects.filter(active=True).order_by('categorie_classement_id','priorite')
	T_contenu = ['- Compétence#Orientation#Description']
	for competence in qst_competence:
		T_cat = []
		for categorie in competence.categorie.all():
			T_cat.append(categorie.nom)
		ligne = competence.nom+'#'+', '.join(T_cat)+'#'+competence.description
		T_contenu.append(ligne)
		
	tableau_competences.description = '\n- '.join(T_contenu)
	tableau_competences.save()
	
	#liste des Charges
	tableau_charge = Tableau.objects.get(nom_info="influence_charge")
	qst_charges = Charge.objects.filter(active=True).order_by('priorite')
	T_contenu = ['- Charge#Influence']
	for charge in qst_charges:
		ligne = charge.nom+'#'+str(charge.influence)
		T_contenu.append(ligne)
		
	tableau_charge.description = '\n- '.join(T_contenu)
	tableau_charge.save()
	
	
def testLIO():
	qst_perso = Perso.objects.filter(active=True)
	qst_action = Action.objects.filter(active=True)
	qst_lieu = Lieu.objects.filter(active=True)
	print('\n\n')
	'''testperso = Perso.objects.get(id=2)
	print(testperso)
	if testperso in qst_perso : print('OK')
	else : print('KO')'''
	
	qst_action = qst_action.filter(condition_competence=None)
	
	for action in qst_action :
		print('	'+str(action))
		#print('		'+action.condition_competence.nom)
		
	print('\n\n')
	