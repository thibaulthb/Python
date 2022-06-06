#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 17:05:42 2022

@author: thibault
"""


## Importation des bibliotheques
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from numpy import pi

## Creation de la fenetre

fig, ax = plt.subplots(figsize=(8,5))
plt.subplots_adjust(bottom=0.25,left=0.1,right=.7)         # dimensions du graphique

t = np.arange(-1, 2, 0.001)    # temps allant de -2 s Ã  4s par pas de 0.01s (sur trois periodes)
t1 = np.linspace(-1,2,151)
# Creation de la courbe initiale (avec la serie de Fourier Ã  un terme)
def quantifie(f,N):
    return np.floor(f*N)/N
quant_vect=np.vectorize(quantifie)

def filtrePB(E,s0,omegac,Te,mode):
    x = omegac*Te
    if mode == 'Dérivation':
        a0 = x/(1+x)
        b1 = 1/(1+x)
    elif mode == 'Intégration':
        a0 = x/(2+x)
        a1 = a0
        b1 = (2-x)/(2+x)
    n=len(E)
    S = np.zeros(n)
    S[0]  =s0
    for k in range(1,n):
        if mode == 'Dérivation':
            S[k] = a0*E[k] + b1*S[k-1]
        elif mode == 'Intégration':
            S[k] = a0*E[k] +a1*E[k-1] + b1*S[k-1]
    return S

def H(f,f1):
    return 1/complex(1,f/f1)
H_vect=np.vectorize(H)

N0=0                                                # initialisation Ã  1 le nombre de composantes de la serie de Fourier
l, = plt.plot(t, np.sin(2*pi*t), lw=1, color='red',label="Signal d'entrée")         # courbe Ã  tracer i en fonction de omega
lq, = plt.step(t1,quant_vect(np.sin(2*pi*t1),2048), lw=.8, color='blue',where='post',label="Signal numérisé")
lfa, = plt.plot(t,np.sin(2*pi*t+np.angle(H_vect(1,1)))*np.abs(H_vect(1,1)),lw=1,color="green",label="Filtrage analogique")
lfn, = plt.step(t1,filtrePB(quant_vect(np.sin(2*pi*t1),2048),0,2*pi,1/50,'Dérivation'),lw=.8,color="orange", where='post',label="Filtrage numérique")
leg = plt.legend(handles=[l,lq,lfa,lfn],bbox_to_anchor=(1.05, .5),
                         loc='center left', borderaxespad=0.)
lfa.set_visible(not lfa.get_visible())
lfn.set_visible(not lfn.get_visible())
plt.axis([-1, 2, -1.2, 1.2])                     # limite des axes (xmin,xmax,ymin,ymax)
plt.xlabel("Temps (s)")                     # titre de l'axe des abscisses
plt.ylabel("Amplitude du signal (V)")                               # titre de l'axe des ordonnees
plt.title("Numérisation d'un signal") 
plt.grid(True)                                          # quadrille le graphique

#print(filtrePB(quant_vect(np.sin(2*pi*t1),2048),0,1,8))

## Ajout des barres de changement de valeur des variables initiales
axcolor = 'lightgoldenrodyellow'                            # couleur des barres
axN = plt.axes([0.15, 0.1, 0.55, 0.03], facecolor=axcolor)    # localisation de la barre pour N
ioN = Slider(axN,"Niveaux/V",0,11,valinit=11,valstep=1,valfmt='2^'+'%0.0f')
axf = plt.axes([0.15, 0.06, 0.55, 0.03], facecolor=axcolor)    # localisation de la barre pour N
iof = Slider(axf,"Échantillons/s",1,50,valinit=50,valstep=.1,valfmt='%0.1f')
axfc = plt.axes([0.15, 0.02, 0.55, 0.03], facecolor=axcolor,visible=False)    # localisation de la barre pour N
iofc = Slider(axfc,r"$\omega_c/\omega$",-1,1,valinit=0,valstep=.1,valfmt='10^'+'%0.1f')
rax = plt.axes([.75, 0.35, 0.2, 0.1],visible=False)               #Boutons radio >>> modification du référentiel
radio = RadioButtons(rax, ('Dérivation', 'Intégration'))


## Definition de la fonction qui permet de reinitialiser les valeurs initiales par celle choisie Ã  la barre
def update(val):
    N = 2**ioN.val
    ech = iof.val                                           # prend la valeur de la barre pour N
    t1 = np.arange(-1,2,1/ech)
    lq.set_data(t1,quant_vect(np.sin(2*pi*t1),N))    # ressort le nouveau profil de resonance
    lfa.set_ydata(np.sin(2*pi*t+np.angle(H_vect(1,10**iofc.val)))*np.abs(H_vect(1,10**iofc.val)))
    lfn.set_data(t1,filtrePB(quant_vect(np.sin(2*pi*t1),N),0,2*pi*10**iofc.val,1/ech,radio.value_selected))
    fig.canvas.draw_idle()                                  # redessine la courbe


ioN.on_changed(update)                                      # affiche Ã  cÃ´te de la barre la valeur de N
iof.on_changed(update)                                      # affiche Ã  cÃ´te de la barre la valeur de N
iofc.on_changed(update)                                      # affiche Ã  cÃ´te de la barre la valeur de N
radio.on_clicked(update)

## Definition d'un bouton reset
resetax = plt.axes([.75, 0.8, 0.2, 0.05])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
filtrerax = plt.axes([.75, 0.73, 0.2, 0.05])
button2 = Button(filtrerax, 'Filtrer', color=axcolor, hovercolor='0.975')
    
def reset(event):
    ioN.reset()
    iof.reset()
    iofc.reset()
button.on_clicked(reset)

def filtrer(event):
    lq.set_visible(not lq.get_visible())
    lfa.set_visible(not lfa.get_visible())
    lfn.set_visible(not lfn.get_visible())
    axfc.set_visible(not axfc.get_visible())
    rax.set_visible(not rax.get_visible())
button2.on_clicked(filtrer)

plt.show()