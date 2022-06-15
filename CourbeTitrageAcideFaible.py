import numpy as np
import numpy.polynomial.polynomial as nppol# pour le polyn�me
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker # pour le format des �tiquettes en x (remplacer le point d�cimal par la virgule)

# format vectoriel par d�faut des images
from IPython.display import set_matplotlib_formats
# Param�tres g�n�raux de pyplot
set_matplotlib_formats('svg')

# Param�tres acido-basiques
pKa=4.8
Ke=1e-14# produit ionique de l'eau
Ca = 0.12
Cb = 0.10
Va = 10.0
Vbmax=20
#------------------------------------------------------------

#r�glage perso de la grille secondaire du graphe :
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
minor_xticks = np.arange(0, 101, 1)#espaces de la grille
minor_yticks = np.arange(0, 101, 0.2)#espaces de la grille
ax.set_xticks(minor_xticks, minor=True)
ax.set_yticks(minor_yticks, minor=True)
ax.grid(which='minor', alpha=0.2)

def concentration(Vb):#Calcule [H3O+]
    Ka=10**(-pKa)
    a=Cb*Vb/(Vb+Va)+Ka# a, b et c les coefficients du polynôme
    b=Ka*(Cb*Vb-Ca*Va)/(Vb+Va)-Ke
    c=Ka*Ke
    vm = nppol.polyroots([-c,b,a,1])#chercher les racines du polyn�me
    positive=filter(lambda x: x>0,filter(np.isreal,vm))
    C=next(positive)
    return C

def titrage(Vmin,Vmax):# calcul du pH
    volume = np.linspace(Vmin, Vmax, 256,endpoint=True)
    ph=-np.log10(np.vectorize(concentration)(volume))
    return volume,ph

#---------------------------remplacer  les points décimaux par des virgules :
def func(x, pos):  # formatter function takes tick label and tick position
    s = str(x)
    ind = s.index('.')
    return s[:ind] + ',' + s[ind+1:]   # change dot to comma
x_format = ticker.FuncFormatter(func)  # make formatter
#----------------------------------------------------------------------------------------------------------

def graphique_ph(Vmin,Vmax):
    volume,ph=titrage(Vmin,Vmax)
    plt.plot(volume, ph)

plt.title("Titrage pH-m�trique d'un acide faible")
plt.xlabel(r'Volume $V_b$ de base vers� (mL)')
plt.ylabel("pH")
plt.grid()
plt.axis([0, Vbmax, 0, 14])#limites des axes
plt.yticks(np.arange(0, 14, 1))# ajuster l'espace entre valeurs axe y
plt.xticks(np.arange(0, Vbmax, 2.0))# ajuster l'espace entre valeurs axe x
#    ax.xaxis.set_major_formatter(x_format)  # appliquer le format de virgule décimale

#for pKa in [3, 5, 7]:# Si on veut montrer l'effet du pKa sur l'allure du graphe
#indenter la ligne suivante, si ligne pr�c�dente.
graphique_ph(0,Vbmax)

fig.savefig('CourbeTitrageAcideFaible.png', transparent=False, dpi=150)# Cr�ation image PNG (adapter la r�solution au r�sultat souhait�)

plt.show()
