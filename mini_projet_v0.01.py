#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 11:09:03 2019

@author: waneibr
"""


###########################################################################
# Application : find citys in 'baie de saint de michel' cited in survey   #
# Survey      : TOURS                                                     #
# Program name: mini_projet_v0.00.py                                      #
# Description : version with no relative so it can runed by anyone        #
#_________________________________________________________________________#
# Localisation: https://github.com/Ibrwa/Mini_projet/mini_projet_v0.00.py #           
# Developped     : Under spyder in Windows                                #
#_________________________________________________________________________#
# Creation    : 10/10/2018 by Ibrwa                                       #    
# Historical update: 15/10/2018 remove relative path in importing files		#
#                    11/01/2019 Add function for splitting city cited in  #
#                               a list                                    #
#_________________________________________________________________________#

### Import the library 

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt, matplotlib
import string
import levenshtein 


## Use nice style of ggplot
matplotlib.style.use('ggplot')

### define ponctuation caracters==> can be enhcanced !!
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~ '''

## Read the data that contains all city (commune) in France. Can be found in insee website

communes = pd.read_csv("correspondance-code-insee-code-postal.csv",
                       delimiter=";",
                       usecols = [1,2,3,4,15,16],
                       dtype = 'object')

### filter only in departement of interest : ie 50 and 35 which contain the city of 'baie de saint michel'

communes = communes.loc[(communes['code_departement'] =='50') | (communes['code_departement'] =='35')]

### read the data source of survey 

msm_ods = pd.read_csv("MSM.txt",
                      delimiter=";",
                      dtype={'id':int,'villes':'object'})

######################################################################
## processing the survey data ###
######################################################################

### changer les valeurs des lignes en miniscule et enlever les accents 

msm_ods['villes'] = msm_ods['villes'].str.lower()

### remplacer les caracteres bizarres 

### on definit une fonction qui permet de remplacer un caracter par un autre

def replacement(s,source,target):
    """
    This function help us to remove all specific french caracteres so we can made the match easiky
    """
    return s.replace(source,target)



######################################################################
## Traitement des donnees de l enquete
######################################################################

spec_car_fr    = "éèêçîôâûäëüïö"
spec_car_clean = "eeecioauaeuio"


## On l applique a nos donnees 
for car_fr,car_clean in zip(spec_car_fr,spec_car_clean):
    msm_ods['villes'] = replacement(msm_ods['villes'].str,car_fr,car_clean)


######################################################################
## Traitement des données du fichier de l'insee  ###
######################################################################
communes['commune'] = communes['commune'].str.lower()
for car_fr,car_clean in zip(spec_car_fr,spec_car_clean):
    communes['commune'] = replacement(communes['commune'].str,car_fr,car_clean)
    

#######################  Data cleaning ###########################
# On cree une fonction qui va chercher tous les separateur 
# dans un string et faire un split du string selon ses separateur # 

def splitting_by_sep(s):
    """
    Cette fonction prend en argument une chaine de caractere 
    et retourne une liste en faisant un split de tous les sepaateurs possibles
    Enfin la fonction retourne une liste qui est une union de tous les splits effectues
    """
    # define puncation string 
    ponctuation = string.punctuation
    l_ponc_for_split = []
    for _ in ponctuation:
        if _ in s:
            l_ponc_for_split.append(_)
    l_final = []
    for _ in l_ponc_for_split:
        l_final = l_final + s.split(_)
    l_final = list(set(l_final))
    ### on enleve les espaces du debut 
    l_final = [_.lstrip() for _ in l_final] 
    #### on enleve les pace à la fin 
    l_final = [_.rstrip() for _ in l_final] 
    ##### Si la liste l_final est vide ## Alors on fait un split par le caractere espace
    if len(l_final) ==0:
        l_final = s.split(' ')
    return l_final


######################################################################
########### Creation du data frame  ###################################
######################################################################

dict_data = {} ## initialisation du dictionnaire

#### on cree maintenant les cles qui sont les noms officiels des communes issue du fichier de l insee
#### on initialise les cles avec des valeurs d une liste à 0 d une longeur vide

for cle in  communes["commune"].tolist():
    dict_data[cle] = [0]*msm_ods.shape[0]


# I. on parcous chaque reponse et si une ville citee correspond a une cle du dictionnaire on met 1 sinon on met zeros



for i in range(msm_ods.shape[0]):
    reponse = splitting_by_sep(msm_ods.iloc[i,1]) ## on recupere la reponse ici 
    #### on parcours la reponse pour voir si une ville citee match avec les noms dans le dictionnaire 
    for ville_citee in reponse:
        if ville_citee in dict_data.keys():
            dict_data[ville_citee][i] = 1
    
bitmap_data = pd.DataFrame(dict_data)
    
    
### Graphique des 10 reponses les plus citees #########

### Definition d une fonction qui calcule la somme 

def calcul_sum(x):
    return np.sum(x)

###  Create a data frame ordered by top city cited 
    
top_villes = bitmap_data.apply(calcul_sum,axis=0).sort_values(ascending=False)

## Add column with name of city 
top_villes = pd.DataFrame({'villes':top_villes.index.tolist(),'total':top_villes})

## Orrder the column 
top_villes = top_villes[['villes','total']].reset_index(drop=True)

### Filter only in city which it's match 

top_villes = top_villes.loc[top_villes['total']>0]

#### Graphique en barplot ####################
_, ax = plt.subplots()
ax.barh(top_villes['villes'][:10], top_villes['total'][:10], color = '#539caf', align = 'center')
ax.set_ylabel("Nombre total")
ax.set_xlabel("Nom de la ville")
ax.set_title("Top 10 des villes les plus citées")
plt.show()




#########################################################################"
#########################################################################
# Comparison with first version of data ###############################

##### Comparison with first version ######################

top_ville_v0 = pd.read_csv("top_villes.0.01.csv")

### rename column total 

top_ville_v0.rename(columns = {'total':'total_v0'},inplace = True)


### Make comparison between the new and the old data ###############

ville_version_comp = pd.merge(left = top_villes,right = top_ville_v0,
                              on = 'villes',how='left')

######## Liste des villes trouves  à la premiere version #####
ville_version_comp.loc[ville_version_comp['total_v0'].isnull()]
ville_version_comp.loc[ville_version_comp['total_v0'].isnull()].apply(calcul_sum,axis=0)

########### Liste des villes ameliorees #################

villes_ameliorees = ville_version_comp.loc[ville_version_comp['total'] > ville_version_comp['total_v0'] ]

villes_ameliorees['ratio'] = (villes_ameliorees['total'] - villes_ameliorees['total_v0'])*100/villes_ameliorees['total_v0']

#### Graphiques des villes #############
villes_ameliorees.plot(x = 'villes',y='ratio',kind='bar', figsize=(8, 8))

plt.xlabel('Villes') # add to x-label to the plot
plt.ylabel("% d'amelioration") # add y-label to the plot
plt.title('Villes dont le nombre de citation a augmenté') # add title to the plot

plt.show()





