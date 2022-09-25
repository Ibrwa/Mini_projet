#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 18:44:50 2022

@author: pydata
"""

import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances # for jaccard diss
from sklearn import manifold 


## read the data 
data = pd.read_csv("data.csv")

## compute matrix distance 
matrice_distance = pairwise_distances(data.to_numpy(), metric='jaccard')

## fit multidimensionnal scaling 
mds_model = manifold.MDS(n_components=2, random_state=57100, dissimilarity='precomputed')

## fit the model 
mds_fit = mds_model.fit(matrice_distance)
mds_coord = mds_model.fit_transform(matrice_distance)

##" Graphics mds 
nom_villes = data.columns.to_list()
plt.figure(figsize=(10,10))
plt.scatter(mds_coord[:,0],mds_coord[:,1],facecolors = 'none', edgecolors = 'none')  # points in white (invisible)
for label, x, y in zip(nom_villes, mds_coord[:,0], mds_coord[:,1]):
    plt.annotate(label, (x,y), xycoords = 'data')
plt.axhline(0, color='black')
plt.axvline(0, color='black')
plt.xlabel('Première dimension')
plt.ylabel('Seconde Dimension')
plt.title('Matrice de similarité des villes')    
plt.show()