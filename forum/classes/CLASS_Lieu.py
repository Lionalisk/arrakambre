import math
from django.db import models
from django.db.models import Count
from django.utils import timezone
#from ..models import Perso
from ..models import Post,Joueur,Atelier

class Lieu(models.Model):
	active = models.BooleanField(default=True)
	influence = models.SmallIntegerField(default=15)
	nom = models.CharField(max_length=100, unique=True)
	description = models.TextField(default='', blank=True)
	image = models.CharField(max_length=40, default = 'lieu_none.jpg')
	#maison = models.ForeignKey('Maison', verbose_name="Maison", null=True, on_delete=models.SET_NULL, blank=True)
	atelier = models.ManyToManyField('Atelier', related_name = 'atelier_lieu', blank=True)
	taille = models.SmallIntegerField(default=1)
	QG = models.BooleanField(default=False)
	gestion_gardes = models.BooleanField(default=True, verbose_name="gestion_gardes : si True, l'hote peut donner des gardes a qui bon lui semble")
	
	passages = models.ManyToManyField('self', blank=True)
	fuite =  models.ForeignKey('self', verbose_name="Lieu de fuite", null=True, on_delete=models.SET_NULL, blank=True, related_name = 'lieu_fuite')
	lieu_parent = models.ForeignKey('self', verbose_name="Lieu parent", null=True, on_delete=models.SET_NULL, blank=True)
	
	dissimulation = models.SmallIntegerField(default=0)
	gain_administration = models.SmallIntegerField(default=1)
	nom_action_administration = models.CharField(max_length=100, default="Administrer")
	
	#nbtroupe_max = models.SmallIntegerField(default=8)
	#nbgarde_max = models.SmallIntegerField(default=8)
	#nbgarde = models.SmallIntegerField(default=0)
	#nbtroupe = models.SmallIntegerField(default=0)
	defense_assault = models.SmallIntegerField(default=0)
	defense_assault_bonusmax = models.SmallIntegerField(default=0)
	defense_intrusion = models.SmallIntegerField(default=0)
	piege = models.PositiveIntegerField(default=0)
	
	ferme = models.BooleanField(default=False)
	perso_autorise = models.ManyToManyField('Perso', blank=True, related_name = 'persos_autorises') # liste des personnes autorisees par le maitre des lieux a entrer
	
	inconnu = models.BooleanField(verbose_name="INCONNU : a besoin d'être visité pour être dans la carte ?",default=True) # = n'apparait pas dans la carte d'Arrakambre, mais se decouvre sans champ possible par exploration
	secret = models.BooleanField(verbose_name="SECRET : le passage pour y accéder est secret ?",default=False)	# = ne se decouvre que par une recherche
	users_connaissants = models.ManyToManyField('Joueur', blank=True, related_name = 'users_connaissants') # liste des personnes pour qui le lieu a deja ete visite
	users_connaissants_place = models.ManyToManyField('Joueur', blank=True, related_name = 'users_connaissants_place') # liste des personnes qui connaissent l'emplacement du lieu
	
	
	priorite =  models.SmallIntegerField(default=9)
	priorite_temp = models.PositiveIntegerField(default=9, editable=False)
	
	
	#action =

	def __str__(self):
		return self.nom
	
	def maison(self):
		resultat = False
		if len(self.hote.all())>0 : resultat = self.hote.all()[0].maison
		return resultat
	
	def proprietaire(self):
		resultat = False
		if self.hote : resultat = self.hote.all()[0]
		return resultat
	
	def save(self):
        
		old_priority_temp = self.priorite_temp
		self.priorite_temp = self.defini_priorite_temp()
		
		if self.taille<1 : self.taille=1
		
		if self.secret : self.inconnu = True
		
		if self.piege < 0 : self.piege = 0
		if len(self.hote.all())>0 and self.hote.all()[0].nbGardes == 0 : self.ferme=False
		
		if self.inconnu or self.secret :
			qst_joueur_hote = Joueur.objects.filter(maison=self.maison()).exclude(maison__isnull=True)
			if self.id :
				for j in qst_joueur_hote :
					if not j in self.users_connaissants.all() : self.users_connaissants.add(j)
					if not j in self.users_connaissants_place.all() : self.users_connaissants_place.add(j)
		
		
		#print(self.users_connaissants.all())
		
		if self.atelier.filter(nom="Discret").exists() and self.dissimulation==0 : 
			self.dissimulation=1
		
		super().save()  # Call the "real" save() method.
		
		
		print("############# SAVE LIEU "+self.nom+" - "+str(timezone.now()))
		'''print('SAVE OK - '+self.nom+' - '+str(self.priorite_temp))
		if old_priority_temp != self.priorite_temp :
			list_lieux = Lieu.objects.all()
			for lieu in list_lieux:
				lieu.save()
				print('SAVE OK - '+lieu.nom+' - '+str(lieu.priorite_temp))'''
				
	
	def defini_priorite_temp(lieu) :
		#lieu = self
		max=5
		a=0
		priorite_temp = lieu.priorite*math.pow(100, max)
		
		if lieu.lieu_parent:
			lieu2 = lieu.lieu_parent
			a=a+1
			
			priorite_temp = lieu2.priorite*math.pow(100, max) + priorite_temp/100
			
			while lieu2.lieu_parent and a<=max:
				a=a+1
				lieu2 = lieu2.lieu_parent
				priorite_temp = lieu2.priorite*math.pow(100, max) + priorite_temp/100
				
		return int(priorite_temp)
		
	def get_passages(self) :
		resultat = self.passages.filter(active=True).all()
		return resultat
	
	def get_hote(self):
		qst_resultat = self.hote.filter(active=True).all()
		if qst_resultat : resultat = qst_resultat[0]
		else : resultat = None
		return resultat
	
	def return_lieu_parent(self):
		resultat = self.nom
		if self.lieu_parent_id :
			parent = self
			while parent.lieu_parent_id :
				parent = parent.lieu_parent
				resultat = parent.nom
		return resultat
		
	def return_T_perso_present(self):
		#qst_perso_present = Perso.objects.filter(lieu__id=self.id).filter(active=True)
		qst_perso_present = self.persos_presents.filter(active=True).all()
		return qst_perso_present
		
	def return_nb_perso_present(self):
		T_perso_present = self.return_T_perso_present()
		return len(T_perso_present)
		
	def return_last_post(self):
		last_post_present = Post.objects.filter(lieu__id=self.id).filter(active=True).order_by('created_date').last()
		return last_post_present
		
	def return_nb_post(self):
		nb_post_present = Post.objects.filter(lieu__id=self.id).count()
		return nb_post_present
		
	def return_invites(self):
		T_resultat = []
		for p in self.perso_autorise.all() :
			if not p.no in T_resultat : T_resultat.append(p.nom)
		resultat = ', '.join(T_resultat)
		return resultat
	
	def return_ateliers(self):
		T_resultat = []
		for a in self.atelier.all() :
			T_resultat.append(a.nom)
		resultat = ', '.join(T_resultat)
		return resultat
		
	def return_resultats(self):
		qst_resultat = self.lieu_recherche.filter(active=True).filter(fini=False).all()
		return qst_resultat
		
	
	def return_user_connaissants_inconnu(self):
		T_resultat = []
		for p in self.users_connaissants.all() :
			T_resultat.append(p.nom)
		resultat = ', '.join(T_resultat)
		if resultat == '' : resultat = 'personne'
		return resultat
		
	def return_user_connaissants_secret(self):
		T_resultat = []
		for p in self.users_connaissants_place.all() :
			T_resultat.append(p.nom)
		resultat = ', '.join(T_resultat)
		if resultat == '' : resultat = 'personne'
		return resultat
		
	def nbgarde(self):
		resultat = 0
		if len(self.hote.all())>0 : resultat = self.hote.all()[0].nbGardes
		return resultat
		
	def nbtroupe(self):
		resultat = 0
		if len(self.hote.all())>0 : resultat = self.hote.all()[0].nbTroupes
		return resultat
	
	def nbgarde_max(self):
		resultat = 0
		if len(self.hote.all())>0 : resultat = self.hote.all()[0].gardes_MAX
		return resultat
		
	def nbtroupe_max(self):
		resultat = 0
		if len(self.hote.all())>0 : resultat = self.hote.all()[0].troupes_MAX
		return resultat