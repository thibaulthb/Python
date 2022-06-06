#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 16:19:35 2022

@author: thibault
"""

#-----------------------------------------------------------------------
# Analyse spectrale d'un signal issu du diapason
#-----------------------------------------------------------------------

# Bibliothèques utilisées

import numpy as np
import numpy.fft as fft
import matplotlib
import matplotlib.pyplot as plt
from IPython.display import set_matplotlib_formats
from matplotlib.widgets import RadioButtons, Slider, CheckButtons   # et pour l'interface.
set_matplotlib_formats('svg')
# import matplotlib.animation as ani
# import matplotlib.widgets as mwg

from numpy import array

#-----------------------------------------------------------------------
# Charger les données à analyser
s_full=np.loadtxt(open("diapason_seul_20000.csv"), delimiter=",", skiprows=2)
#s_full=np.loadtxt(open("diapason_deux_10000.csv"), delimiter=",", skiprows=2)
# array of data
data_full=array(s_full)

# Simuler les données à analyser
# x=np.linspace(0,1,5001)
# x=x[0:5000]
# signal=np.sin(2*np.pi*440*x)*np.exp(-x/.2)
# data_full=np.vstack((x,signal)).T

# Calcul du spectre

spectre_full = fft.fft(data_full[:,1])
freq_full = fft.fftfreq(len(data_full[:,0]),data_full[1,0]-data_full[0,0])

size=len(spectre_full)
print(len(spectre_full))

freq_ech0=1/(data_full[1,0]-data_full[0,0])

# Tracés
xmin=np.floor(min(data_full[:,0]))
xmax=np.floor(max(data_full[:,0]))+1
ymin=np.floor(min(data_full[:,1])*10)/10
ymax=np.floor(max(data_full[:,1])*10)/10+.1

# Tr = np.linspace(0.0, 2.0, 2*N)
# Ampl = 20*np.log10(np.abs(Yp[:max_harm]))

# Signal

# axTmp = plt.axes([0.11, 0.6, 0.78, 0.32])


def plot_ani():
    fig = plt.figure(constrained_layout=True, figsize=(10,8))
    gs = fig.add_gridspec(ncols=10, nrows=8)
    ax0 = fig.add_subplot(gs[0:5,0:10])
    ax1 = fig.add_subplot(gs[5:8,0:6])
    
    # Création des bouttons
    
#    plt.text(0.6, 0.2, "Fréquence d'échantillonnage", transform=ax0.transAxes)
    rax = plt.axes([0.7, 0.05, 0.25, 0.3])    #Boutons radio >>> modification de l'échantillonage
    radio = RadioButtons(rax, ('$f_{ech}=$'+f'{freq_ech0:5.0f}'+'Hz','$f_{ech}=$'+f'{(freq_ech0/2):5.0f}'+'Hz','$f_{ech}=$'+f'{(freq_ech0/3):5.0f}'+'Hz','$f_{ech}=$'+f'{(freq_ech0/4):5.0f}'+'Hz','$f_{ech}=$'+f'{(freq_ech0/5):5.0f}'+'Hz',
                               '$f_{ech}=$'+f'{(freq_ech0/6):5.0f}'+'Hz','$f_{ech}=$'+f'{(freq_ech0/8):5.0f}'+'Hz','$f_{ech}=$'+f'{(freq_ech0/10):5.0f}'+'Hz','$f_{ech}=$'+f'{(freq_ech0/15):5.0f}'+'Hz',
                               '$f_{ech}=$'+f'{(freq_ech0/20):5.0f}'+'Hz','$f_{ech}=$'+f'{(freq_ech0/33):5.0f}'+'Hz','$f_{ech}=$'+f'{(freq_ech0/50):5.0f}'+'Hz','$f_{ech}=$'+f'{(freq_ech0/100):5.0f}'+'Hz'))
    ech=1
    
    
    # Tracé du signal
    ax0.set_xlim(xmin,xmax)
    ax0.set_ylim(ymin,ymax)
    ax0.plot(data_full[::ech,0],data_full[::ech,1], "b--",linewidth=.3)
    ax0.title.set_text("Signal échantillonné")
    ax0.set_ylabel("Amplitude (V)")
    ax0.set_xlabel("Temps (s)")
    # inset axes: choose position of inset axes
    axins = ax0.inset_axes([0.5, 0.7, 0.47, 0.27])
    # axins.imshow(Z2, extent=extent, origin="lower")
    # sub region of the original image
    imin=np.int_(np.floor(size*.25))
    imax=np.int_(np.floor(size*.25))+100
    x1, x2 = data_full[imin,0], data_full[imax,0]
    y1, y2 = np.floor(min(data_full[imin:imax,1])*10)/10, np.floor(max(data_full[imin:imax,1])*10)/10+.1
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)
    axins.plot(data_full[imin:imax+1:ech,0],data_full[imin:imax+1:ech,1], "b-",linewidth=.75)
    axins.plot(data_full[imin:imax+1:ech,0],data_full[imin:imax+1:ech,1], "g", linewidth=.25, marker="+")
    
    ax0.indicate_inset_zoom(axins, edgecolor="black")
    
    # Tracé du spectre
    n_split=int(np.floor(len(spectre_full)/2))
    ax1.plot(freq_full[0:n_split],np.abs(spectre_full[0:n_split]), "b-",linewidth=1.5)
    ax11 = ax1.twinx()
    ax11.plot(freq_full[0:n_split],np.abs(spectre_full[0:n_split]), "g-", linewidth=1)
    ax1.set_ylim(0,(np.floor(max(np.abs(spectre_full[:]))/20)+2)*20)
    xmin1,xmax1=ax1.get_xlim()
    ymin1,ymax1=ax1.get_ylim()
    ax11.set_ylim(0,(np.floor(max(np.abs(spectre_full[:]))/20)+2)*20)
    ax1.plot([freq_ech0/2,freq_ech0/2],[0,ymax1],'r--')
    ax1.set_xlim(xmax1*0.05,min(500,freq_ech0/2))
    ax1.text(0,ymax1*.95,"$f_{max}$="+f'{freq_full[np.argmax(np.abs(spectre_full))]:5.0f}'+'Hz',va='top',ha='left')
    ax11.set_xlim(0,min(500,freq_ech0/2))
    ax1.title.set_text("Spectre")
    ax1.set_ylabel("Amplitude")
    ax1.set_xlabel("Fréquence (Hz)")
    
    def update_echantillonnage(val):
        if radio.value_selected == '$f_{ech}=$'+f'{freq_ech0:5.0f}'+'Hz':
            ech=1
        elif radio.value_selected == '$f_{ech}=$'+f'{(freq_ech0/2):5.0f}'+'Hz':
            ech=2
        elif radio.value_selected == '$f_{ech}=$'+f'{(freq_ech0/3):5.0f}'+'Hz':
            ech=3
        elif radio.value_selected == '$f_{ech}=$'+f'{(freq_ech0/4):5.0f}'+'Hz':
            ech=4
        elif radio.value_selected == '$f_{ech}=$'+f'{(freq_ech0/5):5.0f}'+'Hz':
            ech=5
        elif radio.value_selected == '$f_{ech}=$'+f'{(freq_ech0/6):5.0f}'+'Hz':
            ech=6
        elif radio.value_selected == '$f_{ech}=$'+f'{(freq_ech0/8):5.0f}'+'Hz':
            ech=8
        elif radio.value_selected == '$f_{ech}=$'+f'{(freq_ech0/10):5.0f}'+'Hz':
            ech=10
        elif radio.value_selected == '$f_{ech}=$'+f'{(freq_ech0/15):5.0f}'+'Hz':
            ech=15
        elif radio.value_selected == '$f_{ech}=$'+f'{(freq_ech0/20):5.0f}'+'Hz':
            ech=20
        elif radio.value_selected == '$f_{ech}=$'+f'{(freq_ech0/33):5.0f}'+'Hz':
            ech=33
        elif radio.value_selected == '$f_{ech}=$'+f'{(freq_ech0/50):5.0f}'+'Hz':
            ech=50
        elif radio.value_selected == '$f_{ech}=$'+f'{(freq_ech0/100):5.0f}'+'Hz':
            ech=100
        axins.lines[1].set_data(data_full[imin:imax+1:ech,0],data_full[imin:imax+1:ech,1])
        spectre_ech = fft.fft(data_full[::ech,1])
        n_split_ech=int(np.floor(len(spectre_ech)/2))
        freq_ech = fft.fftfreq(len(data_full[::ech,0]),data_full[ech,0]-data_full[0,0])
        ax11.set_ylim(0,(np.floor(max(np.abs(spectre_ech))/20)+2)*20)
        ax11.lines[0].set_data(freq_ech[0:n_split_ech],np.abs(spectre_ech[0:n_split_ech]))
        ax1.lines[1].set_data([freq_ech0/(2*ech),freq_ech0/(2*ech)],[0,ymax1])
        ax1.texts[0].set_text("$f_{max}$="+f'{freq_ech[np.argmax(np.abs(spectre_ech))]:5.0f}'+'Hz')
        del spectre_ech,freq_ech
        
    radio.on_clicked(update_echantillonnage)
    
    
    # Afficher la figure
    plt.show()

if __name__ =='__main__':
   plot_ani()