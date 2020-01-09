from django.db import models
from django.utils import timezone
from ..models import Effet_perso
from ..fonctions_base import bonus_des_obj

class Objet_perso(models.Model):
	active = models.BooleanField(default=True)
	etat = models.SmallIntegerField(default=1, verbose_name="état : quantité pour objet cumulable/pour objet réparable : 2=OK, 1=cassé")
	valeur = models.SmallIntegerField(default=0, verbose_name="valeur : puissance de l'objet (pas pour arme et armure)/ si =0, alors prend valeur1 de obj")
	perso = models.ForeignKey('Perso',blank=True,null=True,on_delete=models.SET_NULL, verbose_name="perso : perso qui a l'objet", related_name="objet")
	obj = models.ForeignKey('Objet',blank=True,null=True,on_delete=models.SET_NULL, verbose_name="obj: objet concerne", related_name="possedant")
	resultat = models.ForeignKey('Resultat',blank=True,null=True,on_delete=models.SET_NULL, verbose_name="resultat : dans quel resultat est l'objet", related_name="tresor")
	porte = models.BooleanField(default=False)
	
	def __str__(self):
		#return self.perso.nom+' - '+self.obj.nom + ' - '+str(self.etat)
		return str(self.id)+'- '+self.perso.nom_origine+' - '+self.get_nom() + ' - '+str(self.etat)
		
	def save(self, *args, **kwargs):
		if self.obj.reparable and self.etat==1 : self.etat=2
		
		if not self.id and self.valeur==0 and self.obj : self.valeur = self.obj.valeur1
		
		#L'objet ne peut etre a la fois a un perso et dans un tresor	
		if self.perso and self.resultat : self.resultat = None
		
		#cumulable
		create_OK = True
		if self.perso and self.obj :
			qst_objet = self.perso.objet.filter(obj=self.obj).filter(valeur=self.valeur).filter(obj__cumulable=True).all()
			quantite = self.etat
			for o in qst_objet :
				if not (self.id and self.id==o.id):
					quantite = quantite+o.etat
				o.delete()
			self.etat = quantite
				
		super().save()  # Call the "real" save() method.'''
		
		if self.obj.effet and self.obj.effet_si_porte :
			
			if self.obj.effet.support == 'perso':
			
				if self.porte :
					#creation de Effet_perso sur le perso et supression des anciens
					
					for e in self.perso.effet_perso.filter(eft=self.obj.effet): e.delete()
					e = Effet_perso.objects.create(\
					perso = self.perso, \
					objet = None, \
					eft = self.obj.effet, \
					valeur = self.valeur, \
					objet_initial = self, \
					commence = True, infini = True)
					
				else :
					for e in self.perso.effet_perso.filter(eft=self.obj.effet) :
						e.delete()
						self.perso.save()
						
			elif len(self.effet_objet.filter(eft=self.obj.effet))==0 :
				e = Effet_perso.objects.create(\
				perso = None, \
				objet = self, \
				eft = self.obj.effet, \
				valeur = self.valeur, \
				objet_initial = self, \
				commence = True, infini = True)
						
		
	
	def get_nom(self):
		add = ''
		if self.obj and self.obj.classe != 'arme' and self.obj.classe != 'armure':
			if self.valeur == 2 : add = ' Supérieur'
			if self.valeur == 3 : add = ' de Maître'
		return self.obj.nom+add
	
	def special(self):
		resultat = self.obj.special
		now = timezone.now()
		for effet in self.effet_objet.filter(fini=False).filter(commence=True).filter(date_debut__lt=now).filter(date_fin__gt=now).all():
			resultat = resultat +','+ effet.eft.special
		return resultat
		
	def arme_valeur1(self):
		valeur = 0
		now = timezone.now()
		if self.obj.classe=='arme':
			valeur = self.obj.valeur1
			for effet in self.effet_objet.filter(fini=False).filter(commence=True).filter(date_debut__lt=now).filter(date_fin__gt=now).all():
				valeur = valeur + effet.eft.bonus_combat
			
		return valeur
		
	def get_duel(self):
		valeur = 0
		if self.obj.classe=='arme': valeur = self.obj.valeur1
		return valeur
		
	def get_melee(self):
		valeur = 0
		if self.obj.classe=='arme': valeur = self.obj.valeur1 + self.obj.valeur2
		return valeur
		
	def get_dommage(self):
		valeur = 0
		if self.obj.classe=='arme': valeur = self.obj.valeur3
		return valeur
	
	def get_initiative(self):
		return 0
		
	def armure_valeur1(self):
		valeur = 0
		now = timezone.now()
		if self.obj.classe=='armure':
			valeur = self.obj.valeur1
			for effet in self.effet_objet.filter(fini=False).filter(commence=True).filter(date_debut__lt=now).filter(date_fin__gt=now).all():
				valeur = valeur + effet.eft.bonus_PA
			
		return valeur
		
	def get_PA(self):
		valeur = 0
		if self.obj.classe=='armure': valeur = self.obj.valeur1
		return valeur
		
	def get_defense(self):
		valeur = 0
		if self.obj.classe=='armure': valeur = self.obj.valeur2
		return "+ "+str(valeur)
		
	def get_endurance(self):
		valeur = 0
		if self.obj.classe=='armure': valeur = self.obj.valeur3
		return "+ "+str(valeur)
		
	def prend_effet(self,eft):
		#evite le cumule de differents effets du meme type
		valide=True
		
		if eft.classe == '': 
			for effet in self.effets().filter(eft=eft):
				if effet.eft.priorite() <= eft.priorite() and effet.eft.priorite()<100 : 
					effet.fini=True
					effet.save()
				else : valide = False
				
		if eft.classe != '':
			for effet in self.effets().filter(eft__classe=eft.classe):
				if effet.eft.priorite() <= eft.priorite() : 
					effet.fini=True
					effet.save()
				else : valide = False
				
		if valide :
			e = Effet_perso.objects.create(\
			objet = self, \
			eft = eft, \
			infini=True)
			print(e)
			return e
		else : return False
		
	def effets(self):
		return self.effet_objet.filter(eft__active=True).filter(fini=False).filter(commence=True).filter(eft__support='perso').all()