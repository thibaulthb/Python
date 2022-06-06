#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 19:30:45 2022

@author: Thibault Hiron-Bédiée, agrégation spéciale 2022, préparation Rennes 1
"""

#-----------------------------------------------------------------------------
# Tracé d'un diagramme espace temps pour un train traversant un tunnel (LP26)
#-----------------------------------------------------------------------------

# Bibliothèques utilisées

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as anim                   # pour l'animation
from matplotlib.widgets import RadioButtons, Slider, CheckButtons   # et pour l'interface.
from matplotlib.patches import Rectangle
# format vectoriel par défaut des images
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('svg')

"""
Déclaration des classes utilisées
"""

class objet:
    def __init__(self, xA, L):
        self.LONGUEUR = L
        self.xA = xA
        self.xB = xA+L
        self.xA_INI = xA
        self.xB_INI = xA+L
        self.xA_prime = 0
        self.xB_prime = 0
        self.visuA = 0
        self.visuB = 0
        
class evenement:
    def __init__(self, x,ct):
        self.x = x
        self.ct = ct
        self.x_prime = x
        self.ct_prime = ct
        self.coords = self.Coords()
    class Coords:
        def __init__(self):
            self.x =0
            self.ct=0
            self.x_prime_x=0
            self.x_prime_ct=0
            self.ct_prime_x=0
            self.ct_prime_ct=0
            
"""
Déclaration des fonctions
"""

def initialize(beta):
    global ECH_L,ECH_T,ECH_VISU,VITESSE_LUMIERE,A1,A2,B1,B2,tunnel,train
    
    VITESSE_LUMIERE = 3e8 # (m/s)
    
    # Définition des objets
    train  = objet(   0,475) # x(queue)  =    0, L(TGV)    = 475m
    tunnel = objet(1500,400) # x(entrée) = 1000, L(tunnel) = 400m
    
    # Entrée de la queue du train dans le tunnel
    A1 = evenement(tunnel.xA_INI,calc_event(train.xA_INI,tunnel.xA_INI,beta))
    # Sortie de la queue du train du tunnel
    A2 = evenement(tunnel.xB_INI,calc_event(train.xA_INI,tunnel.xB_INI,beta))
    # Entrée de la tête du train dans le tunnel
    B1 = evenement(tunnel.xA_INI,calc_event(train.xB_INI*np.sqrt(1-beta**2),tunnel.xA_INI,beta))
    # Sortie de la tête du train du tunnel
    B2 = evenement(tunnel.xB_INI,calc_event(train.xB_INI*np.sqrt(1-beta**2),tunnel.xB_INI,beta))
    
    # Détermination de l'échelle pour ct (A1 a lieu en y=15)
    ECH_T = 15/A1.ct
    # Détermination de l'échelle pour x (le tunnel est situé entre 15 et 19)
    ECH_L = 15/tunnel.xA_INI

def calc_event(pos_mobile,pos_immobile,beta):
    
    ct = (pos_immobile-pos_mobile)/beta
    
    return ct
    

def lorentz(a,b,beta):
    
    a_prime=(a-beta*b)/np.sqrt(1-beta**2)
    
    return a_prime

def coords_ref_tunnel_obj(objet,ct,beta):
    objet.xA = lorentz(objet.xA_prime,ct,beta)
    objet.xB = lorentz(objet.xB_prime,ct,beta)
    
def coords_ref_tunnel_event(event,beta):
    event.x  = lorentz(event.x_prime ,event.ct_prime,-beta)
    event.ct = lorentz(event.ct_prime,event.x_prime ,-beta)
    
def coords_ref_train_obj(objet,ct,beta):
    objet.xA_prime = lorentz(objet.xA,ct,beta)
    objet.xB_prime = lorentz(objet.xB,ct,beta)
    
def coords_ref_train_event(event,beta):
    event.x_prime  = lorentz(event.x ,event.ct,beta)
    event.ct_prime = lorentz(event.ct,event.x ,beta)
    
def proj(event,beta,normalize):
    
    gamma=1/np.sqrt(1-beta**2)
    
    # Dans le référentiel du tunnel
    event.coords.x  = event.x *ECH_L
    event.coords.ct = event.ct*ECH_T
    # Dans le référentiel du train
    # selon x'
    event.coords.x_prime_x=gamma**2*(event.coords.x-event.coords.ct)
    event.coords.x_prime_ct=beta**2*event.coords.x_prime_x
    #selon y'
    event.coords.ct_prime_x=gamma**2*(event.coords.ct-beta**2*event.coords.x)
    event.coords.ct_prime_ct=event.coords.ct_prime_x
    
def proj_visu(ct,beta,referentiel):
    global ECH_VISU
    
    gamma=1/np.sqrt(1-beta**2)
    
    # Coordonnées du train dans le référentiel du tunnel
    if referentiel == 'Référentiel du tunnel' :
        train.xA = beta*ct*A1.ct
        train.xB = train.xA+train.LONGUEUR/gamma
        # Coordonnées du tunnel (et du train) dans le référentiel du train
        coords_ref_train_obj(tunnel, ct, beta)
        train.xA_prime = 0
        train.xB_prime = train.LONGUEUR
    if referentiel == 'Référentiel du train' :
        train.xA_prime = train.xA_INI
        train.xB_prime = train.xB_INI
        tunnel.xA_prime = tunnel.xA_INI/gamma-beta*ct*A1.ct/gamma
        tunnel.xB_prime = tunnel.xA_prime+tunnel.LONGUEUR/gamma
        # Coordonnées du tunnel (et du train) dans le référentiel du train
#        coords_ref_train_obj(tunnel, ct, beta)
#        train.xA = beta*ct*A1.ct
#        train.xB = train.xA+train.LONGUEUR/gamma
    
    if referentiel == 'Référentiel du tunnel' :
        train.visuA=train.xA*ECH_L # train en position initiale à 3 (pour moins de mouvement avec ref train)
        train.visuB=(train.xB-train.xA)*ECH_L
        tunnel.visuA=tunnel.xA*ECH_L # tunnel immobile
        tunnel.visuB=(tunnel.xB-tunnel.xA)*ECH_L
    if referentiel == 'Référentiel du train' :
        train.visuA=train.xA_prime*ECH_L # train en position initiale à 3 (pour moins de mouvement avec ref train)
        train.visuB=(train.xB_prime-train.xA_prime)*ECH_L
        tunnel.visuA=tunnel.xA_prime*ECH_L # tunnel immobile
        tunnel.visuB=(tunnel.xB_prime-tunnel.xA_prime)*ECH_L
    
"""
Fonction principale : tracé d'un diagramme de Minkovski interactif
"""


def plot_ani():
    # Tracé des axes du référentiel du tunnel
    fig = plt.figure(constrained_layout=True, figsize=(8,6))
    gs = fig.add_gridspec(ncols=8, nrows=6)
    ax0 = fig.add_subplot(gs[0:5,0:5])
    ax1 = fig.add_subplot(gs[5,0:8])
        
#    fig, ax=plt.subplots(2,1, gridspec_kw={'height_ratios': [5, 1]})
    axcolor = 'white'
    rax = plt.axes([0.62, 0.6, 0.33, 0.33])
    cb = CheckButtons(rax, ['Diagramme symétrique'],[True])
    for r in cb.rectangles:
        r.set_facecolor("blue") 
        r.set_edgecolor("k")
    axct = plt.axes([0.62, 0.68, .33, 0.03], facecolor=axcolor)
    sl_axct = Slider(axct, 'ct', 0, 2.0*0.7, valinit=0., valstep=0.01)  
    ct=sl_axct.val                       #Slider pour modifier le temps
    axv = plt.axes([0.62, 0.63, .33, 0.03], facecolor=axcolor)
    sl_axv = Slider(axv, chr(946), 0.01, 2.0*0.495, valinit=0.54, valstep=0.01) 
    beta=sl_axv.val                        #Slider pour modifier la vitesse
    ortho = cb.get_status()
    
    rax = plt.axes([0.62, 0.82, 0.33, 0.13])               #Boutons radio >>> modification du référentiel
    radio = RadioButtons(rax, ('Référentiel du tunnel', 'Référentiel du train'))
    referentiel=radio.value_selected
#    referentiel='Référentiel du train'
    
    def plot_ini():
        # Zone de tracé du diagramme
        ax0.set_xlim(xmin0, xmax0)
        ax0.set_ylim(ymin0, ymax0)
        ax0.set_frame_on(False)
        ax0.xaxis.set_visible(False)
        ax0.yaxis.set_visible(False)
    
        # Tracé des axes du référentiel du tunnel
        # Axe x
        ax0.arrow(xmin, ymin, xmax, ymin, shape='full', lw=.75, length_includes_head=True, head_width=.25, color='black')
        ax0.text(xmax, ymin+.2, "$x$", color='black', va = "bottom", ha="right")
        # Axe ct
        ax0.arrow(xmin, ymin, xmin, ymax, shape='full', lw=.75, length_includes_head=True, head_width=.25, color='black')
        ax0.text(xmin+.2, ymax, "$ct$", color='black', va = "top", ha="left")
    
        # Tracé de l'axe x' du référentiel du train
        ax0.arrow(0, 0, ymax, ymax*beta**2*normalize, shape='full', lw=.75, length_includes_head=True, head_width=.25, color='blue')
        ax0.text(ymax, ymax*beta**2*normalize+.2, "x'", color='blue', va = "bottom", ha="right")
        # Tracé de l'axe ct' du référentiel du train
        ax0.arrow(0, 0, xmax/normalize, ymax, shape='full', lw=.75, length_includes_head=True, head_width=.25, color='blue')
        ax0.text(xmax/normalize-.9, ymax, "$ct'$", color='blue', va = "top", ha="right")
        
    def visu_ini():
        # Zone de tracé de la visualisation du train et du tunnel
        ax1.set_xlim(xmin0, xmax0)
        ax1.set_ylim(ymin0, ymax0/20)
        ax1.set_frame_on(False)
        ax1.xaxis.set_visible(False)
        ax1.yaxis.set_visible(False)
        
        # Dessiner le train
        ax1.add_patch(Rectangle((train.visuA, ymin), train.visuB, ymin+1,
                     edgecolor = 'blue',
                     facecolor = 'blue',
                     fill=True,
                     lw=1))
        # Dessiner le tunnel
        ax1.add_patch(Rectangle((tunnel.visuA, ymin), tunnel.visuB, ymin+1.2,
                     edgecolor = 'red',
                     facecolor = 'red',
                     fill=False,
                     lw=1))
        
        # Tracé de l'axe horizontal
        ax1.arrow(xmin, ymin, xmax, ymin, shape='full', lw=.75, length_includes_head=True, head_width=.15, color='black')
        ax1.text(xmax-.2, ymin+.2, "$x$", color='black', va = "bottom", ha="left")
            
    def trace_event(beta,normalize):
        # Calcul des coordonnées
        proj(A1,beta,normalize)
        proj(A2,beta,normalize)
        proj(B1,beta,normalize)
        proj(B2,beta,normalize)
        
        # Marquage des événements A1, A2, B1 et B2
        ax0.plot(A1.coords.x/normalize, A1.coords.ct, marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red")
        ax0.text(A1.coords.x/normalize-.8, A1.coords.ct+.4, "$A_1$", color="red")
        ax0.plot(A2.coords.x/normalize, A2.coords.ct, marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red")
        ax0.text(A2.coords.x/normalize-.8, A2.coords.ct+.4, "$A_2$", color="red")
        ax0.plot(B1.coords.x/normalize, B1.coords.ct, marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red")
        ax0.text(B1.coords.x/normalize+.2, B1.coords.ct+.2, "$B_1$", color="red")
        ax0.plot(B2.coords.x/normalize, B2.coords.ct, marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red")
        ax0.text(B2.coords.x/normalize+.2, B2.coords.ct+.2, "$B_2$", color="red")
        # Coordonnées de A1 et B1 dans le référentiel du tunnel
        ax0.plot([A1.coords.x/normalize,A1.x*ECH_L/normalize],[ymin,A1.ct*ECH_T],'k--',linewidth=.5) # coordonnée x de A1
        ax0.plot([A2.coords.x/normalize,A2.x*ECH_L/normalize],[ymin,A2.ct*ECH_T],'k--',linewidth=.5) # coordonnée x de A2
        ax0.plot([xmin,A1.coords.x/normalize],[A1.coords.ct,A1.coords.ct],'k--',linewidth=.5) # coordonnée ct de A1
        ax0.plot([xmin,A2.coords.x/normalize],[A2.coords.ct,A2.coords.ct],'k--',linewidth=.5) # coordonnée ct de A2
        ax0.plot([xmin,B1.coords.x/normalize],[B1.coords.ct,B1.coords.ct],'k--',linewidth=.5) # coordonnée ct de B1
        ax0.plot([xmin,B2.coords.x/normalize],[B2.coords.ct,B2.coords.ct],'k--',linewidth=.5) # coordonnée ct de B2
        # Coordonnées de A1, A2, B1 et B2 dans le référentiel du train
        ax0.plot([B2.coords.x_prime_x,B2.coords.x/normalize],[B2.coords.x_prime_ct*normalize,B2.coords.ct],'b--',linewidth=.5) # coordonnée x' de B2
        ax0.plot([B1.coords.ct_prime_x/normalize,B1.coords.x/normalize],[B1.coords.ct_prime_ct,B1.coords.ct],'b--',linewidth=.5) # coordonnée ct' de B1
        ax0.plot([B2.coords.ct_prime_x/normalize,B2.coords.x/normalize],[B2.coords.ct_prime_ct,B2.coords.ct],'b--',linewidth=.5) # coordonnée ct' de B2
        # Indication de la longueur du tunnel
 #       ax0.annotate("", xytext=(A1.x, ymin-.5), xy=(B1.x, ymin-.5), 
 #                     arrowprops=dict(arrowstyle="<->",color='black',shrinkA=0,shrinkB=0))
 #       ax0.annotate( "$\Delta x$", xy=((A1.x+B1.x)/2 , ymin-.7), xytext=((A1.x+B1.x)/2 , ymin-.7) , 
 #                    va = "top", ha="center", color="black")
        # Indication de la longueur du tunnel dans le référentiel du train
 #       ax0.annotate("", xytext=(A1.x_prime, A1.x_prime*beta-.5), xy=(B1.x_prime, B1.x_prime*beta-.5), 
 #                     arrowprops=dict(arrowstyle="<->",color='blue',shrinkA=0,shrinkB=0))
 #       ax0.annotate( "$\Delta x'$", xy=((A1.x_prime+B1.x_prime)/2 , (A1.x_prime+B1.x_prime)*beta/2-.7),
 #                      xytext=((A1.x_prime+B1.x_prime)/2 , (A1.x_prime+B1.x_prime)*beta/2-.7) , 
 #                    va = "top", ha="center", color="blue")
        if referentiel == "Référentiel du tunnel":
            ax0.plot([xmin,xmax],[ct*A1.coords.ct,ct*A1.coords.ct],'g-',linewidth=.5) # droite du temps
        if referentiel == "Référentiel du train":
            ax0.plot([ct*A1.coords.ct_prime_x,xmax],[ct*A1.coords.ct_prime_ct,(xmax-ct*A1.coords.ct_prime_x)*beta**2+ct*A1.coords.ct_prime_ct],'g-',linewidth=.5) # droite du temps
        
    def plot_visu(referentiel):
        # Déplacer le train
        ax1.patches[0].set_x(train.visuA)
        # Déplacer le tunnel
        ax1.patches[0].set_x(tunnel.visuA)

    def update_ct(val): 
        ct = sl_axct.val
        beta = sl_axv.val
        gamma = 1/np.sqrt(1-beta**2)
        referentiel=radio.value_selected
        # Normalisation (passage d'ortho à ct'=x)
        if cb.get_status() == [True]:
            normalize=1/beta
        else:
            normalize=1
        if referentiel == "Référentiel du tunnel": # droite du temps et déplacement
            train.visuA=beta*ct*A1.ct*ECH_L
            ax0.lines[13].set_data([xmin,xmax],[ct*A1.coords.ct,ct*A1.coords.ct])
        if referentiel == "Référentiel du train": # droite du temps et déplacement
            tunnel.visuA=(tunnel.xA_INI/gamma-beta*ct*A1.ct/gamma)*ECH_L
            ax0.lines[13].set_data([ct*A1.coords.ct_prime_x/normalize,xmax],[ct*A1.coords.ct_prime_ct,(xmax-ct*A1.coords.ct_prime_x/normalize)*beta**2*normalize+ct*A1.coords.ct_prime_ct])        
        ax1.patches[0].set_x(train.visuA)
        ax1.patches[1].set_x(tunnel.visuA)
        
    def update_v(val):
        global ECH_T
        sl_axct.set_val(0)
        ct = sl_axct.val
        beta = sl_axv.val
        referentiel=radio.value_selected
        # Normalisation (passage d'ortho à ct'=x)
        if cb.get_status() == [True]:
            normalize=1/beta
        else:
            normalize=1
        
        ax0.patches[2].set_xy([(xmin,ymin),(xmax,ymax*beta**2*normalize)])
        ax0.texts[2].set_position((xmax,ymax*beta**2*normalize+.2))
        ax0.patches[3].set_xy([(xmin,ymin),(xmax/normalize,ymax)])
        ax0.texts[3].set_position((xmax/normalize,ymax+.2))
        # Recalcul des événements
        A1 = evenement(tunnel.xA_INI,calc_event(train.xA_INI,tunnel.xA_INI,beta))
        ECH_T = 15/A1.ct
        proj(A1,beta,normalize)
        B1 = evenement(tunnel.xA_INI,calc_event(train.xB_INI*np.sqrt(1-beta**2),tunnel.xA_INI,beta))
        proj(B1,beta,normalize)
        B2 = evenement(tunnel.xB_INI,calc_event(train.xB_INI*np.sqrt(1-beta**2),tunnel.xB_INI,beta))
        proj(B2,beta,normalize)
        # Modification du graphique
        ax0.lines[0].set_data([A1.coords.x/normalize, A1.coords.ct])
        ax0.texts[4].set_position((A1.coords.x/normalize+.2, A1.coords.ct))
        ax0.lines[1].set_data([A2.coords.x/normalize, A2.coords.ct])
        ax0.texts[5].set_position((A2.coords.x/normalize+.2, A2.coords.ct))
        ax0.lines[2].set_data([B1.coords.x/normalize, B1.coords.ct])
        ax0.texts[6].set_position((B1.coords.x/normalize+.2, B1.coords.ct))
        ax0.lines[3].set_data([B2.coords.x/normalize, B2.coords.ct])
        ax0.texts[7].set_position((B2.coords.x/normalize+.2, B2.coords.ct))
        ax0.lines[4].set_data([A1.coords.x/normalize,A1.coords.x/normalize],[ymin,A1.coords.ct])
        ax0.lines[5].set_data([A2.coords.x/normalize,A2.coords.x/normalize],[ymin,A2.coords.ct])
        ax0.lines[6].set_data([xmin,A1.coords.x/normalize],[A1.coords.ct,A1.coords.ct])
        ax0.lines[7].set_data([xmin,A2.coords.x/normalize],[A2.coords.ct,A2.coords.ct])
        ax0.lines[8].set_data([xmin,B1.coords.x/normalize],[B1.coords.ct,B1.coords.ct])
        ax0.lines[9].set_data([xmin,B2.coords.x/normalize],[B2.coords.ct,B2.coords.ct])
        ax0.lines[10].set_data([B2.coords.x_prime_x/normalize,B2.coords.x/normalize],[B2.coords.x_prime_ct,B2.coords.ct])
        ax0.lines[11].set_data([B1.coords.ct_prime_x/normalize,B1.coords.x/normalize],[B1.coords.ct_prime_ct,B1.coords.ct])
        ax0.lines[12].set_data([B2.coords.ct_prime_x/normalize,B2.coords.x/normalize],[B2.coords.ct_prime_ct,B2.coords.ct])

        proj_visu(ct, beta, referentiel)
        if referentiel == "Référentiel du tunnel":
            ax1.patches[0].set_bounds(train.visuA, ymin, train.visuB,1)
        if referentiel == "Référentiel du train":
            ax1.patches[1].set_bounds(tunnel.visuA, ymin, tunnel.visuB,1.2)
        
    def update_ref(label):
        beta = sl_axv.val
        gamma=1/np.sqrt(1-beta**2)
        referentiel= radio.value_selected
        if referentiel == "Référentiel du tunnel": # droite du temps
            train.visuA=beta*ct*A1.ct*ECH_L # train en position initiale à 3 (pour moins de mouvement avec ref train)
            tunnel.visuA=tunnel.xA_INI*ECH_L
            ax1.patches[0].set_bounds(train.visuA, ymin, train.LONGUEUR/gamma*ECH_L,1)
            ax1.patches[1].set_bounds(tunnel.visuA, ymin, tunnel.LONGUEUR*ECH_L,1.2)
            ax1.texts[0].set_text("$x$")
            ax1.patches[2].set_color("black")
            ax1.texts[0].set_color("black")
            sl_axct.label.set_text("ct")
            sl_axct.label.set_color("black")
        if referentiel == "Référentiel du train": # droite du temps
            train.visuA=train.xA_INI*ECH_L
            tunnel.visuA=(tunnel.xA_INI/gamma-beta*ct*A1.ct/gamma)*ECH_L
            ax1.patches[0].set_bounds(train.visuA, ymin, train.LONGUEUR*ECH_L,1)
            ax1.patches[1].set_bounds(tunnel.visuA, ymin, tunnel.LONGUEUR/gamma*ECH_L,1.2)
            ax1.texts[0].set_text("$x'$")
            ax1.patches[2].set_color("blue")
            ax1.texts[0].set_color("blue")
            sl_axct.label.set_text("ct'")
            sl_axct.label.set_color("blue")
        sl_axct.set_val(0)
        update_ct(0)

    
    """
    Initialisation
    """
    
    # Coordonnées du graphe (référentiel du tunnel)
    xmin=0
    ymin=0
    xmax=22
    ymax=22
    # Coordonnées avec les marges
    margin=1
    xmin0=xmin-margin
    ymin0=ymin-margin
    xmax0=xmax+margin
    ymax0=ymax+margin
    
    # Création des événements
    global A1,A2,B1,B2
    if cb.get_status()==[True]:
        normalize=1/beta
        print('here')
    else:
        normalize=1
        
    initialize(beta)
    plot_ini()
    trace_event(beta,normalize)
    proj_visu(ct, beta, referentiel)
    visu_ini()
    
    sl_axct.on_changed(update_ct)
    sl_axv.on_changed(update_v)
    radio.on_clicked(update_ref)
    cb.on_clicked(update_v)
   
    # Tracé de la figure
    plt.show()

if __name__ =='__main__':
   plot_ani()