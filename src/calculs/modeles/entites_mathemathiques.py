from .enums import *
from numpy import cos, sin, pi, matrix, sqrt
import numpy as np


class Vecteur3D(matrix):

    @staticmethod
    def vecteur_depuis_difference_deux_vecteurs(vecteur_depart, vecteur_arrivee):
        return vecteur_arrivee - vecteur_depart

    def __new__(cls, x, y, z):
        return super(Vecteur3D, cls).__new__(cls, "{}; {}; {}".format(x, y, z))

    def set_xyz(self,x,y,z):

        self[0] = x
        self[1] = y
        self[2] = z

    def get_x(self):
        return self.item(0)

    def get_y(self):
        return self.item(1)

    def get_z(self):
        return self.item(2)

    def get_coordonnees(self):
        return self.item(0), self.item(1), self.item(2)

    def norme(self):
        return sqrt((self.T *self).item((0,0)))

    def get_vecteur_diretion(self):
        return self.copy() / self.norme()

    def scalar_product(self,v):
        return self.item(0)*v.item(0) + self.item(1)*v.item(1) + self.item(2)*v.item(2)

    def normalize(self):
        norme = self.norme()
        self[0] /= norme
        self[1] /= norme
        self[2] /= norme

    def cross(self,v2):
        return Vecteur3D(self[1]*v2[2] , self[2]*v2[0] , self[0]*v2[1])

    def get_nparray(self):
        return np.array([self[0], self[1], self[2]]).reshape(1,3)

    def get_nparray_unitaire(self):
        return np.array([self[0], self[1], self[2]]).reshape(1,3)/self.norme()

class TupleAnglesRotation():

    @staticmethod
    def ZERO():
        '''
        Zero rotation dans toutes les directions.
        :return: TupleAnglesRotation(0,0,0)
        '''
        return TupleAnglesRotation(0,0,0)

    def __init__(self, row, pitch, yaw,
                 sequence = SequenceAnglesRotationEnum.YPR,
                 unite    = UniteAngleEnum.DEGRE):

        self._row      = row
        self._pitch    = pitch
        self._yaw      = yaw
        self._sequence = sequence
        self._unite    = unite
        self._recalculer_matrice = True
        self._matrix_x = MatriceRotation3D(
            angle  = AngleRotationEnum.ROW,
            valeur = self._row,
            unite  = self._unite
        )

        self._matrix_y = MatriceRotation3D(
            angle  = AngleRotationEnum.PITCH,
            valeur = self._pitch,
            unite  = self._unite
        )

        self._matrix_z = MatriceRotation3D(
            angle  = AngleRotationEnum.YAW,
            valeur = self._yaw,
            unite  = self._unite
        )

        if self._sequence == SequenceAnglesRotationEnum.RPY:
            self._matrice_rotation = self._matrix_x.dot(self._matrix_y.dot(self._matrix_z))

        elif self._sequence == SequenceAnglesRotationEnum.YPR:
            self._matrice_rotation = self._matrix_z.dot(self._matrix_y.dot(self._matrix_x))

        else:
            raise Exception('SequenceAnglesRotationEnum inconu')

    def incrementer(self,delta_yaw,delta_pitch,delta_row):
        self._yaw+=delta_yaw
        self._pitch+=delta_pitch
        self._row+=delta_row
        self._recalculer_matrice = True



    def get_angles(self):
        def rpy(): return self._row, self._pitch, self._yaw

        def ypr(): return self._yaw, self._pitch, self._row

        switch = {
            SequenceAnglesRotationEnum.RPY : rpy,
            SequenceAnglesRotationEnum.YPR : ypr
        }

        return switch[self._sequence]()


    def get_unite(self):
        return self._unite


    def get_matrice_rotation(self):
        if self._recalculer_matrice:
            self._matrix_x = MatriceRotation3D(
                angle  = AngleRotationEnum.ROW,
                valeur = self._row,
                unite  = self._unite
            )
            self._matrix_y = MatriceRotation3D(
                angle  = AngleRotationEnum.PITCH,
                valeur = self._pitch,
                unite  = self._unite
            )

            self._matrix_z = MatriceRotation3D(
                angle  = AngleRotationEnum.YAW,
                valeur = self._yaw,
                unite  = self._unite
            )
            if self._sequence == SequenceAnglesRotationEnum.RPY:
                self._matrice_rotation = self._matrix_x.dot(self._matrix_y.dot(self._matrix_z))

            elif self._sequence == SequenceAnglesRotationEnum.YPR:
                self._matrice_rotation = self._matrix_z.dot(self._matrix_y.dot(self._matrix_x))
            self._recalculer_matrice = False
        return self._matrice_rotation


    def get_tuple_angles_pour_inverser_rotation(self):
        return TupleAnglesRotation(
            row      = -self._row,
            pitch    = -self._pitch,
            yaw      = -self._yaw,
            sequence = SequenceAnglesRotationEnum.RPY if self._sequence == SequenceAnglesRotationEnum.YPR else
                       SequenceAnglesRotationEnum.YPR if self._sequence == SequenceAnglesRotationEnum.RPY else
                       SequenceAnglesRotationEnum.INCONU,
            unite    = self._unite
        )


class MatriceRotation3D(matrix):

    ROTATION_X_STR = '1,   0,    0 ;' +\
                     '0, {c}, -{s} ;' +\
                     '0, {s},  {c}  '

    ROTATION_Y_STR = ' {c}, 0, {s} ;' + \
                     '   0, 1,   0 ;' + \
                     '-{s}, 0, {c}  '

    ROTATION_Z_STR = '{c}, -{s}, 0 ;' + \
                     '{s},  {c}, 0 ;' + \
                     '  0,    0, 1  '

    ROTATION_STR_SWITCH = {
        AngleRotationEnum.ROW   : ROTATION_X_STR,
        AngleRotationEnum.PITCH : ROTATION_Y_STR,
        AngleRotationEnum.YAW   : ROTATION_Z_STR
    }


    def __new__(cls, angle, valeur, unite = UniteAngleEnum.DEGRE):
        radians = valeur if unite == UniteAngleEnum.RADIAN else valeur * pi / 180

        str = cls.ROTATION_STR_SWITCH[angle].format(s = sin(radians), c = cos(radians))

        return super(MatriceRotation3D, cls).__new__(cls, str)


    def __init__(self, angle, valeur, unite):
        self._angle  = angle
        self._valeur = valeur
        self._unite  = unite


class CoordonnesSpherique():
    def __init__(self, roh, theta, phi, unite):
        self.roh   = roh
        self.theta = theta
        self.phi   = phi
        self.unite = unite


    def get_coordonnees_spheriques(self, unite_desiree = UniteAngleEnum.INCONU):
        if unite_desiree == self.unite or unite_desiree == UniteAngleEnum.INCONU:
            return self.roh, self.theta, self.phi

        elif unite_desiree == UniteAngleEnum.DEGRE and self.unite == UniteAngleEnum.RADIAN:
            return self.roh, self.theta * 180 / pi, self.phi * 180 / pi

        elif unite_desiree == UniteAngleEnum.RADIAN and self.unite == UniteAngleEnum.DEGRE:
            return self.roh, self.theta * pi / 180, self.phi * pi / 180

        else:
            raise Exception('pbm dunité')


class SystemeRepereSpherique():
    def __init__(self, centre, ypr_angles):
        self.centre     = centre
        self.ypr_angles = ypr_angles


    def get_centre_et_ypr_angles(self):
        return self.centre, self.ypr_angles


    def convertir_en_cartesien(self, coordonnees_spheriques):
        roh, theta, phi = coordonnees_spheriques.get_coordonnees_spheriques(unite_desiree=UniteAngleEnum.RADIAN)

        return Vecteur3D(roh * cos(phi) * cos(theta),
                         roh * cos(phi) * sin(theta),
                         roh * sin(phi))


class IntervalleLineaire():
    def __new__(cls, min, max, pas):
        return np.arange(start=min, stop=max, step=pas)


class SpaceRechercheAnglesLimites():
    def __init__(self, intervalle_rho, intervalle_phi, intervalle_theta, unite):
        self.intervalle_rho   = intervalle_rho
        self.intervalle_phi   = intervalle_phi
        self.intervalle_theta = intervalle_theta
        self.unite            = unite

    def get_intervalles(self):
        return self.intervalle_rho, self.intervalle_phi, self.intervalle_theta
