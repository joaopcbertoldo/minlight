import math
import numpy as np
import shapely.geometry as geom

'''
Paramètres 
'''

LongCC = 1000; #CC pour chambre climatique en cm
LargCC = 500;
HautCC = 400;
O = [0,0,0]; # _center du repère lié à la chambre

LongM = 500; #M pour maison
LargM = 250;
HautM = 380;

LongS = 100; #Longeur de la source
LargS = 100; 
HautS = 100;


def creerPoint(x, y, z):
    return np.matrix([[x], [y], [z]])

def getCoordonnees(point):
    return point.item(0), point.item(1), point.item(2)

def distance2points(ax,ay,az,bx,by,bz):
    l = math.sqrt((ax-bx)**2+(ay-by)**2+(az-bz)**2);
    return l

""" 
On suppose qu'on veut orienter le _center de la source par des angles 
et la position du _center, on calcule les positios des sommets
"""
def anglesToPos(centreSoleil,theta,phi): #thisdir comme prime
    xp, yp, zp = getCoordonnees(centreSoleil)

    matriceRot = np.matrix([[math.cos(theta)*math.cos(phi), -math.cos(theta)*math.sin(phi), math.sin(theta)],
                            [math.sin(phi),                  math.cos(phi)                , 0              ],
                            [-math.sin(theta)*math.cos(phi), math.sin(phi)*math.sin(theta), math.cos(theta)]]);

    demiLong = LongS/2
    demiLarg = LargS/2
    demiHaut = HautS/2

    B11 = creerPoint(xp-demiLong, yp-demiLarg, zp+demiHaut)
    B12 = creerPoint(xp-demiLong, yp-demiLarg, zp-demiHaut)
    B21 = creerPoint(xp-demiLong, yp+demiLarg, zp+demiHaut)
    B22 = creerPoint(xp-demiLong, yp+demiLarg, zp-demiHaut)
    B31 = creerPoint(xp+demiLong, yp-demiLarg, zp+demiHaut)
    B32 = creerPoint(xp+demiLong, yp-demiLarg, zp-demiHaut)
    B41 = creerPoint(xp+demiLong, yp+demiLarg, zp+demiHaut)
    B42 = creerPoint(xp+demiLong, yp+demiLarg, zp-demiHaut)
    B = (B11, B12, B21, B22, B31, B32, B41, B42)

    return [matriceRot.dot(b) for b in B]


"""
Fonction qui teste si un point est dans le volume de la maisonnette
"""
def appartientVolumeMaison(point):
    x, y, z = getCoordonnees(point)
    return (LongCC-LongM) <= x <= LongCC and ((LargCC-LargM)/2) <= y <= (LargCC - ((LargCC-LargM)/2)) and 0 <= z <= HautM


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

    def matriceRotation(angle, vecteur):
        norm = vecteur / np.linalg.norm(vecteur)
        x, y, z = getCoordonnees(norm)
        c = math.cos(angle)
        s = math.sin(angle)
        r11 = x**2 + (1-x**2)*c
        r12 = x*y*(1-c)-z*s
        r13 = x*z*(1-c)+y*s

        r21 = x*y*(1-c) + z*s
        r22 = y**2 + (1-y**2)*c
        r23 = y*z*(1-c) - x*s

        r31 = x*z*(1-c) - y*s
        r32 = y*z*(1-c) + x*s
        r33 = z**2 + (1-z**2)*c

        return np.matrix([[r11, r12, r13],
                          [r21, r22, r23],
                          [r31, r32, r33]])

    Ry = matriceRotation(theta, np.matrix([[0],[1],[0]]))
    Rz = matriceRotation(phi,   np.matrix([[0],[0],[1]]))

    R = np.dot(Ry,Rz)
    T = -centre

    TR = np.concatenate((R,T),axis=1)
    ligne_homogene = np.matrix([[0, 0, 0, 1]])
    TRhomogene = np.concatenate((TR, ligne_homogene),axis=0)

    pointHomogene = np.concatenate((point,np.matrix([[1]])), axis=0)

    pointHomogeneRelatif = np.dot(TRhomogene, pointHomogene)

    pointRelatif = np.matrix([[pointHomogeneRelatif.item(0)],
                              [pointHomogeneRelatif.item(1)],
                              [pointHomogeneRelatif.item(2)]])
    #"""
    print(point)
    print(pointHomogene)
    print(centre)
    print(Ry)
    print(Rz)
    print(R)
    print(TR)
    print(TRhomogene)
    print(pointHomogeneRelatif)
    print(pointRelatif)
    #"""

    x, y, z = getCoordonnees(pointRelatif)

    demiLong = LongS / 2
    demiLarg = LargS / 2
    demiHaut = HautS / 2

    return -demiLong <= x <= demiLong and -demiLarg <= y <= demiLarg and -demiHaut <= z <= demiHaut


"""
On calcule le vecteur normalisé entre les vertices_points_list d'encrages et les 
sommets de la sources c'est cette fonction qu'il faut modifier pour 
tester plusieurs configuration
"""
def vecteursAtoB(Pa,centreSoleil,theta,phi):
    L = anglesToPos(centreSoleil, theta, phi)
    D = [distance2points(p.item(0), p.item(1), p.item(2), l.item(0), l.item(1), l.item(2)) for p, l in zip(Pa, L)]
    V = [ (l - pa)/d for l, pa, d in zip(L, Pa, D) ]
    return (V,D)


'''
Cette fonction teste si pour une position voulue (xp,yp,zp) 
et theta, phi, les câbles entre dans la maisonnette, par la 
suite il faudrait tester si les câbles entrent dans la source 
et s'ils se touchent
'''
def ConflitDePosition(centreSoleil,theta,phi,Pa,n):
    V, D = vecteursAtoB(Pa,centreSoleil,theta,phi);

    ListeNumero = (11,12,21,22,31,32,41,42);

    print("Centre : " + str(tuple(centreSoleil.tolist())))
    print("Angles : " + str((theta, phi)))

    """
    Pour chaque câble on discrétise en n nombre de point, 
    et on les teste, ce n'est pas la plus optimal mais 
    ça peu le faire pour l'instant.
    """

    print(" " * len("Cable xx : ") + " "*2 + \
          "maisonette"             + " "*2 + \
          "murs"                   + " "*2 + \
          "soleil"                 + " "*2 + \
          "instersections cables" )
    for v, d, pa, num in zip(V, D, Pa, ListeNumero):
        toucheMaisonette = False
        toucheSoleil = False
        interieur = False

        for k in range(1,n):
            sommet = pa + v*(k/n)*d;

            toucheMaisonette = appartientVolumeMaison(sommet)
            toucheSoleil     = appartientVolumeSoleil(sommet,centreSoleil,theta,phi)
            interieur        = estDansLaChambreClimatique(sommet)

            if toucheMaisonette or not interieur:
                break

        toucheCable = []
        for v2, d2, pa2, num2 in zip(V, D, Pa, ListeNumero):
            if num != num2:
                b = pa + v * d
                b2 = pa2 + v2 * d2
                cable1 = geom.LineString([getCoordonnees(pa),  getCoordonnees(b)])
                cable2 = geom.LineString([getCoordonnees(pa2), getCoordonnees(b2)])
                i = cable1.intersection(cable2)
                toucheCable.append((" ! " if i.geom_type == 'Point' else "   "))
            else:
                toucheCable.append(' m ')

        print("Cable " + str(num) + " : "                                       + " " * 2 + \
              ("ok" if not toucheMaisonette else "!").center(len("maisonette")) + " " * 2 + \
              ("ok" if interieur else "!").center(len("murs"))                  + " " * 2 + \
              ("ok" if not toucheSoleil else "!").center(len("mur"))           + " " * 2 + \
              "".join(toucheCable))
    print()
"""
ConflitDePosition(xp,yp,zp,theta,phi,
                  xa11,ya11,za11,
                  xa12,ya12,za12,
                  xa21,ya21,za21,
                  xa22,ya22,za22,
                  xa31,ya31,za31,
                  xa32,ya32,za32,
                  xa41,ya41,za41,
                  xa42,ya42,za42,
                  n)
"""

Pa = (creerPoint(   0,   0, 400), \
      creerPoint(   0,   0,   0), \
      creerPoint(   0, 500, 400), \
      creerPoint(   0, 500,   0), \
      creerPoint(1000,   0, 400), \
      creerPoint(1000,   0,   0), \
      creerPoint(1000, 500, 400), \
      creerPoint(1000, 500,   0))

#ConflitDePosition(100,100,300,0.52,0.24,Pa,1000)

"""
ConflitDePosition(creerPoint(100,100,300),0,0,Pa,1000)
ConflitDePosition(creerPoint(600,250,200),0,0,Pa,1000)
ConflitDePosition(creerPoint(100,50,100),0,0,Pa,1000)
ConflitDePosition(creerPoint(100,200,40),0,0,Pa,1000)
"""

#print(appartientVolumeSoleil(creerPoint(0,0,0), creerPoint(0,0,0), 0, 0))
#print(appartientVolumeSoleil(creerPoint(40,40,40), creerPoint(200,200,200), 0, 0))
#print(appartientVolumeSoleil(creerPoint(200,200,200), creerPoint(200,200,200), 0, 0))
print(appartientVolumeSoleil(creerPoint(200,200,200), creerPoint(200,200,200), math.pi/4, math.pi/4))
print(appartientVolumeSoleil(creerPoint(205,205,205), creerPoint(200,200,200), math.pi/4, math.pi/4))

