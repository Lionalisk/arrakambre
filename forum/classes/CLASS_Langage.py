from django.db import models
from ..models import Jeu
from ..fonctions_base import *


class Langage(models.Model):
	active = models.BooleanField(default=True)
	priorite = models.SmallIntegerField(default=1)
	nom = models.CharField(max_length=30, unique=True)
	nom_info = models.CharField(max_length=30, null=True)
	description = models.TextField(null=True, blank=True)
	est_parle = models.BooleanField(default=True)
	#competence = models.ForeignKey('Competence', models.SET_DEFAULT, default=8, related_query_name="competence_langage")
	#niveau = models.SmallIntegerField(default=2)
	
	
	alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789éàè,.;'
	alphabet2 = '-;-'.join(alphabet)
	alphabet_commun = models.TextField(verbose_name='Alphabet Commun (caractères à la suite)',default=alphabet)
	alphabet_langue = models.TextField(verbose_name='Alphabet Correspondant(-;- entre chaque caractère)',default=alphabet2)
	
	def __str__(self):
		return self.nom
	
	
	def traduction(self,txt):
		texte_traduit = ''
		T_alphabet_langue = self.alphabet_langue.split('-;-')
		for c in txt.lower() :
			if c in self.alphabet_commun :
				texte_traduit = texte_traduit + (T_alphabet_langue[(self.alphabet_commun).index(c)]).replace(' ','')
			else :
				texte_traduit = texte_traduit + c
			
		return texte_traduit

		
	def save(self, *args, **kwargs):
		
		T_alphabet_langue = self.alphabet_langue.split('-;-')
		if len(T_alphabet_langue)!=len(self.alphabet_commun):
			print('ERREUR : '+str(len(self.alphabet_commun))+' caracteres pour '+str(len(T_alphabet_langue))+' renseignés')
			i=0
			for c in self.alphabet_commun :
				if i<len(T_alphabet_langue) : print(c+'  ->  '+T_alphabet_langue[i])
				i=i+1
		else : print('OK langage')
		super().save()  # Call the "real" save() method.'''