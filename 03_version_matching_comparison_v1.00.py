# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 15:02:00 2019

@author: Utilisateur
"""


###########################################################################
# Application : find citys in 'baie de saint de michel' cited in survey   #
# Program name: mini_projet_v1.00.py                                      #
# Description : This program do the statistics comparison between the     #
#                                                    three version        #
#_________________________________________________________________________#
# Localisation: https://github.com/Ibrwa/Mini_projet/mini_projet_v1.00.py #           
# Developped     : Under spyder in Windows                                #
#_________________________________________________________________________#
# Creation    : 21/01/2019 by Ibrwa                                       #    
# Historical update:                                                      #                                                      
#_________________________________________________________________________#


### Import the library 

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt, matplotlib
import seaborn as sns
from matplotlib import rc



matplotlib.style.use('ggplot')
title_font = {'fontname':'Arial', 'size':'14','fontweight': 'bold'}
axis_font = {'fontname':'Arial', 'size':'13','fontweight': 'bold'}
plt.rcParams["axes.labelweight"] = "bold"
rc('font', weight='bold')



############" Load all results from the three version #####################

top_ville_v0 = pd.read_csv("top_villes.0.00.csv")
top_ville_v1 = pd.read_csv("top_villes.0.01.csv")
top_ville_v2 = pd.read_csv("top_villes.0.02.csv")

### rename column total with number of version 
top_ville_v0.rename(columns = {'total':'Total v0'},inplace = True)
top_ville_v1.rename(columns = {'total':'Total v1'},inplace = True)
top_ville_v2.rename(columns = {'total':'Total v2'},inplace = True)


### Make joint on all three dataframe ###############

ville_version_comp = pd.merge(left = top_ville_v2,right = top_ville_v1,
                              on = 'villes',how='left')
ville_version_comp = pd.merge(left = ville_version_comp,right = top_ville_v0,
                              on = 'villes',how='left')


################ Statistics descriptives ##########################

#### Replacer les valeurs manquantes par zero #############
ville_version_comp.replace({np.nan:0},inplace=True)

ville_version_comp.describe()


#### Graphiques des villes < 5 #############
filtre = ville_version_comp['Total v2'] <= 5
ville_version_comp.loc[filtre].plot(x = 'villes',kind='bar',figsize=(12, 9))
plt.xlabel('Villes',fontdict=axis_font) # add to x-label to the plot
plt.ylabel("Nombre trouvé",fontdict=title_font) # add y-label to the plot
plt.title('Matching dont le nombre trouvé est < 5',fontdict=title_font) # add title to the plot
plt.tick_params(labelsize=13)
plt.show()

#### Graphiques des villes >= 5 and villes <15 #############

filtre = (ville_version_comp['Total v2'] >= 5) & (ville_version_comp['Total v2'] < 15)
ville_version_comp.loc[filtre].plot(x = 'villes',kind='bar', figsize=(11, 9))
plt.xlabel('Villes',fontdict=axis_font) # add to x-label to the plot
plt.ylabel("Nombre trouvé",fontdict=axis_font) # add y-label to the plot
plt.title('Matching dont le nombre trouvé est entre 5 et 15',fontdict=title_font) # add title to the plot
plt.tick_params(labelsize=13)
plt.show()


#### Graphiques des villes > 15 #############

filtre = (ville_version_comp['Total v2'] >= 15) 

ville_version_comp.loc[filtre].plot(x = 'villes',kind='bar', figsize=(11, 9))
plt.xlabel('Villes',fontdict=axis_font) # add to x-label to the plot
plt.ylabel("Nombre trouvé",fontdict=axis_font) # add y-label to the plot
plt.title('Matching dont le nombre est > 15',fontdict=title_font) # add title to the plot
plt.tick_params(labelsize=13)

plt.show()

##### Boxplot sur les donnees #################

### 
agg_data = pd.DataFrame()

### merge data from wide to long ###
# v0
temp_data = top_ville_v0; temp_data.rename(columns = {'Total v0':'Nbr'},inplace=True);temp_data['Version'] = 'Version 0.00'
agg_data = agg_data.append(temp_data)
# v1
temp_data = top_ville_v1; temp_data.rename(columns = {'Total v1':'Nbr'},inplace=True);temp_data['Version'] = 'Version 0.01'
agg_data = agg_data.append(temp_data)
# v2
temp_data = top_ville_v2; temp_data.rename(columns = {'Total v2':'Nbr'},inplace=True);temp_data['Version'] = 'Version 0.02'
agg_data = agg_data.append(temp_data)

### plotting here ###
sns.set_style("whitegrid") 
fig = plt.figure(figsize=(11, 9))
ax = sns.boxplot(x = 'Version', y = 'Nbr', data = agg_data,palette="PRGn") 
plt.xlabel('Version du matching') # add to x-label to the plot
plt.ylabel("Nombre trouvé par communes") # add y-label to the plot
plt.title('Boxplot du nombre de communes trouvées selon la version du matching') # add title to the plot

plt.show()

