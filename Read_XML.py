"""
Auteur : Hanssens Dimitri
Date : février - mars 2021

Sur base d'un fichier .svg d'une image vectorisée, renvoie les coordonnées de chacun des noeuds de l'objet vectoriel.

Conditions d'utilisation : Les noeuds doivent tous être réliés linéairement.
Il faut donc applatir les courbes au préalable.
Pour ce faire, il faut augmenter le nombre de noeuds (précision) et rendre rectiligne chaque segment
sur l'ensemble de l'image via le logiciel de dessin vectoriel.
"""


def find_path(file):
    """
    Cherche et enregistre le chemin de noeuds dans le fichier SVG entré en paramètre
    Renvoie le chemin brut
    """
    for line in open(file, 'r', encoding="utf-8"):
        # La ligne correspondante au chemin commence par l'assignation de la variable d au string recherché
        if line.strip().find('d') == 0:  # Si d est le premier caractère de la ligne
            res = line.strip().strip()[3:-1]  # On assigne le chemin net en nettoyant les bords des guillemets
    return res


def clear(str):
    """
    Nettoye le chemin de noeuds du fichier .svg
    Renvoie une liste contenant les coordonnées et la commande associées pour chaque noeud
    """
    lst = str.strip().split()
    res = []
    balise = ["Z", "z"]
    commande = ["H", "h", "V", "v", "Z", "z", "M", "m", "L", "l"]  # Regroupe les commandes de noeuds dans une liste
    dico2 = {1: str}  # Indique la balise activée au moyen d'un dictionnaire
    for elem in lst:
        if elem in balise:
            # Rajoute la balise permettant de renouveler le chemin depuis le point de départ
            res.append("Start")
        if elem in commande:
            dico2[1] = elem  # Active la nouvelle commande en remplaçant la dernière active
        if not elem.isalpha():
            res.append(elem + "," + dico2[1])  # Rajoute l'élément (x,y,balise) sous forme de string dans la liste
    return res


def coord(path):
    """
    Récolte les coordonnées cartésiennes en x et y du chemin sur base des informations liées à chaque noeud
    Renvoie les coordonnées traitables sous forme de liste
    """
    # Définition d'un point de référence (vecteur nul)
    X = [0]
    Y = [0]
    start = 1
    for elem in path:
        coord = elem.split(",")
        # Si la coordonnée est une balise "closepath" : Entame un nouveau chemin depuis le dernier point de départ
        if elem == "Start":
            X.append(X[start])
            Y.append(Y[start])
            start = len(X)  # Réinitialise l'indice du point de départ
        # Si la balise est une lettre minuscule, les coordonnées du noeud indiquent le déplacement à effectuer
        # pour atteindre les coordonnées du point correspondant
        if coord[-1].islower():
            if coord[-1] not in ["h", "v"]:  # Cas général
                x = X[-1] + float(coord[0])
                y = Y[-1] - float(coord[1])
                X.append(x)
                Y.append(y)
            elif coord[-1] == "h":  # Tracé horizontal : On ne dispose que du déplacement en x
                x = X[-1] + float(coord[0])
                y = Y[-1]
                X.append(x)
                Y.append(y)
            elif coord[-1] == "v":  # Tracé vertical : On ne dispose que du déplacement en y
                x = X[-1]
                y = Y[-1] - float(coord[0])
                X.append(x)
                Y.append(y)
        # Si la balise est une lettre majuscule, les coordonnées du noeud sont les coordonnées du point souhaité
        if coord[-1].isupper():
            if coord[-1] not in ["H", "V"]:  # Cas général
                X.append(float(coord[0]))
                Y.append(-float(coord[1]))
            elif coord[-1] == "H":  # Tracé horizontal : On ne dispose que de la coord. en x
                X.append(float(coord[0]))
                Y.append(Y[-1])
            elif coord[-1] == "V":  # Tracé vertical : On ne dispose que de la coord. en y
                X.append(X[-1])
                Y.append(-float(coord[0]))
    del X[0], Y[0]  # Supprime le point de référence
    return X, Y


def center(x,y):
    """
    Centre l'objet (défini par ses coordonnées) en l'origine
    """
    X = []
    Y = []
    a = -(max(x)-min(x))/2 - min(x)                   # Vecteur déplacement horizontal
    b = (max(y) - min(y))/2 - max(y)                  # Vecteur déplacement vertical
    for xi in x:
        X.append(xi + a)
    for yi in y:
        Y.append(yi + b)
    return X,Y
