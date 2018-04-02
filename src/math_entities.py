import numpy as np

from numpy import cos, sin, pi, matrix, sqrt, ndarray, isfinite
from numpy.linalg import norm

from deprecated import deprecated
from copy import deepcopy
from typing import Set, Iterable, Callable, Tuple, Union
from threading import Thread
from abc import ABC, abstractmethod

from src.enums import RotationAngleEnum, AngleUnityEnum, RotationOrderEnum


# Vec3
class Vec3(matrix):
    """3D vector. Used to perform vector operations. (immutable)"""

    @staticmethod
    def zero():
        """Null vector (0, 0, 0)."""
        return Vec3(0, 0, 0)

    @staticmethod
    def vec3_from_ndarray(ndarray_: ndarray) -> 'Vec3':
        """Create a Vec3 from a ndarray's 3 first items."""
        return Vec3(ndarray_.item(0), ndarray_.item(1), ndarray_.item(2))

    # new
    def __new__(cls, x: float, y: float, z: float):
        """Vector 3D from its 3 euclidean coordinates."""
        # validate values
        assert isfinite(x), f"Coordinates must be finite (x = {x})."
        assert isfinite(y), f"Coordinates must be finite (y = {y})."
        assert isfinite(z), f"Coordinates must be finite (z = {z})."
        # create matrix (3,1)
        return super(Vec3, cls).__new__(cls, "{}; {}; {}".format(x, y, z))

    """******************************************** deprecated section ******************************************** """
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
    """******************************************** deprecated section ******************************************** """

    # x
    @property
    def x(self) -> float:
        """The x component (first)."""
        return self.item(0)

    # y
    @property
    def y(self) -> float:
        """The y component (second)."""
        return self.item(1)

    # z
    @property
    def z(self) -> float:
        """The y component (third)."""
        return self.item(2)

    # (x, y, z)
    def get_tuple(self):
        """Return a tuple with the 3 coordinates (x, y, z)."""
        return self.item(0), self.item(1), self.item(2)

    # norm
    @property
    def norm(self) -> float:
        """Euclidean norm of the vector."""
        return norm(self)

    # direction
    @property
    def direction(self) -> 'Vec3':
        """Return a normalized instance of itself (same direction, norm = 1)."""
        # noinspection PyTypeChecker
        return Vec3.vec3_from_ndarray(deepcopy(self) / self.norm)

    # inner product
    def inner(self, v: 'Vec3') -> float:
        """Inner product of self * v ('Scalar product')."""
        x1, y1, z1 = self.get_tuple()
        x2, y2, z2 = v.get_tuple()
        return sqrt(x1 * x2 + y1 * y2 + z1 * z2)

    # cross product
    def cross(self, v: 'Vec3') -> 'Vec3':
        """Cross product of self * v."""
        res = np.cross(self.T, v.T)
        return Vec3(res[0, 0], res[0, 1], res[0, 2])

    # str
    def __str__(self):
        """Vec(x, y, z)"""
        return f'Vec3({self["x"]:.1f}, {self["y"]:.1f}, {self["z"]:.1f})'

    # repr = str
    def __repr__(self):
        """Vec(x, y, z)"""
        return str(self)

    # [] operator
    def __getitem__(self, item):
        """Elements accessible via 0, 1, 2 or x, y, z."""
        # 0 or x
        if item == 0 or str(item).lower() == 'x':
            return self.item(0)
        # 1 or y
        elif item == 1 or str(item).lower() == 'y':
            return self.item(1)
        # 2 or z
        elif item == 2 or str(item).lower() == 'z':
            return self.item(2)
        # error
        else:
            raise IndexError('Elements are only accessible via 0, 1, 2 or x, y, z.')


# Point
class Point:
    """Point 3D. It represents an entity (immutable)."""

    _vec3: Vec3
    _name: str

    @staticmethod
    def _point_from_vec3(vec: Vec3) -> 'Point':
        """Create a Point from a Vec3."""
        return Point(*vec.get_tuple())

    # init
    def __init__(self, x: float, y: float, z: float, name: str = None):
        """Create a Point from its 3 coordinates (x, y, z). Name is optional."""
        # internal Vec3
        self._vec3 = Vec3(x, y, z)  # validation done in Vec3's __new__
        # remove white leading and trilling spaces
        name = name.strip()
        self._name = str(name) if name else ""  # better safe than sorry

    # vec3
    @property
    def vec3(self) -> Vec3:
        """Return a Vec3 of the point (copy). Equivalent to the vector from a supposed origine to the point."""
        return deepcopy(self._vec3)

    """******************************************** deprecated section ******************************************** """
    @deprecated("A Point should not be mutable. Use MobilePoint if needed or calculate a new point.")
    def set_xyz(self, x, y, z):
        """Set all 3 coordinates at a time."""
        self._vec3 = Vec3(x, y, z)
    """******************************************** deprecated section ******************************************** """

    # name
    @property
    def name(self) -> str:
        """Get the name of the point (void string if it doesn't have one)."""
        return self._name

    # x
    @property
    def x(self) -> float:
        """X component (first)."""
        return self._vec3.x

    # y
    @property
    def y(self) -> float:
        """Y component (second)."""
        return self._vec3.y

    # z
    @property
    def z(self) -> float:
        """Z component (third)."""
        return self._vec3.z

    # (x, y, z)
    def get_tuple(self) -> Tuple[float, float, float]:
        """Return a tuple with the 3 coordinates (x, y, z)."""
        return self._vec3.get_tuple()

    # + add
    def __add__(self, other: Vec3) -> 'Point':
        """Addition of a point and a Vec3 (gives a Point). Point + Vec3 = Point."""
        # assert type
        assert type(other) == Vec3, f"Operation undefined for {type(self).__name__} and {type(other).__name__}."
        # compute
        res = Point._point_from_vec3(self._vec3 + other)
        # return
        return res

    # - sub
    def __sub__(self, other: 'Point') -> Vec3:
        """Subtraction of two points (gives a Vector). Point - Point = Vec3."""
        # assert type
        assert isinstance(other, Point), f"Operation undefined for {type(self).__name__} and {type(other).__name__}."
        # compute
        res = self._vec3 - other._vec3
        # return
        return res

    # str
    def __str__(self):
        """name(if present): Point(x, y, z)."""
        str_ = f'{self.name}: ' if self.name else ""
        return str_ + f"Point({self.x:.1f}, {self.y:.1f}, {self.z:.1f})"

    # repr = str
    def __repr__(self):
        """name(if present): Point(x, y, z)."""
        return str(self)


# MobilePoint
class MobilePoint(Point):
    """
    Point with the capability of changing its position dinamically (mutable).
    It keeps followers informed about changes (observer pattern).
    """

    # init
    def __init__(self, x: float, y: float, z: float, name: str = None):
        # Point init (validation in Point)
        super().__init__(x, y, z, name)
        # followers (observers)
        self._followers: Set['AbsMobilePointFollower'] = set()

    # notify
    def _notify(self):
        """Call notify on all the followers."""
        for f in self._followers:
            f.notify(self)

    # subscribe
    def subscribe(self, follower: 'AbsMobilePointFollower'):
        """Subscribe a new follower to the MobilePoint."""
        assert isinstance(follower, AbsMobilePointFollower), f'Follower must be \'{AbsMobilePointFollower.__name__}\'.'
        # update the set
        self._followers.update([follower])

    # subscribe_many
    def subscribe_many(self, followers: Iterable['AbsMobilePointFollower']):
        """Subscribe all the followers."""
        for f in followers:
            self.subscribe(f)

    # set_xyz
    def set_xyz(self, x: float, y: float, z: float):
        """Set all 3 coordinates at a time and notify followers."""
        self._vec3 = Vec3(x, y, z)  # validation in Vec3's __new__
        self._notify()

    # set
    def set(self, position: Union[Point, Vec3]):
        """Set to the given point's (or Vec3's) coordinates and notify followers."""
        assert isinstance(position, Point) or isinstance(position, Vec3), \
            f'position has to be an instance of {Point.__name__} or {Vec3.__name__}.'
        # set it and notify
        self.set_xyz(*position.get_tuple())  # validation in Vec3's __new__

    # increment
    def increment(self, dx: float, dy: float, dz: float):
        """Increment all 3 coordinates at a time and notify followers."""
        dv = Vec3(dx, dy, dz)  # validation in Vec3's __new__
        self._vec3 = self.vec3 + dv
        self._notify()


# AbsMobilePointFollower
class AbsMobilePointFollower(ABC):
    _serial_register = 1

    @abstractmethod
    def _on_notify(self, p: MobilePoint):
        pass

    # def __init__(self, action: Callable[[MobilePoint], None]):
    def __init__(self):
        self._serial_nb = AbsMobilePointFollower._serial_register
        AbsMobilePointFollower._serial_register += 1
        # self._on_notify: Callable[[MobilePoint], None] = action

    def __hash__(self):
        return hash(self._serial_nb)

    def notify(self, mobile_point):
        p = Thread(target=self._on_notify, args=(mobile_point,))
        p.start()


class RotationMatrix(matrix):
    """Rotation matrix for a specific orientation."""

    _ROTATION_X_STR = '1,   0,    0 ;' + \
                      '0, {c}, -{s} ;' + \
                      '0, {s},  {c}  '

    _ROTATION_Y_STR = ' {c}, 0, {s} ;' + \
                      '   0, 1,   0 ;' + \
                      '-{s}, 0, {c}  '

    _ROTATION_Z_STR = '{c}, -{s}, 0 ;' + \
                      '{s},  {c}, 0 ;' + \
                      '  0,    0, 1  '

    _ROTATION_STR_SWITCH = {
        RotationAngleEnum.row: _ROTATION_X_STR,
        RotationAngleEnum.pitch: _ROTATION_Y_STR,
        RotationAngleEnum.yaw: _ROTATION_Z_STR
    }

    def __new__(cls, angle: RotationAngleEnum, valeur: float, unite: AngleUnityEnum = AngleUnityEnum.degree):
        radians = valeur if unite == AngleUnityEnum.radian else valeur * pi / 180
        str_ = cls._ROTATION_STR_SWITCH[angle]
        str_ = str_.format(s=sin(radians), c=cos(radians))
        return super(RotationMatrix, cls).__new__(cls, str_)

    def __init__(self, angle: RotationAngleEnum, valeur: float, unite: AngleUnityEnum = AngleUnityEnum.degree):
        self._angle = angle
        self._valeur = valeur
        self._unite = unite

    def __mul__(self, other):
        # rot mat * vec3
        if type(other) == Vec3:
            return Vec3.vec3_from_ndarray(self.dot(other))
        # rot mat * rot mat
        elif type(other) == RotationMatrix:
            return self.dot(other)
        # rot mat * point
        elif isinstance(other, Point):
            x, y, z = other.get_tuple()
            x, y, z = (self * Vec3(x, y, z)).get_tuple()
            return Point(x, y, z)
        else:
            raise Exception(f'Operation not defined for {type(self)} * {type(other)}.')

    def __add__(self, other):
        raise Exception(f'Operation not defined for {type(self)}.')

    def __sub__(self, other):
        raise Exception(f'Operation not defined for {type(self)}.')

    def __truediv__(self, other):
        raise Exception(f'Operation not defined for {type(self)}.')


class Orientation:
    """(Mutable) Represent the orientation of a rigid body with 3 rotation angles in a specific order."""

    @staticmethod
    def zero():
        """Zero rotation dans toutes les directions (0, 0, 0)."""
        return Orientation(0, 0, 0)

    def __init__(self, row: float, pitch: float, yaw: float,
                 order: RotationOrderEnum = RotationOrderEnum.ypr,
                 unite: AngleUnityEnum = AngleUnityEnum.degree):
        self._row = row
        self._pitch = pitch
        self._yaw = yaw
        self._order = order
        self._unite = unite
        self._recompute_flag = True
        # compute rotation matrices
        self._compute_rotation_matrices()
        assert order == RotationOrderEnum.rpy or order == RotationOrderEnum.ypr, 'RotationOrderEnum inconu.'

    @property
    def unity(self) -> AngleUnityEnum:
        """ """
        return self._unite

    @property
    def rotation_matrix(self) -> RotationMatrix:
        """ """
        # check if it needs to be recomputed
        if self._recompute_flag:
            # compute them
            self._compute_rotation_matrices()
            # reset flag
            self._recompute_flag = False
        # return
        return self._matrice_rotation

    @property
    def inversed_rotation_matrix(self):
        # garantie updates if necessary
        self.rotation_matrix
        # get an orientation inversed
        inv_orient = Orientation(
            row=-self._row,
            pitch=-self._pitch,
            yaw=-self._yaw,
            order=RotationOrderEnum.rpy if self._order == RotationOrderEnum.ypr else
            RotationOrderEnum.ypr if self._order == RotationOrderEnum.rpy else
            RotationOrderEnum.unknown,
            unite=self._unite
        )
        # get its rot mat
        rot = inv_orient.rotation_matrix
        # return
        return rot

    def _compute_rotation_matrices(self):
        """ """
        # row (rotation around x)
        self._matrix_x = RotationMatrix(
            angle=RotationAngleEnum.row,
            valeur=self._row,
            unite=self._unite
        )
        # pitch (rotation around y)
        self._matrix_y = RotationMatrix(
            angle=RotationAngleEnum.pitch,
            valeur=self._pitch,
            unite=self._unite
        )
        # yaw (rotation around z)
        self._matrix_z = RotationMatrix(
            angle=RotationAngleEnum.yaw,
            valeur=self._yaw,
            unite=self._unite
        )
        # resultant rotation matrix
        # multiplication for row-pitch-yaw
        if self._order == RotationOrderEnum.rpy:
            self._matrice_rotation = self._matrix_x.dot(self._matrix_y.dot(self._matrix_z))
        # multiplication for yaw-pitch-row
        elif self._order == RotationOrderEnum.ypr:
            self._matrice_rotation = self._matrix_z.dot(self._matrix_y.dot(self._matrix_x))

    def increment(self, delta_yaw: float, delta_pitch: float, delta_row: float):
        """Increment internal angles. Unity must agree with Rotation object's unity."""
        # validate values
        assert isfinite(delta_yaw), f"Deltas must be finite (delta_yaw = {delta_yaw})."
        assert isfinite(delta_pitch), f"Deltas must be finite (delta_pitch = {delta_pitch})."
        assert isfinite(delta_row), f"Deltas must be finite (delta_row = {delta_row})."
        # yaw
        self._yaw += delta_yaw
        # pitch
        self._pitch += delta_pitch
        # row
        self._row += delta_row
        # rotation matrix must be recalculated
        self._recompute_flag = True

    def get_angles(self):
        def rpy(): return self._row, self._pitch, self._yaw

        def ypr(): return self._yaw, self._pitch, self._row

        switch = {
            RotationOrderEnum.rpy: rpy,
            RotationOrderEnum.ypr: ypr
        }

        return switch[self._order]()


class SphericalCoordinates:
    """Point in spherical coordinates (roh, theta, phi)."""

    def __init__(self, roh: float, theta: float, phi: float, unity: AngleUnityEnum = AngleUnityEnum.degree):
        """Roh (mm), theta (unity), phi (unity)."""
        self.roh = roh
        self.theta = theta
        self.phi = phi
        self.unity = unity

    def get_tuple(self, output_unity: AngleUnityEnum = AngleUnityEnum.degree):
        """Return a tuple of (roh, theta, phi) with the angles in the given unity."""

        if output_unity == self.unity:
            return self.roh, self.theta, self.phi

        elif output_unity == AngleUnityEnum.degree and self.unity == AngleUnityEnum.radian:
            return self.roh, self.theta * 180 / pi, self.phi * 180 / pi

        elif output_unity == AngleUnityEnum.radian and self.unity == AngleUnityEnum.degree:
            return self.roh, self.theta * pi / 180, self.phi * pi / 180

        else:
            raise Exception('Could not define the correct unity.')


class SystemeRepereSpherique:
    def __init__(self, centre, ypr_angles):
        self.centre = centre
        self.ypr_angles = ypr_angles

    def get_centre_et_ypr_angles(self):
        return self.centre, self.ypr_angles

    def convertir_en_cartesien(self, coordonnees_spheriques):
        roh, theta, phi = coordonnees_spheriques.get_tuple(output_unity=AngleUnityEnum.radian)

        return Vec3(roh * cos(phi) * cos(theta),
                    roh * cos(phi) * sin(theta),
                    roh * sin(phi))


class Interval:
    def __new__(cls, a, b, step):
        return np.arange(start=a, stop=b, step=step)


class SpaceRechercheAnglesLimites:
    def __init__(self, intervalle_rho, intervalle_phi, intervalle_theta, unite):
        self.intervalle_rho = intervalle_rho
        self.intervalle_phi = intervalle_phi
        self.intervalle_theta = intervalle_theta
        self.unite = unite

    def get_intervalles(self):
        return self.intervalle_rho, self.intervalle_phi, self.intervalle_theta
