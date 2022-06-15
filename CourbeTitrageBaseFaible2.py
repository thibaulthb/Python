import numpy as np
import numpy.polynomial.polynomial as nppol# pour le polynôme
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker # pour le format des étiquettes en x (remplacer le point décimal par la virgule)

# format vectoriel par défaut des images
from IPython.display import set_matplotlib_formats
# Paramètres généraux de pyplot
set_matplotlib_formats('svg')

# Paramètres acido-basiques
pKa=9.2
Ke=1e-14# produit ionique de l'eau
Cb = 0.12
Ca = 0.10
Vb = 10.0
Vamax=20
#------------------------------------------------------------

#réglage perso de la grille secondaire du graphe :
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
minor_xticks = np.arange(0, 101, 1)#espaces de la grille
minor_yticks = np.arange(0, 101, 0.2)#espaces de la grille
ax.set_xticks(minor_xticks, minor=True)
ax.set_yticks(minor_yticks, minor=True)
ax.grid(which='minor', alpha=0.2)

def concentration(Va):#Calcule [H3O+]
    Ka=10**(-pKa)
    Kb=Ke/Ka
    a=Ca*Va/(Vb+Va)+Kb# a, b et c les coefficients du polynôme
    b=Kb*(Ca*Va-Cb*Vb)/(Vb+Va)-Ke
    c=Kb*Ke
    vm = nppol.polyroots([-c,b,a,1])#chercher les racines du polynôme
    positive=filter(lambda x: x>0,filter(np.isreal,vm))
    C=next(positive)
    return C

def titrage(Vmin,Vmax):# calcul du pH
    volume = np.linspace(Vmin, Vmax, 256,endpoint=True)
    ph=14+np.log10(np.vectorize(concentration)(volume))
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

plt.title("Titrage pH-métrique d'une base faible")
plt.xlabel(r"Volume $V_a$ d'acide versé (mL)")
plt.ylabel("pH")
plt.grid()
plt.axis([0, Vamax, 0, 14])#limites des axes
plt.yticks(np.arange(0, 14, 1))# ajuster l'espace entre valeurs axe y
plt.xticks(np.arange(0, Vamax, 2.0))# ajuster l'espace entre valeurs axe x
#    ax.xaxis.set_major_formatter(x_format)  # appliquer le format de virgule décimale

#for pKa in [10, 9, 8]:# Si on veut montrer l'effet du pKa sur l'allure du graphe
#indenter la ligne suivante, si ligne précédente.
graphique_ph(0,Vamax)

fig.savefig('CourbeTitrageBaseFaible.png', transparent=False, dpi=150)# Création image PNG (adapter la résolution au résultat souhaité)

plt.show()
