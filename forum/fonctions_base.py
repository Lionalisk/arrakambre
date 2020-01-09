import random
import math
from django.http import *



def define_num_page(num_page,post_par_page,nb_post):
	nb_page = int(math.ceil(nb_post/post_par_page))
	T_page = []
	i=num_page-2
	while len(T_page)<=4 and i<=nb_page :
		if i>0 : T_page.append(i)
		i=i+1
	if not 1 in T_page : 
		T_page.insert(0,'...')
		T_page.insert(0,1)
	if not nb_page in T_page : 
		T_page.append('...')
		T_page.append(nb_page)
	
	return T_page
	

def distinctLIO(qst):
	T_verif = []
	for a in qst :
		if not a in T_verif : T_verif.append(a)
	return T_verif

def test_reussite(seuil,de):
	d = de(de)
	if d<=seuil : return True
	else : return False

def de(faces):
	i=0
	while i<1 :
	
		resultat = (random.randint(1,faces))
		print('Lancer dé : '+str(resultat)+'/'+str(faces))
		i=i+1
	return resultat
	
def xde(nb_des,faces):
	resultat = 0
	i=0
	while i<= nb_des :
		resultat = resultat+(random.randint(1,faces))
		i=i+1
	print('Lancer de '+str(nb_des)+' dés '+str(faces)+' : '+str(resultat))
	return resultat

def objet_ds_manytomany(objet,manytomany):
	resultat = False
	if manytomany:
		for obj in manytomany.all() :
			if obj == objet :
				resultat = True
				break
	return resultat
	
def manytomany_ds_manytomany(manytomany1,manytomany2):
	resultat = False
	for obj1 in manytomany1.all() :
		for obj2 in manytomany2.all() :
			if obj1 == obj2 :
				resultat = True
				break
	return resultat	

def traduction_msg(txt,commande):
	#print(commande.persos_cible.all())
	if txt :
		persos_cible = txt_liste(commande.persos_cible.all())
		lieux_cible = txt_liste(commande.lieux_cible.all())
		champ_recherche1 = commande.champ_recherche1
		if commande.resultat_cible : resultat_cible = commande.resultat_cible.nom
		else : resultat_cible = ""
		if not champ_recherche1 : champ_recherche1 = ""
		objet = ''
		if commande.objet : objet = commande.objet.obj.nom
		pronom = "il"
		if not commande.perso.genre : pronom = "elle"
		resultat = txt.replace("#perso#",commande.perso.get_nom()).replace("#lieu#",commande.lieu.nom).replace("#persos_cible#",persos_cible).replace("#lieux_cible#",lieux_cible).replace("#objet#",objet)
		resultat = resultat.replace("#champ_recherche1#",champ_recherche1).replace("#chance#",str(commande.chance_reussite)).replace("#date#",str(commande.date_jeu_fin)).replace("#il#",pronom).replace("#resultat_cible#",resultat_cible)
		if commande.perso.leader_id : resultat = resultat.replace('#leader#',commande.perso.leader.get_nom())
		else : resultat = resultat.replace('#leader#','None')
	else : resultat = ''
	return resultat

	
def article_apostrophe(article,nom):
	if len(article)>0 :
		T_voyelles = ['a','e','i','o','u','y','h']
		first_lettre = nom[0].lower()
		if first_lettre in T_voyelles :
			article = article[:-1]+"'"
		else : article = article+' '
	return article
	
def est_ds_heures(heure,heure_debut,heure_fin):
	resultat = False
	if heure>=heure_debut and heure<=heure_fin : resultat = True
	elif heure_fin<heure_debut  :
		if heure>=0 and heure<=heure_fin  : resultat = True
		if heure>=heure_debut and heure_fin<24  : resultat = True
	return resultat

def format_date_jeu(T_date_jeu,format_date):

	minute_jeu = str(T_date_jeu[0]).zfill(2)
	heure_jeu = str(T_date_jeu[1])
	jour_jeu = str(T_date_jeu[2])+'e'
	if jour_jeu == '1e' : jour_jeu='1er'
	mois_jeu = article_apostrophe('de',T_date_jeu[3].nom)+T_date_jeu[3].nom
	annee_jeu = str(T_date_jeu[4])
	resultat = format_date.replace('<minute>',minute_jeu).replace('<heure>',heure_jeu).replace('<jour>',jour_jeu).replace('<mois>',mois_jeu).replace('<annee>',annee_jeu)
	return resultat

def format_T_date_jeu(T_date_jeu):
	resultat = ''
	a=0
	for elt_date_jeu in T_date_jeu :
		if a==3 : resultat = resultat + elt_date_jeu.nom + '#'
		else : resultat = resultat + str(elt_date_jeu) + '#'
		a=a+1
	return resultat
	
def txt_liste(qst):
	resultat = ''
	if qst :
		T_resultat = []
		for elt in qst :
			T_resultat.append(elt.nom)
		
		if len(T_resultat)==1 : resultat = T_resultat[0]
		elif len(T_resultat)==2 : resultat = T_resultat[0]+' et '+T_resultat[1]
		else :
			resultat = ','.join(T_resultat[:-1])
			resultat = resultat+',et '+T_resultat[-1]
	return resultat

def pronom(bool_genre):
	if bool_genre : pronom = 'il'
	else : pronom = 'elle'
	return pronom
	
def addition_TAB(Tableau_nombre):
	resultat = 0
	for a in Tableau_nombre :
		resultat = resultat+a
	return resultat
	
def bonus_des_obj(T_obj,attribut):
	
	valeur = 0
	for obj in T_obj:
	
		TT_bonus = [[obj.competence_bonifie,'competence'],[obj.posture_bonifie,'posture'],[obj.bonus_combat,'bonus_combat'],[obj.bonus_PV,'bonus_PV'],[obj.bonus_PA,'bonus_PA'],[obj.bonus_PC,'bonus_PC'],[obj.bonus_PE,'bonus_PE']]
		T_valeur = [obj.valeur1,obj.valeur2,obj.valeur3,obj.valeur4]
		a=-1
		for T_bonus in TT_bonus :
			if T_bonus[0] : a=a+1
			if T_bonus[1]==attribut : break
		
		if a<len(T_valeur) : valeur = valeur+T_valeur[a]
	
	return valeur
	
def post_frappe(attaquant,defenseur,T_ATT_COMBAT,T_DEF_COMBAT,T_REF_ATTAQUE):
	val_attaque = addition_TAB(T_ATT_COMBAT)
	val_defense = addition_TAB(T_DEF_COMBAT)
	texte = 'TOTAL : '+str(val_attaque-val_defense)+'\n\n'
	texte = texte+'<u><b>Attaquant : '+attaquant.get_nom()+' -> '+str(val_attaque)+'</b></u>'+'\nPosture : '+attaquant.posture.nom
	
	a=0
	for elt in T_REF_ATTAQUE :
		texte = texte + "\n"+elt+" : "+str(T_ATT_COMBAT[a])
		a=a+1
	texte = texte+'\n\n<u><b>Defenseur : '+defenseur.get_nom()+' -> '+str(val_defense)+'</b></u>'+'\nPosture : '+defenseur.posture.nom
	a=0
	for elt in T_REF_ATTAQUE :
		texte = texte + "\n"+elt+" : "+str(T_DEF_COMBAT[a])
		a=a+1
	return texte
	
def recherche_Ok(recherche,champs_cle):
	resultat = False
	T_cles = champs_cle.replace('-','').replace(' ','').replace("'",'').replace("_",'').replace("é",'e').replace("è",'e').replace("ê",'e').replace("î",'i').replace("à",'a').replace(",",';').split(";")
	for cle in T_cles :
		if recherche.upper().replace('-','').replace(' ','').replace("'",'').replace("_",'').replace("é",'e').replace("è",'e').replace("ê",'e').replace("î",'i').replace("à",'a')==cle.upper():
			resultat = True
			break
	return resultat