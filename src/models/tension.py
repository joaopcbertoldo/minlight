import numpy as np

from src.math_entities import *
from src.models.cables import *


def get_tension(cable0, cable1, cable2, cable3, cable4, cable5, cable6, cable7):
    """
    Function to calculate the tension in each cable.
    Reference: "Closed-form force distribution for parallel wire robots",
    A. Pott, T. Bruckmann, and L. Mikelsons

    :param cable: Instances of the Cable class.

    :return: F, a np.array containing 8 tension values (in Newtons).
    """

    # Source's mass and Earth's gravity
    m = 50.0  # kg
    g = 9.8  # m/s^2

    f_min = np.array([cable0.tension_min,
                      cable1.tension_min,
                      cable2.tension_min,
                      cable3.tension_min,
                      cable4.tension_min,
                      cable5.tension_min,
                      cable6.tension_min,
                      cable7.tension_min])

    f_max = np.array([cable0.tension_max,
                      cable1.tension_max,
                      cable2.tension_max,
                      cable3.tension_max,
                      cable4.tension_max,
                      cable5.tension_max,
                      cable6.tension_max,
                      cable7.tension_max])

    # Equilibrium equation: A^t . F + w = 0, f_min < Fi < f_max, A^t = transpose(A)

    # normalized cable vectors
    u0 = cable0.direction_source_to_fixed
    u1 = cable1.direction_source_to_fixed
    u2 = cable2.direction_source_to_fixed
    u3 = cable3.direction_source_to_fixed
    u4 = cable4.direction_source_to_fixed
    u5 = cable5.direction_source_to_fixed
    u6 = cable6.direction_source_to_fixed
    u7 = cable7.direction_source_to_fixed

    # vectors from center of mass to source's vertex
    b0 = cable0.source_point - centre_masse
    b1 = cable1.source_point - centre_masse
    b2 = cable2.source_point - centre_masse
    b3 = cable3.source_point - centre_masse
    b4 = cable4.source_point - centre_masse
    b5 = cable5.source_point - centre_masse
    b6 = cable6.source_point - centre_masse
    b7 = cable7.source_point - centre_masse

    #A = np.array([
    #    [np.append(u0, np.cross(b0, u0))],
    #    [np.append(u1, np.cross(b1, u1))],
    #    [np.append(u2, np.cross(b2, u2))],
    #    [np.append(u3, np.cross(b3, u3))],
    #    [np.append(u4, np.cross(b4, u4))],
    #    [np.append(u5, np.cross(b5, u5))],
    #    [np.append(u6, np.cross(b6, u6))],
    #    [np.append(u7, np.cross(b7, u7))]
    #]).reshape(8, 6)

    A = np.array([
        [u0.x, u0.y, u0.z, b0.cross(u0).x, b0.cross(u0).y, b0.cross(u0).z],
        [u1.x, u1.y, u1.z, b1.cross(u1).x, b1.cross(u1).y, b1.cross(u1).z],
        [u2.x, u2.y, u2.z, b2.cross(u2).x, b2.cross(u2).y, b2.cross(u2).z],
        [u3.x, u3.y, u3.z, b3.cross(u3).x, b3.cross(u3).y, b3.cross(u3).z],
        [u4.x, u4.y, u4.z, b4.cross(u4).x, b4.cross(u4).y, b4.cross(u4).z],
        [u5.x, u5.y, u5.z, b5.cross(u5).x, b5.cross(u5).y, b5.cross(u5).z],
        [u6.x, u6.y, u6.z, b6.cross(u6).x, b6.cross(u6).y, b6.cross(u6).z],
        [u7.x, u7.y, u7.z, b7.cross(u7).x, b7.cross(u7).y, b7.cross(u7).z]
    ])

    #
    print(b0, u0, b0.cross(u0))

    w = np.array([0, 0, -m * g, 0, 0, 0])

    # algorithme retourne np.array[-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.] si la position n'appartient pas
    # au workspace de la chambre

    if np.linalg.matrix_rank(A) < 6:
        print("Wrench matrix not invertible")
        return -1*np.ones(8)

    f_med = (f_min+f_max)/2

    A_pseudo_transp = np.dot(A, np.linalg.inv(np.dot(np.transpose(A), A)))

    F_v = - np.dot(A_pseudo_transp, w + np.dot(np.transpose(A), f_med))

    F = f_med + F_v

#    for i in range(8):
#        if (F[i] < f_min[i] or F[i] > f_max[i]):
#            print("Cable {} is not in the interval [f_min, f_max]".format(i))
#            return -1 * np.ones(8)

#    if (np.linalg.norm(F_v) > np.linalg.norm(f_med) / 2):
#        print("Tension not feasible")
#        return -1 * np.ones(8)

    return F


# TESTE:
long = 1.0
larg = 1.0
haut = 1.0

point_ancrage = [Point(0.0, 0.0, 5.0), Point(4.0, 0.0, 5.0),
                 Point(4.0, 6.0, 5.0), Point(0.0, 6.0, 5.0)]

centre_masse = Point(2.0, 3.0, 2.5)

# sommet_source = [centre_masse + np.array([-long / 2, -larg / 2, -haut / 2]),
#                 centre_masse + np.array([ long / 2, -larg / 2, -haut / 2]),
#                 centre_masse + np.array([ long / 2,  larg / 2, -haut / 2]),
#                 centre_masse + np.array([-long / 2,  larg / 2, -haut / 2]),
#                 centre_masse + np.array([-long / 2, -larg / 2,  haut / 2]),
#                 centre_masse + np.array([ long / 2, -larg / 2,  haut / 2]),
#                 centre_masse + np.array([ long / 2,  larg / 2,  haut / 2]),
#                 centre_masse + np.array([-long / 2,  larg / 2,  haut / 2])]

sommet_source = [
    MobilePoint(1.5, 2.5, 2.0),
    MobilePoint(2.5, 2.5, 2.0),
    MobilePoint(2.5, 3.5, 2.0),
    MobilePoint(1.5, 3.5, 2.0),
    MobilePoint(1.5, 2.5, 3.0),
    MobilePoint(2.5, 2.5, 3.0),
    MobilePoint(2.5, 3.5, 3.0),
    MobilePoint(1.5, 3.5, 3.0),
]

cable0 = Cable(point_ancrage[0], sommet_source[4], BoxVertexEnum.v001, 1., 10., 100.)
cable1 = Cable(point_ancrage[0], sommet_source[5], BoxVertexEnum.v101, 1., 10., 100.)
cable2 = Cable(point_ancrage[1], sommet_source[5], BoxVertexEnum.v101, 1., 10., 100.)
cable3 = Cable(point_ancrage[1], sommet_source[6], BoxVertexEnum.v111, 1., 10., 100.)
cable4 = Cable(point_ancrage[2], sommet_source[6], BoxVertexEnum.v111, 1., 10., 100.)
cable5 = Cable(point_ancrage[2], sommet_source[7], BoxVertexEnum.v011, 1., 10., 100.)
cable6 = Cable(point_ancrage[3], sommet_source[7], BoxVertexEnum.v011, 1., 10., 100.)
cable7 = Cable(point_ancrage[3], sommet_source[4], BoxVertexEnum.v001, 1., 10., 100.)



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

