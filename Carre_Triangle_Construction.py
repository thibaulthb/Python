#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 14:23:06 2022

@author: thibault
"""



## Importation des bibliotheques
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from numpy import pi

## Construction manuelle du signal carre et creation de la fenetre

a0=1            # Amplitude en V
T0=2            # periode effective du signal en s
f0=1/T0         # frequence du signal (inverse de la periode effective)

fig = plt.figure(constrained_layout=True, figsize=(16,6))
gs = fig.add_gridspec(ncols=10, nrows=6)
ax0 = fig.add_subplot(gs[0:5,0:5])
ax1 = fig.add_subplot(gs[0:5,5:10])

# definition de la fonction creneau
def creneau(x):
    reste = x%T0
    if (reste<T0/2):
        res = a0
    else:
        res = -a0
    return res
creneau_vec = np.vectorize(creneau)

# definition de la fonction triangle
def triangle(x):
    a = x % (T0)
    if a < T0/2:
        return a/(T0/4)-1
    else:
        return (2-a/(T0/4))+1
triangle_vec = np.vectorize(triangle)

t = np.arange(-1*T0, 2*T0, 0.001)    # temps allant de -2 s à 4s par pas de 0.01s (sur trois periodes)

# Creation de la courbe de Fourier (avec la serie de Fourier à N terme)
def four_carre(x,N):
    S0 = 0
    for n in np.arange(0,N+1,1):                        # n va varier de 0 à N0 par pas de 1 (attention la borne max est N0+1 car il exclu la borne max
        Cn0 = (4/pi)*(np.sin((2*n+1)*2*pi*x/T0))/(2*n+1)
        S0 = S0 + Cn0
    return S0
# Creation de la courbe de Fourier (avec la serie de Fourier à N terme)
def four_triangle(x,N):
    S0 = 0
    for n in np.arange(0,N+1,1):                        # n va varier de 0 à N0 par pas de 1 (attention la borne max est N0+1 car il exclu la borne max
        Cn0 = -(16*0.5/pi**2)*(np.cos((2*n+1)*2*pi*x/T0))/(2*n+1)**2
        S0 = S0 + Cn0
    return S0


N0=0                                                # initialisation Ã  1 le nombre de composantes de la serie de Fourier
lt, = ax0.plot(t, four_triangle(t,N0), lw=1.5, color='red')         # courbe Ã  tracer i en fonction de omega
ax0.plot(t,triangle_vec(t),'b--',lw=.75)
ax0.axis([-T0, 2*T0, -1.5*a0, 1.5*a0])                     # limite des axes (xmin,xmax,ymin,ymax)
ax0.set_xlabel("Temps (s)")                     # titre de l'axe des abscisses
ax0.set_ylabel("Amplitude du signal (V)")                               # titre de l'axe des ordonnees
ax0.title.set_text("Construction d'un signal triangulaire par série de Fourier") 
ax0.grid(True)                                          # quadrille le graphique
lc, = ax1.plot(t, four_carre(t,N0), lw=1.5, color='red')         # courbe Ã  tracer i en fonction de omega
ax1.plot(t,creneau_vec(t),'b--',lw=.75)
ax1.axis([-1*T0, 2*T0, -1.5*a0, 1.5*a0])                     # limite des axes (xmin,xmax,ymin,ymax)
ax1.set_xlabel("Temps (s)")                     # titre de l'axe des abscisses
ax1.set_ylabel("Amplitude du signal (V)")                               # titre de l'axe des ordonnees
ax1.title.set_text("Construction d'un signal carré par série de Fourier") 
ax1.grid(True)                                          # quadrille le graphique

## Ajout des barres de changement de valeur des variables initiales
axcolor = 'lightgoldenrodyellow'                            # couleur des barres
axN = plt.axes([0.25, 0.02, 0.65, 0.03], facecolor=axcolor)    # localisation de la barre pour N
ioN = Slider(axN,"Nombre d'harmoniques",0,40,valinit=N0,valstep=1,valfmt='%0.0f')

## Definition de la fonction qui permet de reinitialiser les valeurs initiales par celle choisie Ã  la barre
def update(val):
    N = ioN.val                                             # prend la valeur de la barre pour N
    lc.set_ydata(four_carre(t,N))    # ressort le nouveau profil de resonance
    lt.set_ydata(four_triangle(t,N))    # ressort le nouveau profil de resonance
    fig.canvas.draw_idle()                                  # redessine la courbe
ioN.on_changed(update)                                      # affiche Ã  cÃ´te de la barre la valeur de N

plt.show()