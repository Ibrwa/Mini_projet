# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 08:28:56 2018

@author: Utilisateur
"""


import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt, matplotlib


matplotlib.style.use('ggplot')

### caracteres de ponctuations
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~ '''

### Lire les donnees des communes 

communes = pd.read_csv("C:\\Users\\Utilisateur\\Documents\\Python\\data\\correspondance-code-insee-code-postal.csv",
                       delimiter=";",
                       usecols = [1,2,3,4,15,16],
                       dtype = 'object')


### Filtrer uniquement sur les departements 35 et 50

communes = communes.loc[(communes['code_departement'] =='50') | (communes['code_departement'] =='35')]

### Lecture des donnes sources ####

msm_ods = pd.read_csv("C:\\Users\\Utilisateur\\Documents\\Python\\data\\MSM.txt",
                      delimiter=";",
                      dtype={'id':int,'villes':'object'})

######################################################################
## Traitement des données du fichier de reponses ###
######################################################################

### changer les valeurs des lignes en miniscule et enlever les accents 

msm_ods['villes'] = msm_ods['villes'].str.lower()

### remplacer les caracteres bizarres 

### on definit une fonction qui permet de remplacer un caracter par un autre

def replacement(s,source,target):
    return s.replace(source,target)

## On applique notre fonction a nos donnees 

### Tous d abord on cree une chaine avec les caracteres speciaux 

spec_car_fr = "éèêçîôâûäëüïö"
spec_car_clean = "eeecioauaeuio"


## On l applique a nos donnees 
for _ in range(len(spec_car_fr)):
    msm_ods['villes'] = replacement(msm_ods['villes'].str,spec_car_fr[_],spec_car_clean[_])
    

######################################################################
## Traitement des données du fichier de l'insee  ###
######################################################################
communes['commune'] = communes['commune'].str.lower()
for _ in range(len(spec_car_fr)):
    communes['commune'] = replacement(communes['commune'].str,spec_car_fr[_],spec_car_clean[_])





######################################################################
########### Traitement des donnees ###################################
######################################################################

dict_data = {} ## initialisation du dictionnaire

#### on cree maintenant les cles qui sont les noms officiels des communes issue du fichier de l insee
#### on initialise les cles avec des valeurs d une liste à 0 d une longeur vide

for cle in  communes["commune"].tolist():
    dict_data[cle] = [0]*msm_ods.shape[0]

###### Traitement des donnees ##########################
# I. on parcous chaque reponse et si une ville citee correspond a une cle du dictionnaire on met 1 sinon on met zeros


#### on cree une fonction qui supprimes les ponctuations #####
def remove_ponctuation(s):
    new_string = ""
    for char in s:
        if char not in punctuations:
            new_string = new_string + char
    return new_string



for i in range(msm_ods.shape[0]):
    reponse = msm_ods.iloc[i,1].split() ## on recupere la reponse ici 
    ### clean the response 
    reponse = [remove_ponctuation(_) for _ in reponse]
    #### on parcours la reponse pour voir si une ville citee match avec les noms dans le dictionnaire 
    for ville_citee in reponse:
        if ville_citee in dict_data.keys():
            dict_data[ville_citee][i] = 1
    
bitmap_data = pd.DataFrame(dict_data)

### Graphique des 10 reponses les plus citees #########

### Definition d une fonction qui calcule la moyenne 

def calcul_mean(x):
    return np.mean(x)

def calcul_sum(x):
    return np.sum(x)

top_villes = bitmap_data.apply(calcul_sum,axis=0).sort_values(ascending=False)

top_villes = pd.DataFrame({'villes':top_villes.index.tolist(),'total':top_villes})

#### Graphique en barplot ####################
_, ax = plt.subplots()
ax.barh(top_villes['villes'][:10], top_villes['total'][:10], color = '#539caf', align = 'center')
ax.set_ylabel("Pourcentage %")
ax.set_xlabel("Nom de la ville")
ax.set_title("Top 10 des villes les plus citées")
plt.show()


    

