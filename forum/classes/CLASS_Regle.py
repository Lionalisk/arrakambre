from django.db import models
from ..models import Jeu
from ..fonctions_base import *
from ..models import Action,Competence,Posture

class Regle(models.Model):
	active = models.BooleanField(default=True)
	priorite = models.SmallIntegerField(default=1)
	nom = models.CharField(max_length=60)
	parent = models.ForeignKey('self', blank=True, null=True ,on_delete=models.SET_NULL, verbose_name="Categorie de règle parent", related_name="enfant")
	nom_info = models.CharField(max_length=30, null=True)
	description = models.TextField(null=True, blank=True)
	
	tableau1 = models.ForeignKey('Tableau', blank=True, null=True ,on_delete=models.SET_NULL, verbose_name="#tableau1#", related_name="regle1")
	tableau2 = models.ForeignKey('Tableau', blank=True, null=True ,on_delete=models.SET_NULL, verbose_name="#tableau2#", related_name="regle2")
	tableau3 = models.ForeignKey('Tableau', blank=True, null=True ,on_delete=models.SET_NULL, verbose_name="#tableau3#", related_name="regle3")
	
	
	def __str__(self):
		retour = self.nom
		if self.parent_id : retour = str(self.parent)+' - '+self.nom
		return retour
		
	def desc(self):
		description = self.description
		if self.nom_info == 'liste_action': description = description + self.liste_action(False)
		elif len(self.nom_info)>7 and self.nom_info[:7] == 'posture': 
			type = self.nom_info.replace('posture_','')
			description = description.replace('#postures#',self.liste_posture(type,False))
		#elif self.nom_info == 'index' : description = description + self.index()
		html = description
		
		if self.tableau1_id : html = html.replace("#tableau1#",self.tableau1.tab(False))
		if self.tableau2_id : html = html.replace("#tableau2#",self.tableau2.tab(False))
		if self.tableau3_id : html = html.replace("#tableau3#",self.tableau3.tab(False))
		
		html = self.conversion_regle(html)
		return html
		
	def descMJ(self):
		description = self.description
		if self.nom_info == 'liste_action': description = description + self.liste_action(True)
		elif len(self.nom_info)>7 and self.nom_info[:7] == 'posture': 
			type = self.nom_info.replace('posture_','')
			description = description.replace('#postures#',self.liste_posture(type,True))
		#elif self.nom_info == 'index' : description = description + self.index()
			
		html = description
		
		if self.tableau1_id : html = html.replace("#tableau1#",self.tableau1.tab(True))
		if self.tableau2_id : html = html.replace("#tableau2#",self.tableau2.tab(True))
		if self.tableau3_id : html = html.replace("#tableau3#",self.tableau3.tab(True))
		
		html = self.conversion_regle(html)
		return html
	
	
	def enfants(self):
		qst_resultat = self.enfant.all().filter(active=True).order_by('priorite')
		return qst_resultat
	
	
	def conversion_regle(self,html):
	#les liens
		jeu = Jeu.objects.get(id=1)
		if html and '<<' in html :
			
			T_html = html.split('<<')
			new_html = T_html[0]
			a=1
			while a<len(T_html):
				
				T_part = T_html[a].split('>>')
				if len(T_part)==2 :
					
					variable = T_part[0]
					lien = '<error>'
					if len(variable)>6 and variable[:6]=='regle.' : 
						if Regle.objects.filter(nom_info=variable[6:]).exists() :
							obj = Regle.objects.get(nom_info=variable[6:])
							if obj.parent_id :
								rubrique = obj.parent
								while rubrique.parent_id :
									rubrique = rubrique.parent
							else : rubrique = obj
							lien = '<a href="/forum/regles/'+str(rubrique.id)+'/#'+obj.nom_info+'"><u>'+obj.nom+'</u></a>'
					elif len(variable)>7 and variable[:7]=='action.' : 
						if Action.objects.filter(nom_info=variable[7:]).exists() :
							obj = Action.objects.get(nom_info=variable[7:])
							lien = '<a href="/forum/regles/15/#action_'+obj.nom_info+'"><u>'+obj.nom+'</u></a>'
							
					elif len(variable)>11 and variable[:11]=='competence.' :
						if Competence.objects.filter(nom_info=variable[11:]).exists() :
							obj = Competence.objects.get(nom_info=variable[11:])
							lien = '<a href="/forum/regles/1/#competences"><u>'+obj.nom+'</u></a>'
							
					
					elif len(variable)>6 and variable[:6]=='image.' :
						nom_img= variable[6:].replace('.jpg','')
						lien = '<img src="/static/forum/'+jeu.nom_info+'/img/regles/'+nom_img+'.jpg">'
				
					new_html = new_html+lien+T_part[1]
					
				a=a+1
		else : new_html = html
		return new_html
	
	def index(self):
		jeu = Jeu.objects.get(id=1)
		html='<div>\n<ul style="margin-left:20px;">'
		qst_rubrique_regle = Regle.objects.filter(active=True).filter(parent=None).exclude(nom_info=self.nom_info).order_by('priorite')
		for rubrique in qst_rubrique_regle :
			html = html+'<li style="margin-bottom:15px;margin-top:10px;"><a href="/forum/regles/'+str(rubrique.id)+'/"  class=texte_surtitre>'+rubrique.nom+'</a></li>'
			qst_titre = rubrique.enfants()
			if len(qst_titre)>0 :
				html = html+'<ul style="margin-left:20px;margin-bottom:10px;">'
				for titre in qst_titre :
					html=html+'<li style="margin-bottom:5px;"><a href="/forum/regles/'+str(rubrique.id)+'/#'+titre.nom_info+'"  class=texte_titre>'+titre.nom+'</a></li>'
					qst_sstitre = titre.enfants()
					if len(qst_sstitre)>0 :
						html = html+'<ul style="margin-left:20px;margin-bottom:14px;">'
						for sstitre in qst_sstitre :
							html = html+'<li style="margin-bottom:2px;"><a href="/forum/regles/'+str(rubrique.id)+'/#'+sstitre.nom_info+'"  class=texte_sstitre>'+sstitre.nom+'</a></li>'
						html = html+'</ul>'
				html = html+'</ul>'+ '\n<img src="/static/forum/'+jeu.nom_info+'/img/separateur_h.png">'
		html = html+'</ul>\n</div>'
		
		return html
	
	def liste_action(self,MJ_OK):
		T_col = [10,'']
		qst_actions = Action.objects.filter(active=True).filter(MJ_only=False).filter(visible=True).filter(visible_ds_regles=True).order_by('categorie__priorite','priorite')
		html = "<div class=tableau>"
		num_ligne=1
		for action in qst_actions :
			if num_ligne>2 : num_ligne = 1
			
			#if MJ_OK : html = html+ action.return_html_desc_MJ()
			#else : html = html+ action.return_html_desc()
			
			html = html+'<div class=row2>'
			
			k=0
			for col in T_col :
				if col != '' and col != 0 : style =' style="min-width: '+str(col)+'pt;"'
				else : style =''
				
				if k==1 : 
					contenu = action.nom
					if MJ_OK : contenu = '<a href="/admin/forum/action/'+str(action.id)+'/change/" target="_blank">'+action.nom+'</a> - '+str(action.priorite)
				if k==0 : 
					contenu = "<a id='action_"+action.nom_info+"' href=\"#affiche_action_"+str(action.id)+"\" onclick=\"afficheID('action_"+str(action.id)+"','affiche')\"><div id=\"affiche_action_"+str(action.id)+"\" class=colonne_ext><div class=texte_base>+</div></div></a>"
					contenu = contenu + "<a href=\"#affiche_action_"+str(action.id)+"\" onclick=\"afficheID('action_"+str(action.id)+"','masque')\"><div id=\"masque_action_"+str(action.id)+"\" class=colonne_ext style=\"display:none;\"><div class=texte_base>-</div></div></a>"
				html = html+'<div'+style+'>'+contenu+'</div>'
				
				k=k+1
			html = html+'</div>'
			
			contenu_description = action.description2
			if action.regle_associe and action.regle_associe.id != self.id : 
				
				#edit = ''
				if MJ_OK : 
					edit = '<a href="/admin/forum/regle/'+str(action.regle_associe.id)+'/change/" target="_blank">edit</a><br>'
					contenu_description = contenu_description.replace('#regle#',edit+ action.regle_associe.descMJ())
				else : contenu_description = contenu_description.replace('#regle#',action.regle_associe.desc())
			
			html = html+'<div id=action_'+str(action.id)+' class=row1 style=\"display:none;padding:15px\">'+'<div>'+contenu_description+'</div>'
			
			html = html+'</div>'
			
			num_ligne = num_ligne+1
		html =  html + "</div>"
		return html
		
		
	def liste_posture(self,type,MJ_OK):
		T_col = [10,'']
		qst_posture = Posture.objects.filter(active=True).filter(categorie_combat__nom_info=type)
		html = "<div class=tableau>"
		for posture in qst_posture :
			description = ''
			entete = posture.nom
			if MJ_OK : entete = '<a href="/admin/forum/posture/'+str(posture.id)+'/change/" target="_blank">'+posture.nom+'</a>'
			
			if posture.description2 :
				description = posture.description2
			
			html = html+'<div id=posture_'+str(posture.id)+' class=row1 style=\"padding:15px\"><div>'+'<div class=texte_sstitre>'+entete+'</div>\n<div class=texte_base>'+description+'</div>'+'</div></div>'
			
			
		html =  html + "</div>"
		return html
			
		
class Tableau(models.Model):
	active = models.BooleanField(default=True)
	nom_info = models.CharField(max_length=30, null=True)
	titre = models.CharField(max_length=30, unique=True)
	entete = models.BooleanField(default=True, verbose_name="le tableau a t'il une entete ?")
	width = models.CharField(max_length=100, verbose_name="entrez la taille des colonnes, séparé par un #",null=True, blank=True,)
	titre_entete = models.CharField(max_length=100, verbose_name="titre pésent en tant qu'entête",null=True, blank=True,)
	description = models.TextField(null=True, blank=True, verbose_name="un - devant chaque ligne, et un # pour séparer les colonnes")
	
	def __str__(self):
		return self.titre
	
	def tab(self,MJ_OK):
		html = "<br>"
		if self.active :
			html = "<div class=tableau>"
			T_width = (self.width+'######################################################').split('#')
			if self.titre_entete and self.titre_entete!='' : 
				html = html+'<div class=row_entete style="padding-top:2pt;padding-left:5pt;text-align:left;">'+self.titre_entete+'</div>'
			
			T_lignes = ('\n'+self.description).split('\n-')
			if len(T_lignes)>0 : 
				
				num_ligne=0
				for ligne in T_lignes[1:] :
					
					T_colonne = ligne.replace('\n','').split('#')
					
					if self.entete and num_ligne==0 :
						html = html+'<div class=row_entete style="padding-top:2pt;padding-left:5pt;text-align:left;">'
						num_ligne=num_ligne+1
					else : 
						num_ligne=num_ligne+1
						if num_ligne>2 : num_ligne = 1
						html = html+'<div class=row'+str(num_ligne)+'>'
					
					k=0
					while k<len(T_colonne):
						if T_width[k]=='' : style=""
						else : style=' style="min-width: '+T_width[k]+'pt;"'
						
						html = html+'<div'+style+'>'+T_colonne[k]+'</div>'
						k=k+1
						
					html = html+"</div>"
				
			html =  html + "</div>"
		
		if MJ_OK : html = '<a href="/admin/forum/tableau/'+str(self.id)+'/change/" target="_blank">Edit</a><br>'+html
		return html