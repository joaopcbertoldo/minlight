from src.calculs.modeles.entites_systeme_minlight import Cable
from src.calculs.modeles.entites_mathemathiques import Vec3

from numpy import sqrt
from numpy.linalg import inv, det
import numpy as np


def get_tension (cable0, cable1, cable2, cable3, cable4, cable5, cable6, cable7):
    '''
    Function to calculate the tension in each cable.
    Reference: "Closed-form force distribution for parallel wire robots",
    A. Pott, T. Bruckmann, and L. Mikelsons

    :param cable: Instances of the Cable class.

    :return: F, a np.array containing 8 tension values (in Newtons).
    '''

    # Source's mass and Earth's gravity
    m = 50.0  # kg
    g = 9.8  # m/s^2

    F_min = np.array([cable0.get_tension_min(),
                      cable1.get_tension_min(),
                      cable2.get_tension_min(),
                      cable3.get_tension_min(),
                      cable4.get_tension_min(),
                      cable5.get_tension_min(),
                      cable6.get_tension_min(),
                      cable7.get_tension_min()])

    F_max = np.array([cable0.get_tension_max(),
                      cable1.get_tension_max(),
                      cable2.get_tension_max(),
                      cable3.get_tension_max(),
                      cable4.get_tension_max(),
                      cable5.get_tension_max(),
                      cable6.get_tension_max(),
                      cable7.get_tension_max()])

    # Equilibrium equation: A^t . F + w = 0, F_min < Fi < F_max, A^t = transpose(A)

    # normalized cable vectors
    u0 = cable0.get_direction_source_to_fixed()
    u1 = cable1.get_direction_source_to_fixed()
    u2 = cable2.get_direction_source_to_fixed()
    u3 = cable3.get_direction_source_to_fixed()
    u4 = cable4.get_direction_source_to_fixed()
    u5 = cable5.get_direction_source_to_fixed()
    u6 = cable6.get_direction_source_to_fixed()
    u7 = cable7.get_direction_source_to_fixed()

    #vectors from center of mass to source's vertex
    b0 = cable0.get_sommet_source() - centre_masse
    b1 = cable1.get_sommet_source() - centre_masse
    b2 = cable2.get_sommet_source() - centre_masse
    b3 = cable3.get_sommet_source() - centre_masse
    b4 = cable4.get_sommet_source() - centre_masse
    b5 = cable5.get_sommet_source() - centre_masse
    b6 = cable6.get_sommet_source() - centre_masse
    b7 = cable7.get_sommet_source() - centre_masse



    A = np.array([
        [np.append(u0, np.cross(b0, u0))],
        [np.append(u1, np.cross(b1, u1))],
        [np.append(u2, np.cross(b2, u2))],
        [np.append(u3, np.cross(b3, u3))],
        [np.append(u4, np.cross(b4, u4))],
        [np.append(u5, np.cross(b5, u5))],
        [np.append(u6, np.cross(b6, u6))],
        [np.append(u7, np.cross(b7, u7))]

        ]).reshape(8, 6)

    w = np.array([0, 0, -m * g, 0, 0, 0])

    # algorithme retourne np.array[-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.] si la position n'appartient pas
    # au workspace de la chambre


    if (np.linalg.matrix_rank(A) < 6):
        return -1*np.ones(8)
        print("Wrench matrix not invertible")

    F_med = (F_min+F_max)/2

    A_pseudo_transp = np.dot(A, np.linalg.inv(np.dot(np.transpose(A), A)))

    F_v = - np.dot(A_pseudo_transp, w + np.dot(np.transpose(A), F_med))

    F = F_med + F_v

#    for i in range(8):
#        if (F[i] < F_min[i] or F[i] > F_max[i]):
#            print("Cable {} is not in the interval [f_min, f_max]".format(i))
#            return -1 * np.ones(8)

#    if (np.linalg.norm(F_v) > np.linalg.norm(F_med) / 2):
#        print("Tension not feasible")
#        return -1 * np.ones(8)

    return F




# TESTE:
long = 1.0
larg = 1.0
haut = 1.0

point_ancrage = [Vec3(0.0, 0.0, 5.0), Vec3(4.0, 0.0, 5.0),
                 Vec3(4.0, 6.0, 5.0), Vec3(0.0, 6.0, 5.0)]

centre_masse = Vec3(2.0, 3.0, 2.5)
#sommet_source = [centre_masse + np.array([-long / 2, -larg / 2, -haut / 2]),
#                 centre_masse + np.array([ long / 2, -larg / 2, -haut / 2]),
#                 centre_masse + np.array([ long / 2,  larg / 2, -haut / 2]),
#                 centre_masse + np.array([-long / 2,  larg / 2, -haut / 2]),
#                 centre_masse + np.array([-long / 2, -larg / 2,  haut / 2]),
#                 centre_masse + np.array([ long / 2, -larg / 2,  haut / 2]),
#                 centre_masse + np.array([ long / 2,  larg / 2,  haut / 2]),
#                 centre_masse + np.array([-long / 2,  larg / 2,  haut / 2])]
sommet_source = [   Vec3(1.5, 2.5, 2.0),
                    Vec3(2.5, 2.5, 2.0),
                    Vec3(2.5, 3.5, 2.0),
                    Vec3(1.5, 3.5, 2.0),
                    Vec3(1.5, 2.5, 3.0),
                    Vec3(2.5, 2.5, 3.0),
                    Vec3(2.5, 3.5, 3.0),
                    Vec3(1.5, 3.5, 3.0),
                 ]

cable0 = Cable(sommet_source[4], "S001", point_ancrage[0], 1., 10., 100.)
cable1 = Cable(sommet_source[5], "S101", point_ancrage[0], 1., 10., 100.)
cable2 = Cable(sommet_source[5], "S101", point_ancrage[1], 1., 10., 100.)
cable3 = Cable(sommet_source[6], "S111", point_ancrage[1], 1., 10., 100.)
cable4 = Cable(sommet_source[6], "S111", point_ancrage[2], 1., 10., 100.)
cable5 = Cable(sommet_source[7], "S011", point_ancrage[2], 1., 10., 100.)
cable6 = Cable(sommet_source[7], "S011", point_ancrage[3], 1., 10., 100.)
cable7 = Cable(sommet_source[4], "S001", point_ancrage[3], 1., 10., 100.)

F = get_tension(
    cable0,
    cable1,
    cable2,
    cable3,
    cable4,
    cable5,
    cable6,
    cable7,
    )
print(F)
print('')

