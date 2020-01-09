from django.db import models

class Objet(models.Model):
	
	active = models.BooleanField(default=True)
	#buff = models.BooleanField(default = False)
	
	nom = models.CharField(max_length=50,unique=True)
	nom_effet = models.CharField(max_length=30,null=True,blank=True,verbose_name="nom_effet : Si l'objet génère un effet (potion, poison..), indique ce nom dans la fiche perso")
	description = models.TextField(default='', blank=True)
	classe = models.CharField(max_length=100, blank=True,default = "",choices=(('arme','arme'),('armure','armure'),('potion','potion'),('poison','poison'),('parchemin','parchemin'),('rituel','grimoire de rituel'),('artefact','artefact'),('quete','objet de quete'),('','divers')))
	one_use = models.BooleanField(default = False)
	#arme_OK = models.BooleanField(default = False)
	#armure_OK = models.BooleanField(default = False)
	rune_OK = models.BooleanField(default = False,verbose_name="rune_Ok : une rune est possible sur l'objet ?")
	en_main_OK = models.BooleanField(default = False)
	cumulable = models.BooleanField(default = False,verbose_name='cumulable : se compte avec les autres objets identiques (ex:potion)')
	reparable = models.BooleanField(default = False)
	
	
	valeur1 = models.SmallIntegerField(default=0)
	valeur2 = models.SmallIntegerField(default=0,verbose_name="valeur2 ; pour arme s'agit du bonus/malus pour melee") #pour arme = bonus/malus pour melee
	valeur3 = models.SmallIntegerField(default=0,verbose_name="valeur3 ; pour arme s'agit du bonus/malus pour dommage")
	valeur4 = models.SmallIntegerField(default=0)
	special = models.CharField(max_length=30,default='', null=True, blank=True)
	
	delay = models.SmallIntegerField(verbose_name="delay : Pour arme = valeur d'initiative en %, si Action ou Effet : durée de l'action ou de l'effet", default=100)
	
	action = models.ForeignKey('Action', null=True, blank=True, on_delete=models.SET_NULL, related_name = 'obj_declenche',verbose_name="action : ")
	effet = models.ForeignKey('Effet', null=True, blank=True, on_delete=models.SET_NULL, related_name = 'obj_effet',verbose_name="effet : si Null et action Null, on ne peut pas utiliser l'objet")
	effet_si_porte = models.BooleanField(default=False,verbose_name="effet_si_porte : si True, on n'a pas besoin d'utiliser l'objet, mais juste de le porter pour avoir son Effet")
	
	competence_requise = models.ForeignKey('Competence', null=True, blank=True, on_delete=models.SET_NULL, related_name = 'obj_bonus')
	niveau_requis = models.SmallIntegerField(default=0)
	
	volume = models.SmallIntegerField(default=1)
	solidite = models.SmallIntegerField(default=1)
	
	def arme_OK(self):
		resultat = False
		if self.classe=='arme' : resultat = True
		return resultat
		
	def armure_OK(self):
		resultat = False
		if self.classe=='armure' : resultat = True
		return resultat
		
	def __str__(self):
		
		return self.classe+' - '+self.nom
		
	def save(self, *args, **kwargs):
		
		if self.arme_OK() == True or self.armure_OK() == True : self.reparable = True
		
		if self.reparable == True : self.cumulable = False
		
		if self.arme_OK() and self.delay==0 : self.delay = 100
		
		super().save()  # Call the "real" save() method.'''
		#print("############# SAVE OBJET - "+str(timezone.now()))
		
	def priorite(self):
		priorite = 0
		T_valeurs = [self.valeur1,self.valeur2,self.valeur3,self.valeur4]
		i=0
		while i<len(T_valeurs):
			priorite = priorite + (T_valeurs[i]*(len(T_valeurs)-i))
			i=i+1
		return priorite
	
	def utilise(self):
		resultat = False
		if self.action : resultat = True
		elif self.effet : resultat = True
		if self.effet_si_porte : resultat = False
		return resultat