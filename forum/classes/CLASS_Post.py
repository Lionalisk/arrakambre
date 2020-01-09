from django.db import models
#from ..models import Perso
from ..models import Jeu, Langage, Message
from django.utils import timezone
from datetime import timedelta
from ..fonctions_base import *
#import datetime

class Post(models.Model):
	
	lock = models.BooleanField(default=False)
	joueur = models.ForeignKey('Joueur', on_delete=models.CASCADE, blank=True, null=True)
	perso = models.ForeignKey('Perso', on_delete=models.CASCADE, blank=True, null=True)
	lieu = models.ForeignKey('Lieu', on_delete=models.CASCADE, related_query_name="lieu_post", blank=True, null=True)
	texte = models.TextField(verbose_name='')
	texteVO = models.TextField(verbose_name='texteVO : Texte dans la langue', blank=True, null=True)
	nom_info = models.CharField(verbose_name="Nom informatique (image) - si =='' : rien n'est associé ",max_length=30, default="", blank=True)
	style = models.CharField(max_length=30, default='normal')
	langage = models.ForeignKey('Langage', models.SET_DEFAULT, default=1, related_query_name="post_langage")
	action = models.ForeignKey('Action', on_delete=models.CASCADE, null=True)
	#commande = models.ForeignKey('Commande',  models.SET_NULL, null=True, blank=True)
	etape_action = models.CharField(max_length=30, default='', blank=True)
	
	#valide = models.BooleanField(default=False)
	dissimulation = models.SmallIntegerField(default=0)
	joueur_connaissant = models.ManyToManyField('Joueur', blank=True, related_name = 'joueur_know_post')
	joueur_traduit = models.ManyToManyField('Joueur', blank=True, related_name = 'posts_traduits')
	persos_cible = models.ManyToManyField('Perso', blank=True, related_name = 'perso_cible_post')
	
	#published_date = models.DateTimeField(default=timezone.now)
	date_initiale = models.DateTimeField(default=timezone.now, verbose_name = "Date initiale de création")
	created_date = models.DateTimeField(default=timezone.now, verbose_name = "Date de Publication")
	active = models.BooleanField(default=True)
	#editable = models.BooleanField(default=False, verbose_name="editable par le joueur avant validation")
	
	date_jeu = models.CharField(max_length=50, default='', blank=True)
	T_date_jeu = models.CharField(max_length=50, default='', blank=True)
	#info_MJ = models.TextField(blank=True, default='')
	
	signature = models.TextField(default='', blank=True)
	
	perso_etatsante = models.ForeignKey('Sante', null=True, on_delete=models.SET_NULL, default=1)
	perso_cache = models.BooleanField(default=False)
	perso_capture = models.BooleanField(default=False)
	perso_nom = models.CharField(max_length=30,blank=True,null=True)
	perso_titre = models.CharField(max_length=30,blank=True,null=True)
	perso_image = models.CharField(max_length=30,blank=True,null=True)
	perso_maison = models.ForeignKey('Maison', null=True, blank=True, on_delete=models.SET_NULL)
	text_persos_cible = models.CharField(max_length=200,blank=True,default='')
	
	depart_lieu = models.BooleanField(default=False)
	
	
	def __str__(self):
		a = 20
		if len(self.texte)> a : txt = self.texte[:20]
		else : txt = self.texte
		return self.created_date.strftime("%Y-%m-%d %H:%M")+' - '+self.lieu.nom+'-'+self.perso.nom+' - '+txt
	
	def add_persos_cible(self,perso_cible):
		
		if self.text_persos_cible == '' : self.text_persos_cible = perso_cible.image()+'/#/'+perso_cible.get_nom()+'/#/'+perso_cible.get_nom_info()
		else : self.text_persos_cible = self.text_persos_cible+'#/#'+perso_cible.image()+'/#/'+perso_cible.get_nom()+'/#/'+perso_cible.get_nom_info()
		self.persos_cible.add(perso_cible)
	
	def save(self, *args, **kwargs):
		
		#CONVERSION DATE DE JEU
		jeu = Jeu.objects.get(id = 1)
		T_date_jeu = jeu.convert_date(self.created_date)
		self.date_jeu = format_date_jeu(T_date_jeu,jeu.format_date)
		self.T_date_jeu = format_T_date_jeu(T_date_jeu)
		
		if not self.id :
			self.perso_etatsante = self.perso.etat_sante
			if self.perso.dissimulation>0 : self.perso_cache = True
			if self.perso.geolier : self.perso_capture = True
			self.perso_nom = self.perso.get_nom()
			self.perso_titre = self.perso.get_titre()
			self.perso_image = self.perso.image()
			self.perso_maison = self.perso.get_maison()
			self.signature = self.perso.signature()
		
		
		#TRADUCTION
		T_error = []
		qst_langage = Langage.objects.filter(active=True).exclude(id=1)
		for langage in qst_langage :
			borne_debut = '<'+langage.nom_info+'>'
			borne_fin = '</'+langage.nom_info+'>'
			if borne_debut in self.texte and borne_fin in self.texte:
				T_txt = self.texte.split(borne_debut)
				new_txt = T_txt[0]
				i=1
				while i<len(T_txt) :
					if borne_fin in T_txt[i] :
						T_txt2 = T_txt[i].split(borne_fin)
						txt_a_traduire = T_txt2[0]
						txt_fin = ''.join(T_txt2[1:])
						
						new_txt = new_txt + langage.traduction(txt_a_traduire) + txt_fin

					else : 
						T_error.append('Manque une balise "'+borne_fin+'" pour refermer le dialecte')
						break
					i=i+1
				
				if len(T_error)==0:
					if self.langage.id==1 :
						self.texteVO = new_txt.replace(borne_debut,'').replace(borne_fin,'')
						self.langage = langage
					elif self.langage!=langage :
						T_error.append('Plusieurs langages sont présents dans le Post : '+self.langage.nom+' et '+langage.nom)
		
		if len(T_error)>0 :
			txt_error = 'Une ou plusieurs erreur(s) dans votre message empêche(nt) sa parution :\n'+'\n'.join(T_error)+'\n\n'+self.texte
			
			msg = Message.objects.create(\
			joueur = self.joueur, \
			titre = 'ERREUR Post - '+self.perso.nom+' - '+self.lieu.nom+' - '+self.date_jeu , \
			texte = txt_error)
			
			msg.joueurs_affiche.add(self.joueur)
			msg.joueurs_nonlu.add(self.joueur)
			msg.joueurs_cible.add(self.joueur)
			
			self.texte = ''
				
		'''
		if langage.id!=1:
			for perso in self.lieu.persos_presents.filter(active=True).filter(PV__gte=1).filter(en_fuite=False).filter(en_combat=False).all() :
				for joueur in perso.joueur.all() :
					if not joueur in self.joueur_traduit.add(joueur)'''
		
		
		#########
		if self.texte != '' :
			
			if self.texte.count('<') != self.texte.count('>') or self.texte.count('<') != self.texte.count('</')*2 :
				self.texte = '<b><i>ATTENTION : problème de balise HTML</i></b><br><br>'+self.texte.replace('<\\','').replace('<','').replace('>','')
			
			super().save()  # Call the "real" save() method.'''
			print("############# SAVE POST - "+str(timezone.now()))
		
	def info_MJ(self):
		T_joueur_connaissant = self.joueur_connaissant.all()
		if len(T_joueur_connaissant)>0 : 
			txt_joueur_connaissant = ' (Connu par : '+txt_liste(T_joueur_connaissant)+')'
		else : txt_joueur_connaissant = ''
		info = txt_joueur_connaissant + " - "+str(self.dissimulation)+" - "+self.style[:3]+"   /<b>"+self.joueur.nom+"</b>"
		return info
		
	def editable_OK(self):
		jeu = Jeu.objects.get(id=1)
		timedelta_delay = timedelta(seconds=60*jeu.delai_edit)
		date_delay = self.created_date+timedelta_delay
		if  timezone.now()<= date_delay and self.style!='sys' and self.style!='info' and self.editable : resultat = True
		else : resultat = False
		return resultat
		
	def desc(self):
		resultat = self.perso_nom+' - '+self.perso_etatsante.nom
		return resultat
		
	def T_persos_cible(self):
		T_p = []
		if self.text_persos_cible!='' : 
			T_p = self.text_persos_cible.split('#/#')
			a=0
			while a<len(T_p):
				T_p[a] = T_p[a].split('/#/')
				a=a+1
		return T_p
	
	def get_texte_traduit(self):
		borne_debut = '<'+self.langage.nom_info+'>'
		borne_fin = '</'+self.langage.nom_info+'>'
		resultat = self.texte.replace(borne_debut,'\n<b>Le texte qui suit est exprimé en '+self.langage.nom+' :</b> \n<i>').replace(borne_fin,'</i>\n')
		return resultat