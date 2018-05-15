import math
import numpy as np

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

def distance2points(ax,ay,az,bx,by,bz):
    l = math.sqrt((ax-bx)**2+(ay-by)**2+(az-bz)**2);
    return l

""" 
On suppose qu'on veut orienter le _center de la source par des angles 
et la position du _center, on calcule les positios des sommets
"""
def anglesToPos(xp,yp,zp,theta,phi): #thisdir comme prime
    matriceRot = np.matrix([[math.cos(theta)*math.cos(phi), -math.cos(theta)*math.sin(phi), math.sin(theta)],
                            [math.sin(phi),                  math.cos(phi)                , 0              ],
                            [-math.sin(theta)*math.cos(phi), math.sin(phi)*math.sin(theta), math.cos(theta)]]);

    demiLong = LongS/2
    demiLarg = LargS/2
    demiHaut = HautS/2

    B11 = np.matrix([[xp-demiLong], [yp-demiLarg], [zp+demiHaut]]);
    B12 = np.matrix([[xp-demiLong], [yp-demiLarg], [zp-demiHaut]]);
    B21 = np.matrix([[xp-demiLong], [yp+demiLarg], [zp+demiHaut]]);
    B22 = np.matrix([[xp-demiLong], [yp+demiLarg], [zp-demiHaut]]);
    B31 = np.matrix([[xp+demiLong], [yp-demiLarg], [zp+demiHaut]]);
    B32 = np.matrix([[xp+demiLong], [yp-demiLarg], [zp-demiHaut]]);
    B41 = np.matrix([[xp+demiLong], [yp+demiLarg], [zp+demiHaut]]);
    B42 = np.matrix([[xp+demiLong], [yp+demiLarg], [zp-demiHaut]]);

    return (matriceRot.dot(B11), matriceRot.dot(B12), \
            matriceRot.dot(B21), matriceRot.dot(B22), \
            matriceRot.dot(B31), matriceRot.dot(B32), \
            matriceRot.dot(B41), matriceRot.dot(B42));

"""
Fonction qui teste si un point est dans le volume de la maisonnette
"""
def appartientVolumeMaison(x,y,z):
    return (LongCC-LongM) <= x <= LongCC and ((LargCC-LargM)/2) < y < (LargCC - ((LargCC-LargM)/2)) and 0 < z < HautM

    if x < (LongCC-LongM):
        return False

    elif y < ((LargCC-LargM)/2) and y > (LargCC - ((LargCC-LargM)/2)):
        return False

    elif z > HautM:
        return False

    else :
        return True


"""
On calcule le vecteur normalisé entre les vertices_points_list d'encrages et les 
sommets de la sources c'est cette fonction qu'il faut modifier pour 
tester plusieurs configuration
"""
def vecteursAtoB(Pa,xp,yp,zp,theta,phi):
    L = anglesToPos(xp,yp,zp, theta, phi)
    D = [distance2points(p.item(0), p.item(1), p.item(2), l.item(0), l.item(1), l.item(2)) for p, l in zip(Pa, L)]
    V = [ (l - pa)/d for l, pa, d in zip(L, Pa, D) ]
    return(V,D)

    """
    #création d'un vecteur des distances
    d11 = distance2points(xa11,ya11,za11,L[0][0],L[0][1],L[0][2]);
    d12 = distance2points(xa12,ya12,za12,L[1][0],L[1][1],L[1][2]); 
    d21 = distance2points(xa21,ya21,za21,L[2][0],L[2][1],L[2][2]);
    d22 = distance2points(xa22,ya22,za22,L[3][0],L[3][1],L[3][2]);
    d31 = distance2points(xa31,ya31,za31,L[4][0],L[4][1],L[4][2]);
    d32 = distance2points(xa32,ya32,za32,L[5][0],L[5][1],L[5][2]);
    d41 = distance2points(xa41,ya41,za41,L[6][0],L[6][1],L[6][2]);
    d42 = distance2points(xa42,ya42,za42,L[7][0],L[7][1],L[7][2]);
    D = (d11,d12,d21,d22,d31,d32,d41,d42);
    """

    """
    #Création des vecteurs directeurs de chaque câble
    v11 = (L[0] - creerPoint(xa11,ya11,za11))/d11
    v12 = (L[1] - creerPoint(xa12,ya12,za12))/d12
    v21 = (L[2] - creerPoint(xa21,ya21,za21))/d21
    v22 = (L[3] - creerPoint(xa22,ya22,za22))/d22
    v31 = (L[4] - creerPoint(xa31,ya31,za31))/d31
    v32 = (L[5] - creerPoint(xa32,ya32,za32))/d32
    v41 = (L[6] - creerPoint(xa41,ya41,za41))/d41
    v42 = (L[7] - creerPoint(xa42,ya42,za42))/d42
    V = (v11,v12,v21,v22,v31,v32,v41,v42);
    """

'''
Cette fonction teste si pour une position voulue (xp,yp,zp) 
et theta, phi, les câbles entre dans la maisonnette, par la 
suite il faudrait tester si les câbles entrent dans la source 
et s'ils se touchent
'''
def ConflitDePosition(xp,yp,zp,theta,phi,Pa,n):

    V, D = vecteursAtoB(Pa,xp,yp,zp,theta,phi);

    """
    V, D = vecteursAtoB(xa11,ya11,za11, \
                        xa12,ya12,za12, \
                        xa21,ya21,za21, \
                        xa22,ya22,za22, \
                        xa31,ya31,za31, \
                        xa32,ya32,za32, \
                        xa41,ya41,za41, \
                        xa42,ya42,za42, \
                        xp,yp,zp,theta,phi);
    """

    ListeNumero = (11,12,21,22,31,32,41,42);

    """
    Pour chaque câble on discrétise en n nombre de point, 
    et on les teste, ce n'est pas la plus optimal mais 
    ça peu le faire pour l'instant.
    """
    print("Centre : " + str((xp, yp, zp)))
    print("Angles : " + str((theta, phi)))

    for v, d, pa, num in zip(V, D, Pa, ListeNumero):
        touche = False
        for k in range(n):
            sommet = pa + v*(k/n)*d;
            if appartientVolumeMaison(sommet[0], sommet[1], sommet[2]):
                touche = True
                break
        print("Cable " + str(num) + " : " + ("ok" if not touche else "ca touche"))
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

ConflitDePosition(100,100,300,0,0,Pa,1000)

ConflitDePosition(600,250,200,0,0,Pa,1000)