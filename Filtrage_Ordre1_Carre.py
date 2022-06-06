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
f1=1000*f0

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

# définition d'un filtre passe bas d'ordre 1
def H(f,f1):
    return 1/complex(1,f/f1)
H_vect=np.vectorize(H)
    
t = np.arange(-1*T0, 2*T0, 0.001)    # temps allant de -2 s à 4s par pas de 0.01s (sur trois periodes)
freq = np.linspace(0,100,101)
freqlog = np.logspace(-1,2,301)

# Creation de la courbe de filtrée (avec la serie de Fourier à 100 termes)
def coef_carre(n):
    return (4/pi)/(2*n+1)
def carre_filtre(x,f1):
    S0 = 0
    for n in np.arange(0,101,1):                        # n va varier de 0 à N0 par pas de 1 (attention la borne max est N0+1 car il exclu la borne max
        f = (2*n+1)*2*pi/T0
        Cn0 = a0*coef_carre(n)*np.sin(f*x+np.angle(H(f,f1)))*np.abs(H(f,f1))
        S0 = S0 + Cn0
    return S0

N0=0                                                # initialisation Ã  1 le nombre de composantes de la serie de Fourier
ax0.stem(2*freq+1, coef_carre(2*freq+1), basefmt='none', markerfmt='go', linefmt='g')
ax01=ax0.twinx()
lf, = ax01.plot(freqlog, np.abs(H_vect(freqlog*f0,f1)), lw=1.5, color='red')         # courbe Ã  tracer i en fonction de omega
ax0.axis([.7, 100, 0, coef_carre(1)*a0])                     # limite des axes (xmin,xmax,ymin,ymax)
ax01.axis([.7, 100, 0, 1])                     # limite des axes (xmin,xmax,ymin,ymax)
ax0.set_xscale('log')
ax0.set_xlabel("Fréquence (multiple de $f_0$)")                     # titre de l'axe des abscisses
ax0.set_ylabel("Amplitude du signal")                               # titre de l'axe des ordonnees
ax0.title.set_text("Diagramme de bode pour le gain") 
ax0.grid(True)                                          # quadrille le graphique
lc, = ax1.plot(t, carre_filtre(t,f1), lw=1.5, color='red')         # courbe Ã  tracer i en fonction de omega
ax1.plot(t,creneau_vec(t),'b--',lw=.75)
ax1.axis([-1*T0, 2*T0, -1.5*a0, 1.5*a0])                     # limite des axes (xmin,xmax,ymin,ymax)
ax1.set_xlabel("Temps (s)")                     # titre de l'axe des abscisses
ax1.set_ylabel("Amplitude du signal (V)")                               # titre de l'axe des ordonnees
ax1.title.set_text("Signal carré filtré") 
ax1.grid(True)                                          # quadrille le graphique

## Ajout des barres de changement de valeur des variables initiales
axcolor = 'lightgoldenrodyellow'                            # couleur des barres
axN = plt.axes([0.25, 0.02, 0.65, 0.03], facecolor=axcolor)    # localisation de la barre pour N
ioN = Slider(axN,"Fréquence de coupure du filtre",-1,3,valinit=3,valstep=.1,valfmt='10^'+'%0.1f'+r'$\,\cdot f_0$')

## Definition de la fonction qui permet de reinitialiser les valeurs initiales par celle choisie Ã  la barre
def update(val):
    f1 = 10**ioN.val*f0                                             # prend la valeur de la barre pour N
    lc.set_ydata(carre_filtre(t,f1))    # ressort le nouveau profil de resonance
    lf.set_ydata(np.abs(H_vect(freqlog*f0,f1)))
    fig.canvas.draw_idle()                                  # redessine la courbe
ioN.on_changed(update)                                      # affiche Ã  cÃ´te de la barre la valeur de N

plt.show()