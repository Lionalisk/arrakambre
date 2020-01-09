from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone

class Joueur(models.Model):
	active = models.BooleanField(default=True)
	user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	nom = models.CharField(max_length=30,unique=True)
	statut = models.CharField(max_length=30,choices=(('MJ','MJ'),('PNJ','PNJ'),('PJ','PJ')), default= 'PJ')
	allie = models.ManyToManyField("self", related_name="allie", blank=True)
	background = models.TextField(default='', blank=True, null=True)
	maison = models.ForeignKey('Maison', null=True, on_delete=models.SET_NULL)
	priorite = models.SmallIntegerField(default=1)
	
	nb_posts_par_page = models.SmallIntegerField(default=30)
	
	def __str__(self):
		return self.nom
		
	def save(self):
		'''if self.allie and self.priorite<100 :
			if self.allie.priorite>100 :
				self.priorite = self.allie.priorite
			else :
				self.priorite = self.priorite*10000 + self.id*100 + self.allie.priorite
				self.allie.priorite = self.priorite
				self.allie.save()'''
		
		
		super().save()
	
	
	def list_allies(self):
		T_resultat = []
		if self.allie :
			for allie in self.allie.all() :
				T_resultat.append(allie.nom)
		return '/'.join(T_resultat)
		
	def list_lieux_inconnus(self):
		T_resultat = []
		T= self.users_connaissants.all()
		for lieu in T :
			if lieu.inconnu : T_resultat.append(lieu.nom)
		if len(T_resultat)==0 : resultat = '<b>None</b>'
		else : resultat = '<b>'+'</b>, <b>'.join(T_resultat)+'</b>'
		return resultat
		
	def list_lieux_secrets(self):
		T_resultat = []
		T= self.users_connaissants_place.all()
		for lieu in T :
			if lieu.secret : T_resultat.append(lieu.nom)
		if len(T_resultat)==0 : resultat = '<b>None</b>'
		else : resultat = '<b>'+'</b>, <b>'.join(T_resultat)+'</b>'
		return resultat
		
	def list_lieux_visibles(self):
		T_resultat = []
		T = self.users_connaissants_place.all()
		
		for lieu in T :
			T_resultat.append(lieu.nom)
		if len(T_resultat)==0 : resultat = '<b>None</b>'
		else : resultat = '<b>'+'</b>, <b>'.join(T_resultat)+'</b>'
		return resultat
		
	def nb_msg_nonlu(self):
		return len(self.joueur_non_lu.all())
		
	def list_persos(self):
		qst_persos = self.persos.all()
		resultat = qst_persos.filter(active=True).filter(hote__isnull=True).order_by('priorite')
		#resultat = Perso.objects.filter(joueur=self).filter(active=True).filter(hote__isnull=True).order_by('priorite')
		return resultat
		
	def list_hotes(self):
		qst_persos = self.persos.all()
		resultat = qst_persos.filter(active=True).filter(hote__isnull=False).order_by('hote__priorite')
		#resultat = Perso.objects.filter(joueur=self).filter(active=True).filter(hote__isnull=True).order_by('priorite')
		return resultat
		
	def test(self):
		print("## FINFIN DE LA PAGE - "+str(timezone.now()))
		return(self.nom)