"""
Auteur : Hanssens Dimitri
Date : mars 2021
"""

import Geometry as gm
import Read_XML as xml
import Transfert as tf
import Optimisation as opti
import numpy as np
import matplotlib.pyplot as plt

# Définitions de fonctions main :

def divide(lst, k):
    """
    Renvoie un élément sur <k> des éléments de la liste appelée en paramètre
    """
    res = []
    for i in range(0, len(lst), k):
        res.append(lst[i])
    return res


def amplitude(x,y,c,d):
    """
    Borne le signal envoyé en paramètre entre les valeurs -c et c
    """
    X = []
    Y = []
    a = max(x)
    b = max(y)
    n = 1
    if a > ampli_max:
        n = a/ampli_max
    if b > ampli_max and b > a:
        n = b/ampli_max
    for i in range(len(x)):
        X.append(x[i]/(n*c))
        Y.append(y[i]/(n*d))
    return X,Y


def ajustement(lst):
    """
    Ajuste le signal envoyé en paramètre en tranchant les valeurs supérieures à 1 en valeur absolue
    Renvoie un signal borné entre -1 et 1
    """
    res = []
    for elem in lst:
        if elem > 1:
            res.append(1)
        elif elem < -1:
            res.append(-1)
        else:
            res.append(elem)
    return res


# Constantes globales

freq_laser = 44100
duree_param = 0.1 # Durée définie arbitrairement (La fréquence d'envoi doit être un multiple de 10)
duree_anim = 10    # Durée définie arbitrairement (max : 10 s)
duree_complexe = 0.07 # Durée définie expérimentalement pour obtenir un image complète dans la majorité des cas
k = 1.005         # Coefficient défini arbitrairement selon la rapidité de l'animation

# Paramètres des galvanomètres
wo_h = 118.03 * (2 * np.pi) / freq_laser
wo_v = 175.306 * (2 * np.pi) / freq_laser
a_h = 30.267 * (2 * np.pi) / freq_laser
a_v = 33.69 * (2 * np.pi) / freq_laser

# Coefficients de déformabilité des galvanomètres
a = 541
b = 713
ampli_max = 70

# Commandes avec l'utilisateur (forme souhaitée, nom du fichier de sortie souhaité, taille en temps, ...)
for line in open("Interface.txt",'r',encoding='utf-8'):
    print(line.strip())

figure = input('Veuillez encoder votre choix (sans accent et en minuscule) : ').strip()
if figure == "carre":
    freq_s = float(input("Fréquence du signal envoyé en s^-1 (multiple de 10) : "))
    freq_f = freq_s / freq_laser  # On passe de s^-1 à frame^-1
    duree_f = int(duree_param * freq_laser)
    f = np.arange(duree_f+2)
    cx = float(input("Longueur du demi-côté en x du rectangle (max. 70) : "))
    cy = float(input("Longueur du demi-côté en y du rectangle (max. 70) : "))
    print("Calcul en cours ...")
    xh, xv = gm.square(cx,cy,freq_f,f)
    xh, xv = opti.decalage(xh,xv)

elif figure == "cercle":
    freq_s = float(input("Fréquence du signal envoyé en s^-1 (multiple de 10) : "))
    freq_f = freq_s / freq_laser # On passe de s^-1 à frame^-1
    duree_f = int(duree_param * freq_laser)
    f = np.arange(duree_f + 2)
    r = float(input("Rayon du cercle (max. 70) : "))
    xh,xv = gm.ellipse(r,r,freq_f,f)

elif figure == "ellipse":
    freq_s = float(input("Fréquence du signal envoyé en s^-1 (multiple de 10) : "))
    freq_f = freq_s / freq_laser  # On passe de s^-1 à frame^-1
    duree_f = int(duree_param * freq_laser)
    f = np.arange(duree_f + 2)
    c = float(input("Longueur du demi-axe horizontal (max. 70) : "))
    d = float(input("Longueur du demi-axe vertical (max. 70) : "))
    xh,xv = gm.ellipse(c,d,freq_f,f)

elif figure == "ellipse animee":
    taux = int(input("Taux de rafraîchissement souhaité (1-10) : "))
    freq_s = gm.calcul_freq_anim(k,taux,duree_anim)
    freq_f = freq_s / freq_laser  # On passe de s^-1 à frame^-1
    duree_f = int(duree_anim * freq_laser)
    f = np.arange(duree_f + 2)
    c = float(input("Longueur du demi-axe horizontal (max. 70) : "))
    d = float(input("Longueur du demi-axe vertical (max. 70) : "))
    xh,xv = gm.anim(c,d,k,freq_f,f)

elif figure == "hypotrochoide":
    l = 10*float(input("Valeur de l : "))
    R = 10 * float(input("Valeur de R : "))
    r = 10*float(input("Valeur de r : "))
    taux = int(input("Taux de rafraîchissement souhaité (1-10) : "))
    freq_s = gm.calcul_freq_hypotro(R,r,taux,duree_param)
    freq_f = freq_s / freq_laser  # On passe de s^-1 à frame^-1
    duree_f = int(duree_param * freq_laser)
    f = np.arange(duree_f + 2)
    xh,xv = gm.hypotrochoide(l,R,r,freq_f,f)

elif figure == "lemniscate de bernoulli":
    freq_s = float(input("Fréquence du signal envoyé en s^-1 (multiple de 10) : "))
    freq_f = freq_s / freq_laser  # On passe de s^-1 à frame^-1
    duree_f = int(duree_param*freq_laser)
    f = np.arange(duree_f + 2)
    c = float(input("Amplitude en x (max. 70) : "))
    xh,xv = gm.lemniscate(c,freq_f,f)

elif figure == "forme complexe":
    file_out = input("Veuillez entrer le nom du fichier .svg : ").strip()+".svg"
    print("Calcul en cours ...")
    duree_f = int(duree_complexe * freq_laser)
    f = np.arange(duree_f + 2)
    path = xml.clear(xml.find_path(file_out))
    x,y = xml.coord(path)
    xh,xv = xml.center(x,y)
    xh,xv = opti.optimisation(xh,xv,duree_f)
    xh,xv = opti.decalage(xh,xv)

# Calcul des signaux d'entrée
xh,xv = amplitude(xh,xv,a,b)

dxh = tf.derivative(xh,f)
ddxh = tf.derivative(dxh,f[:-1])

dxv = tf.derivative(xv,f[:-1])
ddxv = tf.derivative(dxv,f[:-1])

xh_in = tf.internal(xh,dxh,ddxh,a_h,wo_h,f)
xv_in = tf.external(xv,dxv,ddxv,a_v,wo_v)

xh_in = ajustement(xh_in)
xv_in = ajustement(xv_in)


# Génération des figures de sortie
data_in = np.zeros((len(xh_in),3))
data_in[:,1] = xh_in
data_in[:,0] = xv_in
data_in[:,2] = 1

file_in = input("Veuillez entrer le nom du fichier de sortie .csv : ").strip()+".csv"
np.savetxt(file_in,data_in,fmt="%.4f",delimiter=",")
print("Le fichier a bien été enregistré.")

# Renvoi visuel des points de sortie
print("Voici un aperçu visuel des points de sortie et d'entrée souhaités :")

plt.subplot(3,1,1)
plt.plot(xh,xv,label="signal de sortie")
plt.axis('equal')
plt.subplot(3,1,2)
plt.plot(xh_in,label="signal d'entrée x")
plt.subplot(3,1,3)
plt.plot(xv_in,label="signal d'entrée y")
plt.show()
