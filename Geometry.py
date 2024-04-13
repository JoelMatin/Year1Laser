""""
Auteur.e.s : Hanssens Dimitri, Matin Joel & Lindemann Theresa
Date : février - mars 2021

Contient les fonctions utilisées dans le calcul des signaux de sorties définis selon leurs équations paramétriques
déterminées au préalable
"""

import numpy as np
from fractions import Fraction


def square(cx, cy, freq, f):
    """
    Sur base des longueurs des demi-côtés du rectangle, créé le signal de sortie rectangulaire
    engendré par un vecteur tournant à vitesse angulaire constante (w = 2pi/T avec T la période du signal)
    autours de l'origine
    """
    Y = []
    X = []

    n = int(freq*(max(f)-2)) # Nombre de périodes au sein du signal de sortie
    t = (max(f)-2) // n      # durée en frame d'une période
    # On calcule la fréquence (en rad/frame) à insérer dans nos fcts trigo. (sur base de T = max(t))
    w = (1 / t) * 2 * np.pi
    for k in range(n):
        for fi in range(t):
            # On travaille quadrant par quadrant sur un cycle complet en fonction de la valeur associée à t
            if fi <= t / 4:
                xi = cx
                yi = cy * (2 * np.sin(fi * w) / (np.cos(fi * w) + np.sin(fi * w)) - 1)
                X.append(xi)
                Y.append(yi)
            elif t / 4 <= fi <= t / 2:
                xi = cx * (1 - 2 * np.cos(fi * w) / (np.cos(fi * w) - np.sin(fi * w)))
                yi = cy
                X.append(xi)
                Y.append(yi)
            elif t / 2 <= fi <= 3 * t / 4:
                xi = - cx
                yi = cy * (1 - 2 * np.sin(fi * w) / (np.cos(fi * w) + np.sin(fi * w)))
                X.append(xi)
                Y.append(yi)
            elif 3 * t / 4 <= fi:
                xi = cx * (2 * np.cos(fi * w) / (np.cos(fi * w) - np.sin(fi * w)) - 1)
                yi = - cy
                X.append(xi)
                Y.append(yi)
    return X, Y

def circle(r,freq,f):
    """
    Sur base du rayon du cercle, créé le signal de sortie circulaire engendré par un vecteur tournant
    à vitesse angulaire constante autours de l'origine
    """
    w = freq*(2*np.pi)
    X = r*np.cos(w*f)
    Y = r*np.sin(w*f)
    return X, Y

def ellipse(c,d,freq,f):
    """
    Sur base des longueurs c et d des demi-axes, créé le signal de sortie elliptique engendré par un vecteur tournant
    à vitesse angulaire constante autours de l'origine. Dans le cas particulier où c = d, la figure de sortie sera
    un cercle
    """
    w = freq*(2*np.pi)
    X =  c * np.cos(w * f)
    Y =  d * np.sin(w * f)
    return X, Y

def anim(c,d,k,freq,f):
    """
    Sur base des longueurs c et d des demi-axes, créé le signal de sortie elliptique dont la forme varie
    au cours du temps t engendré par un vecteur tournant à vitesse angulaire constante autours de l'origine
    """
    w = freq * (2 * np.pi)
    X = c * np.cos(k * w * f)
    Y = d * np.sin(w * f)
    return X, Y

def hypotrochoide(d,R,r,freq,f):
    """
    Sur base des paramètres d, R, r de l'hypotrochoïde, créé le signal de sortie de la figure
    engendrée par un vecteur tournant à vitesse angulaire constante autours de l'origine
    """
    w = freq*(2*np.pi)
    X = (R-r)*np.cos(w*f)+d*np.cos(w*f*(R-r)/r)
    Y = (R-r)*np.sin(w*f)-d*np.sin(w*f*(R-r)/r)
    return X, Y

def lemniscate(c,freq,f):
    """
    Sur base des paramètres c et du lemniscate, créé le signal de sortie de la figure
    engendrée par un vecteur tournant à vitesse angulaire constante autours de l'origine
    """
    w = freq*(2*np.pi)
    X = c*np.sin(w*f)/(1+np.cos(w*f)**2)
    Y = c*np.sin(w*f)*np.cos(w*f)/(1+np.cos(w*f)**2)
    return X,Y

def calcul_freq_hypotro(R, r,taux, duree_signal_s):
    """
    Calcule la fréquence en seconde du signal de l'hypotrochoïde à envoyer
    sur base des paramètres R et r de la figure
    """
    q = str(Fraction((R-r)/r).limit_denominator(1000)) # Renvoie le str du rationnel (R-r)/r sous forme de fraction (approximée)
    n = q.split("/")[1] # On prend le dénominateur de la fraction
    freq_s = int(n)/duree_signal_s # duree_signal_s = T = 2*pi*n/w = n/f (cf. explication rapport)
    return freq_s*taux

def calcul_freq_anim(k,taux, duree_signal_s):
    """
    Calcule la fréquence en seconde du signal de l'ellipse animée à envoyer
    sur base du paramètre psi de la figure
    """
    if type(k) == float:
        q = str(Fraction(k).limit_denominator(1000)) # Renvoie le str du rationnel k sous forme de fraction (approximée)
        n = q.split("/")[1] # On prend le dénominateur de la fraction
    elif type(k) == int:
        n = 1
    freq_s = int(n)/duree_signal_s # duree_signal_s = T = 2*pi*n/w = n/f (cf. explication rapport)
    return freq_s*taux