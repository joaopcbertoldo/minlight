import  math
from math import cos, sin

import numpy as np
from numpy import matrix

"""import shapely.geometry as geom"""


## Paramètres

# CC = chambre climatique
LongCC = 10  # m
LargCC = 5   # m
HautCC = 4   # m

# _center du repère lié à la chambre
OCC = [0, 0, 0]

# M = maison
LongM = 5  # cm
LargM = 2.5 # cm
HautM = 3.80  # cm

# S = source
LongS = 1.00  # cm
LargS = 1.00  # cm
HautS = 1.00  # cm
dimensionsSource = {}
dimensionsSource['length'] = LongS
dimensionsSource['width' ] = LargS
dimensionsSource['height']  = HautS
dimensionsMaison = {}
dimensionsMaison['length'] = LongM
dimensionsMaison['width' ] = LargM
dimensionsMaison['height']  = HautM

## Outils

def creerPoint(x, y, z):
    '''
    Ça met les 3 coordonnées dans une matrice colonne 3x1 (numpy.matrix)
    '''
    return matrix([[x], [y], [z]])


def getCoordonnees(point):
    '''
    Ça prend une matrice colonne 3x1 (numpy.matrix) et retourne une tuple (x,y,z)
    '''
    return point.item(0), point.item(1), point.item(2)


def distance2points(ax, ay, az, bx, by, bz):
    '''Distance euclidienne en 3D entre 2 points.'''
    l = math.sqrt((ax - bx) ** 2 + (ay - by) ** 2 + (az - bz) ** 2);
    return l


def distance2pointsV(A, B):
    '''Distance euclidieinne en 3D entre 2 points (A et B son matrices 3x1).'''
    ax, ay, az = getCoordonnees(A)
    bx, by, bz = getCoordonnees(B)
    return distance2points(ax, ay, az, bx, by, bz)


def matriceRotation(angle, vecteur):
    norm = vecteur / np.linalg.norm(vecteur)
    x, y, z = getCoordonnees(norm)
    c = math.cos(angle)
    s = math.sin(angle)
    r11 = x ** 2 + (1 - x ** 2) * c
    r12 = x * y * (1 - c) - z * s
    r13 = x * z * (1 - c) + y * s

    r21 = x * y * (1 - c) + z * s
    r22 = y ** 2 + (1 - y ** 2) * c
    r23 = y * z * (1 - c) - x * s

    r31 = x * z * (1 - c) - y * s
    r32 = y * z * (1 - c) + x * s
    r33 = z ** 2 + (1 - z ** 2) * c

    return np.matrix([[r11, r12, r13],
                      [r21, r22, r23],
                      [r31, r32, r33]])
                      
                      
# ancien 'anglesToPos'
def sommetsDeLaSource(centreSource, theta, phi, dimensionsSource):  
    '''
    On suppose qu'on veut orienter le _center de la source par des angles
    et la position du _center, on calcule les positios des sommets (les coins de la source).
    :param centreSoleil: _center de la source dans le système de repère de la chambre
    :param theta: remplir...
    :param phi: remplir...
    :param dimensionsSource: (dictionnaire) length, width, height du pave de la source
    :return: liste des sommets de la source par rapport au système de repère de la chambre
    '''

    demiLong = dimensionsSource['length'] / 2
    demiLarg = dimensionsSource['width'] / 2
    demiHaut = dimensionsSource['height'] / 2

    # sommets (coins) de la source repérés par rapport à son _center
    B11 = creerPoint(- demiLong, - demiLarg, + demiHaut)
    B12 = creerPoint(- demiLong, - demiLarg, - demiHaut)
    B21 = creerPoint(- demiLong, + demiLarg, + demiHaut)
    B22 = creerPoint(- demiLong, + demiLarg, - demiHaut)
    B31 = creerPoint(+ demiLong, - demiLarg, + demiHaut)
    B32 = creerPoint(+ demiLong, - demiLarg, - demiHaut)
    B41 = creerPoint(+ demiLong, + demiLarg, + demiHaut)
    B42 = creerPoint(+ demiLong, + demiLarg, - demiHaut)

    # sommets (coins) de la source repérés par rapport à son _center
    B_source = [B11, B12, B21, B22, B31, B32, B41, B42]

    # matrice de rotation du système de la source
    Rot = matrix([[ cos(theta) * cos(phi), -cos(theta) * sin(phi), sin(theta)],
                  [          1 * sin(phi),           1 * cos(phi),          0],
                  [-sin(theta) * cos(phi),  sin(theta) * sin(phi), cos(theta)]])

    # les sommets rotationnés
    B_source_rot = [Rot.dot(b) for b in B_source]
    # les sommets par rapport à la chambre
    B = [(centreSource + b) for b in B_source_rot]

    return B


# deprecated
def appartientVolumeMaison(point):
    """
    Fonction qui teste si un point est dans le volume de la maisonnette.
    """
   # print("deprecated!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
    x, y, z = getCoordonnees(point)
    return (LongCC - LongM) <= x <= LongCC and ((LargCC - LargM) / 2) <= y <= (
    LargCC - ((LargCC - LargM) / 2)) and 0 <= z <= HautM


def appartientVolumePaveALOrigine(point, dimensions):
    '''
    Fonction qui teste si un point est dans le volume d'un pavé localisé à l'origine.
    :param dimensions: (dictionnaire) length, width, height du pave de la source
    :return: False/True
    '''

    demiLong = dimensions['longuer'] / 2
    demiLarg = dimensions['width'] / 2
    demiHaut = dimensions['height'] / 2

    x, y, z = getCoordonnees(point)

    return -demiLong <= x <= demiLong and -demiLarg <= y <= demiLarg and demiHaut <= z <= demiHaut


def appartientVolumePaveDeplace(point, centre, dimensions):
    '''
    Fonction qui teste si un point est dans le volume d'un pavé localisé à l'origine.
    :param dimensions: (dictionnaire) length, width, height du pave de la source
    :param centre: _center du pavé repéré dans le sys de coordonnées globale
    :return: False/True
    '''
    return appartientVolumePaveALOrigine(point - centre, dimensions)


def appartientVolumePaveAPartirDuCoinMini(point, pointMini, dimensions):
    '''
    Fonction qui teste si un point est dans le volume d'un pavé dont le point Mini est donné.
    :param dimensions: (dictionnaire) length, width, height du pave de la source
    :param pointMini: sommet le plus proche de l'origine dans le sys de coordonnées globale
    :return: False/True
    '''

    long = dimensions['length']
    larg = dimensions['width']
    haut = dimensions['height']

    x, y, z = getCoordonnees(point - pointMini)

    return 0 <= x <= long and 0 <= y <= larg and 0 <= z <= haut


"""
Fonction qui teste si un point est à l'intérieur de la chambre climatique
"""
def estDansLaChambreClimatique(point):
    x, y, z = getCoordonnees(point)
    return 0 < x < LongCC and 0 < y < LargCC and 0 < z < HautCC


"""
Fonction qui teste si un point est dans le volume du soleil
"""
def appartientVolumeSoleil(point, centre, theta, phi):
    
    Ry = matriceRotation(theta, np.matrix([[0], [1], [0]]))
    Rz = matriceRotation(phi, np.matrix([[0], [0], [1]]))

    R = np.dot(Ry, Rz)
    T = -centre

    TR = np.concatenate((R, T), axis=1)
    ligne_homogene = np.matrix([[0, 0, 0, 1]])
    TRhomogene = np.concatenate((TR, ligne_homogene), axis=0)

    pointHomogene = np.concatenate((point, np.matrix([[1]])), axis=0)

    pointHomogeneRelatif = np.dot(TRhomogene, pointHomogene)

    pointRelatif = np.matrix([[pointHomogeneRelatif.item(0)],
                              [pointHomogeneRelatif.item(1)],
                              [pointHomogeneRelatif.item(2)]])

    """print(point)
    print(pointHomogene)
    print(_center)
    print(Ry)
    print(Rz)
    print(R)
    print(TR)
    print(TRhomogene)
    print(pointHomogeneRelatif)
    print(pointRelatif)"""

    x, y, z = getCoordonnees(pointRelatif)

    demiLong = LongS / 2
    demiLarg = LargS / 2
    demiHaut = HautS / 2

    return -demiLong <= x <= demiLong and -demiLarg <= y <= demiLarg and -demiHaut <= z <= demiHaut


"""
On calcule le vecteur normalisé entre les points d'encrages et les 
sommets de la sources c'est cette fonction qu'il faut modifier pour 
tester plusieurs configuration
"""


def vecteursAtoB(Pa, centreSoleil, theta, phi,dimentionSource):
    print("Quelle configuration d'ancrage ? \n 1 norm\n 2 diag  ")
    config = input()
    L = sommetsDeLaSource(centreSoleil, theta, phi,dimentionSource)
    if config == "1":
        da11b11 = distance2pointsV(Pa[0],L[0])
        da12b12 = distance2pointsV(Pa[1],L[1])
        da21b21 = distance2pointsV(Pa[2],L[2])
        da22b22 = distance2pointsV(Pa[3],L[3])
        da31b31 = distance2pointsV(Pa[4],L[4])
        da32b32 = distance2pointsV(Pa[5],L[5])
        da41b41 = distance2pointsV(Pa[6],L[6])
        da42b42 = distance2pointsV(Pa[7],L[7])
        D = [da11b11, da12b12, da21b21, da22b22, da31b31, da32b32, da41b41, da42b42]
        V = [(l - pa) / d for l, pa, d in zip(L, Pa, D)]
        return (V, D)
    elif config == "2" :
        da11b21 = distance2pointsV(Pa[0],L[2])
        da12b32 = distance2pointsV(Pa[1],L[5])
        da21b41 = distance2pointsV(Pa[2],L[6])
        da22b12 = distance2pointsV(Pa[3],L[1])
        da31b11 = distance2pointsV(Pa[4],L[0])
        da32b42 = distance2pointsV(Pa[5],L[7])
        da41b31 = distance2pointsV(Pa[6],L[4])
        da42b22 = distance2pointsV(Pa[7],L[3])
        D = [da11b21, da12b32, da21b41, da22b12, da31b11, da32b42, da41b31, da42b22]
        va11b21 = (L[2]-Pa[0])/ da11b21
        va12b32 = (L[5]-Pa[1])/ da12b32
        va21b41 = (L[6]-Pa[2])/ da21b41
        va22b12 = (L[1]-Pa[3])/ da22b12
        va31b11 = (L[0]-Pa[4])/ da31b11
        va32b42 = (L[7]-Pa[5])/ da32b42
        va41b31 = (L[4]-Pa[6])/ da41b31
        va42b22 = (L[3]-Pa[7])/ da42b22
        V =[va11b21, va12b32, va21b41, va22b12, va31b11, va32b42, va41b31, va42b22]
        return(V,D)
    else :
        return("mauvaise cofiguration")

'''
Cette fonction teste si pour une position voulue (xp,yp,zp) 
et theta, phi, les câbles entre dans la maisonnette, par la 
suite il faudrait tester si les câbles entrent dans la source 
et s'ils se touchent
'''


def ConflitDePosition(centreSoleil, theta, phi, Pa, n):
    V,D = vecteursAtoB(Pa, centreSoleil, theta, phi,dimensionsSource);
    ListeNumero = (11, 12, 21, 22, 31, 32, 41, 42);

    print("Centre : " + str(tuple(centreSoleil.tolist())))
    print("Angles : " + str((theta, phi)))

    """
    Pour chaque câble on discrétise en n nombre de point, 
    et on les teste, ce n'est pas la plus optimal mais 
    ça peu le faire pour l'instant.
    """

    print(" " * len("Cable xx : ") + " " * 2 + \
          "maisonette" + " " * 2 + \
          "murs" + " " * 2 + \
          "soleil" + " " * 2 + \
          "instersections cables")
    for v, d, pa, num in zip(V, D, Pa, ListeNumero):
        toucheMaisonette = False
        toucheSoleil = False
        interieur = False

        for k in range(1, n):
            sommet = pa + v * (k / n) * d;

            toucheMaisonette = appartientVolumePaveAPartirDuCoinMini(sommet, creerPoint(5,1.25,0), dimensionsMaison)
            toucheSoleil = appartientVolumeSoleil(sommet, centreSoleil, theta, phi)
            interieur = estDansLaChambreClimatique(sommet)

            if toucheMaisonette or not interieur:
                break

        toucheCable = []
        """for v2, d2, pa2, num2 in zip(V, D, Pa, ListeNumero):
            if num != num2:
                b = pa + v * d
                b2 = pa2 + v2 * d2
                cable1 = geom.LineString([getCoordonnees(pa), getCoordonnees(b)])
                cable2 = geom.LineString([getCoordonnees(pa2), getCoordonnees(b2)])
                i = cable1.intersection(cable2)
                toucheCable.append((" ! " if i.geom_type == 'Point' else "   "))
            else:
                toucheCable.append(' m ')"""

        print("Cable " + str(num) + " : " + " " * 2 + \
              ("ok" if not toucheMaisonette else "!").center(len("maisonette")) + " " * 2 + \
              ("ok" if interieur else "!").center(len("murs")) + " " * 2 + \
              ("ok" if not toucheSoleil else "!").center(len("mur")) + " " * 2 + \
              "".join(toucheCable))
    print()



### Calcul des tensions dans les câbles :

# Matrices pour le produit vectoriel ;
Ex = np.matrix([[0, 1, 0], \
                [0, 0, 1]])
Ey = np.matrix([[1, 0, 0], \
                [0, 0, 1]])
Ez = np.matrix([[1, 0, 0], \
                [0, 1, 0]])
E = np.matrix([[0, -1], \
               [1, 0]])

Hx = np.dot(np.dot(np.transpose(Ex), np.transpose(E)), Ex)
Hy = np.dot(np.dot(-np.transpose(Ey), np.transpose(E)), Ey)
Hz = np.dot(np.dot(np.transpose(Ez), np.transpose(E)), Ez)


def matrice_torsion(centreSoleil, theta, phi, Pa):
    V, D = vecteursAtoB(Pa, centreSoleil, theta, phi,dimensionsSource)
    B = sommetsDeLaSource(centreSoleil, theta, phi,dimensionsSource)

    Mx = np.matrix([np.dot(np.transpose(b), np.dot(Hx, v * d)).item(0) for v, b, d in zip(V, B, D)])
    My = np.matrix([np.dot(np.transpose(b), np.dot(Hy, v * d)).item(0) for v, b, d in zip(V, B, D)])
    Mz = np.matrix([np.dot(np.transpose(b), np.dot(Hz, v * d)).item(0) for v, b, d in zip(V, B, D)])

    Fx = np.matrix([v[0].item(0) for v in zip(V)])
    Fy = np.matrix([v[0].item(1) for v in zip(V)])
    Fz = np.matrix([v[0].item(2) for v in zip(V)])
    W = np.concatenate((Fx,Fy,Fz,Mx,My,Mz),axis = 0)

    return W


#print(matrice_torsion(creerPoint(100, 200, 100), 0, 0, Pa))

masse = 50  # en kg
#B = sommetsDeLaSource(creerPoint(100, 200, 300), 0, 0,dimensionsSource)
g = 9.81

fx = 0
fy = 0
fz = - masse * g
Force = creerPoint(fx, fy, fz)
MomentPoids_P = creerPoint(0, 0, 0)
"""Si d'autre actions extérieur il faudra mettre des moments qui s'appliquent en P
mx = [np.dot(np.transpose(MCentre),np.dot(Hx,F))]
my = [np.dot(np.transpose(MCentre),np.dot(Hy,F))]
mz = [np.dot(np.transpose(MCentre),np.dot(Hz,F))]"""

forceExt = np.concatenate((Force, MomentPoids_P), axis=0)


def vecteurTension(centreSoleil, theta, phi, Pa):
    W = matrice_torsion(centreSoleil, theta, phi, Pa)
    T = -np.dot(np.linalg.pinv(W), (forceExt))
    # il y a une infinité de solutions utiliser la pseudo inverse permet d'avoir les tensions minimales
    return T


## Banc de test

CentreSoleilMilieuHaut = creerPoint(3.50,2.50,3.49)
CentreSoleilMilieu = creerPoint(3.50,2.50,2)
CentreSoleilAube = creerPoint(4.99,0.51,0.51)
CentreSoleilZenith = creerPoint(4.99,2.5,3.5)

#Aux quatres coins extrèmes
# à 10 m
PaHautBas10= (creerPoint(0, 0, 4), \
            creerPoint(0, 0, 0), \
            creerPoint(0, 5, 4), \
            creerPoint(0, 5, 0), \
            creerPoint(10, 0, 4), \
            creerPoint(10, 0, 0), \
            creerPoint(10, 5, 4), \
            creerPoint(10, 5, 0))

#à 7,5 m
PaHautBas7=(creerPoint(0, 0, 4), \
            creerPoint(0, 0, 0), \
            creerPoint(0, 5, 4), \
            creerPoint(0, 5, 0), \
            creerPoint(7.5, 0, 4), \
            creerPoint(7.5, 0, 0), \
            creerPoint(7.5, 0, 4), \
            creerPoint(7.5, 5, 0))
      

#à 5 m ras de la maisonnette
PaHautBas5 =(creerPoint(0, 0, 4), \
            creerPoint(0, 0, 0), \
            creerPoint(0, 5, 4), \
            creerPoint(0, 5, 0), \
            creerPoint(5, 0, 4), \
            creerPoint(5, 0, 0), \
            creerPoint(5, 5, 4), \
            creerPoint(5, 5, 0))
            
#Aux quatres coins hauts et anlges à mi-height
# à 10 m
PaHautMihaut10=(creerPoint(0, 0, 4), \
                creerPoint(0, 0, 2), \
                creerPoint(0, 5, 4), \
                creerPoint(0, 5, 2), \
                creerPoint(10, 0, 4), \
                creerPoint(10, 0, 2), \
                creerPoint(10, 5, 4), \
                creerPoint(10, 5, 2))

#à 7,5 m
PaHautMihaut7= (creerPoint(0, 0, 4), \
                creerPoint(0, 0, 2), \
                creerPoint(0, 5, 4), \
                creerPoint(0, 5, 2), \
                creerPoint(7.5, 0,4), \
                creerPoint(7.5, 0, 2), \
                creerPoint(7.5, 0, 4), \
                creerPoint(7.5, 5, 2))
      

#à 5 m ras de la maisonnette
PaHautMihaut5 =(creerPoint(0, 0, 4), \
                creerPoint(0, 0, 2), \
                creerPoint(0, 5, 4), \
                creerPoint(0, 5, 2), \
                creerPoint(5, 0, 4), \
                creerPoint(5, 0, 2), \
                creerPoint(5, 5, 4), \
                creerPoint(5, 5, 2))
                
#Aux quatres coins hauts
# à 10 m
PaHautHaut10 = (creerPoint(0, 0, 4), \
                creerPoint(0, 0, 3.8), \
                creerPoint(0, 5, 4), \
                creerPoint(0, 5, 3.8), \
                creerPoint(10, 0, 4), \
                creerPoint(10, 0, 3.8), \
                creerPoint(10, 5, 4), \
                creerPoint(10, 5, 3.8))

#à 7,5 m
PaHautHaut7 =  (creerPoint(0, 0, 4), \
                creerPoint(0, 0, 3.8), \
                creerPoint(0, 5, 4), \
                creerPoint(0, 5, 3.8), \
                creerPoint(7.5, 0, 4), \
                creerPoint(7.5, 0, 3.8), \
                creerPoint(7.5, 0, 4), \
                creerPoint(7.5, 5, 3.8))
      

#à 5 m ras de la maisonnette
PaHautHaut5 =  (creerPoint(0, 0, 4), \
                creerPoint(0, 0, 3.8), \
                creerPoint(0, 5, 4), \
                creerPoint(0, 5, 3.8), \
                creerPoint(5, 0, 4), \
                creerPoint(5, 0, 3.8), \
                creerPoint(5, 5, 4), \
                creerPoint(5, 5, 3.8))
                
d90 = 90*np.pi/180