from django.utils import timezone
from datetime import timedelta
from django.http import *

from .models import Jeu
from .models import Perso
from .models import Lieu
from .models import Post
from .models import Action
from .models import Commande


from .fonctions import *
from .fonctions_actions import *
from .fonctions_base import *

from math import *



#############################


def envoie_commande(joueur,perso,action,T_form,chance,date_debut):
	jeu = Jeu.objects.get(id=1)
	
	texte = T_form[0]
	T_persos_cible = T_form[1]
	T_lieux_cible = T_form[2]
	champ_recherche1 = T_form[3]
	champ_recherche2 = T_form[4]
	champ_texte = T_form[5]
	T_instant = T_form[6]
	
	
	
	c = Commande.objects.create(joueur = joueur, perso = perso , action = action , texte_post=texte, dissimulation=perso.dissimulation*10 , chance_reussite = action.chance_reussite , bonus_reussite=chance , date_debut = date_debut)
	c.date_fin = c.date_debut+timedelta(hours=float(jeu.base_delay)*(action.delay/100))
	
	#c.desc = traduction_msg(c.action.msg_encours,c)
	
	for perso_cible in T_persos_cible :
		c.persos_cible.add(perso_cible)
	
	for lieu_cible in T_lieux_cible :
		c.lieux_cible.add(lieu_cible)
		
	if champ_recherche1 : c.champ_recherche1 = champ_recherche1
	if champ_recherche2 : c.champ_recherche1 = champ_recherche2
	if champ_texte : c.champ_texte = champ_texte
	if T_instant[0] : c.instant_heure = T_instant[0]
	if T_instant[1] : c.instant_heure = T_instant[1] 
	if T_instant[2] : c.instant_mois = T_instant[2] 
			
	c.save()
	
	if date_debut <= c.created_date :
		INIT_commande(c)
	else :
		T_verif = aiguille_commande("VERIF",c)
		if len(T_verif) != 0 : erreur(commande,T_verif)
		

	
def renvoie_commande(commande,bonus_chance_reussite):
	T_form = ["" , commande.persos_cible , commande.lieux_cible , commande.champ_recherche1 , commande.champ_recherche2 , commande.champ_texte , [commande.instant_heure,commande.instant_heure,commande.instant_mois]]
	date_debut = timezone.now()
	envoie_commande(commande.joueur , commande.perso , commande.action , T_form , bonus_chance_reussite , date_debut)

def envoie_commande_differe(joueur,perso,action,T_form,chance):
	
	if perso.occupe :
		qst_commande_perso = Commande.objects.filter(perso = perso).filter(fini = False).order_by('-created_date')
		if qst_commande_perso :
			last_commande = qst_commande_perso[0]
			date_debut = last_commande.date_fin+timedelta(seconds=10)
		else :
			perso.occupe = None
			date_debut = timezone.now()	
	else : date_debut = timezone.now()
	
	envoie_commande(joueur,perso,action,T_form,chance,date_debut)
