from deprecated import deprecated

import numpy as np

from numpy import cos, sin, pi, matrix, sqrt
from numpy.linalg import norm

from src.enums import AngleRotationEnum, UniteAngleEnum, SequenceAnglesRotationEnum


class Vec3(matrix):

    def __new__(cls, x, y, z):
        return super(Vec3, cls).__new__(cls, "{}; {}; {}".format(x, y, z))

    @deprecated
    def set_xyz(self, x, y, z):
        self[0] = x
        self[1] = y
        self[2] = z

    @deprecated
    def get_x(self):
        return self.item(0)

    @deprecated
    def get_y(self):
        return self.item(1)

    @deprecated
    def get_z(self):
        return self.item(2)

    def get_tuple(self):
        return self.item(0), self.item(1), self.item(2)

    def norm(self):
        return norm(self)

    def get_direction(self):
        return self.copy() / self.norm()

    def inner(self, v):
        x1, y1, z1 = self.get_tuple()
        x2, y2, z2 = v.get_tuple()
        return sqrt(x1*x2 + y1*y2 + z1*z2)

    def cross(self, v):
        res = np.cross(self.T, v.T)
        return Vec3(res[0, 0], res[0, 1], res[0, 2])

    def __str__(self):
        return f'Vec3({self[0, 0]}, {self[1, 0]}, {self[2, 0]})'

    def __repr__(self):
        return str(self)


class Point:

    @staticmethod
    def _point_from_vec3(vec: Vec3):
        return Point(*vec.get_tuple())

    def __init__(self, x, y, z):
        self._vec3 = Vec3(x, y, z)

    def set_xyz(self, x, y, z):
        self._vec3 = Vec3(x, y, z)

    def get_x(self):
        return self._vec3.item(0)

    def get_y(self):
        return self._vec3.item(1)

    def get_z(self):
        return self._vec3.item(2)

    def get_tuple(self):
        return self._vec3.get_tuple()

    def __add__(self, other: Vec3):
        return Point._point_from_vec3(self._vec3 + other)

    def __sub__(self, other):
        return self._vec3 - other._vec3

    def __str__(self):
        return f'Point({self.get_x()}, {self.get_y()}, {self.get_z()})'

    def __repr__(self):
        return str(self)


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

        return Vec3(roh * cos(phi) * cos(theta),
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
