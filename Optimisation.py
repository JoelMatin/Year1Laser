"""
Auteur : Hanssens Dimitri & Lindemann Theresa
Date : mars 2021

Optimise les listes de points générées par lecture d'un fichier .svg en les répartissant à égale distance
tout en conservant au mieux les propriétés de la figure d'origine
"""

import numpy as np


def distances(x, y):
    """
    Calcule les trois données suivantes :
    - La distance totale de la courbe segmentée en sommant les distances entre deux points
    - La plus petite distance entre deux points parmi tous les points de calcul*
    - La plus grande distance entre deux points parmi tous les points de calcul
    * Cette distance est minorée par une certaine contrainte pour éviter d'atteindre les limites de valeur imposées par
    python dans les calculs ultérieurs.
    Renvoie les trois valeurs mesurées dans le même ordre que mentionné ci-dessus
    """
    # Initialisation des calculs
    d1 = np.sqrt((x[1] - x[0]) ** 2 + (y[1] - y[0]) ** 2)
    res_tot = d1
    res_min = d1
    res_max = d1
    for i in range(2, len(x)):  # On réitère le calcul d1 pour les autres points et on discute de la valeur obtenue
        # Distance entre deux points
        di = np.sqrt((x[i] - x[i - 1]) ** 2 + (y[i] - y[i - 1]) ** 2)
        # On définit arbitrairement une borne inférieure à la valeur de d_min sur base du dernier d_max enregistré :
        if di < res_min and di > res_max / 10e6:
            res_min = di
        if di > res_max:
            res_max = di
        res_tot += di
    return res_tot, res_min, res_max


def rajout(x, y):
    """
    On rajoute le nombre de points nécessaire par interpolation linéaire pour une répartition équidistante
    entre les points définissant la figure initiale, sur base de la distance minimale
    séparant deux points consécutifs donnés.
    Renvoie les nouvelles coordonnées des points de la figure séparés d'une distance égale
    """
    xs = []
    ys = []
    d_min = distances(x, y)[1]  # Calcul de la distance minimale entre deux points
    for i in range(1, len(x)):
        di = np.sqrt((x[i] - x[i - 1]) ** 2 + (y[i] - y[i - 1]) ** 2)
        rapport = int(di / d_min)  # On calcule le nombre de points à rajouter entre nos deux points de calcul
        if rapport >= 1:
            x_inter, y_inter = interpolation(x[i], y[i], x[i - 1], y[i - 1], rapport)  # On génère les points souhaités
            xs.extend(x_inter)
            ys.extend(y_inter)
    return xs, ys


def interpolation(x2, y2, x1, y1, nb):
    """
    Rajoute le nombre de points indiqué en paramètre entre deux points sur base de leur coordonnée
    et par interpolation linéaire
    """
    xs = []
    ys = []
    # Calcul des composantes du vecteur directeur u de la droite passant par (x1,y1) et (x2,y2)
    ux = (x2 - x1) / nb
    uy = (y2 - y1) / nb
    # Rajout pour tout t entier entre 0 et nb non inclus
    for t in range(nb):
        xs.append(x1 + t * ux)
        ys.append(y1 + t * uy)
    return xs, ys


def réduction(x, y, N):
    """
    Sur base du nombre N de points demandé, sélectionne N' points parmi les points donnés en paramètre tel que
    ces derniers sont répartis à distance égale et N' est le plus proche possible de N (par excès)
    Renvoie les coordonnées sous forme de liste des N' points équidistants
    """
    xs = []
    ys = []
    # Si le nombre de point souhaité est moindre que le nombre de points appelé par la fonction
    if N < len(x):
        pas = len(x)//N
        # On itère N' fois
        for i in range(0, len(x), pas):
            xs.append(x[i])
            ys.append(y[i])
    # Sinon, on garde les points appelés
    else:
        xs = x
        ys = y
    return xs, ys


def optimisation(x, y, N):
    """
    Renvoie N' points équidistants conservant le plus fidèlement possible
    les propriétés de la figure intiale définie sur base des points appelés par la fonction
    """
    # Etape 1 : rajout des points pour une répartition équidistante
    x1, y1 = rajout(x, y)
    # Etape 2 = réduction du nombre de points en fonction de celui souhaité
    x2, y2 = réduction(x1, y1, N)
    return x2, y2

def decalage(x,y):
    """
    Renvoie un nouveau signal en déphasage avec le signal envoyé en entrée.
    Le décalage temporel est donné arbitrairement à 1/10 de la longueur totale en frame du signal.
    """
    phi = len(x)//30
    X = []
    Y = []
    # On rajoute au début les derniers points du signal appelé
    for i in range(phi,len(x)):
        X.append(x[i])
        Y.append(y[i])
    # On rajoute à la fin les premiers points du signal appelé
    for i in range(phi):
        X.append(x[i])
        Y.append(y[i])
    return X,Y