def matrice_rotation(angle, vecteur):
    direction = vecteur / norme_vecteur(vecteur)
    x, y, z = get_coordonnees_vecteur_3d(direction)
    c = cos(angle)
    s = sin(angle)

    r11 = x ** 2 + (1 - x ** 2) * c
    r12 = x * y * (1 - c) - z * s
    r13 = x * z * (1 - c) + y * s

    r21 = x * y * (1 - c) + z * s
    r22 = y ** 2 + (1 - y ** 2) * c
    r23 = y * z * (1 - c) - x * s

    r31 = x * z * (1 - c) - y * s
    r32 = y * z * (1 - c) + x * s
    r33 = z ** 2 + (1 - z ** 2) * c

    return matrix([[r11, r12, r13],
                   [r21, r22, r23],
                   [r31, r32, r33]])


### Calcul des tensions dans les câbles :

# Matrices pour le produit vectoriel ;
Ex = matrix([[0, 1, 0],
             [0, 0, 1]])

Ey = matrix([[1, 0, 0],
             [0, 0, 1]])

Ez = matrix([[1, 0, 0],
             [0, 1, 0]])

E  = matrix([[0, -1],
             [1, 0]])

Hx = ( Ex.T * E.T) * Ex
Hy = (-Ey.T * E.T) * Ey
Hz = ( Ez.T * E.T) * Ez

def matrice_torsion(source, configs_ancrage):

    # comment ça marche
    # point d'application des tensions ?
    # momments ?
    # _center de gravité

    sommets_source = sommets_pave(centre     = source['_center'    ],
                                  ypr_angles = source['_orientation'],
                                  dimensions = source['dimensions'])

    points_ancrage = get_points_ancrage_ordones(configs_ancrage)

    vecteurs_cables = creer_vecteurs_cables(points_ancrage, sommets_source)

    Mx = [ss.T * (Hx * vc) for vc, ss in zip(vecteurs_cables, sommets_source)]
    My = [ss.T * (Hy * vc) for vc, ss in zip(vecteurs_cables, sommets_source)]
    Mz = [ss.T * (Hz * vc) for vc, ss in zip(vecteurs_cables, sommets_source)]

    # à quoi ça sert ?
    Fx = [v[0][0] for v in zip(vecteurs_cables)]
    Fy = [v[0][1] for v in zip(vecteurs_cables)]
    Fz = [v[0][2] for v in zip(vecteurs_cables)]

    # ça devrait pas etre pour chaque cable ?
    W = matrix([Fx, Fy, Fz, Mx, My, Mz])

    return W


print(matrice_torsion(source, configs_ancrage))

masse = 50  # en kg

S = sommets_pave(source['_center'], source['_orientation'], source['dimensions'])

g = 9.81

fx = 0
fy = 0
fz = masse * g

Force = vecteur_3d(fx, fy, fz)
MomentPoids_P = vecteur_3d(0, 0, 0)  # ça suppose un bilan fait à partir du _center de masse

"""
Si d'autre actions extérieur il faudra mettre des moments qui s'appliquent en P
mx = [(MCentre.T * (Hx * F))]
my = [(MCentre.T * (Hy * F))]
mz = [(MCentre.T * (Hz * F))]
"""

forceExt = np.concatenate((Force, MomentPoids_P), axis=0)


def vecteurTension(centreSoleil, theta, phi, Pa):
    W = matrice_torsion(centreSoleil, theta, phi, Pa)
    T = - pinv(W) * forceExt
    # il y a une infinité de solutions utiliser la pseudo inverse permet d'avoir les tensions minimales
    return T





class Vecteur(numpy.matrix):
    def __new__(cls, x, y, z):
        # note that we have to send cls to super's __new__, even though we gave it to super already.
        # I think this is because __new__ is technically a staticmethod even though it should be a classmethod
        return super(Vecteur, cls).__new__(cls, "{}; {}; {}".format(x, y, z))




# pas encore utilisé
def tester_interdictions_points(generator_points, tests_interdictions):
    resultats = {t['nom']: t['message_ok'] for t in tests_interdictions}
    for p in generator_points:
        for t in tests_interdictions:
            fonction = t['fonction']
            args = t['args']
            if fonction.__call__(p, **args):
                resultats[t['nom']] = t['message_probleme']
    return resultats






sommets = [Vec3(sommet[0], sommet[1], sommet[2]) for sommet in product((1,-1), repeat=3)]

# !!!!!!!!!!!!!!! faire gaffe avec les arrondissement
def points_dans_meme_plane(p1, p2, p3, p4):
    vec1 = p2 - p1
    vec2 = p3 - p1

    # coordonnees du vec resultant du prod vect
    u, v, w = tuple(cross(vec1.T, vec2.T)[0].tolist())

    normal = Vec3(u,v,w)

    k1 = normal.T.dot(p1)
    k4 = normal.T.dot(p4)
    diff = (k1 - k4)[0][0]
    return diff == 0

faces = []

for quartette in combinations(sommets, 4):
    if points_dans_meme_plane(quartette[0], quartette[1], quartette[2], quartette[3]):
        faces.append(quartette)




'''
def maxTheta(r, phi, maisonette,source,chambre,configs_ancrag)
#r : distance entre _center de la face de la maisonette et le _center de la source, r des coordonnes spheriques
#phi : angle verticale , coordonnes spheriques
#centreRotation:
#maisonette
#source
#chambre


    wallCentre = creerPoint(LargCC/2,LongM,HautM/2) # milieu du mur d'interet

    sourceCentreReference = creerPoint(LargCC/2 + r,LongM,HautM/2) - wallCentre

    maxTheta = [][] #stores a max theta for each phi
    for i in range(90):
        for j in range(90):
            maxTheta[i][j] = 90

    for phiDegrees in range(90):
        for thetaDegrees in range(90):
                phi = math.radians(phiDegrees)
                theta = math.radians(thetaDegrees)
                rotationMatrixTheta = np.matrix([[1,0,0],[0,cos(theta),-sin(theta)],[0,sin(theta),cos(theta)]])
                rotationMatrixPhi = np.matrix([[cos(phi),-sin(phi),0],[sin(phi),cos(phi),0],[0,0,1]])
                sourceRotated = rotationMatrixTheta*rotationMatrixPhi*sourceCentreReference
                directionNormale = sourceRotated - wallCentres
                directionNormale = directionNormale/norme_vecteur(directionNormale)
                roll = arctan(directionNormale[1]/directionNormale[0])
                pitch = arctan(sqrt(directionNormale[0]**2  + directionNormale[1]**2 )/directionNormale[2])
                if(verifySource(sourceCentre,roll,pitch))#a faire
                    continue
                maxTheta[phiDegrees] = thetaDegrees
                break

'''





from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
from numpy import cross
from entites import *
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
from time import sleep

def face_carre(s1, s2, s3, s4):
    p1 = s1.T.tolist()[0]
    p2 = s2.T.tolist()[0]
    p3 = s3.T.tolist()[0]
    p4 = s4.T.tolist()[0]
    return np.array([p1, p2, p3, p4])

def faces_cube(sommets):
    faces = {}
    faces['xy0'] = face_carre(s1= sommets['S000'], s2= sommets['S100'], s3= sommets['S110'], s4= sommets['S010'])
    faces['xy1'] = face_carre(s1= sommets['S001'], s2= sommets['S101'], s3= sommets['S111'], s4= sommets['S011'])
    faces['x0z'] = face_carre(s1= sommets['S000'], s2= sommets['S100'], s3= sommets['S101'], s4= sommets['S001'])
    faces['x1z'] = face_carre(s1= sommets['S010'], s2= sommets['S110'], s3= sommets['S111'], s4= sommets['S011'])
    faces['0yz'] = face_carre(s1= sommets['S000'], s2= sommets['S010'], s3= sommets['S011'], s4= sommets['S001'])
    faces['1yz'] = face_carre(s1= sommets['S100'], s2= sommets['S110'], s3= sommets['S111'], s4= sommets['S101'])
    return faces

def arete_cube(s1, s2):
    return tuple([coord1, coord2] for coord1, coord2 in zip(s1.get_tuple(), s2.get_tuple()))

def aretes_cube(sommets):
    aretes = {}
    aretes['x00'] = arete_cube(sommets['S000'], sommets['S100'])
    aretes['x01'] = arete_cube(sommets['S001'], sommets['S101'])
    aretes['x10'] = arete_cube(sommets['S010'], sommets['S110'])
    aretes['x11'] = arete_cube(sommets['S011'], sommets['S111'])
    aretes['0y0'] = arete_cube(sommets['S000'], sommets['S010'])
    aretes['0y1'] = arete_cube(sommets['S001'], sommets['S011'])
    aretes['1y0'] = arete_cube(sommets['S100'], sommets['S110'])
    aretes['1y1'] = arete_cube(sommets['S101'], sommets['S111'])
    aretes['00z'] = arete_cube(sommets['S000'], sommets['S001'])
    aretes['01z'] = arete_cube(sommets['S010'], sommets['S011'])
    aretes['10z'] = arete_cube(sommets['S100'], sommets['S101'])
    aretes['11z'] = arete_cube(sommets['S110'], sommets['S111'])
    return aretes

pave = Box(centre = Vec3(0,0,0),
            ypr_angles = TupleAnglesRotation(0,0,0),
            dimensions = BoxDimensions(2,2,2))

sommets = pave.get_dictionnaire_sommets()

plt.ion()
fig = plt.figure()
ax = fig.gca(projection='3d')

aretes = {}

for arete, sommets_arete in aretes_cube(sommets).items():
    line, = ax.plot(*sommets_arete, color='k', linewidth=3)
    aretes[arete] = line

fig.show()
ax.imshow()
print('!!!!!!!!!!!!!!!!!!!!11')

faces = {}
for face, sommets_face in faces_cube(sommets).items():
    poly = art3d.Poly3DCollection([sommets_face])
    ax.add_collection3d(poly)
    faces[face] = poly
    poly.set_3d_properties()


for face in faces.values():
    ax.collections.remove(face)
