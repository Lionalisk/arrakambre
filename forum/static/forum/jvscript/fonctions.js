// JavaScript Document
//-------------------------------------------------------------------------------


function deletePost(lien){
	
	if(confirm("ATTENTION : cela supprimera definitivement le Post. Voulez vous continuer ?")){
		document.location.href=lien;
	}
}
function deleteGarde(lien){
	
	if(confirm("ATTENTION : cela supprimera definitivement un garde. Voulez vous continuer ?")){
		document.location.href=lien;
	}
}
function deleteTroupe(lien){
	
	if(confirm("ATTENTION : cela supprimera definitivement une troupe. Voulez vous continuer ?")){
		document.location.href=lien;
	}
}
function deleteObj(lien){
	
	if(confirm("ATTENTION : cela supprimera definitivement l'objet. Voulez vous continuer ?")){
		document.location.href=lien;
	}
}

function changeJoueur(id_joueur){
	lien = document.location.href;
	var T_lien = lien.split('/-');
	var lien_debut = T_lien[0];
	var T_lien2 =  T_lien[1].split('/');
	T_lien2.splice(0, 1, '')
	lien_fin = T_lien2.join('/')
	
	lien = lien_debut+'/-'+id_joueur+lien_fin;

	document.location.href=lien;
}

function afficheID(id,ordre) {
	if(ordre=="affiche"){
		document.getElementById(id).style.display='block';
		document.getElementById("affiche_"+id).style.display='none';
		document.getElementById("masque_"+id).style.display='block';
	}
	if(ordre=="masque"){
		document.getElementById(id).style.display='none';
		document.getElementById("affiche_"+id).style.display='block';
		document.getElementById("masque_"+id).style.display='none';
	}

}

function afficheID2(id,ordre) {
	if(ordre=="affiche"){
		document.getElementById(id).style.display='inline-block';
		document.getElementById("affiche_"+id).style.display='none';
		document.getElementById("masque_"+id).style.display='inline-block';
	}
	if(ordre=="masque"){
		document.getElementById(id).style.display='none';
		document.getElementById("affiche_"+id).style.display='inline-block';
		document.getElementById("masque_"+id).style.display='none';
	}

}

function affiche_allID(ordre) {
	
	if(ordre=="masque"){
		affichage = "none";
		affichage2 = "block";
		}
	if(ordre=="affiche"){
		affichage = "block";
		affichage2 = "none";
		}
	
	var elts = document.getElementsByClassName("msg_post");
	var nbre_elts = elts.length;
	
	for( var i=0; i<nbre_elts; i++)
	{
		elts[i].style.display = affichage;
	}
	
	var elts2 = document.getElementsByClassName("colonne_ext");
	var nbre_elts = elts2.length;
	
	for( var i=0; i<nbre_elts; i++)
	{
		//alert(elts2[i].id.substr(0, 2));
		if (elts2[i].id.substr(0, 3) =="aff"){
			elts2[i].style.display = affichage2;
		}
		if (elts2[i].id.substr(0, 3) =="mas"){
			elts2[i].style.display = affichage;
		}
	}
}

//-------------------------------------------------------------------------------
//-------------------------------------------------------------------------------


function test(){
	alert("BBBBBBBBBBBBBB");
}

function select_perso(id_perso){
	
	document.getElementById(id_id_perso).value = id_perso;
}

function change_perso(num_div,nb_div){
	if (num_div> nb_div) {num_div=1}
	if (num_div< 1) {num_div=nb_div}
	
	for(i=1;i<=nb_div;i++){
		if (i == num_div){
			masque = 'block';
		}
		else {
			masque = 'none';
		}
		document.getElementById(i).style.display=masque;
	}
	
}

function select_action(id_action){
	
	document.getElementById(id_id_action).value = id_action;
}


//-------------------------------------------------------------------------------
//-------------------------------------------------------------------------------


function masquer_categorie(categorie,etat){ //gere le menu déroulant
	
	var titre_cate = "titre_"+categorie;
	var masque = "block";
	var new_etat = "ouvert";
	
	var reg=new RegExp("-///-");
	var garde_memoire = document.getElementById("sauvegarde_donnees").innerHTML;
	var liste_cate_fermee = new Array();
	liste_cate_fermee = garde_memoire.split(reg);
	
	if((etat == "ouvert")&&(document.getElementById(titre_cate))){
		
		masque = 'none';
		new_etat = 'ferme';
		liste_cate_fermee[liste_cate_fermee.length]=categorie;
	}
	
	if((etat == "ferme")&&(document.getElementById(titre_cate))){
		
		masque = 'block';
		new_etat = 'ouvert';
		liste_cate_fermee=supprimer_elt_tableau(liste_cate_fermee,categorie);
	}

		

		var args = "'"+categorie+"','"+new_etat+"'";
			
		// met le bouton en état ouvert ou ferme
		for(ui=0;ui<3;ui++){
			if(document.getElementById(titre_cate)){
				document.getElementById(titre_cate).href='javascript:masquer_categorie('+args+')';
				document.getElementById(titre_cate).id='nulll';
			}
			else{break;}
		}
		
		for(uj=0;uj<3;uj++){
			if(document.getElementById('nulll')){
				document.getElementById('nulll').id=titre_cate;
			}
			else{break;}
		}

		// affiche/masque les projet de la categorie
		for(ju=0;ju<1000;ju++){  
			if(document.getElementById(categorie)){
				document.getElementById(categorie).style.display=masque;
				document.getElementById(categorie).id='null';
			}
			else{break;}
		}
		for(iu=0;iu<1000;iu++){
			if(document.getElementById('null')){
				document.getElementById('null').id=categorie;
			}
			else{break;}
		}
		
	garde_memoire=liste_cate_fermee.join("-///-");
	document.getElementById("sauvegarde_donnees").innerHTML=garde_memoire;

}


//-------------------------------------------------------------------------------
//-------------------------------------------------------------------------------

function masquer_ttes_categories(categorie){ // masque les categories du menu déroulant
	
	for(f=0;f<categorie.length;f++) {
	masquer_categorie(categorie[f],'ouvert');
	f=f+1;
	}
}

//-------------------------------------------------------------------------------
//-------------------------------------------------------------------------------



function resetChamp(){
	document.forms["chercher"].elements["texte_search"].value="";
	
	if (document.title != "Index"){
		categorie=liste_categories();
		tri_categorie();
		masquer_ttes_categories(categorie);
	}
}

//-------------------------------------------------------------------------------
//-------------------------------------------------------------------------------
function remplirChamp(mot_cle){
	document.forms["chercher"].elements["texte_search"].value=mot_cle;

}
//-------------------------------------------------------------------------------
//-------------------------------------------------------------------------------


function insertAtCursor(myValue) {
   var myField = form_action.texte;
   //IE support
   /* if (document.selection) {
        myField.focus();
        sel = document.selection.createRange();
        sel.text = myValue;
    }*/
    //MOZILLA and others
    
	if (myField.selectionStart || myField.selectionStart == '0') {
        var startPos = myField.selectionStart;
        var endPos = myField.selectionEnd;
		var myValue2 = myValue;
		if((myValue.substring(0,3)=="div") || (myValue.substring(0,3)=="txt") || (myValue.substring(0,4)=="span")){myValue2 = myValue.substring(0,4)}
		var new_text = myField.value.substring(0, startPos)
            + "<"+myValue+">"
			+ myField.value.substring(startPos, endPos)
			+ "</"+myValue2+">"
            + myField.value.substring(endPos, myField.value.length);
		myField.value = new_text;
    } else {
        myField.value += myValue;
    }
}