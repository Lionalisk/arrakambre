import random
import math
from django.http import *

def melee_backstab(postureB,B_direct):
	frappe = "frappe"
	return frappe

def melee_combat(postureB,B_direct):
	frappe = "frappe"
	if postureB.nom_info == "serendre" : frappe = "captureB"
	return frappe

def melee_capture(postureB,B_direct):
	frappe = "essaie_capture"
	if postureB.nom_info == "serendre" : frappe = "captureB"
	#if postureB.nom_info == "defense_lieu" : frappe = "frappe"
	return frappe
	
def melee_laisserfuir(postureB,B_direct):
	frappe = "frappe"
	if postureB.nom_info == "serendre" or postureB.nom_info == "fuir" : frappe = "fuiteB"
	#if postureB.nom_info == "repli" : frappe = "repliB"
	return frappe

def melee_intimidation(postureB,B_direct):
	frappe = "frappe"
	if not postureB.choix_attaque : frappe = "arret"
	#if postureB.nom_info == "repli" : frappe = "repliB"
	#if postureB.nom_info == "laisserpasser" : frappe = "laisserpasserB"
	return frappe
	
	
def melee_arret(postureB,B_direct):
	frappe = "frappe"
	if postureB.nom_info == "intimidation" or (not postureB.choix_attaque) or (not B_direct): frappe = "arret"
	#if postureB.nom_info == "fuir" : frappe = "fuiteB"
	if not B_direct : frappe = "arret"
	return frappe

def melee_fuir(postureB,B_direct):
	frappe = "arret"
	if postureB.nom_info == "combat" or postureB.nom_info == "capture" : frappe = "essai_fuite"
	elif postureB.nom_info == "laisserfuir" or postureB.nom_info == "arret" : frappe = "fuiteA"
	if not B_direct : frappe = "arret"
	
	return frappe
	
def melee_serendre(postureB,B_direct):
	frappe = "arret"
	if postureB.nom_info == "combat" or postureB.nom_info == "capture" : frappe = "captureA"
	elif postureB.nom_info == "laisserfuir" : frappe = "fuiteA"
	elif postureB.nom_info == "backstab" : frappe = "essai_fuite"
	if not B_direct : frappe = "arret"
	return frappe

	
	
	
def meleelieu_attaque_lieu(postureB,B_direct):
	frappe = "frappe"
	if postureB.nom_info == "laisserpasser" : frappe = "laisserpasserB"
	return frappe

def meleelieu_repli(postureB,B_direct):
	frappe = "repliA"
	return frappe
	
def meleelieu_defense_lieu(postureB,B_direct):
	frappe = "frappe"
	if postureB.nom_info == "repli" : frappe = "repliB"
	return frappe

def meleelieu_laisserpasser(postureB,B_direct):
	frappe = "laisserpasserA"
	if postureB.nom_info == "repli" : frappe = "repliB"
	return frappe
	


def bataille_bataille_charge(postureB,B_direct):
	frappe = "frappe_bataille"
	if postureB.nom_info == "bataille_retraite" : frappe = "essai_retraiteB"

def bataille_bataille_encerclement(postureB,B_direct):
	frappe = "frappe_bataille"
	if postureB.nom_info == "bataille_retraite" : frappe = "essai_retraiteB"

def bataille_bataille_defense(postureB,B_direct):
	frappe = "frappe_bataille"
	if postureB.nom_info == "bataille_retraite" : frappe = "retraiteB"

def bataille_bataille_mobilite(postureB,B_direct):
	frappe = "frappe_bataille"
	if postureB.nom_info == "bataille_retraite" : frappe = "essai_retraiteB"

def bataille_bataille_retraite(postureB,B_direct):
	frappe = "essai_retraiteA"
	if postureB.nom_info == "bataille_retraite" : frappe = "retraiteB"
	if postureB.nom_info == "bataille_defense" : frappe = "retraiteA"
	


def bataillelieu_bataille_lieu(postureB,B_direct):
	frappe = "frappe"
	if postureB.nom_info == "laisserpasser" : frappe = "laisserpasserB"
	return frappe

def bataillelieu_bataille_repli(postureB,B_direct):
	frappe = "repliA"
	return frappe
	