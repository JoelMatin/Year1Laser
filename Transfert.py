"""
Auteurs : Hanssens Dimitri & Matin Joel
Date : février - mars 2021

Contient les fonctions utilisées dans le calcul des points du signal d'entrée
sur base du signal de sortie désiré
"""


def derivative(x, t):
    """
    Renvoie la dérivée de la fonction x(t)
    Entrée : liste des valeurs de x et de t
    """
    res = []
    dt = (max(t) - min(t)) / (len(t) - 1)  # On calcule l'accroissement entre deux points de t
    for i in range(len(x) - 1):
        slope = (x[i + 1] - x[i]) / dt  # On calcule la pente entre deux points
        res.append(slope)
    return res

def external(x2,dx2,ddx2,a,wo):
    """
    On  calcule le résultat de l'équation x1 = x2''/(wo²) + 2*a/(wo²)*x2' + x2
    Avec x2 la fonction de sortie et x1 la fonction d'entrée
    """
    res = []
    for i in range(len(ddx2)):                            # On rajoute un à un (sur base de la plus petite liste, ddmass)
        x1_i = ddx2[i]/(wo**2)+2*a/(wo**2)*dx2[i]+x2[i]   # Traduction de l'équation
        res.append(x1_i)
    return res

def internal(x2, dx2, ddx2, a, wo, t):
    """
    On calcule le résultat de l'équation x1' = x2''/(2a) + x2' + (wo²)/(2a)*(x2-x1)
    Par la méthode d'Euler
    Avec x2 la fonction de sortie et x1 la fonction d'entrée
    """
    ys = [x2[0]]  # ys initial (= x2 initial)
    for i in range(1, len(ddx2)):  # Plus petite liste = ddx2
        dt = t[1]  # Pas
        y = ys[-1] + dt * (wo ** 2 / (2 * a) * (x2[i - 1] - ys[i - 1]) + dx2[i - 1] + ddx2[i - 1] / (2 * a))
        ys.append(y)
    return ys