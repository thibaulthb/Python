#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 31 10:09:14 2022

@author: Thibault Hiron-Bédiée, agrégation spéciale 2022, préparation Rennes 1
"""

#-----------------------------------------------------------------------------
# Tracé d'un diagramme espace temps pour un train traversant un tunnel (LP26)
#-----------------------------------------------------------------------------

# Bibliothèques utilisées

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as anim                   # pour l'animation
from matplotlib.widgets import RadioButtons, Slider, Button   # et pour l'interface.
from matplotlib.patches import Rectangle
# format vectoriel par défaut des images
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('svg')

"""
Déclaration des classes utilisées
"""
            
"""
Déclaration des fonctions
"""
    
"""
Fonction principale : tracé d'un diagramme de Minkovski interactif
"""

# Tracé des axes du référentiel du tunnel
fig = plt.figure(constrained_layout=True, figsize=(8,5))
gs = fig.add_gridspec(ncols=8, nrows=6)
ax0 = fig.add_subplot(gs[0:5,0:5])
ax1 = fig.add_subplot(gs[1:4,5:8])
    
#    fig, ax=plt.subplots(2,1, gridspec_kw={'height_ratios': [5, 1]})
axcolor = 'white'
axN = plt.axes([0.62, .95, .33, 0.03], facecolor=axcolor)
sl_axN = Slider(axN, 'N', 1, 2*6+1, valinit=1, valstep=2)  
N=sl_axN.val                       #Slider pour modifier le nombre d'encoches
axtheta = plt.axes([0.62, 0.9, .33, 0.03], facecolor=axcolor)
sl_axtheta = Slider(axtheta, r'$\alpha_{var}$', 0.9, 1.1, valinit=1, valstep=0.01)
axt = plt.axes([0.62, 0.85, .33, 0.03], facecolor=axcolor)
sl_axt = Slider(axt, '$t/T$', 0, 1, valinit=0, valstep=0.01)
axprev = plt.axes([0.6,0.18,0.25,0.05])
button = Button(axprev,'Configuration monophasée')
axprev = plt.axes([0.6,0.12,0.25,0.05])
button2 = Button(axprev,'Montrer champ entrefer')
axprev = plt.axes([0.86,0.12,0.11,0.11])
button3 = Button(axprev,'Start\n anim')

def plot_ini():
    # Zone de tracé du diagramme
    ax0.set_xlim(xmin0, xmax0)
    ax0.set_ylim(ymin0, ymax0)
    ax0.set_frame_on(False)
    ax0.xaxis.set_visible(False)
    ax0.yaxis.set_visible(False)

    # Tracé des axes du référentiel du tunnel
    # Axe x
    ax0.arrow(xmin-.4, 0,xmax-xmin+.8, 0, shape='full', lw=.75, length_includes_head=True, head_width=.25, color='black')
    ax0.text(xmax+.4, .2, r'$\theta$', color='black', va = "bottom", ha="right")
    # Axe B
    ax0.arrow(0, ymin-.4, 0, ymax-ymin+1.2, shape='full', lw=.75, length_includes_head=True, head_width=.25, color='black')
    ax0.text(.2, ymax+.8, "$B_{entrefer}$", color='black', va = "top", ha="left")

def visu_plot(N,theta0):
    ax1.clear()
    # Zone de tracé de la visualisation du train et du tunnel
    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-2, 2)
    ax1.set_frame_on(False)
    ax1.xaxis.set_visible(False)
    ax1.yaxis.set_visible(False)
    ax1.set_aspect('equal')
    
    ax1.text(-.7,-2.25, r'$\theta_{max}=$'+f'{0:3.1f}'+'°', color='black', va = "top", ha="left")

    
    # Dessiner le stator
    stator1 = plt.Circle((0, 0), 2, color='grey', fill=True)
    stator2 = plt.Circle((0, 0), 1.5, color='white', fill=True)
    ax1.add_patch(stator1)
    ax1.add_patch(stator2)
    
    # Dessiner le rotor
    rotor = plt.Circle((0, 0), 1, color='grey', fill=True)
    ax1.add_patch(rotor)
    
    # Dessiner les encoches bobinage 1
    # Encoches supérieures
    encochecolor='k'
    for i in range (0,N):
        angleN=(i-(N-1)/2)*theta0+np.pi/2
        cost=np.cos(angleN)
        sint=np.sin(angleN)
        rectl=np.sqrt(1.5**2+.1**2)
        encoche1=patches.Rectangle((1.5*cost+.1*sint,1.5*sint-.1*cost),0.2,0.2,color='white',angle=angleN*180/np.pi)
        ax1.add_patch(encoche1)
        fil1=patches.Circle((1.63*cost,1.63*sint),radius=0.1,color=encochecolor,linewidth=0.5,fill=False)
        fil2=patches.Circle((1.63*cost,1.63*sint),radius=0.03,color=encochecolor,fill=True)
        ax1.add_patch(fil1)
        ax1.add_patch(fil2)
    # Encoches inférieures
    for i in range (0,N):
        angleN=(i-(N-1)/2)*theta0-np.pi/2
        cost=np.cos(angleN)
        sint=np.sin(angleN)
        rectl=np.sqrt(1.5**2+.1**2)
        encoche1=patches.Rectangle((1.5*cost+.1*sint,1.5*sint-.1*cost),0.2,0.2,color='white',angle=angleN*180/np.pi)
        ax1.add_patch(encoche1)
        fil1=patches.Circle((1.63*cost,1.63*sint),radius=0.1,color=encochecolor,linewidth=0.5,fill=False)
        fil2=patches.Circle((1.63*cost,1.63*sint),radius=0.03,color=encochecolor,fill=True)
        ax1.add_patch(fil1)        
        ax1.plot([1.53*cost, 1.73*cost], [1.53*sint, 1.73*sint], color=encochecolor, linewidth=0.5)
        ax1.plot([1.63*cost-.1*sint, 1.63*cost+.1*sint], [1.63*sint+.1*cost, 1.63*sint-.1*cost], color=encochecolor, linewidth=0.5)
    # Dessiner les encoches bobinage 2
    if button.label.get_text() == 'Configuration diphasée':
    # Encoches supérieures
        encochecolor='r'
        for i in range (0,N):
            angleN=(i-(N-1)/2)*theta0
            cost=np.cos(angleN)
            sint=np.sin(angleN)
            rectl=np.sqrt(1.5**2+.1**2)
            encoche1=patches.Rectangle((1.5*cost+.1*sint,1.5*sint-.1*cost),0.2,0.2,color='white',angle=angleN*180/np.pi)
            ax1.add_patch(encoche1)
            fil1=patches.Circle((1.63*cost,1.63*sint),radius=0.1,color=encochecolor,linewidth=0.5,fill=False)
            fil2=patches.Circle((1.63*cost,1.63*sint),radius=0.03,color=encochecolor,fill=True)
            ax1.add_patch(fil1)
            ax1.add_patch(fil2)
        # Encoches inférieures
        for i in range (0,N):
            angleN=(i-(N-1)/2)*theta0-np.pi
            cost=np.cos(angleN)
            sint=np.sin(angleN)
            rectl=np.sqrt(1.5**2+.1**2)
            encoche1=patches.Rectangle((1.5*cost+.1*sint,1.5*sint-.1*cost),0.2,0.2,color='white',angle=angleN*180/np.pi)
            ax1.add_patch(encoche1)
            fil1=patches.Circle((1.63*cost,1.63*sint),radius=0.1,color=encochecolor,linewidth=0.5,fill=False)
            fil2=patches.Circle((1.63*cost,1.63*sint),radius=0.03,color=encochecolor,fill=True)
            ax1.add_patch(fil1)        
            ax1.plot([1.53*cost, 1.73*cost], [1.53*sint, 1.73*sint], color=encochecolor, linewidth=0.5)
            ax1.plot([1.63*cost-.1*sint, 1.63*cost+.1*sint], [1.63*sint+.1*cost, 1.63*sint-.1*cost], color=encochecolor, linewidth=0.5)
    
  
def champ_1(theta,theta0,t):
    if button.label.get_text() == 'Configuration monophasée':
        x= theta-theta0
        for i in range (0,300):
            if x[i]<-3.5*np.pi or x[i]>-2.5*np.pi and x[i]<-1.5*np.pi or x[i]>-np.pi/2 and x[i]<np.pi/2 or x[i]> 1.5*np.pi and x[i] < 2.5*np.pi or x[i] > 3.5*np.pi:
                x[i]=5*np.cos(2*np.pi*t)
            else:
                x[i]=-5*np.cos(2*np.pi*t)
    else:
        x= theta-theta0-2*np.pi*t
        for i in range (0,300):
            if x[i]<-3.5*np.pi or x[i]>-2.5*np.pi and x[i]<-1.5*np.pi or x[i]>-np.pi/2 and x[i]<np.pi/2 or x[i]> 1.5*np.pi and x[i] < 2.5*np.pi or x[i] > 3.5*np.pi:
                x[i]=5
            else:
                x[i]=-5
    return x
    
def champ_N(theta,N,theta0,t):
    val=0
    for i in range (0,N):
        val=val+champ_1(theta,(i-(N-1)/2)*theta0,t)/(N)
    return val

def trace_champ_entrefer(t):
    if button2.label.get_text() == 'Cacher champ entrefer':
        for i in range (0,32):
            cosi=np.cos((i-7)*np.pi/16)
            sini=np.sin((i-7)*np.pi/16)
            if button.label.get_text() == 'Configuration monophasée':
                cost=np.cos((i-7)*np.pi/16)*np.cos(2*np.pi*t)
                sint=np.sin((i-7)*np.pi/16)*np.cos(2*np.pi*t)
            else:
                cost=np.cos((i-7)*np.pi/16-2*np.pi*t)
                sint=np.sin((i-7)*np.pi/16-2*np.pi*t)
            ax1.arrow(1.25*cosi, 1.25*sini,(.4*cost)*cosi, (.4*cost)*sini, shape='full', lw=.75, length_includes_head=False, head_width=.05, color='black')
        if button.label.get_text() == 'Configuration monophasée':
            ax1.arrow(-.7*np.cos(2*np.pi*t), 0,1.8*np.cos(2*np.pi*t), 0, shape='full', lw=1.3, length_includes_head=True, head_width=.3, color='blue')
            ax1.texts[0].set_text(r'$\theta_{max}=$'+f'{(np.sign(np.cos(2*np.pi*t))-1)*90:3.1f}'+'°')
        else:
            ax1.arrow(-.7*np.cos(2*np.pi*t), -.7*np.sin(2*np.pi*t),1.8*np.cos(2*np.pi*t), 1.8*np.sin(2*np.pi*t), shape='full', lw=1.3, length_includes_head=True, head_width=.3, color='blue')
            ax1.texts[0].set_text(r'$\theta_{max}=$'+f'{360*t:3.1f}'+'°')
  
def trace_champ(N,theta0,t):
    # Calcul des coordonnées
    x=np.linspace(xmin,xmax,300)
    ax0.plot(x,5*np.cos(x),'r-')
    ax0.plot(x,champ_N(x,N,theta0,t),'b-')
 
def update(val): 
    N = sl_axN.val
    t=sl_axt.val
    theta0=2.63/(N+1)*sl_axtheta.val
    if N==1:
        theta0=0
    x=np.linspace(xmin,xmax,300)
    visu_plot(N,theta0)
    if button.label.get_text() == 'Configuration monophasée':
        ax0.lines[1].set_data(x,champ_N(x,N,theta0,t))
        ax0.lines[0].set_data(x,5*np.cos(x)*np.cos(2*np.pi*t))
    else:
        ax0.lines[0].set_data(x,5*np.cos(x-2*np.pi*t))
    trace_champ_entrefer(t)
    
def update_t(val): 
    N = sl_axN.val
    t=sl_axt.val
    theta0=2.63/(N+1)*sl_axtheta.val
    if N==1:
        theta0=0
    x=np.linspace(xmin,xmax,300)
    ax0.lines[1].set_data(x,champ_N(x,N,theta0,t))
    if button.label.get_text() == 'Configuration monophasée':
        ax0.lines[0].set_data(x,5*np.cos(x)*np.cos(2*np.pi*t))
        ax1.patches[3+5*N:].remove()
    else:
        ax0.lines[0].set_data(x,5*np.cos(x-2*np.pi*t))
        ax1.patches[3+10*N:].remove()
    trace_champ_entrefer(t)
    
def change_phase(val):
    if button.label.get_text() == 'Configuration monophasée':
        ax0.lines[1].remove()
        button.label.set_text('Configuration diphasée')
    else:
        ax0.plot([0,0],[0,0],'b-')
        button.label.set_text('Configuration monophasée')
    sl_axN.set_val(1)
    update(0)
    
def show_entrefer(val):
    if button2.label.get_text() == 'Montrer champ entrefer':
        button2.label.set_text('Cacher champ entrefer')
    else:
        button2.label.set_text('Montrer champ entrefer')
    sl_axN.set_val(1)
    update(0)
    
def anim_status(val):
    if button3.label.get_text() == 'Start\n anim':
        button3.label.set_text('Stop\n anim')
    else:
        button3.label.set_text('Start\n anim')
    sl_axN.set_val(1)
    update(0)

"""
Initialisation
"""

# Coordonnées du graphe (référentiel du tunnel)
xmin=-5
ymin=-5
xmax=5
ymax=5
# Coordonnées avec les marges
margin=1
xmin0=xmin-margin
ymin0=ymin-margin
xmax0=xmax+margin
ymax0=ymax+margin
    
plot_ini()
N=sl_axN.val
t=sl_axt.val
theta0=2.63/(N+1)*sl_axtheta.val
if N==1:
    theta0=0
visu_plot(N,theta0)
trace_champ(N,theta0,t)
# trace_event(beta,normalize)
# proj_visu(ct, beta, referentiel)

sl_axN.on_changed(update)
sl_axtheta.on_changed(update)
sl_axt.on_changed(update)
button.on_clicked(change_phase)
button2.on_clicked(show_entrefer)
button3.on_clicked(anim_status)
"""
fonction animate : C'est elle qui permet l'animation du champ dans l'entrefer'
"""

def animate(i):
    t=i/25-np.floor(i/25)
    if button3.label.get_text() == 'Stop\n anim':
        sl_axt.set_val(t)
        update(0)

ani = anim.FuncAnimation(fig, animate, 400) #pour lancer l'animation
 
plt.show()