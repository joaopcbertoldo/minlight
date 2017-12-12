from numpy import sqrt
from numpy.linalg import inv, det
import numpy as np

# testando com classe cabo abaixo

class Cable:

    def __init__(self, point_ancrage, sommet_source, tension_min, tension_max):
        self.point_ancrage     = point_ancrage
        self.sommet_source     = sommet_source
        self.vecteur           = np.array ([self.point_ancrage[0]-self.sommet_source[0],
                                            self.point_ancrage[1]-self.sommet_source[1],
                                            self.point_ancrage[2]-self.sommet_source[2]])
        self.tension_min = tension_min
        self.tension_max = tension_max

    def longueur(self):
        return sqrt(self.vecteur[0] * self.vecteur[0] +
                    self.vecteur[1] * self.vecteur[1] +
                    self.vecteur[2] * self.vecteur[2])

    def get_sommet_source (self):
        return self.sommet_source

    def get_point_ancrage(self):
        return self.point_ancrage

# adicionei esses metodos

    def get_tension_min(self):
        return self.tension_min

    def get_tension_max(self):
        return self.tension_max

    def get_unitaire(self):
        return self.vecteur / self.longueur()
                    #-----------------------------------------------------


# Calculer les tensions F :

def get_tension (cable0, cable1, cable2, cable3, cable4, cable5, cable6, cable7):
    '''

    :param cable0:
    :param cable1:
    :param cable2:
    :param cable3:
    :param cable4:
    :param cable5:
    :param cable6:
    :param cable7:
    :return: F, un np.array contenant 8 valeurs de tension de chaque cable
    '''

    # masse du cube et gravité de la Terre
    m = 2.0  # kg
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

    # eq de l'equilibre: A^t . F + w = 0, F_min < Fi < F_max, A^t = transpose(A)

    A = np.array([
        [np.append(cable0.get_unitaire(), np.cross(cable0.get_sommet_source() - centre_masse, cable0.get_unitaire()))],
        [np.append(cable1.get_unitaire(), np.cross(cable1.get_sommet_source() - centre_masse, cable1.get_unitaire()))],
        [np.append(cable2.get_unitaire(), np.cross(cable2.get_sommet_source() - centre_masse, cable2.get_unitaire()))],
        [np.append(cable3.get_unitaire(), np.cross(cable3.get_sommet_source() - centre_masse, cable3.get_unitaire()))],
        [np.append(cable4.get_unitaire(), np.cross(cable4.get_sommet_source() - centre_masse, cable4.get_unitaire()))],
        [np.append(cable5.get_unitaire(), np.cross(cable5.get_sommet_source() - centre_masse, cable5.get_unitaire()))],
        [np.append(cable6.get_unitaire(), np.cross(cable6.get_sommet_source() - centre_masse, cable6.get_unitaire()))],
        [np.append(cable7.get_unitaire(), np.cross(cable7.get_sommet_source() - centre_masse, cable7.get_unitaire()))]
    ]).reshape(8, 6)

    w = np.array([0, 0, -m * g, 0, 0, 0])

    # algorithme retourne np.array[-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.] si la position n'appartient pas
    # au workspace de la chambre


    if (np.linalg.matrix_rank(A) < 6):
        return -1*np.ones(8)
        print("Wrench matrix not invetible")

    F_med = (F_min+F_max)/2

    A_pseudo_transp = np.dot(A, np.linalg.inv(np.dot(np.transpose(A), A)))

    F_v = - np.dot(A_pseudo_transp, w + np.dot(np.transpose(A), F_med))

    F = F_med + F_v

    for i in range(8):
        if (F[i] < F_min[i] or F[i] > F_max[i]):
            print("Cable {} is not in the interval [f_min, f_max]".format(i))
            return -1 * np.ones(8)

    if (np.linalg.norm(F_v) > np.linalg.norm(F_med) / 2):
        print("Tension not feasible")
        return -1 * np.ones(8)

    return F



# TESTE:


long = 1.0
larg = 1.0
haut = 1.0

point_ancrage = [np.array([0.0, 0.0, 5.0]), np.array([4.0, 0.0, 5.0]),
                 np.array([4.0, 6.0, 5.0]), np.array([0.0, 6.0, 5.0])]

centre_masse = np.array([2.0, 3.0, 2.5])

sommet_source = [centre_masse + np.array([-long / 2, -larg / 2, -haut / 2]),
                 centre_masse + np.array([ long / 2, -larg / 2, -haut / 2]),
                 centre_masse + np.array([ long / 2,  larg / 2, -haut / 2]),
                 centre_masse + np.array([-long / 2,  larg / 2, -haut / 2]),
                 centre_masse + np.array([-long / 2, -larg / 2,  haut / 2]),
                 centre_masse + np.array([ long / 2, -larg / 2,  haut / 2]),
                 centre_masse + np.array([ long / 2,  larg / 2,  haut / 2]),
                 centre_masse + np.array([-long / 2,  larg / 2,  haut / 2])]

# cables de chaque sommet

cable0 = Cable(point_ancrage[0], sommet_source[4], 1., 100.)
cable1 = Cable(point_ancrage[0], sommet_source[5], 1., 100.)
cable2 = Cable(point_ancrage[1], sommet_source[5], 1., 100.)
cable3 = Cable(point_ancrage[1], sommet_source[6], 1., 100.)
cable4 = Cable(point_ancrage[2], sommet_source[6], 1., 100.)
cable5 = Cable(point_ancrage[2], sommet_source[7], 1., 100.)
cable6 = Cable(point_ancrage[3], sommet_source[7], 1., 100.)
cable7 = Cable(point_ancrage[3], sommet_source[4], 1., 100.)


F = get_tension(cable0,
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
