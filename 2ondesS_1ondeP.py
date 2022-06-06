#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ugo Hincelin - Novembre 2016
Animation pour montrer que deux ondes stationnaires peuvent donner une onde progressive.
Remarque :
Pour ne pas crÃ©er un fichier gif et visualiser directement l'animation dans la fenÃªtre graphique de pyzo, commenter la ligne plt.savefig(filename) dans la boucle for et le bloc "convert" Ã  la fin du code.
"""

import numpy as np
import pylab as plt
import os

plt.close("all")

Am = 1
omega = 1
t = 0
k = 1
phi = 0
psi = 0
x = np.linspace(0,100,1000)

for t in range(1000):
    t = t/10
    a = Am*np.cos(omega*t+phi)*np.cos(k*x+psi)
    b = Am*np.cos(omega*t+phi+np.pi/2)*np.cos(k*x+psi+np.pi/2)
    c = a + b
    plt.plot(x,a,'-')
    plt.plot(x,b,'-')
    plt.plot(x,c,'o-')
    plt.xlabel("position x")
    plt.ylabel("vibration")
    plt.xlim(40,60)
    plt.ylim(-1.5,1.5)
    i = t*10
    filename = 'fichierTemp'+str('%02d' %i)+'.pdf'
#    plt.savefig(filename)
    plt.show()
    plt.pause(0.01)
    plt.clf()
    
# convert est une fonction d'ImageMagick : option -delay en 1/100 de seconde
#cmd = 'convert fichierTemp*.pdf 2ondesS_ondeP.gif'
#os.system(cmd)
#os.system('rm fichierTemp*.pdf')