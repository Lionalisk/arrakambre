
from django.urls import include,path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

#urlpatterns = [
#    path('', views.index, name='index'),
#]

urlpatterns = [
	
	path('accounts/', include('django.contrib.auth.urls')),
	#path('connexion', views.connexion, name='connexion'),
	path('', views.index_redirect, name='index_redirect'),
	path('-<int:joueur_id>', views.index, name='index'),
	
	path('regles/<int:regle_id>/', views.regles_init, name='regles_init'),
	path('regles/-<int:joueur_id>/<int:regle_id>/', views.regles, name='regles'),
	path('createregle/<int:regle_parent_id>/', views.create_regle, name='create_regle'),
	
	path('lieu/', views.indexlieu_redirect, name='index_lieu_redirect'),
	path('lieu/-<int:joueur_id>', views.indexlieu, name='index lieu'),
	
	path('lieu/<int:lieu_id>/', views.lieu_redirect, name='lieu_redirect'),
	path('lieu/-<int:joueur_id>/<int:lieu_id>/<int:perso_id>/<str:action_str>/<int:num_page>', views.lieu, name='lieu'),
	#path('lieu/<int:lieu_id>/desc/', views.desclieu, name='description lieu'),
	path('traduire/-<int:joueur_id>/<int:lieu_id>/<int:perso_id>/<int:action_id>:<str:option>/<int:langage_id>/<int:post_id>/<int:num_page>/', views.traduire_post, name='traduire post'),
	path('removetraduction/-<int:joueur_id>/<int:lieu_id>/<int:perso_id>/<int:action_id>:<str:option>/<int:post_id>/<int:num_page>/', views.enlever_traduction, name='enlever traduction'),
	
	path('perso/-<int:joueur_id>/<int:perso_id>/', views.perso, name='fiche perso'),
	path('perso/-<int:joueur_id>/<int:perso_id>/<str:rubrique>/<int:num_page>/', views.perso_rubrique, name='fiche perso rubrique'),
	path('porte_objet/-<int:joueur_id>/<int:perso_id>/<int:objet_id>/<int:laisse_ou_porte>/', views.porte_obj, name='Porte objet'),
	path('delete/<str:elt>/-<int:joueur_id>/<int:perso_id>/<int:id>/', views.deleteElt, name='Delete Element'),
	
	#path('perso/desc/-<int:joueur_id>/<int:perso_id>', views.descperso, name='description perso'),
	
	path('messagerie/', views.message_redirect, name='messagerie_redirect'),
	path('messagerie/-<int:joueur_id>/<int:perso_id>/<str:filtre>/', views.message, name='messagerie'),
	path('messagerie/supprime/<int:msg_id>/', views.masqueMSG, name='masqueMSG'),
	path('messagerie/restaure/<int:msg_id>/', views.restaureMSG, name='restaureMSG'),
	
	#path('background/<int:bg_id>/', views.background, name='background'),
	path('background/-<int:joueur_id>/<bg_id>/', views.background, name='background'),
	path('createbackg/<int:backg_parent_id>/', views.create_backg, name='create_backg'),
	
	path('deletePost/<int:lieu_id>/<int:post_id>/',views.deletePost, name='deletePost'),
	path('deleteLoi/-<int:joueur_id>/<int:perso_id>/<int:loi_id>/',views.deleteLoi, name='deleteLoi'),
	path('voteLoi/-<int:joueur_id>/<int:perso_id>/<int:loi_id>/',views.voteLoi, name='voteLoi'),
	path('soumettreLoi/-<int:joueur_id>/<int:perso_id>/<int:loi_id>/',views.soumettreLoi, name='soumettreLoi'),
	path('annuleVoteLoi/-<int:joueur_id>/<int:perso_id>/<int:loi_id>/',views.annuleVoteLoi, name='annuleVoteLoi'),
	
	path('commmandesMJ/<str:filtre>/<int:tri>/<str:str_joueur_id>/',views.liste_commande, name='liste_commande'),
	path('postsMJ/<str:filtre>/',views.liste_post, name='liste_post'),
	
	path('lieuxMJ/<str:filtre>/',views.liste_lieu, name='liste_lieu'),
	path('personnagesMJ/<str:filtre>/',views.liste_perso, name='liste_perso'),
	path('maisonsMJ/<str:filtre>/',views.liste_maison, name='liste_maison'),
	path('joueursMJ/<str:filtre>/',views.liste_joueur, name='liste_joueur'),
	path('resultatsMJ/<int:lieu_id>/<int:action_id>/<str:filtre>/',views.liste_resultat, name='liste_resultat'),
	path('evenementsMJ/<int:lieu_id>/<str:filtre>/',views.liste_evenement, name='liste_evenement'),
	
	#path('loisMJ/<str:filtre>/',views.liste_loi, name='liste_loi'),
	#path('objetsMJ/<str:filtre>/',views.liste_objet, name='liste_objet'),
	#path('actionsMJ/<str:filtre>/',views.liste_action, name='liste_action'),
	
	path('modifCompetence/<int:perso_id>/<int:competence_id>/<int:valeur>/',views.modifCompetence, name='modification competence'),
	path('modifClass/<int:perso_id>/<int:classe_id>/<int:valeur>/',views.modifClasse, name='modification classe'),
	path('modifPosture/<int:perso_id>/<int:posture_actuelle_id>/<str:type_posture>/<int:valeur>/',views.modifPosture, name='modification posture'),
	path('modifComportementIntervention/<int:perso_id>/<int:comportement_actuel_id>/',views.modifComportementIntervention, name='modification comportement intervention'),
	
	path('modifPt/<int:perso_id>/<str:attribute>/<int:valeur>/',views.modifPt, name='modification Pts'),
	path('modifJet/<int:commande_id>/<str:success>/',views.modifJet, name='modification Jet'),
	
	path('resultat/<int:resultat_id>/',views.fiche_resultat, name='Fiche Resultat'),
	path('modifresultat/<int:resultat_id>/<str:elt>/<int:valeur>/',views.modifresultat, name='Fiche Resultat'),
	path('MakeResultat/<int:lieu_id>/',views.MkResultat, name='Make Resultat'),
	path('MakeResultat/<str:type>/<int:resultat_parent_id>/',views.MkResultatChild, name='Make Resultat'),
	path('lierResultat/new/<int:commande_id>/',views.lierResultatNew, name='Lier Resultat New'),
	path('lierResultat/<int:resultat_id>/<int:commande_id>/',views.lierResultat, name='Lier Resultat'),
	path('delete/objetresultat/<int:resultat_id>/<int:objet_id>/',views.delete_objet_resultat, name='Delete Objet Résultat'),
	
	path('modifCommande/-<int:joueur_id>/<int:commande_id>/<str:option>/',views.modifCommande, name='Modifier Commande'),
	
	path('reset/<str:option>',views.resetdb2, name='Reset Base'),
	path('reset/',views.resetdb1, name='Reset Base'),
	path('MAJ_regles/',views.MAJ_regles, name='MAJ regles'),
	path('test/',views.test, name='Test'),
	
]