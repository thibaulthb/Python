import numpy as np
import numpy.polynomial.polynomial as nppol# pour le polynôme
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker # pour le format des étiquettes en x (remplacer le point décimal par la virgule)

# format vectoriel par défaut des images
from IPython.display import set_matplotlib_formats
# Paramètres généraux de pyplot
set_matplotlib_formats('svg')

# Paramètres acido-basiques
pKa1=10
pKa2=4
Ke=1e-14# produit ionique de l'eau
C1 = 0.2
C2 = 0.10
V1 = 5.0
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

def concentration(V2):#Calcule [H3O+]
    Ka1=10**(-pKa1)
    Kb1=Ke/Ka1
    Ka2=10**(-pKa2)
    Kb2=Ke/Ka2
    K=Ka2/Ka1
    C1_prime=C1*V1/(V1+V2)
    C2_prime=C2*V2/(V1+V2)
    alpha=np.sqrt(Kb1/C1_prime)
    a=(1-K)# a, b et c les coefficients du polynôme
    b=alpha*C1_prime+K*(C1_prime+C2_prime)
    c=-K*C1_prime*C2_prime
#    vm = nppol.polyroots([-c,b,a,1])#chercher les racines du polynôme
#    print(vm)
#    positive=filter(lambda x: x>0,filter(np.isreal,vm))
#    C=Kb*next(positive)/(Cb_prime-next(positive))
    x=(-b+np.sqrt(b**2-4*a*c))/(2*a)
    h=Ka1*(alpha*C1_prime+x)/(C1_prime-x)
    return h

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

plt.title("Titrage pH-métrique d'une base faible par un acide faible")
plt.xlabel(r"Volume $V_2$ de titrant versé (mL)")
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
