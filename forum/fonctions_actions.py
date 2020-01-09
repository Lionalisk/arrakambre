#from django.utils import timezone
#from datetime import *
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Count

from .models import *


from .fonctions_base import *
from .fonctions_combat import *
from math import *

	
# STYLES POST :
# normal : post public
# msg : message prive entre perso
# cache : post qui n'est pas public (exemple, dans un espace ferme)
# cache2 : post qui a ete deliberemment dissimule
# info : post abrege qui peut decrire l'action d'un perso, ou peut etre un message RP du MJ
# sys : info HRP, personnel au joueur. Exemple : un message d'erreur

jeu = Jeu.objects.get(id=1)

def post(commande,texte,style):
	texte2 = traduction_msg(texte,commande)
	if commande.action.est_deplacement and texte == commande.action.msg_fin : texte2 = "#depart#"+texte2
	if commande.date_debut<=timezone.now() or style=='sys' : active = True
	else : active = False
	if style == 'sys' or style == "msg" : lieu = commande.perso.lieu
	else : lieu = commande.lieu
	
	post_final = post_general(commande.joueur,commande.perso,lieu,texte2,commande.action,style,commande.dissimulation,commande.joueur_connaissant.all(),commande.persos_cible.all(),active)
	return post_final
	
def post_MJpersonnage(perso,texte,dissimulation,T_persos_cible):
	joueur = Joueur.objects.get(pk=1)
	if dissimulation == 200 : style = "sys"
	else : style = "info"
	
	T_joueurs_connaissant = []
	for p in T_persos_cible :
		for j in p.joueur.all():
			if not j in T_joueurs_connaissant : T_joueurs_connaissant.append(j)
	
	post_general(joueur,perso,perso.lieu,texte,Action.objects.get(pk=1),style,dissimulation,perso.joueur.all(),T_persos_cible,True)

def post_MJ(lieu,texte,dissimulation,T_persos_cible):
	joueur = Joueur.objects.get(pk=1)
	perso = Perso.objects.get(pk=1)
	if dissimulation == 200 : style = "sys"
	else : style = "info"
	
	T_joueurs_connaissant = []
	'''for p in T_persos_cible :
		for j in p.joueur.all():
			if not j in T_joueurs_connaissant : T_joueurs_connaissant.append(j)'''
	
	post_general(joueur,perso,lieu,texte,Action.objects.get(pk=1),style,dissimulation,T_joueurs_connaissant,T_persos_cible,True)
	

	
def post_general(joueur,perso,lieu,texte,action,style,dissimulation_commande,T_commande_joueurs_connaissants,T_persos_cible,active):
	if texte and texte !='' :
		
		#dissimulation_commande < 10 : cas d'un post dans un lieu ferme ou d'un lieu qui dissimule les actions : sera visible par les persos presents
		#dissimulation_commande >=10 : cas d'un post cree par un perso cache
		
		dissimulation = 0
		if dissimulation_commande == 0 and (lieu.dissimulation > 0 or lieu.ferme) : dissimulation_commande = 1
		elif action.est_deplacement and dissimulation_commande == 1 and lieu.dissimulation == 0 and not lieu.ferme : dissimulation_commande = 0
		
		if (dissimulation_commande > 0 and dissimulation_commande<10) : dissimulation = 1
		if dissimulation_commande >= 10 and dissimulation_commande<100 : dissimulation = int(floor(dissimulation_commande/10))
		if dissimulation_commande>=100 : dissimulation = dissimulation_commande
		
		if style == "sys" :
			dissimulation = 200
			dissimulation_commande = 200
		if style == "msg" :
			dissimulation = 100
			dissimulation_commande = 100
		
		if style == '' : style = 'normal'
		if style == 'normal' and dissimulation_commande>0 : style = 'cache'
		if style == 'cache' and dissimulation_commande>=10 : style = 'cache2'
		
		if perso.id == 1 and (style!='sys') : style == 'info'
		
		T_joueur_connaissant = []
		
		if dissimulation>0 :
			T_joueur_connaissant.append(joueur)
			for j in perso.joueur.all():
				if not j in T_joueur_connaissant : T_joueur_connaissant.append(j)
		
		if dissimulation>0 and (style != "sys" or perso.id == 1) :
			if len(T_commande_joueurs_connaissants)>0 :
				for j in T_commande_joueurs_connaissants :
					T_joueur_connaissant.append(j)
					#post.joueur_connaissant.add(j)
				
			#joueurs_connaissant = post.joueur_connaissant.all()
			

			if dissimulation_commande<100 and dissimulation_commande>0 :
				persos_ds_lieu = Perso.objects.filter(lieu=lieu).filter(en_combat=False).filter(prisonnier=False).filter(PV__gt=0)
				for perso_ds_lieu in persos_ds_lieu :
					joueurs_du_perso = perso_ds_lieu.joueur.all()
					for joueur_du_perso in joueurs_du_perso :
						if not joueur_du_perso in T_joueur_connaissant :
							if (dissimulation_commande==1 and perso_ds_lieu.secteur==perso.secteur) or (objet_ds_manytomany(joueur_du_perso,perso.joueur_repere)): 	# cas du lieu ferme : ajout dans post.joueur_connaissant tous les persos presents dans le mm lieu
								T_joueur_connaissant.append(joueur_du_perso)
			
		
		depart_lieu = False
		if style=="info" and (action.est_deplacement or action.nom_info=='secacher') and texte[:8]=="#depart#" :
			depart_lieu = True
			texte = texte.replace("#depart#","")
		
		post = Post.objects.create(joueur = joueur ,\
		texte = texte,\
		lieu = lieu ,\
		perso = perso ,\
		style = style,\
		action = action ,\
		dissimulation = dissimulation ,\
		depart_lieu = depart_lieu,\
		active = active)
		
		for joueur_connaissant in T_joueur_connaissant :
			post.joueur_connaissant.add(joueur_connaissant)
			
		if style == 'msg' :
			for perso_cible in T_persos_cible:
				post.add_persos_cible(perso_cible)
			post.save()
		return post


def renvoie_commande(c,bonus_chance_reussite):
	date_debut = timezone.now()
	c.texte_post = ""
	c.jet = 0
	c.chance_reussite = c.chance_reussite
	c.bonus_reussite = bonus_chance_reussite
	c.created_date = date_debut
	c.date_debut = date_debut
	c.date_fin = c.date_debut+timedelta(hours=float(jeu.base_delay)*(c.action.delay/100))
	c.commence = False
	c.fini = False
	c.erreur = False
	
	c.save()
	

	
def verif_action_base(commande):
	if commande.action.action_parent_id : action = commande.action.action_parent
	else : action = commande.action
	
	perso = commande.perso
	T_resultat = []
	
	if perso.id == 1 : perso.lieu = commande.lieu
	
	'''if (not commande.active) and (not commande.commence) and commande.commande_precede :
		perso.lieu = perso.dernier_lieu_programme()
		perso.occupe = None
		if commande.perso.lieu.taille <=1 : commande.perso.secteur = 1
		elif commande.commande_precede.action.nom_info == 'retrouver' :
			perso.secteur = commande.commande_precede.persos_cible.all()[0].secteur
		else : commande.perso.secteur = 0'''
	
	T_verif = action.verif(perso)
	if len(T_verif)>0 : T_resultat.append('Erreur :\n'+'\n'.join(T_verif))

	if action.cible_perso :
		persos_cible = commande.persos_cible.all()
		if not persos_cible : T_resultat.append('Erreur : personnage cible non renseigné')
		else :
			perso_cible = persos_cible[0]
			T_verif = action.verif_perso_cible(perso,perso_cible)
			if len(T_verif)>0 : T_resultat.append('Erreur :\n'+'\n'.join(T_verif))
			
	if action.cible_persos :
		persos_cible = commande.persos_cible.all()
		if not persos_cible :  T_resultat.append('Erreur : personnage(s) cible non renseigné(s)')
		else :
			for p_cible in persos_cible :
				T_verif = action.verif_perso_cible(perso,p_cible)
				if len(T_verif)>0 :  T_resultat.append('Erreur :\n'+'\n'.join(T_verif))

	if action.cible_lieu :
		lieux_cible = commande.lieux_cible.all()
		if not lieux_cible :  T_resultat.append('Erreur : lieu cible non renseigné')
		else : 
			lieu_cible = lieux_cible[0]
			
			T_verif = action.verif_lieu_cible(perso,lieu_cible)
			if len(T_verif)>0 :  T_resultat.append('Erreur :\n'+'\n'.join(T_verif))

	if action.cible_lieux :
		lieux_cible = commande.lieux_cible.all()
		if not lieux_cible :  T_resultat.append('Erreur : lieu(x) cible non renseigné(s)')
		else :
			for l_cible in lieux_cible :
				#print(commande)
				T_verif = action.verif_lieu_cible(perso,l_cible)
				if len(T_verif)>0 :  T_resultat.append('Erreur :\n'+'\n'.join(T_verif))
				
	return T_resultat	

	
# VERIF : renvoie un TAB avec les erreurs. PAS DE SAVE !
# INIT : SAVE la commande (uniquement si elle n'est pas instantanee) avec chance de reussite et jets / rendre perso occupe si besoin et le SAVE
# GO : SAVE les consequences de l'action. Ne pas oublier de poster ce qu'il faut

############################################# AUTRE

def verif_autre(commande):

	T_verif = []
	return T_verif

def init_autre(commande):
	commande.save()
	if not commande.perso.occupe:
		commande.perso.occupe = commande
		commande.perso.save()

def go_autre(commande):
	
	a=0
	



############################################# SEDEPLACER

def verif_sedeplacer(commande):
	joueur = commande.joueur
	perso = commande.perso
	lieu_depart = commande.perso.lieu
	lieu_arrive = commande.lieux_cible.all()[0]
	
	T_verif = []
	if perso.PV <= 0 or not perso.vivant : T_verif.append(perso.get_nom()+' est trop blessé pour se déplacer')
	if not objet_ds_manytomany(lieu_arrive,lieu_depart.passages) : T_verif.append("le lieu de départ ne propose aucun passage vers le lieu d'arrivé")
	
	if lieu_arrive.ferme and (lieu_arrive.maison!=perso.maison or not perso.maison_id) and not objet_ds_manytomany(perso,lieu_arrive.perso_autorise) : 
		if perso.dissimulation==0:
			T_verif.append(lieu_arrive.nom+" est fermé pour "+perso.get_nom()+". Le maître des lieux a été averti de votre volonté d'entrer.")
			texte = "Les gardes du lieu informent que "+perso.get_nom()+" a demandé à entrer dans "+lieu_arrive.nom
			post_MJ(lieu_arrive,texte,0,[])
		else : T_verif.append(lieu_arrive.nom+" est fermé pour "+perso.get_nom())
	
	for prisonnier in perso.perso_prisonnier.all():
		if prisonnier.hote_id : T_verif.append("Le prisonnier "+prisonnier.get_nom()+" ne peut pas quitter "+prisonnier.hote.get_nom()+". Il doit être libéré si vous voulez vous déplacer.")
	
	return T_verif

# init_sedeplacer(commande) se trouve exceptionellement dans fonctions.py
'''def init_sedeplacer(commande):
	commande.save()
	commande.perso.occupe = commande
	commande.perso.save()
	
	#post(commande,commande.action.msg_init,"info")'''

def go_sedeplacer(commande):
	
	texte = commande.action.msg_encours
	texte2 = commande.action.msg_fin
	post(commande,texte2,"info")
	
	#commande.perso.occupe = None
	commande.perso.lieu = commande.lieu = commande.lieux_cible.all()[0]
	commande.perso.secteur = commande.num
	
	#si le perso est caché, il perd son bonus de dissimulation dû à une action (cas de sortie d'une intrusion ou d'une embuscade)
	if commande.perso.dissimulation > 0 :
		commande.perso.dissimulation = int(commande.perso.dissimulation/10)*10
		if commande.perso.lieu.dissimulation>0 : commande.perso.dissimulation = commande.perso.dissimulation+10
	
	
	commande.perso.save()
	
	if commande.action.nom_info == 'sedeplacer_suivre' : txt_persos_ds_mm_secteur = ''
	else :
		qst_persos_ds_mm_secteur = Perso.objects.filter(active=True).filter(lieu=commande.perso.lieu).filter(secteur=commande.perso.secteur).exclude(id=commande.perso.id).filter(dissimulation=0)
		if commande.perso.leader :
			qst_persos_ds_mm_secteur = qst_persos_ds_mm_secteur.exclude(id = commande.perso.leader.id)
		if commande.perso.geolier :
			qst_persos_ds_mm_secteur = qst_persos_ds_mm_secteur.exclude(id = commande.perso.geolier.id)
		txt_persos_ds_mm_secteur = txt_liste(qst_persos_ds_mm_secteur)
	
	if commande.champ_recherche1=="attaquer_lieu" :
		#creation de la commande attaquer_lieu
		action_attaquer = Action.objects.get(nom_info="attaquer_lieu")
		date_debut = timezone.now()
		date_fin = date_debut+timedelta(hours=float(jeu.base_delay)*(action_attaquer.delay/100))
		c = Commande.objects.create(\
		joueur = commande.joueur, \
		perso = commande.perso , \
		action = action_attaquer , \
		lieu = commande.lieu , \
		dissimulation = 0, \
		date_debut = date_debut , \
		date_fin = date_fin)
		
	
	else :
		if txt_persos_ds_mm_secteur=='' : txt_supp = ''
		else :
			if commande.perso.lieu.taille>1 : txt_supp = " et y croise par hasard "+txt_persos_ds_mm_secteur
			else : txt_supp = " et y rencontre "+txt_persos_ds_mm_secteur
		
		#message arrive
		post(commande,texte+txt_supp,"info")
	
def prog_sedeplacer(commande):
	commande.perso.lieu = commande.lieux_cible.all()[0]
	if commande.perso.lieu.taille <= 1 : commande.perso.secteur=1
	else : commande.perso.secteur=0
	return commande.perso
	
############################################# SEDEPLACER_SUIVRE

def verif_sedeplacer_suivre(commande):
	T_verif = verif_sedeplacer(commande)
	return T_verif

def init_sedeplacer_suivre(commande):
	commande.save()
	commande.perso.occupe = commande
	commande.perso.save()
	
	#post(commande,commande.action.msg_init,"info")'''

def go_sedeplacer_suivre(commande):
	
	if commande.perso.leader.lieu != commande.lieux_cible.all()[0]:
		commande.perso.save()
	else :
		go_sedeplacer(commande)

def prog_sedeplacer_suivre(commande):
	commande.perso = prog_sedeplacer(commande)
	return commande.perso
	
############################################# PARLER				

def verif_parler(commande):
	T_verif = []
	if commande.perso.PV<0 : T_verif.append(commande.perso+" est mort")
	if not commande.texte_post or commande.texte_post=='' : T_verif.append("Pas de texte à poster")
	'''if commande.lieu != commande.perso.lieu :
		commande.lieu = commande.perso.lieu
		commande.save()'''
			

	return T_verif

def init_parler(commande):
	if not commande.post :
		commande.post = post(commande,commande.texte_post,"Normal")
		#commande.save()

def go_parler(commande):
	if commande.post :
		commande.post.active = True
		commande.post.created_date = timezone.now()
		commande.post.save()
		
############################################# POSTMJ				

def verif_postmj(commande):
	T_verif = []
	return T_verif

def init_postmj(commande):
	a=0

def go_postmj(commande):
	
	if commande.texte_post!='':
		post_MJ(commande.lieu,commande.texte_post,0,[])
		
############################################# MSG MJ				

def verif_msgmj(commande):
	T_verif = []
	return T_verif

def init_msgmj(commande):
	a=0

def go_msgmj(commande):
	
	'''T_joueurs_connaissants = []
	for perso_cible in commande.persos_cible.all():
		for joueur in perso_cible.joueur.all() :
			if not joueur in T_joueurs_connaissants : T_joueurs_connaissants.append(joueur)
	
	for jc in T_joueurs_connaissants : commande.joueur_connaissant.add(jc)
	commande.dissimulation=100'''
	if commande.texte_post!='':
		post_MJ(commande.lieu,commande.texte_post,100,commande.persos_cible.all())
	
	
############################################# MSG MJ HRP			

def verif_msgmjhrp(commande):
	T_verif = []
	return T_verif

def init_msgmjhrp(commande):
	a=0

def go_msgmjhrp(commande):
	
	'''T_joueurs_connaissants = []
	for perso_cible in commande.persos_cible.all():
		for joueur in perso_cible.joueur.all() :
			if not joueur in T_joueurs_connaissants : T_joueurs_connaissants.append(joueur)
	
	for jc in T_joueurs_connaissants : commande.joueur_connaissant.add(jc)
	commande.dissimulation=200'''
	
	if commande.texte_post!='':
		post_MJ(commande.lieu,commande.texte_post,200,commande.persos_cible.all())
		
############################################# MURMURER				

def ajuste_persos_cible_murmurer(commande):
	persos_cible = commande.persos_cible.all()
	for perso_cible in persos_cible:
		if perso_cible.PV<1: persos_cible.exclude(id=perso_cible.id)
		elif perso_cible.lieu!=commande.perso.lieu or perso_cible.secteur!=commande.perso.secteur : persos_cible.exclude(id=perso_cible.id)
		elif perso_cible.en_combat: persos_cible.exclude(id=perso_cible.id)
		elif perso_cible.geolier_id and perso_cible.geolier!=commande.perso: persos_cible.exclude(id=perso_cible.id)
		elif perso_cible.dissimulation>0 and not manytomany_ds_manytomany(commande.perso.joueur,perso_cible.joueur_repere): persos_cible.exclude(id=perso_cible.id)
	return persos_cible
	
	
def verif_murmurer(commande):
	persos_cible = commande.persos_cible.all()
	
	if commande.fini :
		
		persos_cible = ajuste_persos_cible_murmurer(commande)
		'''
		for perso_cible in persos_cible:
			if perso_cible.PV<1: persos_cible.exclude(id=perso_cible.id)
			elif perso_cible.lieu!=commande.perso.lieu or perso_cible.secteur!=commande.perso.secteur : persos_cible.exclude(id=perso_cible.id)
			elif perso_cible.en_combat: persos_cible.exclude(id=perso_cible.id)
			elif perso_cible.geolier_id and perso_cible.geolier!=commande.perso: persos_cible.exclude(id=perso_cible.id)
			elif perso_cible.dissimulation>0 and not manytomany_ds_manytomany(commande.perso.joueur,perso_cible.joueur_repere): persos_cible.exclude(id=perso_cible.id)
		'''
		#commande.save()
	
	T_verif = []
	if commande.perso.PV<1 : T_verif.append(commande.perso+" est mort ou inconscient")
	if not commande.texte_post or commande.texte_post=='' : T_verif.append("Pas de texte")
	if not persos_cible.exists() : T_verif.append("Pas d'interlocuteur")
	
	comp_aura = Competence.objects.get(nom_info="aura")
	valeur_aura = commande.perso.valeur_competence(comp_aura)
	nb_interlocuteur_max = valeur_aura+1
	if len(persos_cible) > nb_interlocuteur_max : T_verif.append(commande.perso.get_nom()+" N'a pas assez dans la Compétence "+comp_aura.nom+" pour échanger discrétement avec autant de personnages. Son nombre d'interlocuteur est limité à <b>"+str(nb_interlocuteur_max)+"</b>")
	
	return T_verif

def init_murmurer(commande):
	if not commande.post :
		persos_cible = ajuste_persos_cible_murmurer(commande)
		'''
		persos_cible = commande.persos_cible.all()
		
		for perso_cible in persos_cible:
			if perso_cible.PV<1: persos_cible.exclude(id=perso_cible.id)
			elif perso_cible.lieu!=commande.perso.lieu or perso_cible.secteur!=commande.perso.secteur : persos_cible.exclude(id=perso_cible.id)
			elif perso_cible.en_combat: persos_cible.exclude(id=perso_cible.id)
			elif perso_cible.geolier_id and perso_cible.geolier!=commande.perso: persos_cible.exclude(id=perso_cible.id)
			elif perso_cible.dissimulation>0 and not manytomany_ds_manytomany(commande.perso.joueur,perso_cible.joueur_repere): persos_cible.exclude(id=perso_cible.id)
		'''
		
		for perso_cible in persos_cible.all():
			for joueur in perso_cible.joueur.all() :
				if not joueur in commande.joueur_connaissant.all() : commande.joueur_connaissant.add(joueur)
		
		commande.dissimulation=100

		commande.post = post(commande,commande.texte_post,"msg")
		commande.save()

def go_murmurer(commande):
	if commande.post :
		commande.post.delete()
		
		persos_cible = ajuste_persos_cible_murmurer(commande)
		'''
		persos_cible = commande.persos_cible.all()
		
		for perso_cible in persos_cible:
			if perso_cible.PV<1: persos_cible.exclude(id=perso_cible.id)
			elif perso_cible.lieu!=commande.perso.lieu or perso_cible.secteur!=commande.perso.secteur : persos_cible.exclude(id=perso_cible.id)
			elif perso_cible.en_combat: persos_cible.exclude(id=perso_cible.id)
			elif perso_cible.geolier_id and perso_cible.geolier!=commande.perso: persos_cible.exclude(id=perso_cible.id)
			elif perso_cible.dissimulation>0 and not manytomany_ds_manytomany(commande.perso.joueur,perso_cible.joueur_repere): persos_cible.exclude(id=perso_cible.id)
		'''	
		
		for perso_cible in persos_cible.all():
			for joueur in perso_cible.joueur.all() :
				if not joueur in commande.joueur_connaissant.all() : commande.joueur_connaissant.add(joueur)
		
		
		texte = commande.action.msg_fin
		post(commande,texte,"info")
		
		commande.post = post(commande,commande.texte_post,"msg")
		
		
		
############################################# ANNULER				

def verif_annuler(commande):
	
	T_verif = []
	if not commande.perso.occupe_id : T_verif.append(commande.perso.get_nom()+" n'est pas en train de faire une action")
	elif not commande.perso.occupe.action.annulable : T_verif.append(commande.perso.occupe.action.nom+" n'est pas une action qui peut être annulable")
	if commande.perso.en_combat : T_verif.append(commande.perso.get_nom()+" est en train de combattre")
	
	
	return T_verif

def init_annuler(commande):
	a=0

def go_annuler(commande):
	if commande.perso.occupe.action.annulable :
		if commande.perso != commande.perso.occupe.perso :
			texte = commande.perso.get_nom()+" a annulé l'action de "+commande.perso.occupe.action.nom+" de "+commande.perso.occupe.perso.get_nom()
			post_MJpersonnage(commande.perso.occupe.perso,texte,200,[])
		
		qst_accompagnant = Perso.objects.filter(leader=commande.perso).filter(occupe__action__nom_info='sedeplacer_suivre')
		for accompagnant in qst_accompagnant :
			accompagnant.occupe.delete()
			accompagnant.occupe = None
			accompagnant.last_commande = None
			accompagnant.save()
		
		commande.perso.occupe.delete()
		commande.perso.occupe = None
		commande.perso.last_commande = None
		commande.perso.save()
		commande.delete()

		
		

############################################# ADMINISTRER				

def verif_administrer(commande):
	
	T_verif = []
	return T_verif

def init_administrer(commande):
	commande.save()
	commande.perso.occupe = commande
	commande.perso.save()
	
	texte = commande.action.msg_init
	post(commande,texte,"msg")

def go_administrer(commande):
	lieu = commande.lieu
	perso = commande.perso
	maison = commande.perso.maison
	
	maison.prestige = maison.prestige + lieu.gain_administration
	maison.save()
	
	texte = commande.action.msg_fin
	post(commande,texte.replace('#pts#',str(lieu.gain_administration)),"sys")


############################################# EMPECHER				

def verif_empecher(commande):
	perso_cible = commande.persos_cible.all()[0]
	T_verif = []
	if not perso_cible.occupe_id : T_verif.append(commande.perso_cible.get_nom()+" n'est pas en train de faire une action")
	elif perso_cible.occupe.fini : T_verif.append(commande.perso_cible.get_nom()+" a déjà fini son action")
	if commande.perso.en_combat : T_verif.append(commande.perso_cible.get_nom()+" est en train de combattre")

	return T_verif

def init_empecher(commande):
	commande.save()
	commande.perso.occupe = commande

def go_empecher(commande):
	perso_cible = commande.persos_cible.all()[0]
	commande_a_empecher = perso_cible.occupe
	commande_a_empecher.erreur = True
	commande_a_empecher.desc = "L'action a été empéché par "+commande.perso.get_nom()
	commande_a_empecher.save()
	commande.perso.save()
	
	
############################################# SEFAIRESOIGNER	
	
def verif_sefairesoigner(commande):

	T_verif = []
	
	if not objet_ds_manytomany(commande.action.condition_atelier,commande.perso.lieu.atelier) :  T_verif.append(commande.perso.get_nom()+" n'est pas dans un lieu adequat ; "+commande.perso.lieu.nom+" ne possede pas de "+commande.action.condition_atelier.nom)
	if commande.perso.PV>=3 : T_verif.append(commande.perso.get_nom()+" n'est pas suffisamment blessé")
	if commande.perso.PV<0 :  T_verif.append(commande.perso.get_nom()+" est trop blessé pour être soigné")
	
	return T_verif

def init_sefairesoigner(commande):
	commande.save()
	
	commande.perso.occupe = commande
	commande.perso.en_soin = True
	commande.perso.save()

	texte = commande.action.msg_init
	post(commande,texte,"info")

def go_sefairesoigner(commande):
	perso_blesse = commande.perso
	perso_blesse.PV = perso_blesse.PV+1
	perso_blesse.en_soin = False
	perso_blesse.save()
	
	texte = commande.action.msg_fin
	texte = texte.replace("#1#",perso_blesse.etat_sante.nom)
	post(commande,texte,"info")


############################################# SOIGNER	
	
def verif_soigner(commande):
	perso = commande.perso
	perso_cible = commande.persos_cible.all()[0]
	niveau_soin = perso.valeur_competence(commande.action.condition_competence)
	
	T_verif = []
	
	if perso.occupe_id and not perso.occupe.fini : T_verif.append(perso.get_nom()+' est en train de faire une autre action : '+perso.occupe.action.nom)
	if perso.PV <= 0 or not perso.vivant : T_verif.append(perso.get_nom()+' est trop blessé pour soigner')
	if perso.lieu != perso_cible.lieu : T_verif.append(perso.get_nom()+' est dans '+perso.lieu.nom+' alors que '+perso_cible.get_nom()+' est dans '+perso_cible.lieu.nom)
	elif perso.secteur != perso_cible.secteur : T_verif.append(perso.get_nom()+" n'est pas dans le même secteur ("+str(perso.secteur)+") que "+perso_cible.get_nom()+" ("+str(perso_cible.secteur)+")")
	if niveau_soin <1 : T_verif.append(perso.get_nom()+" n'a que "+str(niveau_soin)+" en soin")
	if perso_cible.PV >= 3 : T_verif.append(perso_cible.get_nom()+" n'a pas besoin d'être soigné avec "+str(perso_cible.PV)+" PV")
	if perso_cible.occupe_id and perso_cible.occupe !=commande and not perso_cible.occupe.fini : T_verif.append(perso_cible.get_nom()+" est trop occupé pour se faire soigner")
	#if chance_reussite==0 : T_verif.append("Aucune chance de réussite")
	
	return T_verif

def reussite_soigner(commande):
	perso_soigneur = commande.perso
	perso_cible = commande.persos_cible.all()[0]
	niveau_soin = perso_soigneur.valeur_competence(commande.action.condition_competence)
	chance_reussite_init = commande.chance_reussite
	
	chance_reussite = 0
	if niveau_soin==1 :
		if perso_cible.PV == 2 : chance_reussite = 80
		if perso_cible.PV == 1 : chance_reussite = 10
		if perso_cible.PV == 0 : chance_reussite = 60
	elif niveau_soin==2 :
		if perso_cible.PV == 2 : chance_reussite = 100
		if perso_cible.PV == 1 : chance_reussite = 60
		if perso_cible.PV == 0 : chance_reussite = 80
	elif niveau_soin>=3 :
		if perso_cible.PV == 2 : chance_reussite = 100
		if perso_cible.PV == 1 : chance_reussite = 100
		if perso_cible.PV == 0 : chance_reussite = 100
	
	chance_reussite = chance_reussite + commande.bonus_reussite
	return chance_reussite
	
def init_soigner(commande):
	perso_soigneur = commande.perso
	perso_cible = commande.persos_cible.all()[0]
	niveau_soin = perso_soigneur.valeur_competence(commande.action.condition_competence)
	
	'''chance_reussite = reussite_soigner(commande)
	commande.bonus_reussite = 0
	
	commande.chance_reussite = chance_reussite
	if commande.jet == 0 : 
		commande.jet = de(100)
		print('jet de soin : '+str(commande.jet)+'/100')
	'''
	if niveau_soin<2 and perso_cible.PV==1 :
		texte = perso_soigneur.get_nom()+" n'a pas le niveau de médecine nécessaire pour soigner le type de blessure qu'endure "+perso_cible.get_nom()
		if perso_soigneur == perso_cible : texte = perso_soigneur.get_nom()+" n'a pas le niveau de médecine nécessaire pour soigner ce type de blessure"
		post(commande,texte,"info")
		commande.fini = True
		commande.save()
	
	else :
		commande.desc = traduction_msg(commande.action.desc,commande)
		commande.save()
		perso_soigneur.occupe = commande
		if perso_cible == perso_soigneur : perso_soigneur.en_soin = True
		perso_soigneur.save()
		
		if perso_cible != perso_soigneur : 
			perso_cible.occupe = commande
			perso_cible.en_soin = True
			perso_cible.save()
		
		if perso_soigneur == perso_cible : texte = perso_soigneur.get_nom()+" est en train de se soigner"
		else : texte = commande.action.msg_init
		post(commande,texte,"info")

def go_soigner(commande):
	#init

	perso_soigneur = commande.perso
	perso_blesse = commande.persos_cible.all()[0]
	niveau_soin = perso_soigneur.valeur_competence(commande.action.condition_competence)
	
	
	#if (perso_blesse==perso_soigneur) or (perso_blesse.occupe_id and perso_blesse.occupe == commande) :
	if perso_blesse.occupe_id and perso_blesse.occupe == commande :
		perso_blesse.occupe = None
		perso_blesse.en_soin = False
		perso_blesse.save()
	
	if niveau_soin<2 and perso_blesse.PV==1 :
		texte = perso_soigneur.get_nom()+" n'a pas le niveau de médecine nécessaire pour soigner le type de blessure qu'endure "+perso_blesse.get_nom()
		if perso_soigneur == perso_blesse : texte = perso_soigneur.get_nom()+" n'a pas le niveau de médecine nécessaire pour soigner ce type de blessure"
		post(commande,texte,"info")
	else :
		perso_blesse.PV = perso_blesse.PV+1
		perso_blesse.occupe = None
		perso_blesse.save()
		
		texte = commande.action.msg_fin
		if perso_soigneur == perso_blesse : texte = perso_soigneur.get_nom()+" s'est soigné : il est maintenant #1#"
		texte = texte.replace("#1#",perso_blesse.etat_sante.nom)
		
		post(commande,texte,"info")
		
	
	
	
	'''chance_reussite = reussite_soigner(commande)
	
	succes = False
	jet = commande.jet
	if jet == 0 : jet = de(100)
	print('jet de soin : '+str(jet)+' sur seuil de '+str(chance_reussite)+'/100')
	if jet <= chance_reussite : succes = True
	
	# faire les consequence de l'action :
	if succes :
		perso_blesse.PV = perso_blesse.PV+1
		perso_blesse.occupe = None
		perso_blesse.save()

		texte = commande.action.msg_fin
		texte = texte.replace("#1#",perso_blesse.etat_sante.nom)
		post(commande,texte,"info")
	
	
	
	if not succes :
		texte = "Tentative de soins sur "+perso_blesse.nom+"\nEchec du jet de médecine : "+str(jet)+" sur "+str(chance_reussite)+"% de chance"
		post(commande,texte,"sys")
		
		renvoie_commande(commande,20)'''
			

	
############################################# FERMER	
	
def verif_fermer(commande):

	T_verif = []
	
	
	return T_verif

def init_fermer(commande):
	commande.save()
	commande.perso.occupe = commande
	commande.perso.save()
	
def go_fermer(commande):
	lieu_cible = commande.perso.lieu
	T_persos_cible = commande.champ_recherche1.split(',')
	#print(T_persos_cible)
	lieu_cible.ferme = True
	lieu_cible.perso_autorise.clear()
	for p in T_persos_cible :
		if p!='' : 
			qst_perso_invite = Perso.objects.filter(nom = p)
			for invite in qst_perso_invite.exists() :
				lieu_cible.perso_autorise.add(invite)
	lieu_cible.save()
	
	texte = commande.action.msg_fin
	post(commande,texte,"info")
	
############################################# OUVRIR	
	
def verif_ouvrir(commande):

	T_verif = []
	
	
	return T_verif

def init_ouvrir(commande):
	commande.save()
	commande.perso.occupe = commande
	commande.perso.save()

def go_ouvrir(commande):
	lieu_cible = commande.perso.lieu
	
	lieu_cible.ferme = False
	lieu_cible.perso_autorise.clear()
	lieu_cible.save()
	
	texte = commande.action.msg_fin
	post(commande,texte,"info")

############################################# RECRUTEGARDE
	
def verif_recrutegarde_perso(commande):
	perso = commande.perso
	T_verif = []
	
	if perso.nbGardes>=perso.gardes_MAX() : T_verif.append(perso.get_nom()+" n'a pas les moyens de commander plus que "+str(perso.gardes_MAX())+" gardes")
	
	return T_verif

def verif_recrutegarde_qg(commande):
	lieu = commande.perso.lieu
	T_verif = []
	
	if lieu.hote.nbGardes>=lieu.hote.gardes_MAX() : T_verif.append(lieu.nom+" ne peut pas avoir plus de "+str(lieu.hote.gardes_MAX())+" gardes")
	
	return T_verif

def init_recrutegarde_qg(commande):
	init_recrutegarde_perso(commande)
	
def go_recrutegarde_qg(commande):
	go_recrutegarde_perso(commande)
	
def init_recrutegarde_perso(commande):
	#commande.jet = de(100)
	commande.save()
	commande.perso.occupe = commande
	commande.perso.save()
	
	texte = commande.action.msg_init
	post(commande,texte,"info")
	
def go_recrutegarde_perso(commande):
	chance_reussite = commande.chance_reussite + commande.bonus_reussite
	
	succes = False
	jet = commande.jet
	if jet == 0 : jet = de(100)
	if jet<=chance_reussite : succes = True
	
	if succes :
		commande.perso.nbGardes = commande.perso.nbGardes+1
		commande.perso.save()
	
		texte = commande.action.msg_fin
		post(commande,texte,"info")
		
	else :
		texte = "Tentative de recrutement :\nEchec du jet : "+str(jet)+" sur "+str(chance_reussite)+"\% de chance"
		post(commande,texte,"sys")
		
		renvoie_commande(commande,10)
		
############################################# RECRUTETROUPE
	
def verif_recrutetroupe_perso(commande):
	perso = commande.perso
	T_verif = []
	
	if perso.nbTroupes>=perso.troupes_MAX() : T_verif.append(perso.get_nom()+" n'a pas les moyens de commander plus que "+str(perso.troupes_MAX())+" régiments")
	
	return T_verif

def verif_recrutetroupe_qg(commande):
	lieu = commande.perso.lieu
	T_verif = []
	
	if lieu.hote.nbTroupes>=lieu.hote.troupes_MAX() : T_verif.append(lieu.nom+" ne peut pas avoir plus de "+str(lieu.hote.troupes_MAX())+" gardes")
	
	return T_verif

def init_recrutetroupe_qg(commande):
	init_recrutetroupe_perso(commande)

def go_recrutetroupe_qg(commande):
	go_recrutetroupe_perso(commande)
	
def init_recrutetroupe_perso(commande):
	#commande.jet = de(100)
	commande.save()
	commande.perso.occupe = commande
	commande.perso.save()
	
	texte = commande.action.msg_init
	post(commande,texte,"info")
	
def go_recrutetroupe_perso(commande):
	chance_reussite = commande.chance_reussite + commande.bonus_reussite
	
	succes = False
	jet = commande.jet
	if jet == 0 : jet = de(100)
	if jet<=chance_reussite : succes = True
	
	if succes :
		commande.perso.nbTroupes = commande.perso.nbTroupes+1
		commande.perso.save()
	
		texte = commande.action.msg_fin
		post(commande,texte,"info")
		
	else :
		texte = "Tentative de recrutement :\nEchec du jet : "+str(jet)+" sur "+str(chance_reussite)+"\% de chance"
		post(commande,texte,"sys")
		
		renvoie_commande(commande,10)
	
############################################# REJOINDRE
	
def verif_rejoindre(commande):
	perso_cible = commande.persos_cible.all()[0]
	T_verif = []
	if commande.perso.leader_id : T_verif.append(commande.perso.get_nom()+" suit déjà quelqu'un")
	if perso_cible.leader_id : T_verif.append(perso_cible.get_nom()+" suit aussi quelqu'un")
	if Perso.objects.filter(leader=perso_cible).count()>= perso_cible.accompagnants_MAX() : T_verif.append(perso_cible.get_nom()+" ne peut pas mener autant de personnages")
	return T_verif
	
def init_rejoindre(commande):
	a=0
		
def go_rejoindre(commande):
	perso_cible = commande.persos_cible.all()[0]
	commande.perso.leader = perso_cible
	commande.perso.ds_groupe_temporaire = False
	commande.perso.save()
	
	if commande.perso.dissimulation>0 :
		for j in commande.perso.joueur.all():
			if not objet_ds_manytomany(j,perso_cible.joueur_repere) : perso_cible.joueur_repere.add(j)
	
	texte = commande.action.msg_fin
	post(commande,texte,"info")

def prog_rejoindre(commande):
	commande.perso.leader = commande.persos_cible.all()[0]
	return commande.perso
	
############################################# SESEPARER
	
def verif_seseparer(commande):
	T_verif = []
	if not commande.perso.leader_id : T_verif.append(commande.perso.get_nom()+" ne suit personne")
	return T_verif
	
def init_seseparer(commande):
	a=0
		
def go_seseparer(commande):
	texte = commande.action.msg_fin
	texte = texte.replace("#leader#",commande.perso.leader.get_nom())
	
	commande.perso.leader = None
	commande.perso.save()
	
	post(commande,texte,"info")

def prog_seseparer(commande):
	commande.perso.leader = None
	return commande.perso
	
############################################# SEMER
	
def verif_semer(commande):
	persos_cible = commande.persos_cible.all()
	for perso_cible in persos_cible :
		if not perso_cible.leader == commande.perso : commande.persos_cible.remove(perso_cible)
	commande.save()
	
	T_verif = []
	if not commande.persos_cible : T_verif.append('Les personnages selectionnes ne suivent pas '+commande.perso.get_nom())
	return T_verif
	
def init_semer(commande):
	a=0
		
def go_semer(commande):
	persos_cible = commande.persos_cible.all()
	for perso_cible in persos_cible :
		perso_cible.leader = None
		perso_cible.save()
	
	texte = commande.action.msg_fin
	post(commande,texte,"info")
	
############################################# SECONCENTRER
	
def verif_seconcentrer(commande):
	PC_MAX = commande.perso.valeur_competence(commande.action.condition_competence)
	
	T_verif = []
	if commande.perso.PC>=PC_MAX : T_verif.append(commande.perso.get_nom()+" a déjà le maximum de point de concentration : "+str(commande.perso.PC)+"/"+str(PC_MAX) )
	return T_verif
	
def init_seconcentrer(commande):
	commande.save()
	commande.perso.occupe = commande
	commande.perso.save()
	
	texte = commande.action.msg_init
	post(commande,texte,"info")
	
def go_seconcentrer(commande):
	commande.perso.PC = commande.perso.PC+1
	PC_MAX = commande.perso.valeur_competence(commande.action.condition_competence)
	if commande.perso.PC>PC_MAX : commande.perso.PC=PC_MAX 
	commande.perso.save()

############################################# UTILISERCONCENTRATION
	
def verif_utiliserconcentration(commande):
	T_verif = []
	if commande.perso.PC>0 : T_verif.append(commande.perso.get_nom()+" n'a pas de point de concentration")
	if not commande.perso.occupe_id : T_verif.append(commande.perso.get_nom()+" doit être en train de faire une action")
	return T_verif
	
def init_utiliserconcentration(commande):
	a=0
	
def go_utiliserconcentration(commande):
	
	commande_cible = commande.perso.occupe
	
	duree_commande = commande_cible.date_fin-commande_cible.date_debut
	duree_minute = (duree_commande.seconds/60) + (duree_commande.days*24*60)
	duree_minute = int(duree_minute/2)
	
	new_date_fin = commande_cible.date_debut + timedelta(hours=float(duree_minute*60))
	new_chance_reussite = commande_cible.chance_reussite * 2
	if new_chance_reussite>100 : new_chance_reussite = 100
	if new_date_fin<timezone.now() : new_date_fin = timezone.now()
	
	commande_cible.date_fin = new_date_fin
	commande_cible.chance_reussite = new_chance_reussite
	commande_cible.save()
	
	commande.perso.PC = commande.perso.PC-1
	commande.perso.save()

############################################# SECACHER
	
def verif_secacher(commande):
	T_verif = []
	if not commande.perso.a_competence(commande.action.condition_competence) and (commande.action.condition_atelier!=commande.lieu.atelier or commande.action.condition_atelier==None) : T_verif.append(commande.perso.get_nom()+" n'a pas la compétence pour se cacher")
	if commande.perso.nbTroupes>0 : T_verif.append(commande.perso.get_nom()+" ne doit pas avoir de troupes pour cette action")
	if commande.perso.nbGardes>0 : T_verif.append(commande.perso.get_nom()+" ne doit pas avoir de gardes pour cette action")
	return T_verif
	
def init_secacher(commande):
	commande.save()
	commande.perso.occupe = commande
	commande.perso.save()
	
def go_secacher(commande):
	
	valeur_comp_dissimulation = commande.perso.valeur_competence(commande.action.condition_competence)
	dissimulation_base = bonus_dissimulation_lieu = 0
	if commande.perso.dissimulation>0 :
		dissimulation_base = int(('0'+str(commande.perso.dissimulation))[-1]) #prend le dernier chiffre de sa valeur dissimulation
	if commande.perso.lieu.dissimulation>0 : bonus_dissimulation_lieu = 10
	
	commande.perso.dissimulation = valeur_comp_dissimulation*10 + bonus_dissimulation_lieu + dissimulation_base
	#print(commande.perso.dissimulation)
	commande.perso.joueur_repere.clear()
	commande.perso.save()
	
	texte = commande.action.msg_encours
	texte2 = "#depart#"+commande.action.msg_fin
	post(commande,texte2,"info")
	commande.dissimulation = commande.perso.dissimulation
	post(commande,texte,"info")

def prog_secacher(commande):
	commande.perso.dissimulation = commande.perso.valeur_competence(commande.action.condition_competence)*10
	return commande.perso
	
############################################# SEMONTRER
	
def verif_semontrer(commande):
	T_verif = []
	if not commande.perso.dissimulation>0 : T_verif.append(commande.perso.get_nom()+" n'est pas caché")
	return T_verif
	
def init_semontrer(commande):
	a=0
	
def go_semontrer(commande):
	commande.perso.dissimulation = 0
	commande.perso.joueur_repere.clear()
	commande.perso.save()
	
	action_sedeplacer = Action.objects.get(nom_info='sedeplacer')
	texte = action_sedeplacer.msg_encours
	commande.dissimulation = 0
	post(commande,texte,"info")

def prog_semontrer(commande):
	commande.perso.dissimulation = 0
	return commande.perso


############################################# SIGNALER
	
def verif_signaler(commande):
	T_verif = []
	return T_verif
	
def init_signaler(commande):
	a=0
	
def go_signaler(commande):
	persos_cible = commande.persos_cible.all()
	persos_cible.dissimulation = 0
	persos_cible.joueur_repere.clear()
	persos_cible.save()
	
	texte = commande.msg_fin
	post(commande,texte,"info")

	
############################################# POSERPIEGE

def reussite_poserpiege(commande):
	piege_actuel = commande.perso.lieu.piege
	valeur_comp_piege = commande.perso.valeur_competence(commande.action.condition_competence)
	
	chance_reussite = 20*((3-piege_actuel)+valeur_comp_piege)-10
	chance_reussite = chance_reussite+commande.bonus_chance_reussite
	return chance_reussite

def verif_poserpiege(commande):
	
	chance_reussite = reussite_poserpiege(commande)
	
	T_verif = []
	if chance_reussite<=0 : T_verif.append("Aucune chance de réussite")
	return T_verif
	
def init_poserpiege(commande):
	commande.chance_reussite = reussite_poserpiege(commande)
	jet = de(100)
	commande.save()
	commande.perso.occupe = commande
	commande.perso.save()
	
	texte = commande.action.msg_init
	post(commande,texte,"info")
	
def go_poserpiege(commande):
	
	chance_reussite = reussite_poserpiege(commande)
	
	succes = False
	jet = commande.jet
	if jet == 0 : jet = de(100)
	if jet<=chance_reussite : succes = True
	
	if succes :
		new_piege = commande.perso.lieu.piege+1
		if new_piege>commande.perso.lieu.defense_assault_bonusmax+jeu.defense_assault_max : new_piege = commande.perso.lieu.defense_assault_bonusmax+jeu.defense_assault_max
		commande.perso.lieu.piege = new_piege
		commande.perso.lieu.save()
	
		texte = commande.action.msg_fin
		post(commande,texte,"info")
		
	else :
		texte = "Tentative d'amélioration des pièges :\Echec du jet d'ingénierie : "+str(jet)+" sur "+str(chance_reussite)+"\% de chance"
		post(commande,texte,"sys")
		renvoie_commande(commande,10)
	
	
############################################# UPDEFENSE

def reussite_updefense(commande):
	def_actuel = commande.perso.lieu.defense_assault
	valeur_comp_def = commande.perso.valeur_competence(commande.action.condition_competence)
	
	chance_reussite = 20*((5-def_actuel)+valeur_comp_def)-10
	chance_reussite = chance_reussite+commande.bonus_chance_reussite
	return chance_reussite

def verif_updefense(commande):
	
	chance_reussite = reussite_updefense(commande)
	
	T_verif = []
	if chance_reussite<=0 : T_verif.append("Aucune chance de réussite")
	return T_verif
	
def init_updefense(commande):
	commande.chance_reussite = reussite_updefense(commande)
	jet = de(100)
	commande.perso.occupe = commande
	commande.perso.save()
			
	texte = commande.action.msg_init
	post(commande,texte,"info")
	
def go_updefense(commande):
	
	chance_reussite = reussite_updefense(commande)
	
	succes = False
	jet = commande.jet
	if jet == 0 : jet = de(100)
	if jet<=chance_reussite : succes = True
	
	if succes :
		new_defense = commande.perso.lieu.defense_assault+1
		if new_defense>commande.perso.lieu.defense_assault_bonusmax+jeu.defense_assault_max : new_defense = commande.perso.lieu.defense_assault_bonusmax+jeu.defense_assault_max
		commande.perso.lieu.defense_assault = new_defense
		commande.perso.lieu.save()
	
		texte = commande.action.msg_fin
		post(commande,texte,"info")
		
	else :
		texte = "Tentative d'amélioration des défenses du lieu :\nEchec du jet d'ingénierie - "+str(jet)+" sur "+str(chance_reussite)+"\% de chance"
		post(commande,texte,"sys")
		renvoie_commande(commande,10)
		
	commande.perso.save()
		
############################################# INTRUSION

def reussite_intrusion(commande):
	lieu_cible = commande.lieux_cible.all()[0]
	valeur_intrusion = commande.perso.valeur_competence(commande.action.condition_competence)
	nb_garde = lieu_cible.hote.nbGardes
	
	chance_reussite = int((100/6)*(6+valeur_intrusion-nb_garde))
	return chance_reussite
	
def verif_intrusion(commande):
	
	chance_reussite = reussite_intrusion(commande)
	
	T_verif = []
	if chance_reussite<=0 : T_verif.append("Aucune chance de réussite")
	return T_verif
	
def init_intrusion(commande):
	commande.chance_reussite = reussite_intrusion(commande)
	#commande.jet = de(100)
	commande.dissimulation = commande.dissimulation + 5
	commande.save()
	
	valeur_dissimulation = int((commande.perso.dissimulation)/10)*10
	commande.perso.dissimulation = valeur_dissimulation + 5
	commande.perso.occupe = commande
	commande.perso.save()
	
	texte = commande.action.msg_init
	post(commande,texte,"info")
	
def go_intrusion(commande):
	lieu_cible = commande.lieux_cible.all()[0]
	valeur_intrusion = commande.perso.valeur_competence(commande.action.condition_competence)
	piege = lieu_cible.piege
	
	chance_reussite = reussite_intrusion(commande)
	chance_reussite_piege = int((100/6)*(5+valeur_intrusion-(2*piege)))
	chance_reussite = int(chance_reussite*chance_reussite_piege/10000) + commande.bonus_reussite
	
	succes = False
	jet = commande.jet
	if jet == 0 : jet = de(100)
	if jet<=chance_reussite : succes = True
	
	commande.perso.lieu = lieu_cible
	
	if succes :
		
		texte = commande.action.msg_fin
		post(commande,texte,"info")
		
	else :
		commande.perso.nbGardes = 0 # les gardes qui pouvaient accompagner le perso s'enfuient devant l'alerte
		commande.perso.dissimulation = 0 
		
		if piege>0 :
			commande.perso.PV = commande.perso.PV-1 # le perso est blesse par un piege
			texte = commande.perso.get_nom()+" s'empêtre et se blesse dans un piège vicieusement placé\nTentative d'intrusion : Echec du jet - "+str(jet)+" sur "+str(chance_reussite)+"\% de chance"
			post(commande,texte,"sys")
			texte_public = "L'alerte est donnée dans "+lieu_cible.nom+" !\n"+commande.perso.get_nom()+" a réussi à s'y introduire frauduleusement, mais les pièges installés dans le lieu ont, semble t'il, eu raisons de son adresse...\nAussitôt les gardes se précipitent vers l'intrus et l'attaquent sans sommation" 
			post(commande,texte_public,"info")
			
			# envoie commande d'une attaque
		else :
			texte = "Tentative d'intrusion : Echec du jet - "+str(jet)+" sur "+str(chance_reussite)+"\% de chance"
			post(commande,texte,"sys")
			texte_public = "L'alerte est donnée dans "+lieu_cible.nom+" !\n"+commande.perso.get_nom()+" a réussi à s'y introduire frauduleusement, mais les gardes ont été suffisamment vigilant pour le repérer...\nAussitôt ils se précipitent vers l'intrus, et l'attaquent sans sommation" 
			post(commande,texte_public,"info")
			# envoie commande d'une attaque
	commande.perso.save()

############################################# EVASION

def reussite_evasion(commande):
	chance_reussite = 0
	comp_evasion = Competence.objects.get(nom_info='intrusion')
	comp_detection = Competence.objects.get(nom_info='detection')
	valeur_evasion = commande.perso.valeur_competence(comp_evasion)
	valeur_detection = commande.perso.geolier.valeur_competence(comp_detection)
	gardes = commande.perso.geolier.nbGardes
	
	chance_reussite = (valeur_evasion*30 - valeur_detection*20)-gardes*10
	if chance_reussite<=12 : chance_reussite = 12-valeur_detection*2-gardes+valeur_evasion*3
	if chance_reussite<=3 : chance_reussite = 3
	if chance_reussite>95 : chance_reussite = 95
	return chance_reussite

def verif_evasion(commande):
	T_verif = []
	return T_verif
	
def init_evasion(commande):
	commande.perso.occupe = commande
	commande.perso.save()
	
	commande.chance_reussite = reussite_evasion(commande)
	
	commande.dissimulation = 8
	commande.jet = de(100)
	commande.save
	
	texte = commande.action.msg_init
	post(commande,texte,"info")
	
def go_evasion(commande):
	perso = commande.perso
	chance_reussite = reussite_evasion(commande)
	
	if commande.jet-60>chance_reussite or commande.jet>95 :
		#ECHEC CRITIQUE
		texte = perso.get_nom()+" a essayé sans succés de s'échapper"
		commande.dissimulation = 0
		post(commande,texte,"info")
	
	elif commande.jet<=chance_reussite :
		#REUSSITE
		perso.geolier = None
		perso.prisonnier = False
		perso.save()
		
		texte = perso.get_nom()+" parvient à s'échapper de son ravisseur et s'enfuit."
		commande.dissimulation = 0
		post(commande,texte,"info")
		
		#creer Commande de la fuite
		jeu = Jeu.objects.get(id=1)
		action = Action.objects.get(nom_info="fuir")
		date_debut = timezone.now()
		date_fin = date_debut+timedelta(hours=float(jeu.base_delay)*(action.delay/100))
		
		c = Commande.objects.create(\
		joueur = commande.joueur, \
		perso = perso , \
		lieu = perso.lieu, \
		action = action , \
		dissimulation = 0 , \
		date_debut = date_debut , \
		date_fin = date_fin)
		
		
	else :
		#ECHEC
		texte = perso.get_nom()+" a essayé sans succés de s'échapper"
		post(commande,texte,"info")

############################################# PROPOSER_LOI

def verif_proposer_loi(commande):
	
	nom = commande.champ_recherche1
	
	T_verif = []
	if Loi.objects.filter(nom=nom).exclude(commande=commande).filter(Q(active=True) | Q(valide=True)).exists() : T_verif.append("Ce nom de Loi existe déjà")
	
	return T_verif
	
def init_proposer_loi(commande):
	
	#commande.champ_recherche2 = str(loi.id)
	commande.save()
	
	texte = '<div class=quote>'+commande.action.msg_init+'</div><div>'+commande.champ_texte+'</div>'
	post(commande,texte,"normal")
	
	loi = Loi.objects.create(\
	lieu = commande.perso.lieu, \
	joueur = commande.joueur, \
	perso = commande.perso , \
	nom = commande.champ_recherche1 , \
	commande = commande , \
	date_fin = commande.date_fin ,\
	post = Post.objects.filter(perso=commande.perso).filter(lieu=commande.perso.lieu).last())
	
	loi.maison_a_vote.add(commande.perso.maison)
	loi.save()
	
def go_proposer_loi(commande):
	if Loi.objects.filter(commande=commande).exists():
		loi = Loi.objects.get(commande=commande)
		if loi.active and not loi.valide :
			votes = loi.get_nb_votes()
			if votes >= 50:
				loi.valide = True
				loi.date_validation = timezone.now()
				texte = 'La proposition soumise au Sénat par '+commande.perso.get_nom()+' intitulée "'+loi.nom+'" est votée avec la majorité de '+str(votes)+' voix POUR sur '+str(99)+'.'
			else : 
				loi.active = False
				texte = 'La proposition soumise au Sénat par '+commande.perso.get_nom()+' intitulée "'+loi.nom+'" est retoquée avec '+str(votes)+' voix POUR sur '+str(99)+'.'
			
			style = 'info'
			post_MJ(loi.lieu,texte,0,[])
			loi.save()
	

############################################# RECHERCHE CLASSIQUE

def trouve_resultat(commande):
	resultat_final = None
	
	qst_resultat = Resultat.objects.filter(active=True).filter(fini=False).filter(lieu=commande.lieu).filter(action=commande.action)
	T_resultats_prioritaires_objet = []
	T_resultats = []
	for resultat in qst_resultat :
		T_verif = resultat.verif_resultat_cible(commande.perso)
		if len(T_verif)==0 :
			T_resultats.append(resultat)
			if resultat.obj_necessaire and resultat.obj_prioritaire and commande.perso.a_type_objet(resultat.obj_necessaire) : T_resultats_prioritaires_objet.append(resultat)
	
	if len(T_resultats_prioritaires_objet)>0 :
		T_resultats = T_resultats_prioritaires_objet[:]
	
	
	total_priorite = 0
	for resultat in T_resultats :
		total_priorite = total_priorite + resultat.priorite
		
	jet = de(total_priorite)
	
	total_priorite2 = 0
	for resultat in T_resultats :
		total_priorite2 = total_priorite2 + resultat.priorite
		if jet >= total_priorite2 :
			resultat_final = resultat
			break
	return resultat_final

def init_recherche_classique(commande):
	commande.perso.occupe = commande
	commande.perso.save()
	
	resultat_final = trouve_resultat(commande)
	if resultat_final :
		commande.resultat = resultat_final
		commande.save()
		
	texte = commande.action.msg_init
	post(commande,texte,"info")
	
def go_recherche_classique(commande):
	T_verif = commande.resultat.verif_resultat_cible(commande.perso)
	if len(T_verif)>0 :
		resultat_final = trouve_resultat(commande)
		if resultat_final :
			commande.resultat = resultat_final
		else : commande.resultat = None
		commande.save()
	
############################################# RUMEURS

def verif_rumeurs(commande):
	T_verif = []
	return T_verif
	
def init_rumeurs(commande):
	init_recherche_classique(commande)
	
def go_rumeurs(commande):
	go_recherche_classique(commande)


############################################# ACHETER

def verif_acheter(commande):
	T_verif = []
	return T_verif
	
def init_acheter(commande):
	init_recherche_classique(commande)
	
def go_acheter(commande):
	go_recherche_classique(commande)
	
############################################# FORGER

def verif_forger(commande):
	T_verif = []
	return T_verif
	
def init_forger(commande):
	init_recherche_classique(commande)
	
def go_forger(commande):
	go_recherche_classique(commande)
	
############################################# FAIRE POTION

def verif_faire_potion(commande):
	T_verif = []
	return T_verif
	
def init_faire_potion(commande):
	init_recherche_classique(commande)
	
def go_faire_potion(commande):
	go_recherche_classique(commande)
	
		
############################################# ETUDIER RITUEL

def verif_etudier_rituel(commande):
	T_verif = []
	return T_verif
	
def init_etudier_rituel(commande):
	init_recherche_classique(commande)
	
def go_etudier_rituel(commande):
	go_recherche_classique(commande)
	
	
		
		
############################################# EXPLORER

def verif_explorer(commande):
	T_verif = []
	return T_verif

def trouve_resultat_explorer(commande) :
	qst_resultat = Resultat.objects.filter(active=True).filter(fini=False).filter(lieu=commande.lieu).filter(action=commande.action)
	T_resultats = []
	for resultat in qst_resultat :
		T_verif = resultat.verif_resultat_cible(commande.perso)
		if len(T_verif)==0 :
			if commande.champ_recherche1 and commande.champ_recherche1!='' :
				if recherche_Ok(commande.champ_recherche1,resultat.cle1) : T_resultats.append(resultat)
			else : T_resultats.append(resultat)
	
	total_priorite = 0
	for resultat in T_resultats :
		total_priorite = total_priorite + resultat.priorite
		
	jet = de(total_priorite)
	
	resultat_final = None
	total_priorite2 = 0
	for resultat in T_resultats :
		total_priorite2 = total_priorite2 + resultat.priorite
		if jet >= total_priorite2 :
			resultat_final = resultat
			break
			
	return resultat_final


def init_explorer(commande):
	commande.perso.occupe = commande
	commande.perso.save()

	commande.resultat = trouve_resultat_explorer(commande)
				
	commande.save()
	
	texte = commande.action.msg_init
	post(commande,texte,"info")
	
def go_explorer(commande):
	T_verif = commande.resultat.verif_resultat_cible(commande.perso)
	if len(T_verif)>0 :
		commande.resultat = None
		commande.resultat = trouve_resultat_explorer(commande)
		commande.save()
		
	lieu = commande.perso.lieu
	if lieu.taille>1 :
		commande.perso.secteur = de(lieu.taille)
		commande.perso.save()
	

############################################# RETROUVER

def verif_retrouver(commande):
	T_verif = []
	return T_verif
	
def init_retrouver(commande):
	commande.perso.occupe = commande
	commande.perso.save()
	
	if commande.perso.hote==commande.lieu:
		commande.date_fin=timezone.now()
	
	commande.save()
	
	texte = commande.action.msg_init
	post(commande,texte,"info")
	
def go_retrouver(commande):
	perso_cible = commande.persos_cible.all()[0]
	commande.perso.secteur = perso_cible.secteur
	
	for accompagnant in commande.perso.perso_accompagne.all():
		accompagnant.secteur = commande.perso.secteur
		accompagnant.save()
	for prisonnier in commande.perso.perso_prisonnier.all():
		prisonnier.secteur = commande.perso.secteur
		prisonnier.save()
	
	commande.perso.save()
	
	qst_persos_ds_mm_secteur = Perso.objects.filter(active=True).filter(lieu=commande.perso.lieu).filter(secteur=commande.perso.secteur).exclude(id=commande.perso.id).filter(dissimulation=0)
	txt_persos_ds_mm_secteur = txt_liste(qst_persos_ds_mm_secteur)
	
	texte = commande.action.msg_fin
	post(commande,texte.replace('#persos_cible#',txt_persos_ds_mm_secteur),"info")

def prog_retrouver(commande):
	commande.perso.secteur = commande.persos_cible.all()[0].secteur
	return commande.perso
	
############################################# FOUILLE

def verif_fouille(commande):
	T_verif = []
	competence = commande.action.condition_competence
	if commande.perso.valeur_competence(competence)==0 :
		if (commande.champ_recherche1=='' or commande.champ_recherche2=='') :
			T_verif.append(commande.perso.get_nom()+" n'a pas la compétence "+competence.nom+', nécessaire pour faire une recherche avec un seul champ de renseigné')
	if commande.champ_recherche1=='' and commande.champ_recherche2=='' : T_verif.append("Fouille impossible : au moins un des deux champs doit être renseignés")
	return T_verif

def delai_fouille(commande,valeur_comp):
	jeu = Jeu.objects.get(id=1)
	#delai normal : 150
	delai = 10
	if commande.champ_recherche2=='' or commande.champ_recherche1=='' :
		if valeur_comp==1 : delai = 3
		elif valeur_comp==2 : delai = 2
		elif valeur_comp>=3 : delai = 1
	else :
		if valeur_comp==0 : delai = 2
		elif valeur_comp==1 : delai = 1
		elif valeur_comp==2 : delai = 0.5
		elif valeur_comp>=3 : delai = 0.25
	
	
	duree_heure = delai*(jeu.base_delay*commande.action.delay/100)
	
	new_date_fin = commande.date_debut + timedelta(hours=float(duree_heure))
		
		
	return new_date_fin

def trouve_resultat_fouille(commande):
	resultat_final = None
	qst_resultat = Resultat.objects.filter(active=True).filter(fini=False).filter(lieu=commande.lieu).filter(action=commande.action)
	
	T_resultat = []
	for resultat in qst_resultat :
		T_verif = verif_resultat_cible(commande.perso)
		if len(T_verif)==0:
		
			if commande.champ_recherche2=='' :
				if recherche_Ok(commande.champ_recherche1,resultat.cle1):
					T_resultat.append(resultat)
				
			elif commande.champ_recherche1=='' :
				if recherche_Ok(commande.champ_recherche2,resultat.cle2):
					T_resultat.append(resultat)
				
			else : 
				if recherche_Ok(commande.champ_recherche2,resultat.cle2) and recherche_Ok(commande.champ_recherche1,resultat.cle1) :
					T_resultat.append(resultat)
					
	total_priorite = 0
	for resultat in T_resultats :
		total_priorite = total_priorite + resultat.priorite
		
	jet = de(total_priorite)
	
	total_priorite2 = 0
	for resultat in T_resultats :
		total_priorite2 = total_priorite2 + resultat.priorite
		if jet >= total_priorite2 :
			resultat_final = resultat
			break
	return resultat_final
	
	
def init_fouille(commande):
	commande.perso.occupe = commande
	commande.perso.save()
	
	comp_fouiller = commande.action.condition_competence
	valeur_comp = commande.perso.valeur_competence(comp_fouiller)
	commande.date_fin = delai_fouille(commande,valeur_comp)
	
	commande.resultat = trouve_resultat_fouille(commande)
	
	commande.save()
	
	texte = commande.action.msg_init
	post(commande,texte,"info")
	
def go_fouille(commande):
	T_verif = commande.resultat.verif_resultat_cible(commande.perso)
	if len(T_verif)>0 :
		commande.resultat = None
		commande.resultat = trouve_resultat_fouille(commande)
		commande.save()

############################################# DETECTION

def verif_detection(commande):
	T_verif = []
	return T_verif

def init_detection(commande):
	commande.perso.occupe = commande
	commande.perso.save()
	
	comp_fouiller = commande.action.condition_competence
	valeur_comp = commande.perso.valeur_competence(comp_fouiller)
	
	
	#if commande.champ_recherche1=='' and commande.champ_recherche2=='' :
	if valeur_comp==0 : commande.chance_reussite = 0
	elif valeur_comp==1 : commande.chance_reussite = 2
	elif valeur_comp==2 : commande.chance_reussite = 3
	elif valeur_comp>=3 : commande.chance_reussite = 4
	#commande.jet = de(100)
	
	
	commande.save()
	
	texte = commande.action.msg_init
	post(commande,texte,"info")
	
def go_detection(commande):
	
	#if commande.champ_recherche1=='' and commande.champ_recherche2=='' :
		
	competence_espionnage = Competence.objects.get(nom_info='espionnage')
	qst_persos_caches = Perso.objects.filter(active=True).filter(lieu=commande.lieu).exclude(dissimulation=0).order_by('dissimulation')
	qst_perso_espion = Perso.objects.filter(active=True).filter(lieu=commande.lieu).filter(occupe__action__nom_info="espionner")
	
	T_texte = []

	for perso_cache in qst_persos_caches:
		
		dissimulation = int(perso_cache.dissimulation/10)
		if dissimulation>4 : dissimulation = 4
		#seuil_reussite = commande.chance_reussite*((5-dissimulation)*5)
		chance_reussite = commande.chance_reussite
		if perso_cache.secteur!=commande.perso.secteur and not commande.perso.hote : chance_reussite = chance_reussite-1
		seuil_reussite = 60+((chance_reussite-dissimulation)*20)
		if seuil_reussite == 0 : seuil_reussite = 10
		elif seuil_reussite < 0 : seuil_reussite = 0
		
		if commande.jet <= seuil_reussite :
			
			for joueur in commande.perso.joueur.all():
				perso_cache.joueur_repere.add(joueur)
							
			T_texte.append(commande.perso.get_nom()+" détecte "+perso_cache.get_nom()+" dissimulé dans ce lieu")
			
			break
	#print(qst_perso_espion)
	for perso_espion in qst_perso_espion:
		#print(perso_espion)
		espionnage = perso_espion.valeur_competence(competence_espionnage)
		seuil_reussite = 60+((commande.chance_reussite-espionnage-1)*15)
		if commande.jet <= seuil_reussite :
			if commande.jet <= seuil_reussite-25 :
				T_texte.append(commande.perso.get_nom()+" détecte "+perso_espion.get_nom()+" en train de l'espionner")
			else :
				T_texte.append(commande.perso.get_nom()+" se sent espionné...")
			
			perso_espion.occupe.fini = True
			perso_espion.occupe.save()
	
	if len(T_texte)==0 : texte = commande.perso.get_nom()+" ne détecte pour l'instant aucun personnage dissimulé dans ce lieu"
	else : texte = "\n".join(T_texte)
	post(commande,texte,"msg")
		
############################################# BIBLIOTHEQUE

def trouve_resultat_bibliotheque(commande):
	resultat_final = None
	qst_resultat = Resultat.objects.filter(active=True).filter(fini=False).filter(lieu=commande.lieu).filter(action=commande.action)
	
	T_resultat = []
	for resultat in qst_resultat :
		T_verif = verif_resultat_cible(commande.perso)
		if len(T_verif)==0:
			if recherche_Ok(commande.champ_recherche2,resultat.cle2):
				T_resultat.append(resultat)
					
	total_priorite = 0
	for resultat in T_resultats :
		total_priorite = total_priorite + resultat.priorite
		
	jet = de(total_priorite)
	
	total_priorite2 = 0
	for resultat in T_resultats :
		total_priorite2 = total_priorite2 + resultat.priorite
		if jet >= total_priorite2 :
			resultat_final = resultat
			break
	return resultat_final

def verif_bibliotheque(commande):
	T_verif = []
	return T_verif
	
def init_bibliotheque(commande):
	jeu = Jeu.objects.get(id=1)
	commande.perso.occupe = commande
	commande.perso.save()
	
	val_comp = commande.perso.valeur_competence(commande.action.condition_competence)
	
	delay = commande.action.delay
	if val_comp == 2 : delay = delay*3/4
	elif val_comp == 3 : delay = delay/2
	timedelta_delay = timedelta(hours=float(jeu.base_delay)*(delay/100))
	commande.date_fin = date_debut+timedelta_delay
	
	commande.resultat = trouve_resultat_bibliotheque(commande)
	
	commande.save()
	
	texte = commande.action.msg_init
	post(commande,texte,"info")
	
def go_bibliotheque(commande):
	T_verif = commande.resultat.verif_resultat_cible(commande.perso)
	if len(T_verif)>0 :
		commande.resultat = trouve_resultat_bibliotheque(commande)
		commande.save()
	
############################################# EXAMINER

def verif_examiner(commande):
	T_verif = []
	return T_verif
	
def init_examiner(commande):
	commande.perso.occupe = commande
	commande.perso.save()
	
	commande.resultat = commande.resultat_cible
	
	commande.save()
	
	texte = commande.action.msg_init
	post(commande,texte,"info")
	
def go_examiner(commande):
	a=0
	
############################################# ENQUETER

def verif_enqueter(commande):
	
	T_verif = []
	if (not commande.champ_recherche1 or commande.champ_recherche1=='') and (not commande.instant_heure) : T_verif.append("Au moins un des deux champs entre le personnage cible et l'heure cible doit être rempli")
	return T_verif
	
def init_enqueter(commande):
	
	commande.perso.occupe = commande
	commande.perso.save()
	
	'''if commande.champ_recherche1 and commande.champ_recherche1!='' : 
		qst_perso_cible = Perso.objects.filter(active=True).filter(nom=commande.champ_recherche1)
		if len(qst_perso_cible)>0 : perso_cible = qst_perso_cible.all()[0]'''
	if commande.instant_heure :
		heure_cible = commande.instant_heure
		jour_cible = 0
		mois_cible = 0
		if commande.instant_jour :
			jour_cible = commande.instant_jour
			if commande.instant_mois :
				mois_cible = commande.instant_mois
		
	
	if commande.champ_recherche1 and commande.champ_recherche1!='' and commande.instant_heure :
		#devoile les posts du perso qui comprends cette heure + action du perso + posts qui impliquent le perso
		timedelta_delay = timedelta(hours=float(jeu.base_delay)*(commande.action.delay/100)/4)
		commande.date_fin = commande.date_debut+timedelta_delay
		#commande.jet = de(100)
		
		texte = commande.action.msg_init
		post(commande,texte,"info")
		
		
	elif commande.champ_recherche1 and commande.champ_recherche1!='' :
		#devoile les heures pour lesquelles le perso est present dans le lieu
		
		texte = commande.action.msg_init
		post(commande,texte,"info")
	
	elif commande.instant_heure :
		#devoile le nb de persos presents lors de cette horaire
		
		texte = commande.action.msg_init
		post(commande,texte,"info")
		
	commande.save()
	
def go_enqueter(commande):
	
	valeur_comp = commande.perso.valeur_competence(commande.action.condition_competence)
	perso = commande.perso
	
	if commande.lieu.taille>1 and perso.hote != commande.lieu : valeur_comp=valeur_comp-1
	
	if commande.champ_recherche1 : 
		qst_perso_cible = Perso.objects.filter(active=True).exclude(id=1).filter(nom=commande.champ_recherche1)
		if len(qst_perso_cible)>0 : perso_cible = qst_perso_cible.all()[0]
		else :  perso_cible = None
		
		
	if commande.instant_heure :
		
		heure_cible = commande.instant_heure
		T_date_jeu_now = jeu.convert_date(timezone.now())
		jour_cible = T_date_jeu_now[2]
		mois_cible = T_date_jeu_now[3]
		annee_cible = T_date_jeu_now[4]
		if commande.instant_jour :
			jour_cible = commande.instant_jour
			if commande.instant_mois :
				mois_cible = commande.instant_mois
				
		T_date_jeu_enquete = [1,heure_cible+1,jour_cible,mois_cible,annee_cible]
		T_date_jeu_enquete2 = [1,heure_cible,jour_cible,mois_cible,annee_cible]
		date_enquete = jeu.convert_date_inverse(T_date_jeu_enquete)
		date_enquete_debut = date_enquete - timedelta(seconds=int(60*60*jeu.rapport_temps))
		date_enquete_fin = date_enquete + timedelta(seconds=int(60*30*jeu.rapport_temps))
				
	#devoile les posts du perso qui comprends cette heure + action du perso + posts qui impliquent le perso			
	if commande.champ_recherche1 and commande.champ_recherche1!='' and commande.instant_heure :
		if perso_cible :
			compteur = 0
			qst_posts_decouvert = Post.objects.filter(active=True).filter(lieu=commande.lieu).exclude(dissimulation=0).filter(created_date__lt=date_enquete_fin).filter(created_date__gt=date_enquete_debut).filter(perso=perso_cible)
			for post_decouvert in qst_posts_decouvert :
				
				decouvert_OK = False
				T_date_jeu = (post_decouvert.T_date_jeu).split('#')
				if len(T_date_jeu)>=5 :
					if heure_cible == int(T_date_jeu[1]) and jour_cible == int(T_date_jeu[2]) and mois_cible.nom == T_date_jeu[3] and annee_cible == int(T_date_jeu[4]) : 
						decouvert_OK = True
				
				if decouvert_OK :
					cat_seuil = post_decouvert.dissimulation+4 - valeur_comp
					
					seuil = 2.5
					a=1
					while a<cat_seuil:
						seuil = seuil *2
						a=a+1
					#print('	Post à découvrir : ')
					#print(post_decouvert)
					#print('---> '+str(commande.jet)+' / '+str(seuil))
					if commande.jet <= seuil : 
						for joueur in perso.joueur.all():
							compteur = compteur+1
							if not objet_ds_manytomany(joueur,post_decouvert.joueur_connaissant): post_decouvert.joueur_connaissant.add(joueur)
							
			compteur = compteur/len(perso.joueur.all())
			if compteur > 0 :
				texte = perso.get_nom()+" à découvert lors de son enquête "+str(compteur)+" actions concernant "+perso_cible.get_nom()+", le "+format_date_jeu(['',T_date_jeu[1],T_date_jeu[2],mois_cible,T_date_jeu[4]],jeu.format_date)
				post(commande,texte,"msg")
			else :
				renvoie_commande(commande,0)
		else :
			texte = 'Personnage inconnu pour '+commande.champ_recherche1+". L'action est annulée"
			post(commande,texte,"sys")
		
		
	#devoile les heures pour lesquelles le perso est present dans le lieu	
	elif commande.champ_recherche1 and commande.champ_recherche1!='' :
		
		if perso_cible :
			qst_posts_decouvert = Post.objects.filter(active=True).filter(perso=perso_cible).filter(lieu=commande.lieu).filter(dissimulation__lte=valeur_comp).filter(created_date__lt=timezone.now()).order_by('created_date')
			print(qst_posts_decouvert)
			present = False
			TT_suivi = [] # [[date_arrivee,date_depart]]
			
			for post_decouvert in qst_posts_decouvert :
				if not present and not post_decouvert.depart_lieu:
					#cas ou on annule le dernier depart du perso
					if len(TT_suivi)>0 and post_decouvert.created_date <= last_date_depart+timedelta(seconds=30) :
						TT_suivi[-1][1]=''
						present = True
					#le perso arrive dans le lieu
					else :
						TT_suivi.append([post_decouvert.date_jeu,''])
						present = True
						#print(post_decouvert)
						#print(present)
				
				#le perso quitte le lieu et n'a pas été détecté avant
				elif not present and not post_decouvert.depart_lieu:
					TT_suivi.append([post_decouvert.date_jeu,'post_decouvert.date_jeu'])
					present = False
				
				#le perso quitte le lieu				
				elif present and post_decouvert.depart_lieu :
					TT_suivi[-1][1]=post_decouvert.date_jeu
					present = False
					last_date_depart = post_decouvert.created_date
					#print(post_decouvert)
					#print(present)
					
				
			print(TT_suivi)	
			TT_suivi.reverse()
			texte = perso.get_nom()+' a terminé son enquête sur les présences éventuelles de <b>'+perso_cible.get_nom()+'</b> dans ce lieu :\n'
			if len(TT_suivi)>0 :
				for T_suivi in TT_suivi :
					fin = " à "+T_suivi[1]
					if not T_suivi[1] or T_suivi[1] == '' : fin = "jusqu'à présent"
					texte = texte + '\nPrésence détectée de <b>' +T_suivi[0]+' '+fin+"</b>"
			else : texte = texte + '\nPas de présence détéctée dans ce lieu'
			
			post(commande,texte,"msg") 
		else :
			post(commande,'Personnage inconnu pour '+commande.champ_recherche1+". L'action est annulée","sys")
			
			
	#devoile le nb de persos presents et agissant lors de cette horaire
	elif commande.instant_heure :
		
		T_persos = []
		T_persos_decouvert = []
		
		qst_posts_decouvert = Post.objects.filter(active=True).filter(lieu=commande.lieu).filter(created_date__lt=date_enquete).filter(created_date__lt=timezone.now()).order_by('created_date')
		for post_decouvert in qst_posts_decouvert :
			if not post_decouvert.perso in T_persos : T_persos.append(post_decouvert.perso)
		
		for p in T_persos :
			if (not p in T_persos_decouvert) and p.id!=1 : 
				perso_OK = False
				qst_posts_decouvert2 = qst_posts_decouvert.filter(perso=p).filter(dissimulation__lte=valeur_comp)
				
				present = False
				for post_decouvert in qst_posts_decouvert2 :
					#print(post_decouvert)
					date_arrive = post_decouvert.created_date
					dernier_post = post_decouvert
					present = True
					
					if present and post_decouvert.depart_lieu : 
						date_depart = post_decouvert.created_date
						present = False
						if date_enquete_debut < post_decouvert.created_date :
							perso_OK=True #dernier post du perso ds ce lieu, et pas de depart avant date de l'enquete 
							break
							
				if present : #dernier post du perso ds ce lieu, et pas de depart avant date de l'enquete 
					perso_OK=True
			
				if perso_OK : T_persos_decouvert.append(p)
			
		texte = perso.get_nom() + ' a terminé son enquête dans #lieu# :\n'
		
		if len(T_persos_decouvert)>0 :
			for p in T_persos_decouvert :
				texte = texte + "\n - "+p.get_nom()
			if len(T_persos_decouvert)>1 :
				texte = texte + "\n\nsemblent avoir été présents de "+str(T_date_jeu_enquete[1]-1)+'h à '+str(T_date_jeu_enquete[1])+"h, le jour "+str(T_date_jeu_enquete[2])+" du mois de "+T_date_jeu_enquete[3].nom
			else : texte = texte + "\n\nsemble avoir été présent de "+str(T_date_jeu_enquete[1]-1)+'h à '+str(T_date_jeu_enquete[1])+"h, le jour "+str(T_date_jeu_enquete[2])+" du mois de "+T_date_jeu_enquete[3].nom
		
		else : texte = texte + "\nPersonne ne semble avoir été présent de "+str(T_date_jeu_enquete[1]-1)+'h à '+str(T_date_jeu_enquete[1])+"h, le jour "+str(T_date_jeu_enquete[2])+" du mois de "+T_date_jeu_enquete[3].nom
		
		post(commande,texte,"msg") 
		
############################################# ESPIONNER_INIT

def verif_espionner_init(commande):
	
	T_verif = []
	return T_verif
	
def init_espionner_init(commande):
	
	perso_cible = commande.persos_cible.all()[0]
	
	commande.chance_reussite = reussite_espionner(commande.perso,perso_cible)
	#commande.jet = de(100)
		
	commande.perso.occupe = commande
	commande.perso.save()
	
	commande.save()
	
def go_espionner_init(commande):
	joueurMJ = Joueur.objects.get(pk=1)
	persoMJ = Perso.objects.get(pk=1)
	perso_cible = commande.persos_cible.all()[0]
		
	if commande.jet>commande.chance_reussite :
		texte = "Jet : "+str(commande.jet)+"/"+str(commande.chance_reussite)+" - Echec de l'espionnage sur "+perso_cible.get_nom()
		post(commande,texte,"sys")
	
	else :
		action = Action.objects.get(nom_info="espionner")
		date_debut = timezone.now()
		date_fin = date_debut+timedelta(hours=float(jeu.base_delay)*(action.delay/100))
		
		c = Commande.objects.create(\
		joueur = commande.joueur, \
		perso = commande.perso , \
		action = action , \
		lieu = commande.lieu , \
		dissimulation = commande.dissimulation , \
		date_debut = date_debut , \
		date_fin = date_fin , \
		active = commande.active)
		c.persos_cible.add(perso_cible)
		
		
		texte = commande.action.msg_fin
		if commande.dissimulation<10 : commande.dissimulation = 5
		post(commande,texte,"info")
		#post_MJpersonnage(commande.perso,texte,5,[])
		
		for j in commande.perso.joueur.all() :
			if not j in perso_cible.joueur_repere.all() : perso_cible.joueur_repere.add(j)

############################################# ESPIONNER

def reussite_espionner(perso,perso_cible):
	
	competence_espionnage = Competence.objects.get(nom_info='espionnage')
	competence_detection = Competence.objects.get(nom_info='detection')
	val_espionnage = perso.valeur_competence(competence_espionnage)
	val_detection = perso_cible.valeur_competence(competence_detection)
	
	cat_seuil = val_detection+4 - val_espionnage
	if cat_seuil <=1 : seuil = 98
	elif cat_seuil == 2 : seuil = 90
	elif cat_seuil == 3 : seuil = 80
	elif cat_seuil == 4 : seuil = 65
	elif cat_seuil == 5 : seuil = 50
	elif cat_seuil == 6 : seuil = 30
	else : seuil = 0
	return seuil

def verif_espionner(commande):
	
	T_verif = []
	return T_verif
	
def init_espionner(commande):
	
	perso_cible = commande.persos_cible.all()[0]
	
	commande.chance_reussite = reussite_espionner(commande.perso,perso_cible)
	#commande.jet = de(100)
	
	commande.perso.occupe = commande
	commande.perso.espionne = perso_cible
	commande.perso.save()
	
	commande.save()
	
def go_espionner(commande):
	joueurMJ = Joueur.objects.get(pk=1)
	persoMJ = Perso.objects.get(pk=1)
	perso_cible = commande.persos_cible.all()[0]
	
	if (commande.jet>97 or commande.jet>commande.chance_reussite+40) and commande.jet>commande.chance_reussite :
		post(commande,"Jet : "+str(commande.jet)+"/"+str(commande.chance_reussite)+" - Echec Critique : Interruption de l'espionnage : "+commande.perso.get_nom()+" s'est fait repéré !","sys")
		texte = perso_cible.get_nom()+' repère '+commande.perso.get_nom()+" en train de l'espionner !"
		post_MJpersonnage(perso_cible,texte,100,[])
		
		commande.perso.dissimulation = 0
		commande.perso.save()
		
	elif commande.jet>commande.chance_reussite :
		post(commande,"Jet : "+str(commande.jet)+"/"+str(commande.chance_reussite)+" - Interruption de l'espionnage : "+perso_cible.get_nom()+" semble se douter de quelque chose...","sys")
		texte = perso_cible.get_nom()+" a l'impression d'être espionné..."
		post_MJpersonnage(perso_cible,texte,100,[])
		#commande.perso.save()
	
	else :
		renvoie_commande(commande,0)

		
############################################# DONNER

def verif_donner(commande):
	
	T_verif = []
	if not commande.objet: T_verif.append("Cette action nécessite un objet")
	else :
		if commande.objet.perso != commande.perso : T_verif.append(commande.perso.get_nom()+" n'a pas l'objet "+objet.nom+" en sa possession")
	return T_verif
	
def init_donner(commande):
	a=0
	
def go_donner(commande):
	
	perso_cible = commande.persos_cible.all()[0]
	objet = commande.objet
	objet.porte = False
	
	for j in perso_cible.joueur.all() :
		if not j in commande.joueur_connaissant.all() : commande.joueur_connaissant.add(j)
	
	if objet.obj.cumulable :
		objet.etat = objet.etat-1
		perso_cible.trouve_obj(objet.obj)
	else :
		objet.perso = perso_cible
	objet.save()
	
	texte = commande.action.msg_init
	post(commande,texte,"info")
	
	if commande.texte_post and commande.texte_post!='':
		texte2 = commande.texte_post+"\n\n"+commande.action.msg_fin
	else : texte2 = commande.action.msg_fin
	post(commande,texte2,"msg")


############################################# DONNER GARDE

def verif_donner_garde(commande):
	perso_cible = commande.persos_cible.all()[0]
	T_verif = []
	if perso_cible.nbGardes == perso_cible.gardes_MAX() : (T_verif.append(perso_cible.get_nom()+' ne peut pas recevoir de garde supplémentaire : sa capacité à en mener est à son maximum'))
	return T_verif
	
def init_donner_garde(commande):
	a=0
	
def go_donner_garde(commande):
	perso_cible = commande.persos_cible.all()[0]
	perso = commande.perso
	
	perso.nbGardes = perso.nbGardes-1
	perso.save()
	perso_cible.nbGardes = perso_cible.nbGardes+1
	perso_cible.save()
	
	texte = commande.action.msg_fin
	post(commande,texte,"info")

############################################# DONNER TROUPE

def verif_donner_troupe(commande):
	perso_cible = commande.persos_cible.all()[0]
	T_verif = []
	if perso_cible.nbTroupes == perso_cible.troupes_MAX() : (T_verif.append(perso_cible.get_nom()+' ne peut pas recevoir de troupe supplémentaire : sa capacité à en mener est à son maximum'))
	return T_verif
	
def init_donner_troupe(commande):
	a=0
	
def go_donner_troupe(commande):
	perso_cible = commande.persos_cible.all()[0]
	perso = commande.perso
	
	perso.nbTroupes = perso.nbTroupes-1
	perso.save()
	perso_cible.nbTroupes = perso_cible.nbTroupes+1
	perso_cible.save()
	
	texte = commande.action.msg_fin
	post(commande,texte,"info")
	
	
############################################# CHANGE_POSTURE
def verif_change_posture(commande):
	perso = commande.perso
	posture = Posture.objects.get(nom_info=commande.champ_recherche2)
	
	if perso.occupe.est_combat and perso.dissimulation>0 :
		adversaire = Perso.objects.filter(occupe=perso.occupe).exclude(id=perso.id).all()[0]
		if commande.joueur in adversaire.joueur_repere.all() : visible = True
	else : visible = False
	
	T_verif = []
	if perso.PV<posture.PV_min : T_verif.append(perso.get_nom()+" n'est pas en assez bonne santé pour adopter cette posture de combat")
	if perso.PV>posture.PV_max : T_verif.append(perso.get_nom()+" n'est pas blessé pour adopter cette posture de combat")
	if posture.condition_cache == 1 and perso.dissimulation>0 and not visible : T_verif.append(perso.get_nom()+" ne doit pas être dissimulé pour adopter cette posture de combat")
	if posture.condition_cache == 2 and (perso.dissimulation==0 or visible): T_verif.append(perso.get_nom()+" doit être caché pour adopter cette posture de combat")
	if perso.hote and posture.condition_hote == 1 : T_verif.append("Le gardien d'un lieu ne peut pas adopter cette posture de combat")
	if not perso.hote and posture.condition_hote == 2 : T_verif.append(perso.get_nom()+"Il faut être le gardien d'un lieu pour adopter cette posture de combat")
	if not objet_ds_manytomany(perso.espece,posture.condition_espece) and len(posture.condition_espece.all())>0 : T_verif.append("Un "+perso.especenom+" ne peut adopter cette posture de combat")
	if posture.categorie_combat != perso.posture.categorie_combat : T_verif.append("La posture "+posture.nom+" est incompatible avec ce type de combat ("+perso.posture.categorie_combat.nom+")")
	return T_verif

def init_change_posture(commande):	
	a=0
	
def go_change_posture(commande):
	new_posture = Posture.objects.get(nom_info=commande.champ_recherche2)
	commande.perso.posture = new_posture
	commande.perso.save()

	texte = commande.action.msg_fin+' : '+new_posture.nom
	post(commande,texte,"sys")
	



############################################# PROVOQUER_DUEL
def verif_provoquer_duel(commande):
	attaquant = commande.perso
	defenseur = commande.persos_cible.all()[0]
	
	T_verif = []
	
	return T_verif

def init_provoquer_duel(commande):	
	defenseur = commande.persos_cible.all()[0]
	
	if defenseur.leader :
		defenseur.leader = None
		defenseur.save()
	
	commande.chance_reussite = reussite_provoquer_duel(commande)
	#commande.jet = de(100)
	#commande.jet_opposition = de(10)
	commande.desc = traduction_msg(commande.action.desc,commande)
	
	commande.save()
	
	commande.perso.dissimulation = 0
	commande.perso.occupe = commande
	commande.perso.save()
	
	if defenseur.dissimulation!=0 :
		defenseur.dissimulation=0
		defenseur.save()
	
	texte = commande.action.msg_init
	post(commande,texte,"info")
	
def go_provoquer_duel(commande):
	attaquant = commande.perso
	defenseur = commande.persos_cible.all()[0]
	
	chance_reussite = reussite_provoquer_duel(commande)
	
	succes = False
	jet = commande.jet
	if jet == 0 : jet = de(100)
	if jet<=chance_reussite : succes = True
	
	
	if succes :
		action = Action.objects.get(nom_info="duel")
		date_debut = timezone.now()
		date_fin = date_debut+timedelta(hours=float(jeu.base_delay)*(action.delay/100))
		
		c = Commande.objects.create(\
		lieu = attaquant.lieu, \
		joueur = commande.joueur, \
		perso = attaquant , \
		action = action , \
		dissimulation = 0 , \
		date_debut = date_debut , \
		date_fin = date_fin)
		c.persos_cible.add(defenseur)
		
		texte = commande.action.msg_fin
		post(commande,texte,"info")
		
		#comprends pas ce bout de code :
		'''qst_commande_suivante = Commande.objects.filter(commande_parent=commande)
		if qst_commande_suivante.exists():
			for commande_suivante in qst_commande_suivante :
				commande_suivante.commande_parent = c
				commande_suivante.save()'''
		
		
	else :
		attaquant.persos_deja_provoques.add(defenseur)
		
		texte = "Tentative de provoquation en Duel : échec du jet : "+str(jet)+" sur "+str(chance_reussite)+"% de chance"
		post(commande,texte,"sys")
		
		texte = attaquant.get_nom()+" échoue à obtenir son duel. "+defenseur.get_nom()+" tourne les talons en faisant fi de ces provocations"
		post(commande,texte,"info")
		
		
def reussite_provoquer_duel(commande):
	attaquant = commande.perso
	defenseur = commande.persos_cible.all()[0]
	
	
	if defenseur.accepte_duel : chance_reussite = 100
	else :
		if defenseur in attaquant.persos_deja_provoques.all() : chance_reussite = 0
		else :
			chance_reussite = ((attaquant.aura-defenseur.aura)*15)+60
			if chance_reussite>=95 : chance_reussite=95
			if chance_reussite<=5 : chance_reussite=5
	
	return chance_reussite
	
	

############################################# DUEL

def verif_duel(commande):
	attaquant = commande.perso
	defenseur = commande.persos_cible.all()[0]
	
	T_verif = []
	return T_verif

def init_duel(commande):	
	attaquant = commande.perso
	defenseur = commande.persos_cible.all()[0]

	attaquant.posture = attaquant.posture_defaut_duel
	defenseur.posture = defenseur.posture_defaut_duel

	debut_attaquer(commande,attaquant.posture)
	
def go_duel(commande):
	fin_attaquer(commande)

############################################# MELEE

def verif_melee(commande):
	attaquant = commande.perso
	defenseur = commande.persos_cible.all()[0]
	
	T_verif = []
	if defenseur.leader and defenseur.leader != attaquant : T_verif.append(defenseur.get_nom()+" est dans un groupe. Pour l'atteindre, vous devez combattre ce groupe en attaquant son meneur : "+defenseur.leader.get_nom())
	if attaquant.leader and attaquant.leader == attaquant : T_verif.append(attaquant.get_nom()+" ne peut pas attaquer le meneur de son groupe. Pour faire cette action, il doit se séparer de ce groupe.")
	return T_verif

def init_melee(commande):
	
	attaquant = commande.perso
	defenseur = commande.persos_cible.all()[0]
	
	#definition du defenseur
	if defenseur.leader : 
		if defenseur.leader == attaquant :
			defenseur.leader = None
			defenseur.save()
		else : defenseur = defenseur.leader
	
	# cas ou on rejoint un combat (groupe)
	if defenseur.occupe.nom_info == "melee" or defenseur.occupe.nom_info == "attaquer_lieu" :
		attaquant_a_rejoindre = Perso.objects.filter(active=True).filter(occupe=defenseur.occupe).exclude(id=defenseur.id).all()[0]
		attaquant.leader = attaquant_a_rejoindre
		attaquant.ds_groupe_temporaire = True
		attaquant.save()
		texte = attaquant.get_nom()+' rejoint '+attaquant_a_rejoindre.get_nom()+' dans son combat contre '+defenseur.get_nom()
		post(commande,texte,"msg")
	#	
	else :
		
		#intervention des persos selon comportement
		qst_aide_defenseur = Perso.objects.filter(active=True).filter(lieu=defenseur.lieu).exclude(id=defenseur.id).exclude(comportement_intervention__nom_info='no_intervention').exclude(PV__lt=2).exclude(en_fuite=True).exclude(en_combat=True).filter(geolier=None).filter(leader=None).filter(Q(occupe=None) | Q(occupe__action__annulable=True))
		if defenseur.hote : qst_aide_defenseur = qst_aide_defenseur.filter(maison=defenseur.maison)
		else : qst_aide_defenseur = qst_aide_defenseur.exclude(hote=defenseur.lieu).filter(Q(maison=defenseur.maison) | Q(comportement_intervention='aide_all'))
		if len(qst_aide_defenseur)>0 :
			for aide_defenseur in qst_aide_defenseur :
				aide_defenseur.occupe=None
				aide_defenseur.leader = defenseur
				aide_defenseur.ds_groupe_temporaire = True
				aide_defenseur.save()
				
				
		if commande.champ_recherche2 and commande.champ_recherche2 !="" : qst_posture = Posture.objects.filter(nom_info=commande.champ_recherche2)
		else : qst_posture = Posture.objects.filter(priorite=0).filter(categorie_combat__nom_info="melee")

		attaquant.posture = qst_posture.all()[0]
		defenseur.posture = defenseur.posture_defaut_melee
		if defenseur.PV==1 : defenseur.posture = Posture.objects.filter(nom_info="fuir").filter(categorie_combat__nom_info="melee").all()[0]

		debut_attaquer(commande,attaquant.posture)
	
def go_melee(commande):
	fin_attaquer(commande)

############################################# EMBUSCADE
def verif_embuscade(commande):
	attaquant = commande.perso
	defenseur = commande.persos_cible.all()[0]
	comp_embuscade = commande.action.condition_competence
	
	T_verif = []
	if commande.perso.nbTroupes>0 : T_verif.append(attaquant.get_nom()+" ne doit pas avoir de troupes pour cette action")
	if commande.perso.nbGardes>0 : T_verif.append(attaquant.get_nom()+" ne doit pas avoir de gardes pour cette action")
	if defenseur.leader and attaquant.valeur_competence(comp_embuscade)<3 : T_verif.append(defenseur.get_nom()+" ne doit pas être dans un groupe pour subir une embuscade")
	return T_verif

def init_embuscade(commande):
	
	attaquant = commande.perso
	defenseur = commande.persos_cible.all()[0]
	
	backstab_OK = True
	if defenseur.occupe and defenseur.occupe.action.nom_info=='detection' :
		attaquant.posture = Posture.objects.get(nom_info='combat')
		backstab_OK = False
	else :
		for accompagnant in defenseur.perso_accompagne.all():
			if accompagnant.occupe and accompagnant.occupe.action.nom_info=='detection' :
				attaquant.posture = Posture.objects.get(nom_info='combat')
				backstab_OK = False
				break
	
	if backstab_OK :
		if attaquant.dissimulation < 6 : attaquant.dissimulation = 6
		attaquant.posture = Posture.objects.get(nom_info='backstab')
		
	if defenseur.leader : 
		if defenseur.leader == attaquant :
			defenseur.leader = None
		else : defenseur = defenseur.leader
	
	
	defenseur.posture = defenseur.posture_defaut_melee
	if defenseur.PV==1 : defenseur.posture = Posture.objects.filter(nom_info="fuir").filter(categorie_combat__nom_info="melee").all()[0]
	defenseur.save()
	attaquant.save()
	
	debut_attaquer(commande,attaquant.posture)
	
def go_embuscade(commande):
	fin_attaquer(commande)


############################################# ATTAQUER_LIEU_DPLCT : CF. def envoie_commande dans fonctions.py

############################################# ATTAQUER_LIEU
def verif_attaquer_lieu(commande):
	lieu_cible = commande.lieux_cible.all()[0]
	if not lieu_cible.ferme : T_verif.append("Attaque annulée : le lieu n'est pas fermé pour le personnage")
	T_verif = []
	return T_verif

def init_attaquer_lieu(commande):	
	attaquant = commande.perso
	lieu_cible = commande.lieux_cible.all()[0]
	
	#attribution du defenseur (hote du lieu)
	if len(lieu_cible.hote.all())>0:
		defenseur = lieu_cible.hote.all()[0]
	else :
		defenseur = Perso.objects.create(\
		nom = "Capitaine de "+lieu_cible.nom , \
		hote = lieu_cible , \
		active = False , \
		en_combat = True , \
		occupe = commande, \
		espece = 2, \
		maison = lieu_cible.maison)
	
	commande.num = commande.perso.lieu.id
	commande.persos_cible.add(defenseur) 
	attaquant.secteur = 1
	
	#si l'hote etait en train d'accompagner qq'un, notament dans un combat : il quitte ce groupe pour defendre le lieu
	if defenseur.leader : 
		defenseur.leader = None
		if defenseur.en_combat :
			defenseur.en_combat = False
			if defenseur.occupe : defenseur.occupe = None
	
	#attribution des postures et lancement des attaques
	if attaquant.NB_TROUPES_GROUPE()>0 :
		attaquant.posture = Posture.objects.get(nom_info="bataille_lieu")
		init_bataille(commande)
		
	else :
		attaquant.posture = Posture.objects.get(nom_info="attaque_lieu")
		init_melee(commande)
	
	
	
def go_attaquer_lieu(commande):
	fin_attaquer(commande)
	
############################################# BATAILLE

def verif_bataille(commande):
	attaquant = commande.perso
	defenseur = commande.persos_cible.all()[0]
	
	T_verif = []
	if defenseur.leader and defenseur.leader != attaquant : T_verif.append(defenseur.get_nom()+" est dans un groupe. Pour l'atteindre, vous devez combattre ce groupe en attaquant son meneur : "+defenseur.leader.get_nom())
	if attaquant.leader and attaquant.leader == attaquant : T_verif.append(attaquant.get_nom()+" ne peut pas attaquer le meneur de son groupe. Pour faire cette action, il doit se séparer de ce groupe.")
	return T_verif

def init_bataille(commande):
	
	attaquant = commande.perso
	defenseur = commande.persos_cible.all()[0]
	
	#definition du defenseur
	if defenseur.leader : 
		if defenseur.leader == attaquant :
			defenseur.leader = None
			defenseur.save()
		else : defenseur = defenseur.leader
	
	# cas ou on rejoint un combat (groupe)
	if defenseur.occupe.nom_info == "bataille" or defenseur.occupe.nom_info == "attaquer_lieu" :
		attaquant_a_rejoindre = Perso.objects.filter(active=True).filter(occupe=defenseur.occupe).exclude(id=defenseur.id).all()[0]
		attaquant.leader = attaquant_a_rejoindre
		attaquant.ds_groupe_temporaire = True
		attaquant.save()
		texte = attaquant.get_nom()+' rejoint '+attaquant_a_rejoindre.get_nom()+' dans son combat contre '+defenseur.get_nom()
		post(commande,texte,"msg")
	#	
	elif attaquant.posture.nom_info!="bataille_lieu" :
		qst_posture = Posture.objects.filter(priorite=0).filter(categorie_combat__nom_info="bataille")
		attaquant.posture = qst_posture.all()[0]
		defenseur.posture = attaquant.posture
		debut_attaquer(commande,attaquant.posture)
		
	
def go_bataille(commande):
	fin_attaquer(commande)



############################################# ATTAQUER_GENERAL

def debut_attaquer(commande,posture):
	#debut de l'attaque
	attaquant = commande.perso
	defenseur = commande.persos_cible.all()[0]
	commande.date_fin = commande.date_debut+timedelta(days=300)
	
	attaquant.posture = Posture.objects.get(nom_info=posture.nom_info)
	attaquant.occupe = commande
	attaquant.en_combat = True
	attaquant.save()
	
	type_combat = attaquant.posture.categorie_combat
	commande.champ_recherche1 = type_combat.nom_info
	commande.save()
	
	defenseur_deja_engage = False
	if not defenseur.en_combat :
		if defenseur.occupe :
			#Annule la commande en cours du perso sous l'attaque
			c = defenseur.occupe
			c.erreur = True
			c.desc = "action interrompue pour "+c.perso.get_nom()+" / "+c.action.nom+" : "+c.perso.get_nom()+" est attaqué(e) par "+attaquant.get_nom()
			c.save()
		defenseur.en_fuite = False
		defenseur.en_combat = True
		defenseur.occupe = commande
	
	elif defenseur.occupe and defenseur.occupe.action.nom_info=="duel" :
		commande_attaque = defenseur.occupe
		att_duel = commande_attaque.perso
		def_duel = commande_attaque.persos_cible.all()[0]
		texte = "Le duel entre "+att_duel.get_nom()+" et "+def_duel.get_nom()+" est interrompu car "+defenseur.get_nom()+" se fait attaquer"
		post_MJpersonnage(defenseur,texte,0,[])
		globals()['fin_'+commande_attaque.action.nom_info.lower()](commande_attaque)
	
	else : 
		defenseur_deja_engage = True
	
	if type_combat.nom_info == "duel" : defenseur.posture = defenseur.posture_defaut_duel
	elif type_combat.nom_info == "melee" : defenseur.posture = defenseur.posture_defaut_melee
	elif type_combat == "meleelieu" : defenseur.posture = Posture.objects.get(nom_info="defense_lieu")
	elif type_combat == "bataillelieu" : defenseur.posture = Posture.objects.get(nom_info="bataille_defense_lieu")
	elif type_combat == "bataille" : defenseur.posture = attaquant.posture
	else : 
		qst_posture = Posture.objects.filter(categorie_combat__nom_info=type_combat).filter(priorite=0)
		defenseur.posture = qst_posture.all()[0]
	defenseur.dissimulation = 0
	defenseur.save()
	
	intiative_attaquant = 0
	intiative_defenseur = 0
	
	if type_combat.nom_info == "meleelieu" or type_combat.nom_info == "bataillelieu" :
		actionsedeplacer = Action.objects.get(nom_info="sedeplacer")
		delay_deplct =  timedelta(hours=float(jeu.base_delay)*(actionsedeplacer.delay/100))
		intiative_attaquant = intiative_attaquant + delay_deplct
		intiative_defenseur = intiative_defenseur + delay_deplct
	
	if type_combat.nom_info == "bataille" and defenseur.nbTroupes<=0 :
		#le defenseur va essayer de s'enfuir
		comp_evasion = Competence.objects.get(nom_info='intrusion')
		if attaquant.VALEUR_FRAPPE_BATAILLE()+de(10) < defenseur.valeur_competence(comp_evasion)*3+de(10) :
			texte = attaquant.get_nom()+" lance ses troupes capturer "+defenseur.get_nom()+", mais celui-ci parvient à s'enfuir"
			post(commande,texte,"info")
			
			#creer Commande de la fuite
			action_fuir = Action.objects.get(nom_info="fuir")
			date_debut = timezone.now()
			date_fin = date_debut+timedelta(hours=float(jeu.base_delay)*(action.delay/100))
			
			c = Commande.objects.create(\
			joueur = defenseur.joueur.all()[0], \
			perso = defenseur , \
			lieu = defenseur.lieu, \
			action = action_fuir , \
			dissimulation = 0 , \
			date_debut = date_debut , \
			date_fin = date_fin)
			
		else :
		
			texte = defenseur.get_nom() +" se fait capturer par les troupes de "+attaquant.get_nom()
			post_MJpersonnage(defenseur,texte,0,[])
			defenseur.geolier = attaquant
		
			for accompagnant in defenseur.perso_accompagne.all():
				accompagnant.PV = 0
				accompagnant.leader = None
				accompagnant.save()
				
		fin_attaquer(commande)
				
	else :
	
		#envoie des commandes FRAPPER
		action = Action.objects.get(nom_info="frapper")
		date_fin = timezone.now()+timedelta(days=100)
		
		
		c_attaque = Commande.objects.create(\
		joueur = commande.joueur, \
		perso = attaquant , \
		lieu = defenseur.lieu , \
		action = action , \
		dissimulation = commande.dissimulation , \
		date_debut = timezone.now()+timedelta(hours=intiative_attaquant) , \
		champ_recherche1 = type_combat.nom_info , \
		commande_parent = commande , \
		date_fin = date_fin)
		
		c_attaque.persos_cible.add(defenseur)
		dissimulation_lieu = 0
		if defenseur.lieu.dissimulation>0 or defenseur.lieu.ferme : dissimulation_lieu=1
		
		if not defenseur_deja_engage and type_combat!='bataille' and type_combat!='bataillelieu' :
			c_defense = Commande.objects.create(\
			joueur = defenseur.joueur.all()[0], \
			perso = defenseur , \
			lieu = defenseur.lieu , \
			action = action , \
			dissimulation = 0+dissimulation_lieu , \
			date_debut = timezone.now()+timedelta(hours=intiative_defenseur) , \
			champ_recherche1 = type_combat.nom_info , \
			commande_parent = commande , \
			date_fin = date_fin)
			c_defense.persos_cible.add(attaquant)
		
		
		
		#message du début de combat
		if type_combat.nom_info == "meleelieu"  :
			txt = commande.action.msg_init
			post_MJpersonnage(attaquant,txt,0,[])
			
		if type_combat.nom_info == "bataillelieu"  :
			txt = attaquant.get_nom()+" est en train d'attaquer #lieu# avec une armée"
			post_MJpersonnage(attaquant,txt,0,[])

		texte = commande.action.msg_init
		post(commande,texte,"info")

		if c_attaque.dissimulation >= 10 :
			if type_combat.nom_info == "meleelieu" : texte = "Un intrus attaque les portes de "+defenseur.lieu.nom
			else : texte = defenseur.get_nom()+" se fait attaquer"
			post_MJpersonnage(defenseur,texte,0,[])
	
def fin_attaquer(commande):
	#fin de l'attaque
	attaquant = commande.perso
	defenseur = commande.persos_cible.all()[0]
	T_combattants_impliques = [attaquant,defenseur]
	type_combat = attaquant.posture.categorie_combat

	commande.fini = True
	commande.save()


	#interrompre les action FRAPPER en cours
	qst_commande_enfant = Commande.objects.filter(commande_parent=commande).filter(commence=True).filter(fini=False)
	for c in qst_commande_enfant :
		c.fini = True
		c.save()
	#
	
	for combattant in T_combattants_impliques :
		combattant.en_combat = False
		combattant.occupe = None
	
	
	if type_combat.nom_info=="duel":
		attaquant.persos_deja_provoques.add(defenseur)
	
	else :
		#verifie si les protagonistes du combat ne sont pas encore engages par qq'un d'autre, et si oui si ce combat doit se poursuivre ou continuer - ANCIENNES REGLE DE COMABT MULTIPLE
		for combattant in T_combattants_impliques :

			qst_combat_en_cours = Commande.objects.filter(action__nom_info=commande.action.nom_info).filter(commence=True).filter(fini=False).filter(Q(perso=combattant) | Q(persos_cible=combattant)).distinct()
			for c in qst_combat_en_cours :
				
				T_verif = verif_action_base(c)
				try : T_verif.extend(globals()['verif_'+c.action.nom_info.lower()](c))
				except :
					txt_erreur = 'ERREUR : COMMANDE '+c.action.nom.lower()+' NON TROUVE'
					T_verif.append(txt_erreur)
				
				if len(T_verif)==0 : #le combat se poursuit
					combattant.occupe = c
					combattant.en_combat=True
					
					new_frapper = Commande.objects.create(\
					joueur = None, \
					perso = combattant , \
					lieu = combattant.lieu, \
					dissimulation = c.dissimulation , \
					commande_parent = c , \
					action = Action.objects.get(nom_info="frapper") , \
					date_debut = timezone.now() , \
					date_fin = timezone.now()+timedelta(days=100))
					
				else :  #le combat s'arrete
					c.erreur = True
					texte_erreur = "ERREUR, action annulée pour "+commande.perso.get_nom()+" / "+commande.action.nom+" :\n --- "+'\n---'.join(T_verif)
					commande.desc = texte_erreur
					c.save()
					
			
	if type_combat.nom_info == 'meleelieu':
		#si attaquant gagnant, alors il va dans le lieu, sinon il sort du lieu avec ses accompagnants
		if commande.lieu.hote.nbGardes!=0 and attaquant.lieu == commande.lieu :
			lieu_retraite = Lieu.objects.get(id=commande.num)
			attaquant.lieu = lieu_retraite
			qst_accompagnants = Perso.objects.filter(active=True).filter(leader=attaquant)
			for accompagnant in qst_accompagnants :
				accompagnant.lieu = lieu_retraite

	for combattant in T_combattants_impliques :
		if not combattant.en_combat : 
		
			combattant.posture = None
			
			#casse les groupes temporaire
			qst_accompagnants_total = Perso.objects.filter(active=True).filter(leader=combattant)
			qst_accompagnants_temp = qst_accompagnants_total.filter(ds_groupe_temporaire=True)
			qst_accompagnants = qst_accompagnants_total.filter(ds_groupe_temporaire=False)
			
			for accompagnant_temp in qst_accompagnants_temp :
				accompagnant_temp.leader = None
				accompagnant_temp.ds_groupe_temporaire = False
				accompagnant_temp.save()
			
			for accompagnant in qst_accompagnants :				
				if combattant.geolier : 
					accompagnant.leader = None
					accompagnant.en_combat = False
					accompagnant.occupe = None
					accompagnant.save()
					
				if combattant.en_fuite : #leur fuite est indiqué dans def combat_fuite()
					accompagnant.leader = None
					accompagnant.en_combat = False
					accompagnant.occupe = None
					accompagnant.save()
					
				if combattant.PV<0 : 
					accompagnant.leader = None
					accompagnant.en_combat = False
					accompagnant.occupe = None
					accompagnant.save()
			
		combattant.save()
			
	
		
		
		
############################################# FRAPPER

	
def verif_frapper(commande):
	T_verif = []
	attaquant = commande.perso
	defenseur = commande.persos_cible.all()[0]

	T_combattants = [attaquant,defenseur]

	for combattant in T_combattants :
	
		if combattant.PV<=0 : T_verif.append(combattant.get_nom() + ' est inconscient')
		if combattant.geolier : T_verif.append(combattant.get_nom() + ' est prisonnier')
	
	if attaquant.lieu != defenseur.lieu : T_verif.append(defenseur.get_nom() + " n'est pas dans le même lieu que "+attaquant.get_nom())
	if attaquant.en_fuite : T_verif.append(attaquant.get_nom()+" est en fuite")
	
	return T_verif
	
def init_frapper(commande):
	attaquant = commande.perso
	defenseur = commande.persos_cible.all()[0]
	
	delay_frappe_attaquant = 115 - (de(30))
	arme = attaquant.arme()
	if arme : delay_frappe_attaquant = arme.obj.delay + 15 - (de(30))
	
	timedelta_delay = timedelta(hours=float(jeu.base_delay)*(commande.action.delay/100)*(delay_frappe_attaquant/100))
	commande.date_fin = commande.date_debut+timedelta_delay
	
	commande.jet = de(10)
	commande.jet_opposition = de(10)
	
	
	commande.save()

def go_frapper(commande):
	attaquant = commande.perso
	defenseur = commande.persos_cible.all()[0]
	commande_attaque = commande.commande_parent
	T_combattants = [attaquant,defenseur]

	#qst_commande_frapper_adv = Commande.objects.filter(commande_parent=commande_attaque).filter(perso=defenseur).filter(persos_cible=attaquant).filter(fini=False)
	type_combat = attaquant.posture.categorie_combat.nom_info

	#Posture du Defenseur par defaut :
	if not defenseur.posture or defenseur.posture.categorie_combat.nom_info != type_combat :
		if type_combat == "duel" : defenseur.posture = defenseur.posture_defaut_duel
		elif type_combat == "melee" : defenseur.posture = defenseur.posture_defaut_melee
		elif type_combat == "meleelieu" : defenseur.posture = Posture.objects.get(nom_info="defense_lieu")
		elif type_combat == "bataillelieu" : defenseur.posture = Posture.objects.get(nom_info="bataille_defense_lieu")
		else : 
			qst_posture = Posture.objects.filter(categorie_combat__nom_info=type_combat).filter(priorite=0)
			defenseur.posture = qst_posture.all()[0]
		defenseur.save()

	#Posture obligatoire :
	if type_combat == "melee" :
		for combattant in T_combattants :
			if combattant.PV < combattant.posture.PV_min : 
				combattant.posture = Posture.objects.get(nom_info="fuir")
				combattant.save()

	if type_combat == "meleelieu" :
		for combattant in T_combattants :
			if combattant.hote and (combattant.nbGardes == 0 or not combattant.hote.ferme): 
				combattant.posture = Posture.objects.get(nom_info="laisserpasser")
				combattant.save()
			elif combattant.PV < combattant.posture.PV_min and not combattant.hote : 
				combattant.posture = Posture.objects.get(nom_info="repli")
				combattant.save()
				
	if type_combat == "bataillelieu" :
		for combattant in T_combattants :
			if combattant.hote and (combattant.nbTroupes == 0 or not combattant.hote.ferme): 
				combattant.posture = Posture.objects.get(nom_info="bataille_laisserpasser")
				combattant.save()
			elif not combattant.hote and combattant.nbTroupes<=0 : 
				combattant.posture = Posture.objects.get(nom_info="bataille_repli")
				combattant.save()

	defenseur_replique = True
	if not defenseur.occupe == commande_attaque : defenseur_replique = False

	#Definition du type de frappe :
	frappe = "frappe"
	if type_combat == "duel" : frappe = "frappe_duel"
	else :
		fonction = type_combat+"_"+attaquant.posture.nom_info
		try : frappe = globals()[fonction](defenseur.posture,defenseur_replique)
		except : print('ERROR : fonction "' +fonction+ '"" non trouve')
	#
	
	#capture impossible si la cible a des accompagnants valides en train de combattre
	if frappe == "essaie_capture" and len(defenseur.perso_accompagne.filter(active=True).filter(PV__gt=1).all())>0 : frappe = "frappe"
	
	#jet de detection du backstab : si l'attaquant le reussi, le defenseur perd cette posture
	if defenseur.posture.nom_info == 'backstab' : attaquant.DETECTION_BACKSTAB(defenseur)
	
	#print('Attaquant Valeur Frappe Duel : '+str(attaquant.VALEUR_FRAPPE_DUEL()))
	bonus_posture_attaquant = attaquant.BONUS_POSTURE(defenseur)
	bonus_posture_defenseur = defenseur.BONUS_POSTURE(attaquant)
	
	
	if type_combat == "duel" :
		valeur_frappe_attaquant = attaquant.VALEUR_FRAPPE_DUEL()
		valeur_frappe_defenseur = defenseur.VALEUR_FRAPPE_DUEL()
		
	elif type_combat == "bataille" :
		valeur_frappe_attaquant = attaquant.VALEUR_FRAPPE_BATAILLE()
		valeur_frappe_defenseur = defenseur.VALEUR_FRAPPE_BATAILLE()
		
	else : 
		valeur_frappe_attaquant = attaquant.VALEUR_FRAPPE_MELEE_GROUPE()
		valeur_frappe_defenseur = defenseur.VALEUR_FRAPPE_MELEE_GROUPE()
	
	#cas embuscade niveau 3 : ne prend pas en compte le groupe
	if type_combat == "melee" and ((attaquant.posture.nom_info=='backstab' and attaquant.valeur_competence(attaquant.posture.commpetence_bonus)>=3) or (defenseur.posture.nom_info=='backstab' and defenseur.valeur_competence(defenseur.posture.commpetence_bonus)>=3)) :
		valeur_frappe_attaquant = attaquant.VALEUR_FRAPPE_MELEE()
		valeur_frappe_defenseur = defenseur.VALEUR_FRAPPE_MELEE()
		
	#Comportement : 
	if frappe[:-1]=='assassinat':
		if frappe[-1]=="A" : valeur_frappe_attaquant = bonus_posture_attaquant = commande.jet = 0
		if frappe[-1]=="B" : valeur_frappe_defenseur = bonus_posture_defenseur = commande.jet_opposition = 0
		frappe = "frappe"
	
	if frappe == "frappe" :
		
		ATT_COMBAT = valeur_frappe_attaquant + bonus_posture_attaquant + commande.jet
		DEF_COMBAT = valeur_frappe_defenseur + bonus_posture_defenseur + commande.jet_opposition
		
		texte = post_frappe(attaquant,defenseur,[valeur_frappe_attaquant,bonus_posture_attaquant,commande.jet],[valeur_frappe_defenseur,bonus_posture_defenseur,commande.jet_opposition],["Valeur de Combat","Bonus de Posture","Jet D10"])
		post(commande,texte,"sys")

		#if ATT_COMBAT<DEF_COMBAT and ATT_COMBAT+4>DEF_COMBAT and defenseur.nbGardes>0 : dommage = 1
		#elif ATT_COMBAT>=DEF_COMBAT : dommage = int(math.floor(float(ATT_COMBAT-DEF_COMBAT)/4+1))
		#else : dommage = 0
		dommage = 1 + ATT_COMBAT - DEF_COMBAT
		

		combat_inflige_dommage(commande,dommage)

		if type_combat == "meleelieu" and defenseur.nbGardes==0 : frappe = "laisserpasserB"
		
	elif frappe == "frappe_duel" :
		
		ATT_COMBAT = valeur_frappe_attaquant + bonus_posture_attaquant + commande.jet
		DEF_COMBAT = valeur_frappe_defenseur + bonus_posture_defenseur + commande.jet_opposition
		
		texte = post_frappe(attaquant,defenseur,[valeur_frappe_attaquant,bonus_posture_attaquant,commande.jet],[valeur_frappe_defenseur,bonus_posture_defenseur,commande.jet_opposition],["Valeur de Combat","Bonus de Posture","Jet D10"])
		post(commande,texte,"sys")
		
		#if ATT_COMBAT>=DEF_COMBAT : dommage = int(math.floor(float(ATT_COMBAT-DEF_COMBAT)/4+1))
		#else : dommage = 0
		dommage = 1 + ATT_COMBAT - DEF_COMBAT
		

		combat_inflige_dommage(commande,dommage)
		
	elif frappe == "frappe_bataille" or frappe[:-1] == "essai_retraite" :
		
		bonus_troupe_attaquant = bataille_bonus_surnombre(attaquant,defenseur)
		bonus_troupe_defenseur = bataille_bonus_surnombre(defenseur,attaquant)
		
		if attaquant.posture.nom_info == 'bataille_encerclement' : bonus_posture_attaquant = bonus_posture_attaquant + bonus_troupe_attaquant
		if defenseur.posture.nom_info == 'bataille_encerclement' : bonus_posture_defenseur = bonus_posture_defenseur + bonus_troupe_defenseur
		
		if (attaquant.posture.nom_info == 'bataille_defense' or attaquant.posture.nom_info == 'bataille_retraite') and (defenseur.posture.nom_info == 'bataille_defense' or defenseur.posture.nom_info == 'bataille_retraite') :
			texte = "L'armée de "+attaquant.get_nom()+" et celle de "+defenseur.get_nom()+" adoptent toutes deux une stratégie défensive et aucune d'entre elles ne semblent décidées à mener l'assault."
			post_MJ(commande.lieu,texte,0,[attaquant,defenseur])
		else :
		
			ATT_COMBAT = valeur_frappe_attaquant + bonus_posture_attaquant + bonus_troupe_attaquant + commande.jet
			DEF_COMBAT = valeur_frappe_defenseur + bonus_posture_defenseur + bonus_troupe_defenseur + commande.jet_opposition
			
			texte = post_frappe(attaquant,defenseur,[valeur_frappe_attaquant,bonus_troupe_attaquant,bonus_posture_attaquant,commande.jet],[valeur_frappe_defenseur,bonus_troupe_defenseur,bonus_posture_defenseur,commande.jet_opposition],["Valeur de Stratégie","Bonus de sur-nombre","Bonus de Posture","Jet D10"])
			post_MJ(commande.lieu,texte,200,[attaquant,defenseur])
			
			dommage = ATT_COMBAT-DEF_COMBAT
			
			if frappe[-1]=="A" :
				frappe = 'retraiteA'
				if dommage>0 : dommage=0
				if defenseur.posture.nom_info == 'bataille_encerclement' : dommage = dommage*2
			if frappe[-1]=="B" :
				frappe = 'retraiteB'
				if dommage<0 : dommage=0
				if attaquant.posture.nom_info == 'bataille_encerclement' : dommage = dommage*2
			
			bataille_inflige_dommage(commande,dommage)
	

	elif frappe == "essaie_capture" :
		ATT_COMBAT = valeur_frappe_attaquant + bonus_posture_attaquant + commande.jet
		DEF_COMBAT = valeur_frappe_defenseur + bonus_posture_defenseur + commande.jet_opposition

		texte = post_frappe(attaquant,defenseur,[valeur_frappe_attaquant,bonus_posture_attaquant,commande.jet],[valeur_frappe_defenseur,bonus_posture_defenseur,commande.jet_opposition],["Valeur de Combat","Bonus de Posture","Jet D10"])
		post(commande,texte,"sys")

		#if ATT_COMBAT+4>DEF_COMBAT and ATT_COMBAT<DEF_COMBAT and defenseur.nbGardes>0 : dommage = 1
		#elif ATT_COMBAT>=DEF_COMBAT : dommage = int(math.floor(float(ATT_COMBAT-DEF_COMBAT)/4+1))
		#else : dommage = 0
		dommage = 1 + ATT_COMBAT - DEF_COMBAT
		

		if dommage>4 : frappe = "captureB"
		else : combat_inflige_dommage(commande,dommage)

		if defenseur.PV==0 : frappe = "captureB"

	elif frappe == "essai_fuite" :
		ATT_COMBAT = valeur_frappe_attaquant + bonus_posture_attaquant + commande.jet
		DEF_COMBAT = valeur_frappe_defenseur + bonus_posture_defenseur + commande.jet_opposition

		texte = post_frappe(attaquant,defenseur,[valeur_frappe_attaquant,bonus_posture_attaquant,commande.jet],[valeur_frappe_defenseur,bonus_posture_defenseur,commande.jet_opposition],["Valeur de Combat","Bonus de Posture","Jet D10"])
		post(commande,texte,"sys")
		
		if ATT_COMBAT>=DEF_COMBAT : frappe = "fuiteA"
		else :
			texte = attaquant.get_nom() +" essaie sans succés de s'enfuir du combat"
			post(commande,texte,"info")
			renvoie_commande(commande,0)

	if frappe == "arret" :
		attaquant.dissimulation = defenseur.dissimulation = 0
		texte = attaquant.get_nom()+" et "+defenseur.get_nom() +" arrêtent le combat"
		post_MJ(commande.lieu,texte,0,[])
		fin_attaquer(commande_attaque)

	elif frappe[:-1] == "laisserpasser" :
		if frappe[-1]=="A" : texte = attaquant.get_nom()+" arrête le combat et laisse entrer "+defenseur.get_nom()
		if frappe[-1]=="B" :texte = defenseur.get_nom()+" arrête le combat et laisse entrer "+attaquant.get_nom()
		post_MJ(commande.lieu,texte,0,[])
		fin_attaquer(commande_attaque)

	elif frappe[:-1] == "repli" :
		if frappe[-1]=="A" : combat_repli(commande,attaquant)
		if frappe[-1]=="B" : combat_repli(commande,defenseur)

	elif frappe[:-1] == "fuite" :
		if frappe[-1]=="A" : combat_fuite(commande,attaquant)
		if frappe[-1]=="B" : combat_fuite(commande,defenseur)
		
	elif frappe[:-1] == "retraite" and not commande_attaque.fini :
		if frappe[-1]=="A" : bataille_retraite(commande,attaquant)
		if frappe[-1]=="B" : bataille_retraite(commande,defenseur)

	elif frappe[:-1] == "capture" :
		if frappe[-1]=="A" : combat_capture(defenseur,attaquant,commande)
		if frappe[-1]=="B" : combat_capture(attaquant,defenseur,commande)


def bataille_bonus_surnombre(attaquant,defenseur):		
	nb_troupes_attaquant = attaquant.NB_TROUPES_GROUPE()
	nb_troupes_defenseur = defenseur.NB_TROUPES_GROUPE()
	
	bonus_troupe_attaquant = 0
	if nb_troupes_attaquant>nb_troupes_defenseur*3 : bonus_troupe_attaquant = 4
	elif nb_troupes_attaquant>nb_troupes_defenseur*2 : bonus_troupe_attaquant = 3
	elif nb_troupes_attaquant>nb_troupes_defenseur*1.5 : bonus_troupe_attaquant = 2
	elif nb_troupes_attaquant>nb_troupes_defenseur : bonus_troupe_attaquant = 1
	else : bonus_troupe_attaquant = 0
	
	'''elif nb_troupes_attaquant<nb_troupes_defenseur*3 : bonus_troupe_attaquant = -4
	elif nb_troupes_attaquant<nb_troupes_defenseur*2 : bonus_troupe_attaquant = -3
	elif nb_troupes_attaquant<nb_troupes_defenseur*1.5 : bonus_troupe_attaquant = -2
	elif nb_troupes_attaquant<nb_troupes_defenseur : bonus_troupe_attaquant = -1'''
	
	return bonus_troupe_attaquant
	
	
def bataille_inflige_dommage(commande_frapper,dommage_init):
	attaquant = commande_frapper.perso
	defenseur = commande_frapper.persos_cible.all()[0]
	T_combattant = [attaquant,defenseur]
	commande_attaque = commande_frapper.commande_parent
	
	dommage = int(math.ceil(float(dommage_init)/4))
	
	for combattant in T_combattant :
		txt = ''
	
		if dommage == 0 : txt = combattant.ENCAISSE_TROUPE_GROUPE(1)	
		elif dommage<0 and combattant == attaquant : txt = combattant.ENCAISSE_TROUPE_GROUPE(dommage*(-1))
		elif dommage>0 and combattant == defenseur : txt = combattant.ENCAISSE_TROUPE_GROUPE(dommage)
		
		if txt!='' : post_MJpersonnage(combattant,txt,0,[])
		
		if combattant.nbTroupes <=0 :
			# cas ou c'est un attaquant de lieu
			if combattant.posture.categorie_combat.nom_info == 'bataillelieu' and not combattant.hote:
				combat_repli(commande_frapper,combattant)
			#
			else :
				texte = combattant.get_nom() +" perd la bataille et se fait capturer"
				post_MJpersonnage(combattant,texte,0,[])
				for combattant_autre in T_combattant :
					if combattant_autre != combattant : combattant.geolier = combattant_autre
				
				for accompagnant in combattant.perso_accompagne.all():
					accompagnant.PV = 0
					accompagnant.leader = None
					accompagnant.save()
			
				combattant.save()
				fin_attaquer(commande_attaque)
	
def combat_inflige_dommage(commande_frapper,dommage):
	attaquant = commande_frapper.perso
	defenseur = commande_frapper.persos_cible.all()[0]
	type_combat = attaquant.posture.categorie_combat.nom_info
	commande_attaque = commande_frapper.commande_parent

	arme = attaquant.arme()
	if arme : special = arme.special()
	else : special = ''
	
	texte_echec = attaquant.get_nom() +" rate son attaque"
	
	if dommage>-2 and dommage<=0 and defenseur.nbGardes()>0 and type_combat!='duel' :
		dommage = 1
	
	elif dommage>0 :
		#dommage = dommage - defenseur.DEFENSE()
		if dommage<=0 : texte_echec = "L'attaque de "+attaquant.get_nom() +" est absorbé par l'armure de "+defenseur.get_nom()
					
		
	if dommage>0 :
		denominateur = defenseur.BONUS_DENOMINATEUR_DOMMAGE() - attaquant.MALUS_DENOMINATEUR_DOMMAGE()
		dommage_subi = int(math.ceil(float(dommage)/denominateur))
		#texte = attaquant.get_nom() +" inflige "+str(dommage_subi)+" dommage à "+defenseur.get_nom()
		#post(commande_frapper,texte,"info")
			
		if type_combat=='duel':
			txt = defenseur.ENCAISSE(dommage_subi,special+';cible')
		else :
			if attaquant.posture.nom_info=='backstab' and attaquant.valeur_competence(attaquant.posture.commpetence_bonus)>=2 : special = special+';cible'
			txt = defenseur.ENCAISSE_GROUPE(dommage_subi,special)

		if txt != '' : post_MJpersonnage(defenseur,txt,0,[])
		
	if dommage<=0 or txt=='' : 
		post(commande_frapper,texte_echec,"info")

	if defenseur.PV<=0 :
		texte = defenseur.get_nom() +" s'effondre dans le combat"
		post(commande_frapper,texte,"info")
		fin_attaquer(commande_attaque)

	else : renvoie_commande(commande_frapper,0)

def combat_capture(attaquant,defenseur,commande_frapper):

	commande_attaque = commande_frapper.commande_parent
	txt = defenseur.get_nom() +" se fait capturer"
	post_MJpersonnage(defenseur,txt,0,[])
	defenseur.geolier = attaquant
	defenseur.prisonnier = True
	defenseur.save()
	fin_attaquer(commande_attaque)

	'''
	if indic_combat == "lieu" and commande_attaque.perso.lieu != commande_attaque.lieux_cible.all()[0]:
		commande_attaque.perso.lieu = commande_attaque.lieux_cible.all()[0]
		commande_attaque.perso.save()
	
	
	'''
		
def combat_fuite(commande_frapper,fuyard):
	texte = fuyard.get_nom()+" arrive à s'enfuir du combat"
	post(commande_frapper,texte,"info")

	commande_attaque = commande_frapper.commande_parent
	
	#creer Commande de la fuite
	action = Action.objects.get(nom_info="fuir")
	date_debut = timezone.now()
	date_fin = date_debut+timedelta(hours=float(jeu.base_delay)*(action.delay/100))
	
	c = Commande.objects.create(\
	joueur = commande_frapper.joueur, \
	perso = fuyard , \
	lieu = fuyard.lieu, \
	action = action , \
	dissimulation = 0 , \
	date_debut = date_debut , \
	date_fin = date_fin)
	
	for accompagnant in fuyard.perso_accompagne.all():
		c = Commande.objects.create(\
		joueur = accompagnant.joueur.all()[0], \
		perso = accompagnant , \
		lieu = accompagnant.lieu, \
		action = action , \
		dissimulation = 0 , \
		date_debut = date_debut , \
		date_fin = date_fin)
	
	fin_attaquer(commande_attaque)
	
	
def bataille_retraite(commande_frapper,fuyard):
	
	commande_attaque = commande_frapper.commande_parent
	
	lieu = fuyard.lieu
	lieu_fuite = lieu
	if lieu.fuite_id :
		lieu_fuite = lieu.fuite
	elif lieu.lieu_parent_id :
		lieu_fuite = lieu.lieu_parent
	new_secteur = de(lieu_fuite.taille)
	
	texte = "L'armée de "+fuyard.get_nom()+" bat en retraite vers "+lieu_fuite.nom
	post_MJ(lieu,texte,0,[])
	
	fuyard.lieu = lieu_fuite
	fuyard.secteur = new_secteur
	
	texte2 = "En fuite, l'armée de "+fuyard.get_nom()+" se regrouppe dans "+lieu_fuite.nom
	post_MJ(lieu_fuite,texte2,0,[])
	
	fin_attaquer(commande_attaque)

def combat_repli(commande_frapper,fuyard):
	commande_combat = commande_frapper.commande_parent

	texte = fuyard.get_nom()+" abandonne son attaque et se repli"
	post(commande_frapper,texte,"info")
	post(commande_combat,texte,"info")
	
	fuyard.lieu = commande_combat.lieu
	fuyard.save()
	
	fin_attaquer(commande_attaque)
	
############################################# FUIR
	
def verif_fuir(commande) :
	T_verif = []
	return T_verif
	
def init_fuir(commande) :
	
	
	commande.perso.joueur_repere.clear()
	commande.perso.dissimulation = 0
	
	lieu = commande.perso.lieu
	lieu_fuite = lieu
	if lieu.fuite_id :
		lieu_fuite = lieu.fuite
	elif lieu.lieu_parent_id :
		lieu_fuite = lieu.lieu_parent
	commande.lieux_cible.add(lieu_fuite)
	
	new_secteur = de(lieu_fuite.taille)
	if lieu_fuite != lieu :
		commande.perso.lieu = lieu_fuite
		commande.perso.secteur = new_secteur
	else : 
		if lieu_fuite.taille>1 :
			while new_secteur == commande.perso.secteur : new_secteur = de(lieu.taille)
		commande.perso.secteur = new_secteur
		
	commande.perso.posture_defaut_melee = Posture.objects.get(id=6)
	commande.perso.occupe = commande
	commande.perso.en_fuite = True
	
	commande.save()
	commande.perso.save()
	
	texte = commande.action.msg_init
	commande.lieu = lieu_fuite
	post(commande,texte,"info")
	
def go_fuir(commande):
	#commande.perso.dissimulation = 0
	commande.perso.en_fuite = False
	commande.perso.save()
	
	texte = commande.action.msg_fin
	commande.lieu = commande.perso.lieu
	post(commande,texte,"info")

############################################# ACHEVER				

def verif_achever(commande):
	perso_cible = commande.persos_cible.all()[0]
	T_verif = []
	if perso_cible.PV>0 : T_verif.append(perso_cible.get_nom()+" doit être inconscient")

	return T_verif

def init_achever(commande):
	commande.perso.occupe = commande
	commande.perso.save()
	
	texte = commande.action.msg_init
	post(commande,texte,"info")

def go_achever(commande):
	
	perso_cible = commande.persos_cible.all()[0]
	
	perso_cible.PV=-1
	perso_cible.vivant = False
	perso_cible.save()

	texte = commande.action.msg_fin
	post(commande,texte,"info")


############################################# DEPOUILLER				

def verif_depouiller(commande):
	perso_cible = commande.persos_cible.all()[0]
	T_verif = []
	if perso_cible.geolier != commande.perso : T_verif.append(commande.perso.get_nom()+" doit avoir "+perso_cible.get_nom()+" comme prisonnier")

	return T_verif

def init_depouiller(commande):
	a=0

def go_depouiller(commande):
	perso_cible = commande.persos_cible.all()[0]
	qst_objets = commande.perso_cible.objets().filter(active=True)
	T_objets = []
	for o in qst_objets :
		o.porte = False
		o.perso = perso_cible
		o.save()
		intitule = o.obj.nom
		if o.obj.cumulable : intitule = intitule+' (*'+str(o.etat)+')'
		T_objets.append(intitule)
	
	texte = commande.action.msg_fin
	post(commande,texte,"info")
	
	if len(T_objets)>0 :
		texte2 = "Sur "+perso_cible.get_nom()+", "+commande.perso.get_nom()+' récupère :\n-'+"\n-".join(T_objets)
	else :
		texte2 = commande.perso.get_nom()+' ne trouve aucun objet intéressant sur '+perso_cible.get_nom()
		
############################################# CAPTURER				

def verif_capturer(commande):
	perso_cible = commande.persos_cible.all()[0]
	T_verif = []
	if perso_cible.PV>0 : T_verif.append(perso_cible.get_nom()+" doit être inconscient")
	if commande.perso.dissimulation >0 : T_verif.append(commande.perso.get_nom()+" ne pourra pas rester caché avec un prisonnier... Pour Capturer une cible, vous ne devez pas être caché")

	return T_verif

def init_capturer(commande):
	a=0

def go_capturer(commande):
	
	perso_cible = commande.persos_cible.all()[0]
	
	perso_cible.geolier = commande.perso
	perso_cible.save()

	texte = commande.action.msg_fin
	post(commande,texte,"info")

############################################# UTILISER

def verif_utiliser(commande):
	
	T_verif = []
	if commande.objet :
		if commande.objet.perso != commande.perso : T_verif.append(commande.perso.get_nom()+" n'a pas l'objet "+objet.nom+" en sa possession")
		if not commande.objet.obj.action and not commande.objet.obj.effet : T_verif.append("L'objet à utiliser ("+commande.objet.obj.nom+") ne provoque pas d'action ou d'effet")
	else : T_verif.append("Pas d'objet défini dans l'action")
	return T_verif
	
def init_utiliser(commande):
	a=0
	
def go_utiliser(commande):	
	objet = commande.objet
	if objet.obj.one_use : 
		objet.etat = objet.etat-1
	objet.save()
	
	if commande.objet.obj.effet :
		
		e = commande.perso.prend_effet(objet.obj.effet)
		if e:
			e.objet_initial = objet
			e.save()
		
	if commande.objet.obj.action :
		champ_recherche2 = ""
		champ_recherche1 = ""
		num = 1
		action = objet.obj.action
		date_debut = timezone.now()
		if '__' in action.nom_info :
			T_nom_info = action.nom_info.split('__')
			action = Action.objects.get(nom_info=T_nom_info[0])
			if champ_recherche2 == '' : champ_recherche2 = T_nom_info[1]
			
		if objet.valeur : num = objet.valeur
		if objet.obj.special : champ_recherche1 = objet.obj.special
		 
		
		timedelta_delay = timedelta(hours=float(jeu.base_delay)*(objet.obj.delay/100))
		date_fin = date_debut+timedelta_delay
		
		c = Commande.objects.create(\
		joueur = commande.joueur, \
		perso = commande.perso , \
		lieu = commande.lieu , \
		action = action , \
		dissimulation = commande.dissimulation , \
		date_debut = date_debut , \
		commande_parent = commande , \
		objet=objet , \
		date_fin = date_fin, \
		num = num,\
		champ_recherche1 = champ_recherche1,\
		champ_recherche2 = champ_recherche2)
	

############################################# DOPPELGANGER				

def verif_doppelganger(commande):
	
	T_verif = []
	if not Perso.objects.filter(nom=commande.champ_recherche1).exists() : T_verif.append("Ce personnage n'existe pas")
	return T_verif

def init_doppelganger(commande):
	a=0
	

def go_doppelganger(commande):
	perso_cible = Perso.objects.filter(nom=commande.champ_recherche1)[0]
	perso = commande.perso
	
	if perso.doppelganger :
		for e in perso.effets().filter(doppelganger=True).all():
			e.fini = True
			e.save()
	
	#creation de l'effet
	objet_initial = None
	if commande.objet : objet_initial = commande.objet
	eft = Effet.objects.filter(nom="doppelganger").all()[0]
	
	effet = Effet_perso.objects.create(\
	perso = perso,\
	eft =  eft,\
	objet_initial = objet_initial ,\
	special = perso_cible.get_nom_info(),\
	commence = True)
	


############################################# TERREUR

def verif_terreur(commande):
	
	T_verif = []
	return T_verif

def init_terreur(commande):
	a=0
	
def go_terreur(commande):
	perso = commande.perso
	
	if perso.leader : perso_cible = perso.leader.occupe.persos_cible.all()[0]
	else : perso_cible = commande.persos_cible.all()[0]
	if perso_cible.leader : perso_cible = perso_cible.leader
	
	valeur = commande.num
	
	val_officier = perso_cible.valeur_competence_str('officier')
	val_aura = perso_cible.valeur_competence_str('aura')
	nb_fuite = valeur*3 - val_officier*2 - val_aura
	perso_cible.nbGardes = perso_cible.nbGardes-nb_fuite
	perso_cible.save()
	
	for p in perso_cible.perso_accompagne.all() :
		val_officier = p.valeur_competence_str('officier')
		val_aura = p.valeur_competence_str('aura')
		nb_fuite = valeur*3 - val_officier*2 - val_aura
		p.nbGardes = p.nbGardes-nb_fuite
		p.save()
		
	#mettre effet sur perso pour eviter qu'il en fasse plusieurs d'affilée
	eft = Effet.objects.filter(active=True).filter(nom='Terreur').filter(classe='').all()[0]
	if eft : perso.prend_effet(eft)
	
############################################# DOMMAGE

def verif_dommage(commande):
	
	T_verif = []
	return T_verif

def init_dommage(commande):
	a=0
	
def go_dommage(commande):
	perso = commande.perso
	perso_cible = commande.persos_cible.all()[0]
	
	valeur = commande.num
	special = commande.champ_recherche1
	
	txt = perso_cible.ENCAISSE_GROUPE(valeur,special)
	
	#mettre effet sur cible pour eviter qu'il en subisse plusieurs d'affilée
	eft = Effet.objects.filter(active=True).filter(nom='Douleur').filter(classe='').all()[0]
	if eft : perso.prend_effet(eft)
	
############################################# FUITE_AUTO

def verif_fuite_auto(commande):
	
	T_verif = []
	return T_verif

def init_fuite_auto(commande):
	commande_attaque = commande.perso.occupe
	fin_attaquer(commande_attaque)
	
	init_fuir(commande)
	
def go_fuite_auto(commande):
	go_fuir(commande)
	
############################################# MAJESTE

def verif_majeste(commande):
	
	T_verif = []
	return T_verif

def init_majeste(commande):
	perso = commande.perso
	valeur = commande.num
	if valeur == 3 : T_persos_cible = perso.lieu.persos_presents.filter(secteur=perso.secteur).exclude(joueur=perso.joueur).all()
	else : T_persos_cible = [commande.persos_cible.all()[0]]
	
	for p in T_persos_cible :
		if not p.en_combat :
			if p.occupe :
				#Annule la commande en cours du perso sous l'attaque
				c = p.occupe
				c.erreur = True
				c.desc = p.get_nom()+" interrompt son action en cours et s'immobilise sous l'injonction de "+perso.get_nom()
				c.save()
			p.occupe = commande
		
		else :
			commande_attaque = p.occupe
			texte = p.get_nom()+" s'arrète de combattre et s'immobilise sous l'injonction de "+perso.get_nom()
			post_MJpersonnage(p,texte,0,[])
			globals()['fin_'+commande_attaque.action.nom_info.lower()](commande_attaque)
			p.occupe = commande
			
	commande.save()
	#ajouter effet MAJESTE
	qst_eft = Effet.objects.filter(active=True).filter(nom='Majesté').filter(classe='').all()
	if len(qst_eft)>0 : 
		e = perso.prend_effet(qst_eft[0])
		e.date_fin = commande.action.date_fin
		e.save()
		
	
	
def go_majeste(commande):
	
	a=0
		
############################################# REPLI	

def verif_repli(commande):
	
	T_verif = []
	return T_verif
	
def init_repli(commande):
	a=0
	
def go_repli(commande):
	perso = commande.perso
	valeur = commande.num
	
	i = i+1 - de(3)
	if i > 2 : i=2
	
	if i>=0 :
		if perso.leader : perso_cible = perso.leader.occupe.persos_cible.all()[0]
		else : perso_cible = commande.persos_cible.all()[0]
		if perso_cible.leader : perso_cible = perso_cible.leader
		
		p=perso_cible
		if p.en_combat:
		
			type_combat = p.posture.categorie_combat.nom_info
			T_posture_duel = ["duel_defense","duel_defense","duel_defense"]
			T_posture_melee = ["arret","fuir","serendre"]
			T_posture_meleelieu_hote = ["defense_lieu","laisserpasser","laisserpasser"]
			T_posture_meleelieu = ["attaque_lieu","repli","repli"]
			T_posture_bataille = ["bataille_defense","bataille_retraite","bataille_retraite"]
			T_posture_bataillelieu_hote = ["bataille_defense_lieu","bataille_defense_lieu","bataille_laisserpasser"]
			T_posture_bataillelieu = ["bataille_lieu","bataille_repli","bataille_repli"]
			
			if type_combat.nom_info == "duel" and i>0 : p.posture = Posture.objects.get(nom_info=T_posture_duel[i])
			elif type_combat.nom_info == "melee" : p.posture = Posture.objects.get(nom_info=T_posture_melee[i])
			elif type_combat == "meleelieu" : 
				if p.hote : p.posture = Posture.objects.get(nom_info=T_posture_meleelieu_hote[i])
				else : p.posture = Posture.objects.get(nom_info=T_posture_meleelieu[i])
			elif type_combat == "bataillelieu" : 
				if p.hote : p.posture = Posture.objects.get(nom_info=T_posture_bataillelieu_hote[i])
				else : p.posture = Posture.objects.get(nom_info=T_posture_bataillelieu[i])
			elif type_combat == "bataille" : p.posture = Posture.objects.get(nom_info=T_posture_bataille[i])
			
			p.save()
	
###########################################	EFFETS
##################################################

def effet_guerison(effet):
	effet.fini=True
	effet.save()
	effet.perso.PV = effet.perso.PV + effet.valeur*effet.eft.bonus_PV
	effet.perso.save()
	
def effet_guerison_eft_negatif(effet):
	perso = effet.perso
	qst_effets = perso.effets().filter(eft__negatif)
	for e in qst_effets :
		if e.eft.fonction_suivant in effet.eft.special.split(';'):
			e.fini = True
			e.save()

def effet_reveil(effet):
	perso = effet.perso
	if perso.PV == 0 : 
		perso.PV =1
		perso.save()

def effet_concentration(effet):
	perso = effet.perso
	if perso.occupe and perso.occupe.date_fin < timezone.now() + timedelta(days=100) :
		commande = perso.occupe
		valeur_division = effet.valeur+1
		
		duree_commande = commande.date_fin-timezone.now()
		duree_minute = (duree_commande.seconds/60) + (duree_commande.days*24*60)
		duree_minute = int(duree_minute/valeur_division)
	
		new_date_fin = timezone.now() + timedelta(hours=float(duree_minute*60))
		
		commande.date_fin = new_date_fin
		commande.self
		
	
###### MALADIE

def effet_rhume(effet):
	#guerison
	jet = de(100)
	print(jet)
	if jet>90 :
		effet.fini=True
		
	#eternuement
	elif jet<=40 :
		effet.date_fin = timezone.now()+timedelta(hours=float(jeu.base_delay)*(effet.eft.delai/100))
		if effet.perso.dissimulation>0 :
			effet.perso.dissimulation=0
			effet.perso.save()
		texte='ATCHAAAAAAA !\nVisiblement enrhumé, '+effet.perso.get_nom()+' éternue Bruyamment'
		post_MJpersonnage(effet.perso,texte,0,[])
		
	effet.save()
			
def effet_grippe(effet):
	max_valeur = 4
	jet = de(100)
	#guerison
	if jet>90 :
		effet.valeur = effet.valeur-1
		if effet.valeur<=0 : effet.fini=True

	#agravation
	elif jet<=40 and effet.valeur<max_valeur :
		effet.date_fin = timezone.now()+timedelta(hours=float(jeu.base_delay)*(effet.eft.delai/100))
		effet.valeur = effet.valeur+1

		if effet.valeur>=max_valeur and effet.perso.PV>0 : 
			effet.perso.PV=0
			effet.valeur = max_valeur-1
		
		effet.perso.save()
		
		if effet.perso.PV==0 :  texte='Visiblement gravement malade, '+effet.perso.get_nom()+ " perd soudainement connaissance"
		else : texte='Visiblement malade, '+effet.perso.get_nom()+ " s'affaiblit"
		post_MJpersonnage(effet.perso,texte,0,[])
		
	effet.save()

			
def effet_peste(effet):
	
	
	#guerison
	jet = de(100)
	if jet>90 :
		effet.valeur = effet.valeur-1
		if effet.valeur<=0 : effet.fini=True
	#agravation
	elif jet<=40 :
		effet.date_fin = timezone.now()+timedelta(hours=float(jeu.base_delay)*(effet.eft.delai/100))
		
		effet.valeur = effet.valeur+1
		effet.perso.PV=effet.perso.PV-1
		if effet.valeur>4 and effet.perso.PV>0 : effet.perso.PV=0
		
		effet.perso.save()
		
		if effet.perso.PV==0 :  texte='Visiblement gravement malade, '+effet.perso.get_nom()+ " perd soudainement connaissance"
		elif effet.perso.PV==1 :  texte='Visiblement malade, '+effet.perso.get_nom()+ " s'affaiblit"
		else : texte='Visiblement malade, '+effet.perso.get_nom()+ " s'affaiblit"
		post_MJpersonnage(effet.perso,texte,0,[])
			
	effet.save()
			