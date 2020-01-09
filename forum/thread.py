
from .models import Jeu
from threading import Thread
import time
from .fonctions import *



class thread_jeu(Thread):

	def __init__(self):
		Thread.__init__(self)

	def run(self):
		jeu = Jeu.objects.get(id=1)
		attente = 60*jeu.delai_refresh
		if attente > 0 :
			i=0
			while i<1 :
				
				time.sleep(attente)
				print('	REFRESH AUTO')
				jeu.lock_onload =True
				jeu.save()
				time.sleep(3.0)
				onload2()
				jeu.lock_onload =False
				jeu.save()
			



