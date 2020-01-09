from django.utils import timezone
from datetime import timedelta

from django.http import *

from .models import *

from .fonctions_base import *
from .fonctions_actions import *

from math import *
import time

jeu = Jeu.objects.get(id=1)


def define_list_action(perso):
	liste_action = Action.objects.filter(visible=True).filter(active=True).filter(MJ_only=False).filter(action_parent=None)
	for action in liste_action :
		T_verif = action.verif(perso)
		if action.condition_cible_possible and len(T_verif)==0 :
			#print(action.nom)
			if action.cible_resultat : qst_cibles_possible = define_cible_resultat(action,perso)
			else : qst_cibles_possible = define_cible_perso(action,perso)
			if not qst_cibles_possible : T_verif.append("Pas de cibles possibles pour cette action")


		if perso.en_combat and action.est_combat and len(T_verif)==0 :
			commandes_frappe = Commande.objects.filter(action__nom_info="frapper").filter(fini=False).filter(champ_recherche1 = action.nom_info)
			for commande_frappe in commandes_frappe :
				if (commande_frappe.perso==perso or commande_frappe.persos_cible.all()[0]==perso) :
					T_verif.append(perso.nom+' est deja en situation de '+action.nom_info)
					break

		if len(T_verif)!=0:
			liste_action = liste_action.exclude(id=action.id)
			#print('\n'+perso.nom+' - '+action.nom+' impossible :\n---'+'\n---'.join(T_verif))
	return liste_action


def define_cible_perso(action,perso):
	
	if action.cible_perso or action.cible_persos :
		if action.cibleperso_eloigne == 1 :
			liste_perso_cible = Perso.objects.filter(active=True).filter(vivant=True).filter(lieu=perso.lieu)
		else : liste_perso_cible = Perso.objects.filter(active=True).filter(vivant=True)

		for perso_cible in liste_perso_cible :
			T_verif = action.verif_perso_cible(perso,perso_cible)
			if len(T_verif)!=0:
				liste_perso_cible = liste_perso_cible.exclude(id=perso_cible.id)
				#print(action.nom+' : '+perso_cible.nom+' cible impossible :\n---'+'\n---'.join(T_verif))
	
	else : liste_perso_cible = Perso.objects.none()
	#print(liste_perso_cible)
	return liste_perso_cible.order_by('maison').order_by('-priorite')



def define_cible_lieu(action,perso):
	
	if action.cible_lieu or action.cible_lieux :
		if action.ciblelieu_eloigne == 1 :
			liste_lieu_cible = Lieu.objects.filter(passages=perso.lieu)
		else : liste_lieu_cible = Lieu.objects.all()
		#print(liste_lieu_cible)
		for lieu_cible in liste_lieu_cible :
			T_verif = action.verif_lieu_cible(perso,lieu_cible)
			if len(T_verif)!=0:
				liste_lieu_cible = liste_lieu_cible.exclude(id=lieu_cible.id)
				#print(action.nom+' : '+lieu_cible.nom+' cible impossible :\n---'+'\n---'.join(T_verif))
	
	else : liste_lieu_cible = Lieu.objects.none()
	return liste_lieu_cible.order_by('lieu_parent__priorite_temp','priorite_temp')

def define_cible_resultat(action,perso):
	if action.cible_resultat :
		qst_resultat_cible = Resultat.objects.filter(active=True).filter(action=action).filter(lieu=perso.lieu).filter(fini=False)
		for resultat_cible in qst_resultat_cible :
			T_verif = resultat_cible.verif_resultat_cible(perso)
			if len(T_verif)!=0:
				qst_resultat_cible = qst_resultat_cible.exclude(id=resultat_cible.id)
	
	else : qst_resultat_cible = Resultat.objects.none()	
	return qst_resultat_cible.order_by('-priorite')

	
def define_cible_posture(action,perso):
	
	if action.cible_posture and perso.posture :
		qst_posture_cible = Posture.objects.filter(active=True).filter(categorie_combat=perso.posture.categorie_combat).exclude(id=perso.posture.id)

		for posture_cible in qst_posture_cible :
			T_verif = posture_cible.verif_posture_cible(perso)
			if len(T_verif)!=0:
				qst_posture_cible = qst_posture_cible.exclude(id=posture_cible.id)
				#print(action.nom+' : '+posture_cible.nom+' cible impossible :\n---'+'\n---'.join(T_verif))
	
	else : qst_posture_cible = Posture.objects.none()	
	return qst_posture_cible.order_by('-priorite')
	
#############################


def envoie_commande(joueur,perso,lieu,action,T_form,chance,date_debut,commande_precede):
	jeu = Jeu.objects.get(id=1)
	
	texte_init = T_form[0]
	T_persos_cible = T_form[1]
	T_lieux_cible = T_form[2]
	champ_recherche1 = T_form[3]
	champ_recherche2 = T_form[4]
	champ_texte = T_form[5]
	T_instant = T_form[6]
	posture_cible = T_form[7]
	resultat_cible = T_form[8]
	if len(T_form)>9 : num = T_form[9]
	else : num = 0
	
	active = True
	if commande_precede!=None : 
		active = False
	
	texte = texte_init
	
	#limitation des langages :
	qst_langage = Langage.objects.filter(active=True).exclude(nom_info='commun')
	for langage in qst_langage :
		if '<'+langage.nom_info+'>' in texte :
			if joueur.statut!='MJ' and (not perso.connait_langage(langage) or not langage.est_parle) :
				texte = texte.replace('<'+langage.nom_info+'>','').replace('</'+langage.nom_info+'>','')
	
	#special pour attaque de lieu :
	if action.nom_info == "attaquer_lieu_dplct" :
		action = commande.action = Action.objects.get(nom_info == "sedeplacer")
		champ_recherche1='attaquer_lieu'
	
	#petit délai pour corriger le texte
	if texte!='' and not (action.MJ_only and action.post_only) : date_debut = date_debut + timedelta(seconds=60*jeu.delai_edit)
	
	if not champ_recherche2 : champ_recherche2 = ""
	if not champ_recherche1 : champ_recherche1 = ""
	
	#Si avec objet
	objet = None
	if action.implique_objet :
		qst_objets_perso = perso.objets()
		objet = qst_objets_perso.filter(id=champ_recherche2)[0]
		champ_recherche2 = ''
	
	if '__' in action.nom_info :
		T_nom_info = action.nom_info.split('__')
		action = Action.objects.get(nom_info=T_nom_info[0])
		if champ_recherche2 == '' : champ_recherche2 = T_nom_info[1]
	if champ_recherche2 == '' and posture_cible : champ_recherche2 = posture_cible.nom_info
	 
	
	timedelta_delay = timedelta(hours=float(jeu.base_delay)*(action.delay/100))
	date_fin = date_debut+timedelta_delay
	
	dissimulation = perso.dissimulation
	if dissimulation==0 :
		if lieu.dissimulation>0 or lieu.ferme : dissimulation = dissimulation+1
	
	chance_reussite = action.chance_reussite
	
	jet = de(100)
	
	#espionnage
	# doit etre mis au moment de l'initialisation et non de la creation de la commande
	'''T_joueur_connaissant = []
	qst_commande_espionnage = Commande.objects.filter(action__nom_info='espionner').filter(active=True).filter(commence=True).filter(fini=False).filter(persos_cible=perso).filter(perso__lieu=lieu)
	for commande_espionnage in qst_commande_espionnage :
		for j in commande_espionnage.perso.joueur.all() :
			if not j in T_joueur_connaissant : T_joueur_connaissant.append(j)'''
			
	
	c = Commande.objects.create(\
	joueur = joueur, \
	perso = perso , \
	action = action , \
	lieu = lieu , \
	texte_post=texte, \
	dissimulation = dissimulation , \
	chance_reussite = chance_reussite , \
	bonus_reussite = chance , \
	date_debut = date_debut , \
	date_fin = date_fin , \
	num = num , \
	champ_recherche1 = champ_recherche1 , \
	champ_recherche2 = champ_recherche2 , \
	champ_texte = champ_texte , \
	instant_heure = T_instant[0] , \
	instant_jour = T_instant[1], \
	instant_mois = T_instant[2], \
	active = active, \
	commande_precede = commande_precede, \
	objet = objet, 
	jet = jet, \
	resultat_cible = resultat_cible)
	
	print(c)
	#c.desc = traduction_msg(c.action.msg_encours,c)
	#perso.last_commande = c
	#perso.save()
	
	'''for joueur_connaissant in T_joueur_connaissant :
		c.joueur_connaissant.add(joueur_connaissant)'''
	
	for perso_cible in T_persos_cible :
		c.persos_cible.add(perso_cible)
	
	for lieu_cible in T_lieux_cible :
		c.lieux_cible.add(lieu_cible)
	
	if c.texte_post!='' and not c.action.post_only :
		c.post = post(c,texte,"Normal")
	elif c.action.post_only :
		fonction = "init_"+c.action.nom_info.lower()
		globals()[fonction](c)
		
	if date_debut + timedelta(seconds=1) >= date_fin and not c.commande_precede and not c.action.post_only :
		INIT_commande(c)
	else :
		c.save()
		if active :
			T_verif = VERIF_COMMANDE(c)
			if len(T_verif) != 0 : erreur(c,T_verif)

#verifie si le Thread n'est pas en train d'executer la fonction onload en mm temps. si oui : attend 3s avant de relancer le onload
def onload():
	jeu = Jeu.objects.get(id=1)
	i=0
	while i<10 :
		if not jeu.lock_onload :
			i=100
		else :
			time.sleep(0.3)
			i=i+1
	onload2()
	if jeu.lock_onload :
		jeu.lock_onload = False
		jeu.save()
		


def onload2() :
	print(jeu.nom_info)
	print('\n## DEBUT LOAD PAGE : '+str(timezone.now()))
	date_now = timezone.now()
	#Debuter action	
	qst_commandes_init = Commande.objects.filter(active=True).filter(commence=False).filter(date_debut__lt=date_now).order_by('date_debut')
	first = True
	while qst_commandes_init or first :
		first = False
		
		#Debuter action	
		for commande in qst_commandes_init :
			#print("#INIT 1 "+str(timezone.now()))
			INIT_commande(commande)
			#print("#INIT 2 "+str(timezone.now()))
		
		#Finir action
		qst_commandes_end = Commande.objects.filter(active=True).filter(fini=False).filter(commence=True).filter(date_fin__lt=date_now).order_by('date_fin')
		for commande in qst_commandes_end :
			#print("#GO 1 "+str(timezone.now()))
			if Commande.objects.filter(id=commande.id).filter(fini=False).exists() :
				GO_COMMANDE(commande)
			#print("#GO 2 "+str(timezone.now()))
		
		#enchainer actions suivantes (action programmee)
		qst_commande_differe = Commande.objects.filter(active=False).filter(commence=False).filter(commande_precede__fini=True).order_by('commande_precede__date_fin')
		for commande_differe in qst_commande_differe :
			if (not commande_differe.active) and (not commande_differe.commence) and commande_differe.commande_precede and commande_differe.commande_precede.fini:
				commande_differe.active = True
				commande_differe.date_debut = date_now
				commande_differe.date_fin = date_now+timedelta(hours=float(jeu.base_delay)*(commande_differe.action.delay/100))
				INIT_commande(commande_differe)
		
		date_now = timezone.now()
		qst_commandes_init = Commande.objects.filter(active=True).filter(commence=False).filter(date_debut__lt=date_now).order_by('date_debut')
			
	
	
	#les effets
	qst_effets_perso = Effet_perso.objects.filter(commence=True).filter(fini=False).filter(date_fin__lt=date_now)
	print(qst_effets_perso)
	for e in qst_effets_perso :
		if e.eft.bonus_PV>0 and not e.eft.fonction_suivant : e.eft.fonction_suivant = 'guerison'
		if e.eft.fonction_suivant and e.eft.fonction_suivant!='':
			fonction = 'effet_'+e.eft.fonction_suivant
			globals()[fonction](e)
			
			if not e.fini and date_now > e.date_fin : e.fini=True
			
			'''try :
				e.date_fin = now+timedelta(hours=float(jeu.base_delay)*(e.eft.delai/100))
				fonction = 'effet_'+e.eft.fonction_suivant
				globals()[fonction](e)
			except :
				e.fini = True'''
		else : 
			e.fini = True
			e.save()
	
	
	#Supprimer anciennes commandes finie
	qst_commandes_kill = qst_commandes_end.filter(date_fin__lt=date_now-timedelta(hours=float(jeu.delay_suppr))).delete()
	
	print('\n## FIN LOAD PAGE : '+str(timezone.now()))
		
		
	

def VERIF_COMMANDE(commande):
	T_verif = []
	
	if (not commande.active) and (not commande.commence) and commande.commande_precede :
		
		commande.perso = prog_perso_temp(commande.commande_precede)
		#commande.perso.lieu = commande.perso.dernier_lieu_programme()
		commande.perso.occupe = None
		'''if commande.perso.lieu.taille <=1 : commande.perso.secteur = 1
		elif commande.commande_precede.action.nom_info == 'retrouver' :
			commande.perso.secteur = commande.commande_precede.persos_cible.all()[0].secteur
		else : commande.perso.secteur = 0'''
	
	if commande.lieu and commande.perso.lieu and commande.lieu != commande.perso.lieu : T_verif.append(commande.perso.nom+" est dans "+commande.perso.lieu.nom+" :  il ne peut pas faire l'action dans "+commande.lieu.nom)
	
	if len(T_verif)==0 :
		fonction = 'verif_'+commande.action.nom_info.lower()
		
		try :
			T_verif.extend(globals()[fonction](commande))
		except :
			txt_erreur = 'ERREUR : COMMANDE verif_'+commande.action.nom_info.lower()+' NON TROUVE'
			T_verif.append(txt_erreur)
	
	if len(T_verif)==0 :
		T_verif.extend(verif_action_base(commande))
	return T_verif

def INIT_commande(commande):
	#print("		INIT COMMANDE : "+str(commande.id)+" - "+str(timezone.now()))
	
	fonction = "init_"+commande.action.nom_info.lower()

	commande.commence = True
	
	resave_commande = False
	
	#lieu
	if commande.perso.lieu and commande.lieu and commande.lieu != commande.perso.lieu :
		a=0
		#commande.lieu = commande.perso.lieu
		#resave_commande = True
	
	#dissimulation
	dissimulation = commande.perso.dissimulation
	if dissimulation==0 :
		if commande.lieu.dissimulation>0 or commande.lieu.ferme : dissimulation = dissimulation+1
	if commande.dissimulation != dissimulation :
		 commande.dissimulation = dissimulation
		 resave_commande = True
	
	#date_fin
	timedelta_delay = timedelta(hours=float(jeu.base_delay)*(commande.action.delay/100))
	date_fin = commande.date_debut+timedelta_delay
	if commande.date_fin != date_fin :
		commande.date_fin = date_fin
		resave_commande = True
	
	#espionnage
	commande.joueur_connaissant.clear()
	qst_commande_espionnage = Commande.objects.filter(action__nom_info='espionner').filter(active=True).filter(commence=True).filter(fini=False).filter(persos_cible=commande.perso).filter(perso__lieu=commande.perso.lieu)
	for commande_espionnage in qst_commande_espionnage :
		for j in commande_espionnage.perso.joueur.all() :
			if not j in commande.joueur_connaissant : commande.joueur_connaissant.add(j)
	
	#resave	commande
	if resave_commande : commande.save()
			
	
	T_verif = VERIF_COMMANDE(commande)
	if len(T_verif)==0: 
		if commande.post :
			commande.post.active = True
			commande.post.created_date = timezone.now()
			commande.post.save()
		
		commande.desc = traduction_msg(commande.action.desc,commande)
		
		if commande.date_debut < commande.date_fin : # on evite de SAVE la commande si c'est instantanee
			globals()[fonction](commande)
			'''try :
				globals()[fonction](commande)
			except :
				txt_erreur = 'ERREUR : COMMANDE init_'+commande.action.nom.lower()+' NON TROUVE'
				erreur(commande,[txt_erreur])'''
			
			#if commande.action.appel_resultat : avertiMJ_resultat(commande)
			
			if Commande.objects.get(id=commande.id).commence == False :
				commande.save()
			
		else :
			GO_COMMANDE(commande)
			
			
	else : 
		erreur(commande,T_verif)


def GO_COMMANDE(commande):
	#print("		GO COMMANDE : "+commande.action.nom+" - "+str(timezone.now()))
	nom_info_action = commande.action.nom_info.lower()

	fonction = "go_"+nom_info_action
	
	commande.fini = True
	commande.save()
	T_verif = VERIF_COMMANDE(commande)
	if len(T_verif)==0: 
		globals()[fonction](commande)
		'''try :
			globals()[fonction](commande)
		except :
			txt_erreur = 'ERREUR : COMMANDE go_'+commande.action.nom.lower()+' NON TROUVE : '+fonction
			erreur(commande,[txt_erreur])'''
		if commande.action.appel_resultat :
			if commande.resultat and commande.resultat.active and not commande.resultat.fini : GO_RESULTAT(commande,commande.resultat)
			else : post_general(commande.joueur , commande.perso , commande.perso.lieu , commande.action.msg_fin , commande.action , 'info' , 100 , [] , [], True)
			
		
	else : 
		erreur(commande,T_verif)
	


def GO_RESULTAT(commande,resultat) :
	perso = commande.perso
	T_joueurs = perso.joueur.all()
	
	#definition si echec ou reussite
	T_echec = resultat.verif_reussite_resultat(perso)
	if len(T_echec)>0 and resultat.echec : resultat = resultat.echec

	if resultat.unique : resultat.fini = True
	resultat.save()
	for joueur in T_joueurs:
		if not objet_ds_manytomany(joueur,resultat.users_connaissants) : resultat.users_connaissants.add(joueur)
	
	
	if resultat.passage_trouve and resultat.passage_trouve.secret :
		lieu = resultat.passage_trouve
		for joueur in T_joueurs:
			if not objet_ds_manytomany(joueur,lieu.users_connaissants_place) : lieu.users_connaissants_place.add(joueur)
	
	for objet in resultat.objet_trouve():
		#creation des objets perso
		objet.perso = perso
		objet.reultat = None
		objet.save()
	
	if resultat.effet_recu :
		perso.prend_effet(resultat.effet_recu)
	
	if resultat.resultat_trouve and not resultat.possible_pour_tous :
		for joueur in T_joueurs:
			if not objet_ds_manytomany(joueur,resultat.resultat_trouve.users_possible) : resultat.resultat_trouve.users_possible.add(joueur)
	
	if resultat.perso_trouve and resultat.perso_trouve.dissimulation>0 :
		perso_cible = resultat.perso_trouve
		for joueur in T_joueurs:
			perso_cible.joueur_repere.add(joueur)
			
	if resultat.modif_PV != 0 :
		perso.PV = perso.PV + resultat.modif_PV
	
	if resultat.modif_gardes != 0 :
		perso.nbGardes = perso.nbGardes + resultat.modif_gardes
	
	if resultat.modif_troupes != 0 :
		perso.nbTroupes = perso.nbTroupes + resultat.modif_troupes
	
	perso.save()
	
	style = 'info'
	
	texte = traduction_msg(resultat.texte,commande)
	post_general(commande.joueur , perso , perso.lieu , texte , commande.action , style , 100 , [] , [] , True)
	
	for r in resultat.resultat_additionnel.all():
		if r.verif_resultat_cible(perso): GO_RESULTAT(commande,r)
	

def creation_resultat(T_form,commande):
	#T_form = [texte , public , unique , passage_trouve , objet_trouve , perso_trouve , attaquer_par , modif_PV , nom]
	texte = T_form[0]
	public = T_form[1]
	unique = T_form[2]
	passage_trouve = T_form[3]
	objet_trouve = T_form[4]
	perso_trouve = T_form[5]
	attaquer_par = T_form[6]
	modif_PV = T_form[7]
	nom = T_form[8]
	modif_gardes = T_form[9]
	modif_troupes = T_form[10]
	resultat_trouve = T_form[11]
	effet_recu = T_form[12]
	
	new_resultat = Resultat.objects.create(\
	action = commande.action,\
	nom = nom,\
	description = "",\
	texte = texte,\
	lieu = commande.lieu,\
	public = public,\
	unique = unique,\
	passage_trouve = passage_trouve,\
	perso_trouve = perso_trouve,\
	#attaquer_par = attaquer_par,\
	modif_PV = modif_PV,\
	modif_gardes = modif_gardes,\
	modif_troupes = modif_troupes,\
	resultat_trouve = resultat_trouve,\
	effet_recu = effet_recu,\
	)
	
	for obj in objet_trouve :
		etat = 1
		if obj.reparable : etat = 2
		
		o = Objet_perso.objects.create(\
		resultat = self, \
		obj = obj, \
		etat = etat,\
		)
	#	new_resultat.objet_trouve.add(obj)
	
	#resultat.save()
	commande.resultat = new_resultat
	commande.save()
	


def erreur(commande,T_verif):
	commande.erreur = True
	titre_erreur = 'Action "'+commande.action.nom+'" annulée pour '+commande.perso.nom
	texte_erreur = titre_erreur +" :\n"+'\n'.join(T_verif) 
	commande.desc = texte_erreur
	
	#si la commande qui se stoppe par une erreur a une commande parent : acheve la commande parent
	if commande.commande_parent_id and not commande.commande_parent.fini :
		
		commande.commande_parent.fini = True
		commande.commande_parent.save()
		'''
		fonction = "fin_"+ commande.commande_parent.action.nom_info.lower()
		try : globals()[fonction](commande)
		except :
			print('XXXXXXXXXXXXXXXXXXXXX')
			commande.commande_parent.fini = True
			commande.commande_parent.fini.save()'''
	
	
	commande.save()
	
	print(texte_erreur)
	post(commande,texte_erreur,"sys")
	
	if commande.texte_post and commande.texte_post!='':
		qst_joueur_MJ = Joueur.objects.filter(statut='MJ')
		texte_erreur_msg = texte_erreur+'\n\n'+commande.texte_post
		envoie_msg(qst_joueur_MJ.all()[0],[texte_erreur_msg,titre_erreur,[commande.joueur]],timezone.now())
	
	return HttpResponseRedirect('/forum/lieu/'+str(commande.lieu.id)+'/'+str(commande.perso.id)+'/1')



def avertiMJ(joueur,titre,texte) :
	qst_MJ = Joueur.objects.filter(statut='MJ')
	date = timezone.now()
	envoie_msg(commande.joueur,[texte,titre,qst_MJ.all()],date)
		
	
	
def envoie_msg(joueur,T_form,date):
	texte = T_form[0]
	titre = T_form[1]
	T_joueurs_cible = T_form[2]
	
	T_date_jeu = jeu.convert_date(date)
	date_jeu = format_date_jeu(T_date_jeu,jeu.format_date)
	
	msg = Message.objects.create(\
	joueur = joueur, \
	titre = titre , \
	texte = texte , \
	date_jeu=date_jeu , \
	created_date=date)
	
	#c.desc = traduction_msg(c.action.msg_encours,c)
	
	msg.joueurs_affiche.add(joueur)
	for joueur_cible in T_joueurs_cible :
		msg.joueurs_cible.add(joueur_cible)
		msg.joueurs_affiche.add(joueur_cible)
		msg.joueurs_nonlu.add(joueur_cible)
		
def perso_visible(joueur,perso):
	
	if not objet_ds_manytomany(joueur,perso.joueur) : # on ne peut voir la fiche d'un perso adverse que si on a un de nos perso qui le voit dans le meme lieu
		valide = False
		qst_persos_presents = Perso.objects.filter(active=True).filter(joueur=joueur).filter(lieu=perso.lieu)
		if len(qst_persos_presents)>0 : 
			if perso.dissimulation == 0 or objet_ds_manytomany(joueur,perso.joueur_repere) : 
				valide = True

	else : valide = True
	return valide
	
def langages_connus(perso):
	T_langage_connu = []
	qst_langage = Langage.objects.filter(active=True).exclude(id=1)
	for langage in qst_langage :
		if perso.valeur_competence(langage.competence)>=langage.niveau : T_langage_connu.append(langage)
	return T_langage_connu

	
def prog_perso_temp(commande):
	T_commandes = [commande]
	commande2 = commande
	while commande2.commande_precede :
		commande2 = commande2.commande_precede
		T_commandes.append(commande2)
		print(commande2)
	T_commandes.reverse()
	
	i=0
	for com in T_commandes:
		print(com)
		if i == 0 : perso = com.perso
		com.perso = perso
		fonction = 'prog_'+com.action.nom_info.lower()
		try : perso = globals()[fonction](com)
		except : a=0
		i=i+1
	return perso


	
def init_sedeplacer(commande):
	lieu_cible = commande.lieux_cible.all()[0]
	secteur = de(lieu_cible.taille)
	commande.num = secteur
	
	commande.save()
	commande.perso.occupe = commande
	commande.perso.save()
		
	if len(commande.perso.perso_accompagne.all())>0 :
		action_suivre = Action.objects.get(nom_info="sedeplacer_suivre")
		for suiveur in commande.perso.perso_accompagne.all():
			if suiveur.occupe_id : 
				suiveur.occupe.erreur = True
				suiveur.occupe.save()
			
			date_debut = commande.date_debut
			envoie_commande(commande.joueur,suiveur,commande.lieu,action_suivre,['',[commande.perso],[lieu_cible],'','','',[0,1,None],None,secteur],100,date_debut,None)
	
	
	
		
	#post(commande,commande.action.msg_init,"info")'''
	