import math
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from threading import Thread

from django.contrib.auth.models import User
from .models import *
from .fonctions import *
from .thread import *
from .fonctions_actions import post_MJ, post, post_MJpersonnage, post_general
from .reset_base import *

from .forms import *




# Create your views here.

jeu = Jeu.objects.get(id=1)
qst_joueur = Joueur.objects.filter(active=True)

# Création des threads
#thread_1 = thread_jeu()
#thread_1.start()

def return_jeu_nom_info():
	jeu = Jeu.objects.get(id=1)
	return jeu.nom_info

@login_required(login_url='/forum/accounts/login/')
def index_redirect(request):
	joueur = Joueur.objects.get(user = request.user)
	return HttpResponseRedirect('/forum/-'+str(joueur.id))

def indexlieu_redirect(request):
	joueur = Joueur.objects.get(user = request.user)
	return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id))
	
def lieu_redirect(request,lieu_id):
	joueur = Joueur.objects.get(user = request.user)
	return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/'+str(lieu_id)+'/1/1/1')

def message_redirect(request):
	joueur = Joueur.objects.get(user = request.user)
	return HttpResponseRedirect('/forum/messagerie/-'+str(joueur.id)+'/0/all')	

	
@login_required(login_url='/forum/accounts/login/')
def index(request,joueur_id):
	onload()
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	joueur = get_object_or_404(Joueur, pk=joueur_id)
	joueur_reel = Joueur.objects.get(user = request.user)
	if joueur.user!=request.user and joueur_reel.statut!='MJ' : 
		return HttpResponseRedirect('/forum/-'+str(joueur_reel.id))
	
	
	list_perso = joueur.list_persos()
	list_territoire = Lieu.objects.filter(active=True).filter(hote__isnull=False).filter(hote__joueur=joueur).order_by('priorite_temp')
	
	list_derniers_posts = Post.objects.none()
	for p in list_perso :
		list_post_ds_lieu = Post.objects.filter(active=True).filter(created_date__lt=timezone.now()).filter(lieu=p.lieu).filter(Q(dissimulation=0) | Q(joueur_connaissant=joueur) | Q(perso__joueur=joueur)) #controler la visibilite des posts
		if list_post_ds_lieu:
			dernier_post=list_post_ds_lieu.filter(id=list_post_ds_lieu.latest('created_date').id)
			list_derniers_posts = list_derniers_posts.union(dernier_post)
	
	for lieu in list_territoire :
		if lieu.inconnu or lieu.secret :
			if not joueur in lieu.users_connaissants.all() : lieu.users_connaissants.add(joueur)
			if not joueur in lieu.users_connaissants_place.all() : lieu.users_connaissants_place.add(joueur)
	
	T_date_jeu = jeu.convert_date(timezone.now())
	date_jeu = format_date_jeu(T_date_jeu,jeu.format_date)
	
	
	context = {'nom_jeu':nom_jeu,'joueur':joueur,'joueur_reel':joueur_reel,'qst_joueur':qst_joueur,'list_perso': list_perso, 'list_derniers_posts':list_derniers_posts, 'list_territoire':list_territoire, 'date':date_jeu}
	
	return render(request, 'forum/index.html', context)


	
@login_required(login_url='/forum/accounts/login/')
def indexlieu(request,joueur_id):
	#lieu = get_object_or_404(Lieu, pk=lieu_id)
	onload()
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	
	joueur = get_object_or_404(Joueur, pk=joueur_id)
	joueur_reel = Joueur.objects.get(user = request.user)
	if joueur.user!=request.user and joueur_reel.statut!='MJ' : 
		return HttpResponseRedirect('/forum/lieu-'+str(joueur_reel.id))
	
	if joueur.statut == 'MJ' :
		list_lieux = Lieu.objects.filter(active=True)
	else :
		list_lieux = Lieu.objects.filter(active=True).filter(Q(inconnu=False) | Q(users_connaissants=joueur) | (Q(hote__maison=joueur.maison) & Q(hote__isnull=False))).distinct()#Lieu.users_connaissants.filter(joueur).exists())
	list_lieux = list_lieux.order_by('priorite_temp')
	
	list_derniers_posts = Post.objects.none()
	for L in list_lieux :
		list_post_ds_lieu = Post.objects.filter(active=True).filter(created_date__lt=timezone.now()).filter(lieu=L).filter(Q(dissimulation=0) | Q(joueur_connaissant=joueur) | Q(perso__joueur=joueur)) #controler la visibilite des posts
		if list_post_ds_lieu:
			dernier_post=list_post_ds_lieu.filter(id=list_post_ds_lieu.latest('created_date').id)
			list_derniers_posts = list_derniers_posts.union(dernier_post)
	
	for lieu in list_lieux:
		print(lieu.nom+' - '+str(lieu.priorite_temp))
		list = lieu.users_connaissants.all()
		for a in list:
			print('	'+a.nom)

		#print(lieu.passages.objects.all())
	
	context = {'nom_jeu':nom_jeu,'joueur':joueur,'joueur_reel':joueur_reel,'qst_joueur':qst_joueur,'list_lieux': list_lieux,'list_derniers_posts':list_derniers_posts}
	return render(request, 'forum/index_lieu.html', context)


def regles_init(request,regle_id):
	if request.user.is_authenticated:
		joueur_reel = Joueur.objects.get(user = request.user)
		print(joueur_reel)
		return HttpResponseRedirect('/forum/regles/-'+str(joueur_reel.id)+'/'+str(regle_id)+'/')
	else : return HttpResponseRedirect('/forum/regles/-0/'+str(regle_id)+'/')


def regles(request,joueur_id,regle_id):
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	
	if joueur_id!=0 and request.user.is_authenticated:
		joueur = get_object_or_404(Joueur, pk=joueur_id)
		joueur_reel = Joueur.objects.get(user = request.user)
		if joueur.user!=request.user and joueur_reel.statut!='MJ' : 
			return HttpResponseRedirect('/forum/regles/-0/'+str(regle_id)+'/')
	else : 
		joueur_reel = False
		joueur = False
	
	qst_titre_regle = Regle.objects.filter(parent=None).filter(active=True).exclude(nom_info='index').order_by('priorite')
	
	if regle_id == 0 :
		rubrique = get_object_or_404(Regle, id=jeu.regle_index.id)
	else :
		rubrique = get_object_or_404(Regle, pk=regle_id)
	qst_sstitre_regle = Regle.objects.filter(parent=rubrique).filter(active=True).order_by('priorite')
	
	print(rubrique)
	context = {'nom_jeu':nom_jeu,'joueur':joueur,'joueur_reel':joueur_reel,'qst_joueur':qst_joueur,'rubrique':rubrique,'qst_titre_regle':qst_titre_regle,'qst_sstitre_regle':qst_sstitre_regle}
	return render(request, 'forum/regles.html', context)


def background(request,joueur_id,bg_id):
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	
	
		
	if joueur_id!=0 and request.user.is_authenticated:
		joueur = get_object_or_404(Joueur, pk=joueur_id)
		joueur_reel = Joueur.objects.get(user = request.user)
		if joueur.user!=request.user and joueur_reel.statut!='MJ' : 
			return HttpResponseRedirect('/forum/background/-0/'+str(bg_id))
			
	else :
		joueur = False
		joueur_reel = False
		
		
	qst_titre_background = Background.objects.filter(parent=None).filter(active=True).order_by('priorite')
	
	rubrique = get_object_or_404(Background, pk=bg_id)
	
	qst_sstitre_backg = Background.objects.filter(parent=rubrique).filter(active=True).order_by('priorite')	
	
	qst_maisons = False
	qst_persos = False
	
	if rubrique.nom_info == 'maisons' : qst_maisons = Maison.objects.filter(active=True).order_by('priorite')
	elif rubrique.nom_info == 'persos' : qst_persos = Perso.objects.filter(active=True).order_by('priorite')
	
	context = {'nom_jeu':nom_jeu,'joueur':joueur,'joueur_reel':joueur_reel,'qst_joueur':qst_joueur,'qst_titre_background':qst_titre_background,'qst_sstitre_backg':qst_sstitre_backg,'rubrique':rubrique,'qst_maisons':qst_maisons,'qst_persos':qst_persos}
	return render(request, 'forum/background.html', context)

@login_required(login_url='/forum/accounts/login/')
def lieu(request,lieu_id,joueur_id,perso_id,action_str,num_page):
	
	#print('\n## DEBUT LOAD PAGE : '+str(timezone.now())+"\n")
	onload()
	#print('## FIN fonction onload() : '+str(timezone.now()))
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	
	perso_joueur = get_object_or_404(Perso, pk=perso_id)
	
	
	
	joueur = get_object_or_404(Joueur, pk=joueur_id)
	joueur_reel = Joueur.objects.get(user = request.user)
	if joueur.user!=request.user and joueur_reel.statut!='MJ' : 
		return HttpResponseRedirect('/forum/lieu/-'+str(joueur_reel.id)+'/'+str(lieu_id)+'/'+str(perso_id)+'/1/1')
	
	#DEFINI options et objet implique -- l'ID doit etre celui dans CLASS OBJET_PERSO
	obj_id = 0
	option = '0'
	if ':' in action_str :
		T_action_str = action_str.split(':')
		action_str = T_action_str[0]
		option = T_action_str[1]
	if '!' in action_str :
		T_action_str = action_str.split('!')
		action_id = int(T_action_str[0])
		obj_id = int(T_action_str[1])
	
	else : action_id = int(action_str)
	
	if not Action.objects.filter(pk=action_id).exists() : return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/'+str(lieu_id)+'/'+str(perso_id)+'/1/1')
	
	T_date_jeu = jeu.convert_date(timezone.now())
	date_jeu = format_date_jeu(T_date_jeu,jeu.format_date)	
	lieu = get_object_or_404(Lieu, pk=lieu_id)
	
	if not Lieu.objects.filter(id=lieu.id).filter(Q(inconnu=False) | Q(users_connaissants=joueur) | (Q(hote__maison=perso_joueur.maison) & Q(hote__maison__isnull=False))).exists() and joueur.statut!="MJ" :
		return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/1/'+str(perso_id)+'/1/1')

	action = get_object_or_404(Action, pk=action_id)
	
	
	#DEFINI LA LISTE DES PERSOS PRESENTS
	list_all_perso = Perso.objects.filter(lieu=lieu).filter(active=True)
	
	#persos du joueur
	list_perso_joueur = list_all_perso.filter(joueur=joueur).order_by('-hote','priorite')
	
	#persos des autres joueurs
	if joueur.statut == 'MJ':
		list_perso = list_all_perso.exclude(joueur=joueur).order_by('-hote','priorite_temp').distinct()
	else :
		list_perso = list_all_perso.exclude(joueur=joueur).filter(Q(dissimulation=0) | Q(joueur_repere=joueur)).order_by('-hote','priorite_temp')
		'''if lieu.dissimulation>0 :
			
			if lieu.taille>1 :
				T_secteurs = []
				for p1 in list_perso_joueur : 
					if not p1.secteur in T_secteurs : T_secteurs.append(p1.secteur)
				for p2 in list_perso :
					if not p2.secteur in T_secteurs : list_perso = list_perso.exclude(id=p2.id)'''
	
	# Cas d'une action programme : le perso prend des donnees temporaire
	commande_precede = None
	programme = False
	if option[:4] == 'prog' :
		commande_precede = perso_joueur.last_commande_programme()
		if commande_precede : 
			perso_lieu_initial = perso_joueur.lieu
			
			perso_joueur = prog_perso_temp(commande_precede)
			perso_joueur.occupe = None
			programme = True
			
			if perso_joueur.lieu != lieu : return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/'+str(perso_joueur.lieu.id)+'/'+str(perso_joueur.id)+'/1:prog/1')
		else : return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/'+str(lieu.id)+'/'+str(perso_joueur.id)+'/1/1')
	
	edit_commande = None
	if option == 'editable' :
		edit_commande = perso_joueur.commande_attente()
		if edit_commande :
			edit_commande.post.delete()
			edit_commande.delete()
	
	# VERIF si le perso est bien OK dans ce lieu pour ce joueur
	if perso_joueur.lieu and perso_joueur.lieu != lieu : 
		return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/'+str(perso_joueur.lieu.id)+'/'+str(perso_joueur.id)+'/1/1')
	
	if perso_id!=1 and not (objet_ds_manytomany(joueur,perso_joueur.joueur) and perso_joueur.lieu == lieu and perso_joueur.id == perso_id) :
		perso_joueur = Perso.objects.get(id = 1)
	
	if perso_joueur.id == 1 :
		if joueur.statut=='MJ' and action.id==1 :
			action = Action.objects.get(id = 35)
		elif joueur.statut!='MJ':
			action = Action.objects.get(id = 1)
			if list_perso_joueur and joueur.statut!='MJ' :
				return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/'+str(lieu.id)+'/'+str(list_perso_joueur[0].id)+'/1/1')
				
	
	# DEFINITION DE LA LISTE DE POST
	if joueur.statut == 'MJ':
		list_posts = Post.objects.filter(active=True).filter(lieu__id=lieu.id).filter(created_date__lt=timezone.now()).order_by('-created_date')
	else :
		list_posts = Post.objects.filter(active=True).filter(lieu__id=lieu.id).filter(created_date__lt=timezone.now()).filter(Q(dissimulation=0) | Q(joueur_connaissant=joueur) | Q(joueur=joueur)).order_by('-created_date').distinct()
	
	if option == 'msg' : list_posts = list_posts.filter(style="msg")
	elif option == 'talk': list_posts = list_posts.exclude(Q(style="sys") | Q(style="info"))
	
	#GESTION DU NB DE PAGES
	post_par_page = joueur.nb_posts_par_page
	nb_post = list_posts.count()
	list_posts = list_posts[((num_page-1)*post_par_page):(num_page*post_par_page)]
	
	if num_page>(nb_post/post_par_page)+1 : num_page=1
	
	T_page = define_num_page(num_page,post_par_page,nb_post)
	
	
	#DEFINITION DES ACTIONS POSSIBLES
	if joueur.statut == 'MJ' and perso_joueur.id == 1 : list_action = Action.objects.filter(active=True).filter(visible=True).exclude(action_parent__isnull=False).filter(MJ_only=True)
	else : list_action = define_list_action(perso_joueur).order_by('categorie__priorite','priorite')
	
	#LISTE DES PASSAGES
	list_passage = Lieu.objects.filter(active=True).filter(passages=lieu).filter(Q(users_connaissants_place=joueur) | Q(secret=False)).distinct().order_by('priorite_temp')
	
	# VERIF si l'action est bien OK pour ce perso
	if not action in list_action and perso_id!=1 and not action.OK_ds_post_action :
		print('-- NO ACTION')
		return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/'+str(lieu.id)+'/'+str(perso_joueur.id)+'/1/1')
	
	# VERIF si l'objet necessaire est bien dans l'equipement du perso
	objet = False
	if action.implique_objet:
		if perso_joueur.a_objet(Objet.objects.get(pk=obj_id)):
			objet = Objet_perso.objects.get(pk=obj_id)
			print('OBJET OK')
		else :	
			print('-- NO OBJET')
			return HttpResponseRedirect('/forum/perso/-'+str(joueur.id)+'/'+str(perso_joueur.id)+'/equipement/1/')
			
	#MAJ des persos
	for p in list_all_perso : 
		if p.occupe and p.occupe.fini and (p.occupe or p.en_soin or p.en_combat):
			p.save()
		elif not p.occupe_id and (p.en_soin or p.en_combat):
			p.save()
		if p.leader_id and p.leader.lieu != lieu : p.save()
		if len(p.perso_accompagne.all())>0 :
			for pa in p.perso_accompagne.all() :
				if pa.lieu != p.lieu : pa.save()
	
	if objet and objet.obj.action and action.nom_info == 'utiliser':
		action = objet.obj.action
	
	#POST DU FORMUAIRE
	if request.method == "POST":
		#print('POST : '+str(timezone.now()))
		form = PostForm2(request.POST)
		#print(form.resultat_cible)
		if form.is_valid():
			if (joueur.statut == 'MJ' and perso_joueur.id == 1) or (Perso.objects.filter(joueur=joueur).filter(active=True).filter(id=perso_joueur.id).exists()) :
				texte = form.cleaned_data['texte']
				perso_cible = form.cleaned_data['perso_cible']
				persos_cible = form.cleaned_data['persos_cible']
				lieu_cible = form.cleaned_data['lieu_cible']
				lieux_cible = form.cleaned_data['lieux_cible']
				champ_recherche1 = form.cleaned_data['champ_recherche1']
				champ_recherche2 = form.cleaned_data['champ_recherche2']
				champ_texte = form.cleaned_data['champ_texte']
				heure_cible = form.cleaned_data['heure_cible']
				jour_cible = form.cleaned_data['jour_cible']
				mois_cible = form.cleaned_data['mois_cible']
				option = form.cleaned_data['option_action']
				posture_cible = form.cleaned_data['posture_cible']
				resultat_cible = form.cleaned_data['resultat_cible']
				num = 0
				
				action_commande = action
				if action.options : action_commande = option
				if obj_id!=0 : champ_recherche2 = obj_id
				
				T_persos_cible = []
				if perso_cible : T_persos_cible.append(perso_cible)
				for p_cible in persos_cible.all(): T_persos_cible.append(p_cible)
				
				T_lieux_cible = []
				if lieu_cible : T_lieux_cible.append(lieu_cible)
				if lieux_cible :
					for l_cible in lieux_cible.all(): T_lieux_cible.append(l_cible)
				
				T_form = [texte , T_persos_cible , T_lieux_cible , champ_recherche1 , champ_recherche2 , champ_texte , [heure_cible,jour_cible,mois_cible] , posture_cible , resultat_cible , num]
				print('## DEBUT ENVOIE COMMANDE  : '+str(timezone.now()))
				envoie_commande(joueur,perso_joueur,lieu,action_commande,T_form,0,timezone.now(),commande_precede)
				#print('\n## FIN ENVOIE COMMANDE  : '+str(timezone.now())+'\n')
				
		else :
			
			for field in form:
				for error in field.errors:
					print(field)
					print(error)
		if programme :
			return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/'+str(perso_lieu_initial.id)+'/'+str(perso_joueur.id)+'/1/1')
		else :
			return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/'+str(lieu.id)+'/'+str(perso_joueur.id)+'/1/1')

	else:
		form = PostForm(perso_joueur,lieu,action,T_date_jeu,edit_commande)
	
	list_Loi_encours = Loi.objects.filter(valide=False).filter(lieu=lieu).filter(active=True)
	
	vote_OK=False
	if list_Loi_encours :
		action_loi = Action.objects.get(nom_info='proposer_loi')
		T_verif = action_loi.verif(perso_joueur)
		if len(T_verif)==0 : vote_OK=True

	list_categorie_action = Categorie_action.objects.all()
	#T_langage_connu = langages_connus(perso_joueur)
	
	context = {'nom_jeu':nom_jeu,'joueur':joueur,'joueur_reel':joueur_reel,'qst_joueur':qst_joueur,\
				'lieu':lieu,'perso_joueur':perso_joueur,'list_passage':list_passage,\
				'action':action,'list_action':list_action,'list_categorie_action':list_categorie_action,'programme':programme,\
				'list_perso':list_perso,'list_perso_joueur':list_perso_joueur,\
				'list_posts':list_posts,'form':form, 'date':date_jeu,\
				'T_page':T_page, 'num_page':num_page,'option':option, 'objet':objet,\
				'list_Loi_encours':list_Loi_encours, 'vote_OK':vote_OK}
				
	print('## FIN LOAD PAGE lieu  : '+str(timezone.now()))
	
	return render(request, 'forum/lieu.html', context)


@login_required(login_url='/forum/accounts/login/')
def message(request,joueur_id,perso_id,filtre):
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	onload()
	
	joueur = get_object_or_404(Joueur, pk=joueur_id)
	joueur_reel = Joueur.objects.get(user = request.user)
	if joueur.user!=request.user and joueur_reel.statut!='MJ' :
		return HttpResponseRedirect('/forum/messagerie/-'+str(joueur.id)+'/'+str(perso_id)+'/')
	
	qst_persos_du_joueur = joueur.list_persos()
	T_msg_nonlu = []
	TT_resultat_attente = []
	perso = Perso.objects.none()
	
	#message joueur
	if perso_id == 0 :
		qst_msg_perso = Post.objects.none()
		perso = Perso.objects.none()
		qst_msg_joueur = Message.objects.filter(active=True).filter(Q(joueurs_cible=joueur) | Q(joueur=joueur)).distinct().order_by('-created_date')
		
		if filtre=='corbeille': qst_msg_joueur = qst_msg_joueur.exclude(joueurs_affiche=joueur)
		else : qst_msg_joueur = qst_msg_joueur.filter(joueurs_affiche=joueur)
		
		if filtre=='reception': qst_msg_joueur = qst_msg_joueur.exclude(joueur=joueur)
		elif filtre=='envoi': qst_msg_joueur = qst_msg_joueur.filter(joueur=joueur)
		
		if joueur.statut == "MJ" : qst_persos_cible = Joueur.objects.filter(active=True).exclude(id=joueur.id)
		else : qst_persos_cible = Joueur.objects.filter(Q(statut="MJ") | Q(allie=joueur)).exclude(id=joueur.id)
		
		#les avertissements MJ :
		if joueur.statut == "MJ" : 
			qst_resultat_attente = Commande.objects.filter(action__appel_resultat=True).filter(active=True).filter(resultat__isnull=True).filter(no_result=False)
			
			for resultat_attente in qst_resultat_attente :
				qst_choix_resultat =  Resultat.objects.filter(active=True).filter(lieu=resultat_attente.lieu).filter(fini=False).filter(action=resultat_attente.action)
				TT_resultat_attente.append([resultat_attente,qst_choix_resultat])
			
		#messages non lus
		qst_msg_nonlu = qst_msg_joueur.filter(joueurs_nonlu=joueur)
		for msg_nonlu in qst_msg_nonlu :
			msg_nonlu.joueurs_nonlu.remove(joueur)
			T_msg_nonlu.append(msg_nonlu)
			
		
	else :
		qst_msg_perso = Post.objects.filter(active=True).filter(style="msg").filter(perso__isnull=False).filter(created_date__lt=timezone.now()).filter(Q(joueur_connaissant=joueur) | Q(joueur=joueur)).distinct().order_by('-created_date')
		qst_msg_joueur = Message.objects.none()
		qst_persos_cible = Joueur.objects.none()
		
		#tous les messages des persos
		if perso_id == 1 :
			if filtre=='reception': qst_msg_perso = qst_msg_perso.exclude(perso__joueur=joueur)
			elif filtre=='envoi': qst_msg_perso = qst_msg_perso.filter(perso__joueur=joueur)
			
		#les messages d'un perso
		else :
			
			perso = get_object_or_404(Perso, pk=perso_id)
			if perso.joueur != joueur : 
				HttpResponseRedirect('/forum/messagerie/-'+str(joueur.id)+'/'+str(qst_persos_du_joueur[0].id))
			qst_msg_perso = qst_msg_perso.filter(Q(persos_cible=perso) | Q(perso=perso)).distinct()
	
			if filtre=='reception': qst_msg_perso = qst_msg_perso.exclude(perso=perso).filter(persos_cible=perso)
			elif filtre=='envoi': qst_msg_perso = qst_msg_perso.filter(perso=perso)
					
	
	#####

	if request.method == "POST":
		form = EnvoieMsg2(request.POST)
		if form.is_valid():
			texte = form.cleaned_data['texte']
			titre = form.cleaned_data['titre']
			persos_cible = form.cleaned_data['persos_cible']
				
			T_form = [texte , titre, persos_cible.all()]
			envoie_msg(joueur,T_form,timezone.now())
			
		else :
			for field in form:
				for error in field.errors:
					print(field)
					print(error)	
		return HttpResponseRedirect('/forum/messagerie/-'+str(joueur.id)+'/'+str(perso_id)+'/'+filtre+'/')
		
	else:
		qst_cible_default = Perso.objects.none()
		texte_default = ''
		titre_default = ''
		#qst_cible_default = Perso.objects.filter(pk=3)
		form = EnvoieMsg(qst_persos_cible,qst_cible_default,texte_default,titre_default)
	
	#T_langage_connu = []
	#if perso : T_langage_connu = langages_connus(perso)
	
	context = {'nom_jeu':nom_jeu,'joueur':joueur,'joueur_reel':joueur_reel,'qst_joueur':qst_joueur,'qst_msg_perso': qst_msg_perso,'qst_msg_joueur': qst_msg_joueur,'filtre':filtre,'perso_id':perso_id,'form':form,'qst_persos_cible':qst_persos_cible,'T_msg_nonlu':T_msg_nonlu,'TT_resultat_attente':TT_resultat_attente,'perso':perso}
	return render(request, 'forum/message.html', context)
	


@login_required(login_url='/forum/accounts/login/')
def perso(request,joueur_id,perso_id):
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	onload()
	
	vol= False
	joueur = get_object_or_404(Joueur, pk=joueur_id)
	joueur_reel = Joueur.objects.get(user = request.user)
	if joueur.user!=request.user and joueur_reel.statut!='MJ' :
		return HttpResponseRedirect('forum/erreur.html')
	
	
	if perso_id==0 :
		qst_persos = joueur.persos.all().filter(active=True).filter(hote=None).order_by('priorite')
		if len(qst_persos)==0 : perso = joueur.persos.all().filter(active=True).order_by('priorite')[0]
		else : perso = qst_persos[0]
	else:
		perso = get_object_or_404(Perso, pk=perso_id)
	
	
	valide = True
	if not perso.active : valide = False
	valide = perso_visible(joueur,perso)
	
	if joueur.statut=="MJ": valide = True
	
	if not valide : perso = Perso.objects.get(id = 1)
	
	if perso.id == 1 :
		return HttpResponseRedirect('/forum/-'+str(joueur.id))
	else :
		
		TTT_competences = perso.sortie_competence()
		T_classe_perso = [perso.get_classe_principale(),perso.get_classe_secondaire(),perso.get_classe_tertiaire()]
		
		qst_perso_accompagnant = Perso.objects.filter(leader=perso).filter(active=True)
		qst_perso_prisonnier = Perso.objects.filter(geolier=perso).filter(active=True)
		rubrique = "fiche"
		etatsante_default = Sante.objects.get(PV=3)
		
		if perso.vol_OK(joueur) : vol=True
		
		if joueur.statut=="MJ":
			if request.method == "POST":
				form = MJDonneEffet2(request.POST)
				if form.is_valid():

					effet_maladie_cible = form.cleaned_data['effet_maladie_cible']
					effet_potion_cible = form.cleaned_data['effet_potion_cible']
					effet_poison_cible = form.cleaned_data['effet_poison_cible']
					effet_divers_cible = form.cleaned_data['effet_divers_cible']
					
					T_donne_eft=[]
					if effet_maladie_cible : T_donne_eft.append(effet_maladie_cible)
					if effet_potion_cible : T_donne_eft.append(effet_potion_cible)
					if effet_poison_cible : T_donne_eft.append(effet_poison_cible)
					if effet_divers_cible : T_donne_eft.append(effet_divers_cible)
					for e in T_donne_eft :
						perso.prend_effet(e)

				return HttpResponseRedirect('/forum/perso/-'+str(joueur.id)+'/'+str(perso.id)+'/')
				
			else:
				qst_effet = Effet.objects.filter(active=True).filter(support='perso').order_by('niv_priorite')
				form = MJDonneEffet(qst_effet)
		else : form = False
		
		context= {'nom_jeu':nom_jeu,'joueur':joueur,'joueur_reel':joueur_reel,'qst_joueur':qst_joueur,'perso': perso,'TTT_competences':TTT_competences,'T_classe_perso':T_classe_perso,'rubrique':rubrique,'etatsante_default':etatsante_default,'qst_perso_prisonnier':qst_perso_prisonnier,'qst_perso_accompagnant':qst_perso_accompagnant,'form':form,'vol':vol}
	
		return render(request, 'forum/desc_perso.html', context)
		
		
@login_required(login_url='/forum/accounts/login/')
def perso_rubrique(request,joueur_id,perso_id,num_page,rubrique):
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	perso = get_object_or_404(Perso, pk=perso_id)
	joueur = Joueur.objects.get(user = request.user)
	
	joueur = get_object_or_404(Joueur, pk=joueur_id)
	joueur_reel = Joueur.objects.get(user = request.user)
	if joueur.user!=request.user and joueur_reel.statut!='MJ' :
		return HttpResponseRedirect('forum/erreur.html')
	
	vol=False
	valide = True
	if not perso.active : valide = False
	if not objet_ds_manytomany(joueur,perso.joueur) : valide = False
	if joueur.statut=="MJ": valide = True
	if perso.id == 1 : valide = False
	
	
	if not valide :
		return HttpResponseRedirect('/forum/perso/-'+str(joueur.id)+'/'+str(perso.id)+'/')
	else :
		
		
		qst_msg_perso = Post.objects.filter(active=True).filter(style="msg").filter(perso__isnull=False).filter(created_date__lt=timezone.now()).filter(Q(persos_cible=perso) | Q(perso=perso)).distinct().order_by('-created_date')
		
		qst_action_perso = Post.objects.filter(active=True).filter(created_date__lt=timezone.now()).filter(perso__isnull=False).filter(perso=perso).distinct().order_by('-created_date')
		
		qst_objet = False
		if rubrique == 'equipement': qst_objet = perso.objets().order_by('obj__classe','obj__niveau_requis')
		if perso.vol_OK(joueur) : vol=True
		
		#T_langage_connu = langages_connus(perso)
		
		if joueur.statut == 'MJ':
			if request.method == "POST":
				form = MJDonneObjet2(request.POST)
				
				if form.is_valid():
					arme_cible = form.cleaned_data['arme_cible']
					armure_cible = form.cleaned_data['armure_cible']
					potion_cible = form.cleaned_data['potion_cible']
					parchemin_cible = form.cleaned_data['parchemin_cible']
					rituel_cible = form.cleaned_data['rituel_cible']
					obj_quete_cible = form.cleaned_data['obj_quete_cible']
					divers_cible = form.cleaned_data['divers_cible']
					
					T_donne_obj=[]
					if arme_cible : T_donne_obj.append(arme_cible)
					if armure_cible : T_donne_obj.append(armure_cible)
					if potion_cible : T_donne_obj.append(potion_cible)
					if parchemin_cible : T_donne_obj.append(parchemin_cible)
					if rituel_cible : T_donne_obj.append(rituel_cible)
					if obj_quete_cible : T_donne_obj.append(obj_quete_cible)
					if divers_cible : T_donne_obj.append(divers_cible)
					#print(T_donne_obj)
					for o in T_donne_obj :
						perso.trouve_obj(o)

				return HttpResponseRedirect('/forum/perso/-'+str(joueur.id)+'/'+str(perso.id)+'/equipement/1/')
				
			else:
				qst_obj = Objet.objects.filter(active=True).order_by('competence_requise','niveau_requis')
				form = MJDonneObjet(qst_obj)
		else : form = False	
		
		context= {'nom_jeu':nom_jeu,'joueur':joueur,'joueur_reel':joueur_reel,'qst_joueur':qst_joueur,'perso': perso,'qst_msg_perso':qst_msg_perso,'qst_action_perso':qst_action_perso,'rubrique':rubrique,'form':form,'qst_objet':qst_objet,'vol':vol}
	
		return render(request, 'forum/desc_perso.html', context)
		
@login_required(login_url='/forum/accounts/login/')
def porte_obj(request,joueur_id,perso_id,objet_id,laisse_ou_porte):
	valide = True
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	
	perso = get_object_or_404(Perso, pk=perso_id)
	joueur = get_object_or_404(Joueur, pk=joueur_id)
	joueur_reel = Joueur.objects.get(user = request.user)
	objet = get_object_or_404(Objet_perso, pk=objet_id)
	
	if joueur.user!=request.user and joueur_reel.statut!='MJ' : valide = False
	if objet.perso!=perso : valide = False
	if not perso.active : valide = False
	if not objet_ds_manytomany(joueur,perso.joueur) : valide = False
	if joueur.statut=="MJ": valide = True
	if perso.id == 1 : valide = False
	
	if valide : 
		if laisse_ou_porte == 1:
			if not objet.porte:

				if objet.obj.classe == 'arme' and perso.arme() : 
					o = perso.arme()
					o.porte = False
					o.save()
				if objet.obj.classe == 'armure' and perso.armure() :
					o = perso.armure()
					o.porte = False
					o.save()
				
				objet.porte=True
				objet.save()
				
				
		else :
			if objet.porte:
				objet.porte=False
				objet.save()
				
		#perso.save()
				
	return HttpResponseRedirect('/forum/perso/-'+str(joueur_id)+'/'+str(perso_id)+'/equipement/1/')	
	
@login_required(login_url='/forum/accounts/login/')	
def traduire_post(request,joueur_id,lieu_id,perso_id,action_id,option,langage_id,post_id,num_page):
	joueur = get_object_or_404(Joueur, pk=joueur_id)
	joueur_reel = Joueur.objects.get(user = request.user)
	if option == '0' : action_str = str(action_id)
	else : action_str = action_str+':'+option
	id_post = 'post_'+str(post_id)
	if joueur.user!=request.user and joueur_reel.statut!='MJ' :
		a=0
	else :
		post = get_object_or_404(Post, pk=post_id)
		lieu = get_object_or_404(Lieu, pk=lieu_id)
		langage = get_object_or_404(Langage, pk=langage_id)
		perso = get_object_or_404(Perso, pk=perso_id)
		
		if joueur.statut == 'MJ' or (joueur in perso.joueur.all() and perso.active and perso.lieu == lieu and langage in perso.langage.all()) :
			post.joueur_traduit.add(joueur)
		
	return HttpResponseRedirect('/forum/lieu/-'+str(joueur_id)+'/'+str(lieu_id)+'/'+str(perso.id)+'/'+action_str+'/'+str(num_page)+'#'+id_post)	
	
@login_required(login_url='/forum/accounts/login/')	
def enlever_traduction(request,joueur_id,post_id,lieu_id,num_page,action_id,option,perso_id):
	joueur_reel = Joueur.objects.get(user = request.user)
	if option == '0' : action_str = str(action_id)
	else : action_str = action_str+':'+option
	id_post = 'post_'+str(post_id)
	if joueur_reel.statut=='MJ' :
		post = get_object_or_404(Post, pk=post_id)
		post.joueur_traduit.remove(joueur_reel)
	return HttpResponseRedirect('/forum/lieu/-'+str(joueur_id)+'/'+str(lieu_id)+'/'+str(perso_id)+'/'+action_str+'/'+str(num_page)+'#'+id_post)
		
@login_required(login_url='/forum/accounts/login/')
def deleteLoi(request,joueur_id,perso_id,loi_id):
	joueur = get_object_or_404(Joueur, pk=joueur_id)
	joueur_reel = Joueur.objects.get(user = request.user)
	if joueur.user!=request.user and joueur_reel.statut!='MJ' :
		return HttpResponseRedirect('forum/erreur.html')
	
	perso = get_object_or_404(Perso, pk=perso_id)
	loi = get_object_or_404(Loi, pk=loi_id)
	lieu = loi.lieu
	
	if perso == loi.perso and perso.lieu==lieu and objet_ds_manytomany(joueur,perso.joueur) :
		
		post_MJpersonnage(perso,perso.nom+' retire sa proposition intitulée '+loi.nom+'" du vote du Sénat',0,[])
		loi.delete()
		return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/'+str(lieu.id)+'/'+str(loi.perso.id)+'/1/1')
	
	else : return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/'+str(lieu.id)+'/1/1/1')

	
@login_required(login_url='/forum/accounts/login/')
def soumettreLoi(request,joueur_id,perso_id,loi_id):
	joueur = get_object_or_404(Joueur, pk=joueur_id)
	joueur_reel = Joueur.objects.get(user = request.user)
	if joueur.user!=request.user and joueur_reel.statut!='MJ' :
		return HttpResponseRedirect('forum/erreur.html')
	
	perso = get_object_or_404(Perso, pk=perso_id)
	loi = get_object_or_404(Loi, pk=loi_id)
	lieu = loi.lieu
	
	if perso == loi.perso and perso.lieu==lieu and objet_ds_manytomany(joueur,perso.joueur) :
		
		post_MJ(lieu,perso.nom+' avance la fin des délibérations et soumet immédiatement au vote sa proposition intitulée "'+loi.nom+'" ',0,[])
		
		loi.commande.date_fin = timezone.now()
		loi.commande.save()
		loi.save()
		return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/'+str(lieu.id)+'/'+str(loi.perso.id)+'/1/1')

	else : return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/'+str(lieu.id)+'/1/1/1')

	
@login_required(login_url='/forum/accounts/login/')
def voteLoi(request,joueur_id,perso_id,loi_id):

	joueur = get_object_or_404(Joueur, pk=joueur_id)
	joueur_reel = Joueur.objects.get(user = request.user)
	if joueur.user!=request.user and joueur_reel.statut!='MJ' :
		return HttpResponseRedirect('forum/erreur.html')
	
	perso = get_object_or_404(Perso, pk=perso_id)
	loi = get_object_or_404(Loi, pk=loi_id)
	lieu = loi.lieu
	if perso.id!=1 and objet_ds_manytomany(joueur,perso.joueur) and perso.lieu == lieu and perso.maison.senateur == perso and not objet_ds_manytomany(perso.maison,loi.maison_a_vote) :
		
		post_MJpersonnage(perso,'La Maison '+perso.maison.nom+' apporte son soutien à la proposition de '+loi.perso.nom+' intitulée "'+loi.nom+'" ',0,[])
		
		loi.maison_a_vote.add(perso.maison)
		loi.save()
		return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/'+str(lieu.id)+'/'+str(loi.perso.id)+'/1/1')
	
	else : return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/'+str(lieu.id)+'/1/1/1')

@login_required(login_url='/forum/accounts/login/')
def annuleVoteLoi(request,joueur_id,perso_id,loi_id):

	joueur = get_object_or_404(Joueur, pk=joueur_id)
	joueur_reel = Joueur.objects.get(user = request.user)
	if joueur.user!=request.user and joueur_reel.statut!='MJ' :
		return HttpResponseRedirect('forum/erreur.html')
	
	perso = get_object_or_404(Perso, pk=perso_id)
	loi = get_object_or_404(Loi, pk=loi_id)
	lieu = loi.lieu
	if perso.id!=1 and objet_ds_manytomany(joueur,perso.joueur) and perso.lieu == lieu and perso.maison.senateur == perso and objet_ds_manytomany(perso.maison,loi.maison_a_vote) and perso != loi.perso :
		post_MJpersonnage(perso,'La Maison '+perso.maison.nom+' retire son soutien à la proposition de '+loi.perso.nom+' intitulée "'+loi.nom+'" ',0,[])
		loi.maison_a_vote.remove(perso.maison)
		loi.save()
		return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/'+str(lieu.id)+'/'+str(loi.perso.id)+'/1/1')
	
	else : return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/'+str(lieu.id)+'/1/1/1')

@login_required(login_url='/forum/accounts/login/')
def masqueMSG(request,msg_id):
	joueur = Joueur.objects.get(user = request.user)
	msg = get_object_or_404(Message, pk=msg_id)
	T_joueurs_cible = msg.joueurs_cible.all()
	if msg.joueur == joueur or joueur in T_joueurs_cible :
		msg.joueurs_affiche.remove(joueur)
	return HttpResponseRedirect('/forum/messagerie/-'+str(joueur.id)+'/0/all/')
	
@login_required(login_url='/forum/accounts/login/')
def restaureMSG(request,msg_id):
	joueur = Joueur.objects.get(user = request.user)
	msg = get_object_or_404(Message, pk=msg_id)
	T_joueurs_cible = msg.joueurs_cible.all()
	if msg.joueur == joueur or joueur in T_joueurs_cible :
		msg.joueurs_affiche.add(joueur)
	return HttpResponseRedirect('/forum/messagerie/-'+str(joueur.id)+'/0/corbeille/')
		
		
################# OUTILS MJ

@login_required(login_url='/forum/accounts/login/')
def deletePost(request,lieu_id,post_id):
	joueur = Joueur.objects.get(user = request.user)
	lieu = get_object_or_404(Lieu, pk=lieu_id)
	post = get_object_or_404(Post, pk=post_id)
	if joueur.statut == 'MJ' or (post.style == "sys" and post.joueur == joueur):
		post.delete()
		#print('/forum/lieu/'+str(lieu.id)+'/'+str(joueur.id)+'/1/1/1')
		return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/'+str(lieu.id)+'/1/1/1')
	
	else : return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/'+str(lieu.id)+'/1/1/1')

@login_required(login_url='/forum/accounts/login/')
def deleteElt(request,joueur_id,perso_id,elt,id):
	
	joueur = get_object_or_404(Joueur, pk=joueur_id)
	joueur_reel = Joueur.objects.get(user = request.user)
	perso = get_object_or_404(Perso, pk=perso_id)
	if joueur.user!=request.user and joueur_reel.statut!='MJ' : 
		return HttpResponseRedirect('/forum/perso/-'+str(joueur_id)+'/'+str(perso_id)+'/')
	if not joueur in perso.joueur.all() and joueur_reel.statut!='MJ' : 
		return HttpResponseRedirect('/forum/perso/-'+str(joueur_id)+'/'+str(perso_id)+'/')
	
	if elt == 'garde' :
		perso.nbGardes = perso.nbGardes-1
		perso.save()
	elif elt == 'troupe':
		perso.nbTroupes = perso.nbTroupes-1
		perso.save()
	elif elt == 'objet' :
		objet = get_object_or_404(Objet_perso, pk=id)
		if objet.perso == perso : 
			if objet.obj and objet.obj.cumulable :
				objet.etat = objet.etat-1
				if objet.etat == 0 : objet.delete()
				else : objet.save()
			else :
				objet.delete()
		return HttpResponseRedirect('/forum/perso/-'+str(joueur_id)+'/'+str(perso_id)+'/equipement/1/')
	elif elt == 'effet' :
		effet = get_object_or_404(Effet_perso, pk=id)
		if effet.perso == perso :
			effet.delete()
			perso.save()
			return HttpResponseRedirect('/forum/perso/-'+str(joueur_id)+'/'+str(perso_id)+'/')
		elif not effet.perso and effet.objet.perso == perso :
			effet.delete()
			return HttpResponseRedirect('/forum/perso/-'+str(joueur_id)+'/'+str(perso_id)+'/equipement/1/')
			
	return HttpResponseRedirect('/forum/perso/-'+str(joueur_id)+'/'+str(perso_id)+'/')
	

	
@login_required(login_url='/forum/accounts/login/')
def liste_commande(request,filtre,tri,str_joueur_id):
	onload()
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	
	joueur = Joueur.objects.get(user = request.user)
	joueur_reel = joueur
	
	if joueur.statut != 'MJ' :
		return render(request, 'forum/erreur.html', {'joueur': joueur})
	
	else :
		
		if str_joueur_id[0]=='p' : 
			joueur_id = 0
			perso_id = int(str_joueur_id.replace('p',''))
		else : 
			joueur_id = int(str_joueur_id)
			perso_id = 0
			
		qst_commande = Commande.objects.all()
		#for c in qst_commande :
		#	c.save()
		
		
		if filtre == 'erreur' : qst_commande = qst_commande.filter(erreur=True)
		elif filtre == 'fini' : qst_commande = qst_commande.filter(fini=True).filter(erreur=False)
		elif filtre == 'encours' : qst_commande = qst_commande.filter(commence=True).filter(fini=False)
		elif filtre == 'programme' : qst_commande = qst_commande.filter(commence=False)
		
		if joueur_id !=0 :  
			qst_commande = qst_commande.filter(joueur__id=joueur_id)
			joueur_commande = Joueur.objects.get(pk=joueur_id)
		else : 
			joueur_commande = Joueur.objects.get(pk=1)
			
		if perso_id !=0 :  
			qst_commande = qst_commande.filter(perso__id=perso_id)
			perso_commande = Perso.objects.get(pk=perso_id)
		else :
			perso_commande = Perso.objects.get(pk=1)
		
		if tri==0 : qst_commande = qst_commande.order_by('-created_date')
		elif tri==1 : qst_commande = qst_commande.order_by('-date_debut')
		else : qst_commande = qst_commande.order_by('-date_fin')
		
		qst_perso = Perso.objects.filter(active=True).order_by('nom')
		
		context = {'nom_jeu':nom_jeu,'joueur':joueur,'joueur_reel':joueur_reel,'qst_joueur':qst_joueur,'qst_commande': qst_commande,'perso_commande':perso_commande,'joueur_commande':joueur_commande,'tri':tri,'filtre':filtre,'IDjoueur':joueur_id,'qst_perso':qst_perso}
		return render(request, 'forum/liste_commandes.html', context)

		
@login_required(login_url='/forum/accounts/login/')
def liste_post(request,joueur_id,perso_id,filtre):
	onload()
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	
	joueur = Joueur.objects.get(user = request.user)
	
	if joueur.statut != 'MJ' :
		return render(request, 'forum/erreur.html', {'joueur': joueur})
	
	else :
		#if filtre == 'all'
		qst_post = Post.objects.filter(active=True)
		
		if filtre == 'infosMJ' : qst_post = qst_post.exclude(info_MJ='')
		elif filtre == 'msg' : qst_post = qst_post.filter(style='msg')
		elif filtre == '-msg' : qst_post = qst_post.exclude(style='msg')
		elif filtre == 'sys' : qst_post = qst_post.filter(style='sys')
		elif filtre == '-sys' : qst_post = qst_post.exclude(style='sys')
		elif filtre == 'info' : qst_post = qst_post.filter(style='info')
		elif filtre == '-info' : qst_post = qst_post.exclude(style='info')
		elif filtre == 'normal' : qst_post = qst_post.filter(style='normal')
		elif filtre == '-normal' : qst_post = qst_post.exclude(style='normal')
		elif filtre == 'lock' : qst_post = qst_post.filter(lock=True)
		elif filtre == '-lock' : qst_post = qst_post.exclude(lock=False)
		
		joueur_post = Perso.objects.get(pk=1)
		perso = Perso.objects.get(pk=1)
		
		if joueur_id !=0 :
			qst_post = qst_post.filter(lieu__id=lieu.id).filter(Q(dissimulation=0) | Q(joueur_connaissant=joueur) | Q(joueur=joueur)).distinct()
			joueur_post = Perso.objects.get(pk=joueur_id)
		elif perso_id !=0 :
			qst_post = qst_post.filter(perso__id=perso_id)
			perso = Perso.objects.get(pk=perso_id)
		
		qst_post = qst_post.order_by('-created_date')
		
		return render(request, 'forum/liste_post.html', {'nom_jeu':nom_jeu,'joueur': joueur,'qst_post': qst_post,'joueur_post':joueur_post,'perso':perso})		
		
		
@login_required(login_url='/forum/accounts/login/')
def liste_perso(request,filtre):
	onload()
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	joueur = Joueur.objects.get(user = request.user)
	joueur_reel = joueur
	
	if joueur.statut != 'MJ' :
		return render(request, 'forum/erreur.html', {'joueur': joueur})
	
	else :
		qst_perso = Perso.objects.all().exclude(id=1)
		
		if filtre == "inactive" : qst_perso = qst_perso.filter(active=False)
		elif filtre == "hote" : qst_perso = qst_perso.filter(active=True).exclude(hote=None)
		else : qst_perso = qst_perso.filter(active=True).filter(hote=None)
		
		if filtre == "joueur": qst_perso = qst_perso.order_by('joueur__id','priorite')
		elif filtre == "lieu": qst_perso = qst_perso.order_by('lieu__priorite_temp','priorite')
		else : qst_perso = qst_perso.order_by('maison__priorite','hote','priorite')
		
		T_qst_perso = []
		for p in qst_perso : 
			T_qst_perso.append([p,p.sortie_competence()])
		context = {'nom_jeu':nom_jeu,'joueur':joueur,'joueur_reel':joueur_reel,'qst_joueur':qst_joueur,'qst_perso': T_qst_perso,'filtre':filtre}
		#print('\n## FIN LOAD PAGE  : '+str(timezone.now()))
		return render(request, 'forum/liste_persos.html',context)
		
		
@login_required(login_url='/forum/accounts/login/')
def liste_lieu(request,filtre):
	onload()
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	joueur = Joueur.objects.get(user = request.user)
	joueur_reel = joueur
	
	if joueur.statut != 'MJ' :
		return render(request, 'forum/erreur.html', {'joueur': joueur})
	
	else :
		T_qst_lieu = []
		qst_lieu = Lieu.objects.all()
		
		if filtre != "inactive" : qst_lieu = qst_lieu.filter(active=True)
		else : qst_lieu = qst_lieu.filter(active=False)
		
		if filtre == "maison": qst_lieu = qst_lieu.order_by('maison__priorite','priorite_temp')
		elif filtre == "nbperso": qst_lieu = qst_lieu.annotate(nbperso=Count('persos_presents')).order_by('-nbperso')
		elif filtre == "date": 
			qst_lieu = qst_lieu.order_by('-lieu_post__created_date').filter('')
			#qst_lieu = qst_lieu.distinct()
			#T_qst_lieu = distinctLIO(qst_lieu)
		elif filtre == "nbpost": qst_lieu = qst_lieu.annotate(nbpost=Count('lieu_post')).order_by('-nbpost')
			
		else : qst_lieu = qst_lieu.order_by('priorite_temp')
		
		if len(T_qst_lieu)==0 : T_qst_lieu = qst_lieu.all()
		
		context = {'nom_jeu':nom_jeu,'joueur':joueur,'joueur_reel':joueur_reel,'qst_joueur':qst_joueur,'qst_lieu': T_qst_lieu,'filtre':filtre}
		return render(request, 'forum/liste_lieux.html',context)
		

@login_required(login_url='/forum/accounts/login/')
def liste_maison(request,filtre):
	onload()
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	joueur = Joueur.objects.get(user = request.user)
	joueur_reel = joueur
	
	if joueur.statut != 'MJ' :
		return render(request, 'forum/erreur.html', {'joueur': joueur})
	
	else :
		qst_maison = Maison.objects.all()
		
		if filtre != "inactive" : qst_maison = qst_maison.filter(active=True)
		else : qst_maison = qst_maison.filter(active=False)
		
		if filtre == "influence": qst_maison = qst_maison.order_by('influence','priorite')
		elif filtre == "senateur": qst_maison = qst_maison.order_by('nb_voix_senat','priorite')
		else : qst_maison = qst_maison.order_by('priorite')
		
		T_qst_maison = qst_maison.all()
		
		#####calcul des influences
		comp_aura = Competence.objects.get(nom_info='aura')
		lieu_senat = T_qst_maison[0].senateur.charge.lieu
		
		T_qst_maison2 = []
		prestige_total = 0
		influence_total = 0
		
		#calcul du prestige total
		for maison in T_qst_maison: 
			if maison.get_OK_pr_senat() : prestige_total = prestige_total + maison.prestige
			T_qst_maison2.append(maison)
		
		for maison in T_qst_maison2: 
			if maison.get_OK_pr_senat() : 
				maison.pct_prestige = int(round(float(maison.prestige*100/prestige_total)))
				maison.influence = maison.pct_prestige
				
				for perso in lieu_senat.persos_presents.filter(maison=maison).all() :
					if perso.influence_OK() :
						influence_perso = perso.valeur_competence(comp_aura)
						if perso.charge : influence_perso = influence_perso + perso.charge.influence
						maison.influence = maison.influence+influence_perso
				influence_total = influence_total + maison.influence
					
			else : maison.pct_prestige = maison.pct_prestige = maison.influence = 0
			
		for maison in T_qst_maison2:
			maison.nb_voix_senat = int(round(float(maison.influence*100/influence_total)))
			
		context = {'nom_jeu':nom_jeu,'joueur':joueur,'joueur_reel':joueur_reel,'qst_joueur':qst_joueur,'qst_maison': T_qst_maison2,'filtre':filtre}
		return render(request, 'forum/liste_maisons.html',context)
		
		
@login_required(login_url='/forum/accounts/login/')
def liste_joueur(request,filtre):
	onload()
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	joueur = Joueur.objects.get(user = request.user)
	joueur_reel = joueur
	
	if joueur.statut != 'MJ' :
		return render(request, 'forum/erreur.html', {'joueur': joueur})
	
	else :
		qst_joueur = Joueur.objects.filter(active=True).exclude(statut="MJ").order_by('-priorite')
		
		TT_joueur = []
		for j in qst_joueur :
			qst_perso = Perso.objects.filter(active=True).filter(joueur=j)
			nb_post = Post.objects.filter(active=True).filter(joueur=j).filter(created_date__lt=timezone.now()).count()
			nb_commande = Commande.objects.filter(joueur=j).count()
			last_post = Post.objects.filter(active=True).filter(joueur=j).filter(created_date__lt=timezone.now()).last()
			last_commande = Commande.objects.filter(joueur=j).last()
			
			if last_post and last_commande :
				if last_post.created_date >= last_commande.created_date : last_action = last_post
				else : last_action = last_commande
			elif last_post : last_action = last_post
			else : last_action = last_commande
		
			TT_joueur.append([j,qst_perso,nb_post,nb_commande,last_action])
		
		context = {'nom_jeu':nom_jeu,'joueur':joueur,'joueur_reel':joueur_reel,'qst_joueur':qst_joueur,'TT_joueur':TT_joueur}
		return render(request, 'forum/liste_joueurs.html',context)

@login_required(login_url='/forum/accounts/login/')
def liste_resultat(request,lieu_id,action_id,filtre):
	onload()
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	joueur = Joueur.objects.get(user = request.user)
	joueur_reel = joueur
	action_nom = 'All Actions'
	
	if joueur.statut != 'MJ' :
		return render(request, 'forum/erreur.html', {'joueur': joueur})
	
	else :
		qst_resultat = Resultat.objects.filter(active=True)

		if filtre == 'nonfini' : qst_resultat = qst_resultat.filter(fini=False)
		elif filtre == 'fini' : qst_resultat = qst_resultat.filter(fini=True)
	
		lieu = Lieu.objects.none()
		tri_lieu = True
		if lieu_id !=0 :
			lieu = get_object_or_404(Lieu, pk=lieu_id)
			qst_resultat = qst_resultat.filter(lieu=lieu)
			tri_lieu = False
		if action_id !=0 : 
			action = get_object_or_404(Action, pk=action_id)
			qst_resultat = qst_resultat.filter(action=action)
			action_nom = action.nom
			

		qst_resultat = qst_resultat.order_by('lieu__priorite','action__nom')
		qst_action = Action.objects.filter(active=True).filter(appel_resultat=True)

		context = {'nom_jeu':nom_jeu,'joueur':joueur,'joueur_reel':joueur_reel,'qst_joueur':qst_joueur,'qst_resultat':qst_resultat, 'qst_action':qst_action, 'tri_lieu':tri_lieu, 'filtre':filtre, 'action_id':action_id, 'action_nom':action_nom, 'lieu_select_id':lieu_id, 'lieu_select':lieu}
		return render(request, 'forum/liste_resultats.html',context)

@login_required(login_url='/forum/accounts/login/')
def liste_evenement(request,lieu_id,filtre):
	onload()
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	joueur = Joueur.objects.get(user = request.user)
	joueur_reel = joueur

	if joueur.statut != 'MJ' :
		return render(request, 'forum/erreur.html', {'joueur': joueur})
	
	else :
		qst_evenement = Evenement.objects.filter(active=True)

		if lieu_id !=0 :
			lieu = get_object_or_404(Lieu, pk=lieu_id)
			qst_evenement = qst_evenement.filter(lieu=lieu)

		if filtre == 'avenir' : qst_evenement = qst_evenement.filter(fini=False)
		elif filtre == 'fini' : qst_evenement = qst_evenement.filter(fini=True)


		qst_evenement = Evenement.order_by('lieu__priorite')

		context = {'nom_jeu':nom_jeu,'joueur':joueur,'joueur_reel':joueur_reel,'qst_joueur':qst_joueur,'qst_evenement':qst_evenement}
		return render(request, 'forum/liste_evenements.html',context)

		
@login_required(login_url='/forum/accounts/login/')
def modifCompetence(request,perso_id,competence_id,valeur):
	joueur = Joueur.objects.get(user = request.user)
	joueur_reel = joueur
	
	if joueur.statut != 'MJ' :
		return render(request, 'forum/erreur.html', {'joueur': joueur})
	
	else :
		perso = get_object_or_404(Perso, pk=perso_id)
		competence = get_object_or_404(Competence, pk=competence_id)
		
		perso.modifie_competence(competence,valeur)
		
		return HttpResponseRedirect('/forum/perso/-'+str(joueur.id)+'/'+str(perso.id)+'/')

@login_required(login_url='/forum/accounts/login/')
def modifClasse(request,perso_id,classe_id,valeur):
	joueur = Joueur.objects.get(user = request.user)
	joueur_reel = joueur
	
	if joueur.statut != 'MJ' :
		return render(request, 'forum/erreur.html', {'joueur': joueur})
	
	else :
		perso = get_object_or_404(Perso, pk=perso_id)
		classe = get_object_or_404(Categorie_competence, pk=classe_id)
		
		if valeur==1 :
			if perso.classe_principale != classe :  
				perso.classe_secondaire = perso.classe_principale
				perso.classe_principale = classe
				
		if valeur==2 :
			if perso.classe_secondaire != classe :  
				if perso.classe_principale == classe : perso.classe_principale = perso.classe_secondaire
				perso.classe_secondaire = classe
				
		if valeur==3 :
			qst_classe3 = Categorie_competence.objects.exclude(id=perso.classe_principale.id).exclude(id=perso.classe_secondaire.id)
			classe3 = qst_classe3[0]
			if perso.classe_principale == classe :  
				perso.classe_principale = perso.classe_secondaire
				perso.classe_secondaire = classe3
			if perso.classe_secondaire == classe :  
				perso.classe_secondaire = classe3
		
		perso.save()
		
		#perso.modifie_classe(classe,valeur)
		
		return HttpResponseRedirect('/forum/perso/-'+str(joueur.id)+'/'+str(perso.id)+'/')

	
@login_required(login_url='/forum/accounts/login/')	
def modifPt(request,perso_id,attribute,valeur):
	joueur = Joueur.objects.get(user = request.user)
	valeur = valeur-1
	if joueur.statut != 'MJ' :
		return render(request, 'forum/erreur.html', {'joueur': joueur})
	
	else :
		perso = get_object_or_404(Perso, pk=perso_id)
		if attribute == "PV" : 
			perso.PV = valeur
			if perso.PV <0 : perso.vivant = False
			else : perso.vivant = True
		elif attribute == "PA" : perso.PA = valeur
		elif attribute == "PC" : perso.PC = valeur
		elif attribute == "PE" : perso.PE = valeur
		elif attribute == "nbGardes" : perso.nbGardes = valeur
		elif attribute == "nbTroupes" : perso.nbTroupes = valeur
		perso.save()
		
		return HttpResponseRedirect('/forum/perso/-'+str(joueur.id)+'/'+str(perso.id)+'/')
	
@login_required(login_url='/forum/accounts/login/')	
def modifPosture(request,perso_id,posture_actuelle_id,type_posture,valeur):
	joueur = Joueur.objects.get(user = request.user)
	perso = get_object_or_404(Perso, pk=perso_id)
	if joueur.statut != 'MJ' and not objet_ds_manytomany(joueur,perso.joueur) :
		return render(request, 'forum/erreur.html', {'joueur': joueur})
	
	else :
		if type_posture == 'provocation_duel':
			if posture_actuelle_id == 0 : perso.accepte_duel = False
			elif posture_actuelle_id == 1 : perso.accepte_duel = True
			
		else :
		
			T_postures = []
			posture_actuelle = get_object_or_404(Posture, pk=posture_actuelle_id)
			if valeur==0 : valeur = -1
			if len(type_posture)>1 :
				categorie_combat = Categorie_combat.objects.get(nom_info=type_posture)
				qst_posture = Posture.objects.filter(categorie_combat=categorie_combat).filter(choix_defaut=True).order_by('priorite')
				for posture in qst_posture : T_postures.append(posture)
			
			elif perso.posture :
				qst_posture = Posture.objects.filter(categorie_combat=perso.posture.categorie_combat).order_by('priorite')
				for posture in qst_posture :
					T_verif = posture.verif_posture_cible
					if len(T_verif)==0 : T_postures.append(posture)
					
			if posture_actuelle in T_postures :
				a = T_postures.index(posture_actuelle)+valeur
				if a >= len(T_postures): a=0
				if a < 0 : a = len(T_postures)-1
				new_posture = T_postures[a]
				
				if type_posture=='duel' : perso.posture_defaut_duel = new_posture
				elif type_posture=='melee' : perso.posture_defaut_melee = new_posture
				#elif type_posture=='bataille' : perso. = new_posture
				else : perso.posture = new_posture
		
		perso.save()
		
		return HttpResponseRedirect('/forum/perso/-'+str(joueur.id)+'/'+str(perso.id)+'/#comportements')

@login_required(login_url='/forum/accounts/login/')			
def modifComportementIntervention(request,perso_id,comportement_actuel_id):
	joueur = Joueur.objects.get(user = request.user)
	perso = get_object_or_404(Perso, pk=perso_id)
	if joueur.statut != 'MJ' and not objet_ds_manytomany(joueur,perso.joueur) :
		return render(request, 'forum/erreur.html', {'joueur': joueur})
	else :
		qst_comportement = Comportement_intervention.objects.filter(active=True).filter(id__gt=comportement_actuel_id)
		if perso.hote : qst_comportement = qst_comportement.filter(OK_hote=True).all()
		else : qst_comportement = qst_comportement.filter(OK_perso=True).all()
		
		if len(qst_comportement)>0 : new_comportement = qst_comportement[0]
		else : new_comportement = Comportement_intervention.objects.get(id=1)
		
		perso.comportement_intervention = new_comportement
		perso.save()
		return HttpResponseRedirect('/forum/perso/-'+str(joueur.id)+'/'+str(perso.id)+'/#comportements')
		
		
@login_required(login_url='/forum/accounts/login/')		
def modifJet(request,commande_id,success):
	joueur = Joueur.objects.get(user = request.user)
	joueur_reel = joueur
	
	if joueur.statut != 'MJ' :
		return render(request, 'forum/erreur.html', {'joueur': joueur})
	
	else :
		commande = get_object_or_404(Commande, pk=commande_id)
		if success == "success" :
			commande.make_success()
		elif success == "fail" :
			commande.make_fail()
		commande.save()
		
		return HttpResponseRedirect('/forum/commmandesMJ/encours/0/0/')

		
@login_required(login_url='/forum/accounts/login/')			
def fiche_resultat(request,resultat_id):
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	joueur = Joueur.objects.get(user = request.user)
	if joueur.statut != 'MJ' :
		return render(request, 'forum/erreur.html', {'joueur': joueur})
	else :
		resultat = get_object_or_404(Resultat, pk=resultat_id)
		
		
		if request.method == "POST":
			form = ModifResultat2(request.POST)
			if form.is_valid():
				resultat.nom = form.cleaned_data['nom']
				if form.cleaned_data['action'] : resultat.action = form.cleaned_data['action']
				resultat.texte = form.cleaned_data['texte']
				resultat.cle1 = form.cleaned_data['cle1']
				resultat.cle2 = form.cleaned_data['cle2']
				resultat.competence = form.cleaned_data['competence']
				resultat.obj_necessaire = form.cleaned_data['obj_necessaire']
				resultat.effet_recu = form.cleaned_data['effet_recu']
				resultat.perso_trouve = form.cleaned_data['perso_trouve']
				resultat.passage_trouve = form.cleaned_data['passage_trouve']
				resultat.resultat_trouve = form.cleaned_data['resultat_trouve']
				
				arme_cible = form.cleaned_data['arme_cible']
				armure_cible = form.cleaned_data['armure_cible']
				potion_cible = form.cleaned_data['potion_cible']
				parchemin_cible = form.cleaned_data['parchemin_cible']
				rituel_cible = form.cleaned_data['rituel_cible']
				obj_quete_cible = form.cleaned_data['obj_quete_cible']
				divers_cible = form.cleaned_data['divers_cible']
				
				T_donne_obj=[]
				if arme_cible : T_donne_obj.append(arme_cible)
				if armure_cible : T_donne_obj.append(armure_cible)
				if potion_cible : T_donne_obj.append(potion_cible)
				if parchemin_cible : T_donne_obj.append(parchemin_cible)
				if rituel_cible : T_donne_obj.append(rituel_cible)
				if obj_quete_cible : T_donne_obj.append(obj_quete_cible)
				if divers_cible : T_donne_obj.append(divers_cible)
				#print(T_donne_obj)
				for o in T_donne_obj :
					resultat.trouve_obj(o)

				resultat.save()
				return HttpResponseRedirect('/forum/resultat/'+str(resultat_id)+'/')
		
			else :
				for field in form:
					for error in field.errors:
						print(field)
						print(error)	
				return HttpResponseRedirect('/forum/resultat/'+str(resultat_id)+'/')
			
		else:
			form = ModifResultat(resultat)
		
		context = {'nom_jeu':nom_jeu,'joueur':joueur,'joueur_reel':joueur,'qst_joueur':qst_joueur,'resultat':resultat,'form':form}
		return render(request, 'forum/desc_resultat.html', context)

@login_required(login_url='/forum/accounts/login/')	
def delete_objet_resultat(request,objet_id,resultat_id):
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	joueur = Joueur.objects.get(user = request.user)
	if joueur.statut == 'MJ' :
		objet = get_object_or_404(Objet_perso, pk=objet_id)
		objet.delete()
	return HttpResponseRedirect('/forum/resultat/'+str(resultat_id)+'/')

@login_required(login_url='/forum/accounts/login/')	
def modifresultat(request,resultat_id,elt,valeur):	
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	joueur = Joueur.objects.get(user = request.user)
	if joueur.statut != 'MJ' :
		return render(request, 'forum/erreur.html', {'joueur': joueur})
	else :
		resultat = get_object_or_404(Resultat, pk=resultat_id)
		
		if elt=='active' :
			if resultat.active : resultat.active = False
			else : resultat.active = True
		elif elt == 'priorite':
			if valeur == 0 : resultat.priorite = resultat.priorite - 1
			else : resultat.priorite = resultat.priorite + valeur
		elif elt == 'action':
			T_actions = []
			qst_action = Action.objects.filter(active=True).filter(appel_resultat=True)
			for action in qst_action:
				action_OK = True
				if action.condition_atelier and (not action.condition_competence or action.condition_atelier_ET_competence) and not action.condition_atelier in resultat.lieu.atelier.all() : action_OK = False
				if (action.nom_info == 'explorer' and resultat.lieu.taille==1) or (action.nom_info == 'fouiller' and resultat.lieu.taille>1): action_OK = False
				if action_OK : T_actions.append(action)
			if valeur == 0 :  indice = T_actions.index(resultat.action)-1
			else : indice = T_actions.index(resultat.action)+1
			if indice>len(T_actions) : indice=0
			resultat.action = T_actions[indice]
		elif elt == 'unique':
			if resultat.unique : resultat.unique = False
			else : resultat.unique = True
		elif elt == 'fini':
			if resultat.fini : resultat.fini = False
			else : resultat.fini = True
		elif elt == 'repetable':
			if resultat.repetable : resultat.repetable = False
			else : resultat.repetable = True
		elif elt == 'public':
			if resultat.public : resultat.public = False
			else : resultat.public = True
		elif elt == 'obj_importance':
			if valeur==0:
				resultat.obj_importance = resultat.obj_importance = resultat.obj_importance+1
				if resultat.obj_importance>2 : resultat.obj_importance = 0
			if valeur==1:
				if resultat.obj_importance == 0 : resultat.obj_importance = 1
				else : resultat.obj_importance = 0
		elif elt == 'obj_prioritaire':
			if resultat.obj_prioritaire : resultat.obj_prioritaire = False
			else : resultat.obj_prioritaire = True
			
		elif elt == 'valeur_competence':
			if valeur == 0 and resultat.valeur_competence>1 : resultat.valeur_competence = resultat.valeur_competence - 1
			else : resultat.valeur_competence = resultat.valeur_competence + valeur
		elif elt == 'competence':
			if valeur == 0 : resultat.competence = None
		elif elt == 'modif_PV':
			if valeur == 0 : resultat.modif_PV = resultat.modif_PV - 1
			else : resultat.modif_PV = resultat.modif_PV + valeur
		elif elt == 'modif_gardes':
			if valeur == 0 : resultat.modif_gardes = resultat.modif_gardes - 1
			else : resultat.modif_gardes = resultat.modif_gardes + valeur
		elif elt == 'modif_troupes':
			if valeur == 0 : resultat.modif_troupes = resultat.modif_troupes - 1
			else : resultat.modif_troupes = resultat.modif_troupes + valeur
			
		elif elt == 'passage_trouve':
			if valeur == 1 :
				T_passages = []
				qst_passage = Lieu.objects.filter(active=True).filter(lieu=resultat.lieu).filter(secret=True)
				for passage in qst_passage: T_passages.append(passage)
				if len(T_passages)>0 : 
					if not resultat.passage_trouve : resultat.passage_trouve = T_passages[0]
					else : 
						indice = T_passages.index(resultat.passage_trouve)+1
						if indice>=len(T_passages) : indice = 0
						resultat.passage_trouve = T_passages[indice]
			elif valeur == 0 : resultat.passage_trouve = None
			
		elif elt == 'perso_trouve':
			if valeur == 1 :
				T_persos = []
				qst_persos = Perso.objects.filter(active=True).exclude(dissimulation=0).filter(lieu=resultat.lieu)
				for perso in qst_persos: T_persos.append(perso)
				if len(T_persos)>0 : 
					if not resultat.perso_trouve : resultat.perso_trouve = T_persos[0]
					else : 
						indice = T_persos.index(resultat.perso_trouve)+1
						if indice>=len(T_persos) : indice = 0
						resultat.perso_trouve = T_persos[indice]
			elif valeur == 0 : 
				resultat.perso_trouve = None
				
		elif elt == 'resultat_trouve':
			if valeur == 0 : resultat.resultat_trouve=None
		
		resultat.save()
	return HttpResponseRedirect('/forum/resultat/'+str(resultat_id)+'/')

@login_required(login_url='/forum/accounts/login/')			
def lierResultatNew(request,commande_id):
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	joueur = Joueur.objects.get(user = request.user)
	if joueur.statut != 'MJ' :
		return render(request, 'forum/erreur.html', {'joueur': joueur})
	else :
		commande = get_object_or_404(Commande, pk=commande_id)
		
		if request.method == "POST":
			form = LierResultat2(request.POST)
			if form.is_valid():
			
				texte = form.cleaned_data['texte']
				nom = form.cleaned_data['nom']
				public = form.cleaned_data['public']
				unique = form.cleaned_data['unique']
				passage_trouve = form.cleaned_data['passage_trouve']
				objet_trouve = form.cleaned_data['objet_trouve']
				effet_recu = form.cleaned_data['effet_recu']
				perso_trouve = form.cleaned_data['perso_trouve']
				attaquer_par = ""#form.cleaned_data['attaquer_par']
				modif_PV = form.cleaned_data['modif_PV']
				modif_gardes = form.cleaned_data['modif_gardes']
				modif_troupes = form.cleaned_data['modif_troupes']
				resultat_trouve = form.cleaned_data['resultat_trouve']
					
				T_form = [texte , public , unique , passage_trouve , objet_trouve , perso_trouve , attaquer_par , modif_PV , nom, modif_gardes, modif_troupes, resultat_trouve, effet_recu]
				creation_resultat(T_form,commande)
				
			else :
				for field in form:
					for error in field.errors:
						print(field)
						print(error)	
			return HttpResponseRedirect('/forum/')
			
		else:
			form = LierResultat(commande)
			
		context = {'nom_jeu':nom_jeu,'joueur':joueur,'joueur_reel':joueur,'qst_joueur':qst_joueur,'commande':commande,'form':form}
		return render(request, 'forum/post_resultat.html', context)
		

@login_required(login_url='/forum/accounts/login/')			
def MkResultat(request,lieu_id):
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	joueur = Joueur.objects.get(user = request.user)
	if joueur.statut != 'MJ' :
		return render(request, 'forum/erreur.html', {'joueur': joueur})
	else :
		lieu = get_object_or_404(Lieu, pk=lieu_id)
		
		resultat =  Resultat.objects.create(\
		lieu = lieu, \
		nom = 'NewResultat'+str(de(1000)),\
		texte = "" , \
		)
		
			
		return HttpResponseRedirect('/forum/resultat/'+str(resultat.id)+'/')

@login_required(login_url='/forum/accounts/login/')			
def MkResultatChild(request,type,resultat_parent_id):
	jeu = Jeu.objects.get(id=1)
	nom_jeu = return_jeu_nom_info()
	joueur = Joueur.objects.get(user = request.user)
	if joueur.statut == 'MJ' :
		resultat_parent = get_object_or_404(Resultat, pk=resultat_parent_id)
		
		nom=' - '+resultat_parent.nom
		if nom != '' :
			resultat =  Resultat.objects.create(\
			lieu = resultat_parent.lieu, \
			nom = nom,\
			texte = "" , \
			action = resultat_parent.action , \
			active = False , \
			)
		
		if type == 'echec':
			resultat.nom = 'Echec'+resultat.nom
			resultat_parent.echec = resultat
			resultat_parent.save()
		elif type == 'add':
			resultat.nom = 'Add'+resultat.nom
			resultat.add_resultat = resultat_parent
		
		resultat.save()
		
	return HttpResponseRedirect('/forum/resultat/'+str(resultat.id)+'/')
	
@login_required(login_url='/forum/accounts/login/')			
def lierResultat(request,commande_id,resultat_id):
	joueur = Joueur.objects.get(user = request.user)
	if joueur.statut != 'MJ' :
		return render(request, 'forum/erreur.html', {'joueur': joueur})
	else :
		commande = get_object_or_404(Commande, pk=commande_id)
		if resultat_id == 0 :
			commande.no_result = True
		else :
			resultat = get_object_or_404(Resultat, pk=resultat_id)
			commande.resultat = resultat
		commande.save()
		
		return HttpResponseRedirect('/forum/messagerie/')

def modifCommande(request,joueur_id,commande_id,option):
	joueur = get_object_or_404(Joueur, pk=joueur_id)
	commande = get_object_or_404(Commande, pk=commande_id)
	lieu = commande.perso.lieu
	perso = commande.perso
	joueur_reel = Joueur.objects.get(user = request.user)
	if joueur.user!=request.user and joueur_reel.statut!='MJ' : 
		return HttpResponseRedirect('/forum/lieu/-'+str(joueur_reel.id)+'/'+str(lieu.id)+'/'+str(perso.id)+'/1/1')
	if commande.joueur == joueur:
		if option == 'validation': commande.validation()
		elif option == 'annulation': commande.annulation()
		elif option == 'pause': commande.pause()
		elif option == 'play': commande.play()
		
	return HttpResponseRedirect('/forum/lieu/-'+str(joueur.id)+'/'+str(lieu.id)+'/'+str(perso.id)+'/1/1')

@login_required(login_url='/forum/accounts/login/')		
def create_regle(request,regle_parent_id):
	joueur = Joueur.objects.get(user = request.user)
	if joueur.statut != 'MJ' : return render(request, 'forum/erreur.html', {'joueur': joueur})
	else : 
		regle_parent = get_object_or_404(Regle, pk=regle_parent_id)
		r = Regle.objects.create(\
		nom = 'New', \
		nom_info = 'New'+str(random.randint(1,9999)).zfill(4), \
		parent = regle_parent)
		return HttpResponseRedirect('/admin/forum/regle/'+str(r.id)+'/change/')
		
@login_required(login_url='/forum/accounts/login/')		
def create_backg(request,backg_parent_id):
	joueur = Joueur.objects.get(user = request.user)
	if joueur.statut != 'MJ' : return render(request, 'forum/erreur.html', {'joueur': joueur})
	else : 
		backg_parent = get_object_or_404(Background, pk=backg_parent_id)
		r = Background.objects.create(\
		nom = 'New', \
		nom_info = 'New'+str(random.randint(1,9999)).zfill(4), \
		parent = backg_parent)
		return HttpResponseRedirect('/admin/forum/background/'+str(r.id)+'/change/')

@login_required(login_url='/forum/accounts/login/')		
def resetdb1(request):
	joueur = Joueur.objects.get(user = request.user)
	if joueur.statut == 'MJ' :
		reset("no")
	return HttpResponseRedirect('/forum/')

@login_required(login_url='/forum/accounts/login/')			
def resetdb2(request,option):
	joueur = Joueur.objects.get(user = request.user)
	if joueur.statut == 'MJ' :
		reset(option)
	return HttpResponseRedirect('/forum/')
	
def MAJ_regles(request):
	MAJregles()
	return HttpResponseRedirect('/forum/')
	
@login_required(login_url='/forum/accounts/login/')			
def test(request):
	#qst_obj = Objet.objects.all()
	#for o in qst_obj : o.save()
	qst_p = Perso.objects.all()
	for p in qst_p : 
		if p.hote and p.nom_info=="perso_none" :
			p.nom_info = p.hote.image
			p.save()
	qst_action = Action.objects.all()
	qst_posture = Posture.objects.all()
	qst_maison = Maison.objects.all()
	

	#for posture in qst_posture : 
	#	posture.save()
	
	'''for post in Post.objects.all() :
		print(post)
		post.save()'''
	
	'''atelier_discret = Atelier.objects.get(nom='Discret')
	qst_lieu = Lieu.objects.filter(dissimulation=1)
	for lieu in qst_lieu:
		print(lieu)'''
	return HttpResponseRedirect('/forum/')