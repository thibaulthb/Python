#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 15:31:50 2021

@author: thibault
"""


from math import * # Outils mathematiques
import numpy as np # Outils numeriques
import scipy as sp # Outils scientifiques
import scipy.integrate # pour l’integration
import scipy.optimize # pour trouver les zéros
import matplotlib.pyplot as plt # Outils graphiques
plt.rcParams['text.usetex'] = True
from statistics import mean
from scipy import stats

from PyAstronomy import pyaC

from detecta import detect_peaks # détection des maxima sur la courbe

import csv # importer le fichier CSV (attention, pi=3.14 et non pi=3,14)

#lecture du fichier
x=np.loadtxt(open("Pendule_non-lineaire.csv"), delimiter=";", skiprows=1)#,max_rows=67100)
print(len(x))
#conversion tension-> angle sans recentrage 
x[:,1]=(x[:,1])/4.927

#obtention des positions des maxima et minima
detect_min=0
detect_max=35440
indexes=detect_peaks(x[detect_min:detect_max,1], mph=0, mpd=200,show=False)
indexes_moins=detect_peaks(-x[detect_min:detect_max,1], mph=0, mpd=200,show=False)

#recentrage des valeurs des angles (theta=0 => 0V)
x[:,1]=x[:,1]-mean(x[indexes,1]+x[indexes+1,1]+2*x[indexes_moins,1])/4

#détermination de la valeur de thetam sur une période
maxima=(x[indexes,:]-x[indexes_moins,:])/2

#obtention de la pseudo-période de façon précise
#détermination des changements de signe
zero_crossings = np.where(np.diff(np.signbit(x[detect_min:detect_max,1])))[0]
#élimination des fronts descendants
if x[zero_crossings[1]+1,1]-x[zero_crossings[1],1]<0:
    zero_crossings2=zero_crossings[2:len(zero_crossings):2]
else:
    zero_crossings2=zero_crossings[1:len(zero_crossings):2]
#détermination de la pente et interpolation : détermination de la position du zéro
zero_time=x[zero_crossings2+1,0]-x[zero_crossings2+1,1]*(x[zero_crossings2+1,0]-x[zero_crossings2,0])/(x[zero_crossings2+1,1]-x[zero_crossings2,1])
#calcul de la pseudo-périodez[1]/z[2],err[1]/z[2],
maxima[0:len(indexes)-1,0]=zero_time[1:len(indexes)]-zero_time[0:len(indexes)-1]

#ajustement des résultats par un polynôme d'ordre 2
fit_min=0
fit_max=len(indexes)-1
z,cov = np.polyfit(maxima[fit_min:fit_max,1]**2, maxima[fit_min:fit_max,0], 2, cov=True)
t = np.arange(0,1.01,0.01)
err=np.sqrt(np.diag(cov))

#tracé de la période en fonction du carré de thetam
xmax=floor(max(maxima[0:len(indexes)-1,1]**2)*10+1)/10
xmin=floor(min(maxima[0:len(indexes)-1,1]**2)*10)/10
ymax=floor(max(maxima[0:len(indexes)-1,0])*100+1)/100
ymin=floor(min(maxima[0:len(indexes)-1,0])*100)/100
plt.figure(0,figsize=(14,8))
plt.title(r'Évolution de la période en fonction du carré de $\theta_m$',fontsize=18)
plt.xlabel(r"Carré de l'angle maximum $\theta_m^2$ (rad)",fontsize=14)
plt.ylabel(r"Pseudo--période $T$ (s)",fontsize=14)
plt.xlim(xmin,xmax)
plt.ylim(ymin,ymax)
plt.axvline(x=maxima[fit_min,1]**2,color='g',linewidth=1)
plt.axvline(x=maxima[fit_max,1]**2,color='g',linewidth=1)
fit=plt.plot(t,z[2]+z[1]*t+z[0]*t**2,'r--',label=r'$T=a(1+b\theta_m^2+c\theta_m^4)$ où'+'\n\t'+r'a= %1.4f $\pm$%1.0e'%(z[2],2*err[2])+'\n\t'+r'b= %1.2e$\pm$%1.0e'%(z[1]/z[2],2*err[1]/z[2])+'\n\t'+r'c=  %1.1e$\pm$%1.0e' %(z[0]/z[2],2*err[0]/z[2]))
data=plt.plot(maxima[0:len(indexes)-1,1]**2,maxima[0:len(indexes)-1,0],marker='+',linestyle='None',label=r'Points expérimentaux')
plt.legend(fontsize=12,loc='upper left',framealpha=1)

#écriture dans un fichier pour analyse avec regressi
np.savetxt('Pendule_nl_T_Thetam_4.csv', maxima[0:len(indexes)-1,:], delimiter=',', fmt='%1.5e')

#ajustement de la décroissance linéaire de l'amplitude
fit_min=75
plot_min=0
plot_max_val=floor(max(x[:,0])*5)/5
z2 = np.polyfit(x[indexes[fit_min:len(indexes-1)],0],x[indexes[fit_min:len(indexes-1)],1],1)
z2_moins = np.polyfit(x[indexes_moins[fit_min:len(indexes-1)],0],x[indexes_moins[fit_min:len(indexes-1)],1],1)
t2 = np.arange(plot_min,plot_max_val+5,5)

#tracé de la décroissance linéaire de l'amplitude
plot_ind_min=indexes[plot_min]
plt.figure(1,figsize=(14,8))
plt.plot(x[plot_ind_min:len(x),0],x[plot_ind_min:len(x),1])
plt.xlim(x[plot_ind_min,0],x[len(x)-1,0])
# plt.ylim(ymin,ymax)
# print(x[indexes[100:len(indexes-1)],1])
fit2=plt.plot(t2,z2[1]+z2[0]*t2)
fit3=plt.plot(t2,z2_moins[1]+z2_moins[0]*t2)
# plt.plot(x[indexes[10:len(indexes-1)],0],x[indexes[10:len(indexes-1)],1],marker='+',linestyle='none')
# plt.plot(x[indexes,0],x[indexes,1])
print(z2,z2_moins,(z2[0]-z2_moins[0])/2)

#tracé du diagramme de phase
x_point=(x[0:len(x)-4,1]-8*x[1:len(x)-3,1]+8*x[3:len(x)-1,1]-x[4:len(x),1])/(12*5e-3)
print(x_point)
plt.figure(2,figsize=(14,8))
print(len(x_point))
plt.plot(x[2:len(x)-2,1],x_point)
