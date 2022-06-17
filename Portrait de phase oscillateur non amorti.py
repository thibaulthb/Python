#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 19:36:52 2022

@author: thibault
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

def simple_pendulum(theta_thetadot, t):
    theta, theta_dot = theta_thetadot
    return [theta_dot, - np.sin(theta)]



t = np.linspace(0, 5 * np.pi, 1000)

theta_init = np.linspace(0, np.pi, 20)

fig = plt.figure(figsize=(14, 6))
plt.subplots_adjust(left   = 0.1,
                    bottom = 0.1,
                    right  = 0.9,
                    top    = 0.9,
                    wspace = 0.4,
                    hspace = 0.5)
gs = fig.add_gridspec(ncols=2, nrows=1)
ax_t = fig.add_subplot(gs[0,0])
ax_p = fig.add_subplot(gs[0,1])
# axT = plt.axes([0.45, 0.8, .1, 0.03], facecolor='white')
# sl_theta0 = Slider(axT, '$T_{ini}$(K)', 0, np.pi, 10*np.pi/19, valstep=np.pi/19)  
theta_traj=18*np.pi/19

i=0
for theta_0 in theta_init:
    sol = odeint(simple_pendulum, (theta_0, 0), t).T

    ax_p.plot(sol[0,:], sol[1,:],'k-')
    
    if theta_0==theta_traj:
        ax_t.plot(t, sol[0,:],'b-',label=u"$\\theta$")
        ax_t.plot(t, sol[1,:],'r-',label=u"$\dot{\\theta}$")
        ax_p.lines[i].set_color('red')
        
    i = i+1

ax_t.set_xlabel(u'$t$ (s)', fontsize=26)
ax_t.set_ylabel(r'$\theta, \dot{\theta}$', fontsize=26)
ax_t.legend(bbox_to_anchor=(.99, .99),loc='upper right', borderaxespad=0.)

ax_t.set_xlim(0, 5*np.pi)
ax_t.set_ylim(-np.pi, np.pi)
ax_t.title.set_text('Trajectoire')

ax_p.set_xlabel(u'$\\theta$', fontsize=26)
ax_p.set_ylabel(u'$\dot{\\theta}$', fontsize=26)
ax_p.axis('equal')
ax_p.set_xlim(-np.pi, np.pi)
ax_p.set_ylim(-2, 2)
ax_p.title.set_text('diagramme de phase')

# def update(val):
#     if theta_0==sl_theta0.val:
#         sol2 = odeint(simple_pendulum, (sl_theta0.val, 0), t).T
#         ax_t.lines[0].set_ydata(sol2[0])
#         ax_t.lines[1].set_ydata(sol2[1])
#         for i in range (0,20):
#             if theta_0[i]==sl_theta0.val:
#                 j=i
#         ax_p.lines[:].set_color('black')
#         ax_p.lines[i].set_color('red')
#     plt.draw()
    
# sl_theta0.on_changed(update)

plt.show()