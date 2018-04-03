import numpy as np

from numpy import cos, sin, pi, matrix, sqrt, ndarray, isfinite
from numpy.linalg import norm

from deprecated import deprecated
from copy import deepcopy
from typing import Tuple, Union
from threading import Thread
from abc import ABC, abstractmethod

from src.enums import RotationAngleEnum, AngleUnityEnum, RotationOrderEnum
from src.toolbox.followables import Followable


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
        assert isfinite(x), f'Coordinates must be finite (x = {x}).'
        assert isfinite(y), f'Coordinates must be finite (y = {y}).'
        assert isfinite(z), f'Coordinates must be finite (z = {z}).'
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

    # deepcopy
    def __deepcopy__(self, memodict={}):
        """TODO DOC THIS SHIT (DEBUG OF DEEPCOPY)"""
        x, y, z = self._vec3.get_tuple()
        name = self._name
        dcp = Point(x=x, y=y, z=z, name=name)
        return dcp


# MobilePoint
class MobilePoint(Point, Followable):
    """
    Point with the capability of changing its position dinamically (mutable).
    It keeps followers informed about changes (observer pattern).
    """

    # init
    def __init__(self, x: float, y: float, z: float, name: str = None):
        # Point init (validation in Point)
        Point.__init__(self, x, y, z, name)
        # super(Point, self).__init__(x, y, z, name)
        # followable init
        # super(Followable, self).__init__()
        Followable.__init__(self)

    # set_xyz
    def set_xyz(self, x: float, y: float, z: float):
        """Set all 3 coordinates at a time and notify followers."""
        self._vec3 = Vec3(x, y, z)  # validation in Vec3's __new__
        # notify
        self._notify_followers()

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
        # notify
        self._notify_followers()

    def __deepcopy__(self, memodict={}):
        """TODO DOC THIS SHIT (DEBUG OF DEEPCOPY)"""
        x, y, z = self._vec3.get_tuple()
        name = self._name
        dcp = MobilePoint(x=x, y=y, z=z, name=name)
        return dcp


"""******************************************** deprecated section ******************************************** """
# AbsMobilePointFollower
@deprecated('Use the new class "AbsFollower".')
class AbsMobilePointFollower(ABC):
    """Abstract point follower --> oberver in observer pattern for a mobile point."""

    # CLASS variable - counts the number of existing followers
    _serial_register = 1

    # _on_notify
    @abstractmethod
    def _on_notify(self, p: MobilePoint):
        """Abstract method that takes an action on notification. TO BE OVERWRITTEN."""
        pass

    # init
    def __init__(self):
        """Assign the serial nb (used to uniquely identify a follower)."""
        # assign
        self._serial_nb = AbsMobilePointFollower._serial_register
        # counter ++
        AbsMobilePointFollower._serial_register += 1

    # hash
    def __hash__(self):
        """
        Followers are uniquely identified by the hash of their serial numbers.
        This is done because the mobile points use sets.
        """
        return hash(self._serial_nb)

    # notify
    def notify(self, mobile_point: MobilePoint):
        """Start a new thread to execute the follower's action. Called by the mobile points."""
        p = Thread(target=self._on_notify, args=(mobile_point,))  # create a thread
        p.start()  # start it
        # TODO: remove the join, create a "follower set" --> //ize the followers, but wait until all are done
        p.join()
"""******************************************** deprecated section ******************************************** """


# RotationMatrix
class RotationMatrix(matrix):
    """Rotation matrix for a specific 3D orientation. (immutable)"""

    # *********************************** strings to create matrices in numpy ***********************************
    # rot in X
    _ROTATION_X_STR = '1,   0,    0 ;' + \
                      '0, {c}, -{s} ;' + \
                      '0, {s},  {c}  '

    # rot in Y
    _ROTATION_Y_STR = ' {c}, 0, {s} ;' + \
                      '   0, 1,   0 ;' + \
                      '-{s}, 0, {c}  '

    # rot in Z
    _ROTATION_Z_STR = '{c}, -{s}, 0 ;' + \
                      '{s},  {c}, 0 ;' + \
                      '  0,    0, 1  '

    # switch (dict)
    _ROTATION_STR_SWITCH = {
        RotationAngleEnum.row: _ROTATION_X_STR,
        RotationAngleEnum.pitch: _ROTATION_Y_STR,
        RotationAngleEnum.yaw: _ROTATION_Z_STR
    }
    # *********************************** strings to create matrices in numpy ***********************************

    # new
    def __new__(cls, angle: RotationAngleEnum, value: float, unity: AngleUnityEnum = AngleUnityEnum.degree):
        """Call Matrix's new with a string template."""
        # convert to radians (if necessary) --> for numpy functions
        radians = value if unity == AngleUnityEnum.radian else value * pi / 180
        # format the creation string
        str_ = cls._ROTATION_STR_SWITCH[angle]
        str_ = str_.format(s=sin(radians), c=cos(radians))
        # call the constructor of Matrix
        return super(RotationMatrix, cls).__new__(cls, str_)

    # init
    def __init__(self, angle: RotationAngleEnum, value: float, unity: AngleUnityEnum = AngleUnityEnum.degree):
        """
        Create a new rotation matrix on one of the 3 angles (row, pitch, yaw) of 'value' ['unity'].
        Unity is º by default.
        """
        # check the angle (row, pitch, yaw)
        assert angle != RotationAngleEnum.unknown, f'The rotation angle cannot be unknown.'
        # check the value
        assert isfinite(value), f'Value must be finite (value = {value}).'
        # check the unity
        assert unity != AngleUnityEnum.unknown, f'The angle unity cannot be unknown.'
        # assign attributes
        self._angle = angle
        self._valeur = value
        self._unity = unity

    # * mul
    def __mul__(self, other: Union[Vec3, 'RotationMatrix', Point]) -> Union[Vec3, 'RotationMatrix', Point]:
        """Multiplication. Vec3/Point: rotates it (immutable). RotationMatrix: combined RotationMatrix."""
        # rot mat * vec3
        if type(other) == Vec3:
            return Vec3.vec3_from_ndarray(self.dot(other))  # dot from numpy
        # rot mat * rot mat
        elif type(other) == RotationMatrix:
            return self.dot(other)  # dot from numpy
        # rot mat * point
        elif isinstance(other, Point):
            x, y, z = other.get_tuple()
            x, y, z = (self * Vec3(x, y, z)).get_tuple()
            return Point(x, y, z)
        else:
            raise Exception(f'Operation not defined for {type(self)} * {type(other)}.')

    # + add
    def __add__(self, other):
        """Not defined."""
        raise Exception(f'Operation not defined for {type(self)}.')

    # - sub
    def __sub__(self, other):
        """Not defined."""
        raise Exception(f'Operation not defined for {type(self)}.')

    # / truediv
    def __truediv__(self, other):
        """Not defined."""
        raise Exception(f'Operation not defined for {type(self)}.')

    # deepcopy
    def __deepcopy__(self, memodict={}):
        """TODO DOC THIS SHIT (DEBUG OF DEEPCOPY)"""
        dcp = RotationMatrix(
            angle=self._angle,
            value=self._valeur,
            unity=self._unity
        )


# Orientation
class Orientation(Followable):
    """
    (Mutable) Represents the orientation of a rigid body with 3 rotation angles in a specific order.
    It is followable.
    Cf: https://en.wikipedia.org/wiki/Euler_angles
    Cf: https://en.wikipedia.org/wiki/Aircraft_principal_axes
        http://planning.cs.uiuc.edu/node102.html
        http://planning.cs.uiuc.edu/node104.html
        https://en.wikipedia.org/wiki/Euler_angles#Tait.E2.80.93Bryan_angles
        https://en.wikipedia.org/wiki/Euler_angles#Rotation_matrix
        TODO organize these refs
    """

    # zero
    @staticmethod
    def zero():
        """Zero rotation dans toutes les directions (0, 0, 0)."""
        return Orientation(0.0, 0.0, 0.0)

    # init
    def __init__(self, row: float, pitch: float, yaw: float,
                 order: RotationOrderEnum = RotationOrderEnum.ypr,
                 unity: AngleUnityEnum = AngleUnityEnum.degree):
        """Validate and assign the attributes. """
        # validate values
        assert isfinite(row), f'Angles must be finite (row= {row}).'
        assert isfinite(pitch), f'Angles must be finite (pitch = {pitch}).'
        assert isfinite(yaw), f'Angles must be finite (yaw = {yaw}).'
        # check the order
        assert order != RotationOrderEnum.unknown, f'The rotation order cannot be unknown.'
        # check the unity
        assert unity != AngleUnityEnum.unknown, f'The angle unity cannot be unknown.'
        # assign values
        self._row = row
        self._pitch = pitch
        self._yaw = yaw
        self._order = order
        self._unity = unity
        # this keeps track of changes, which implies recalculation of the rotation matrix
        self._recompute_flag = True
        # compute rotation matrices
        self._compute_rotation_matrices()
        # followable init
        Followable.__init__(self)
        # super(Followable, self).__init__()

    # unity
    @property
    def unity(self) -> AngleUnityEnum:
        """Unity of the angles (º, radians)."""
        return self._unity

    # rotation_matrix
    @property
    def rotation_matrix(self) -> RotationMatrix:
        """Rotation matrix for the combination of rotations."""
        # check if it needs to be recomputed
        if self._recompute_flag:
            # compute them
            self._compute_rotation_matrices()
            # reset flag
            self._recompute_flag = False
        # return
        return self._matrice_rotation

    # inversed_rotation_matrix
    @property
    def inversed_rotation_matrix(self) -> RotationMatrix:
        """Rotation matrix to 'undo' a rotation."""
        # garantie updates if necessary
        _ = self.rotation_matrix
        # get an orientation inversed
        inv_orient = Orientation(
            # values are opposed
            row=-self._row,
            pitch=-self._pitch,
            yaw=-self._yaw,
            # order is reversed
            order=RotationOrderEnum.rpy if self._order == RotationOrderEnum.ypr else
            RotationOrderEnum.ypr if self._order == RotationOrderEnum.rpy else
            RotationOrderEnum.unknown,
            # unity is the same
            unity=self._unity
        )
        # get its rot mat
        rot = inv_orient.rotation_matrix
        # return
        return rot

    # _compute_rotation_matrices
    def _compute_rotation_matrices(self):
        """Internaly compute and update the 3 rotation matrices and the resultant."""
        # row (rotation around x)
        self._matrix_x = RotationMatrix(
            angle=RotationAngleEnum.row,
            value=self._row,
            unity=self._unity
        )
        # pitch (rotation around y)
        self._matrix_y = RotationMatrix(
            angle=RotationAngleEnum.pitch,
            value=self._pitch,
            unity=self._unity
        )
        # yaw (rotation around z)
        self._matrix_z = RotationMatrix(
            angle=RotationAngleEnum.yaw,
            value=self._yaw,
            unity=self._unity
        )
        # resultant rotation matrix
        # multiplication for row-pitch-yaw
        if self._order == RotationOrderEnum.rpy:
            self._matrice_rotation = self._matrix_x.dot(self._matrix_y.dot(self._matrix_z))
        # multiplication for yaw-pitch-row
        elif self._order == RotationOrderEnum.ypr:
            self._matrice_rotation = self._matrix_z.dot(self._matrix_y.dot(self._matrix_x))

    # increment
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
        # notify
        self._notify_followers()

    # angles
    @property
    def angles(self) -> Tuple[float, float, float]:
        """Tuple of the rotation angles in the proper order."""
        # R P Y
        if self._order == RotationOrderEnum.rpy:
            return self._row, self._pitch, self._yaw
        # Y P R
        elif self._order == RotationOrderEnum.ypr:
            return self._yaw, self._pitch, self._row
        # problem
        else:
            raise Exception("The order some how got unknown.")

    # set_angles
    def set_angles(self, angles: Tuple[float, float, float]):
        """Change the angles internaly. The given order is supposed to be the same as in the object."""
        # R P Y
        if self._order == RotationOrderEnum.rpy:
            self._row, self._pitch, self._yaw = angles
        # Y P R
        elif self._order == RotationOrderEnum.ypr:
            self._yaw, self._pitch, self._row = angles
        # problem
        else:
            raise Exception("The order some how got unknown.")
        # notify followers
        self._notify_followers()

    # deepcopy
    def __deepcopy__(self, memodict={}):
        """TODO DOC THIS SHIT (DEBUG OF DEEPCOPY)"""
        dcp = Orientation(
            row=self._row,
            pitch=self._pitch,
            yaw=self._yaw,
            order=self._order,
            unity=self._unity
        )
        return dcp

    """******************************************** deprecated section ******************************************** """
    @deprecated('Use the property angles.')
    def get_angles(self):
        def rpy(): return self._row, self._pitch, self._yaw

        def ypr(): return self._yaw, self._pitch, self._row

        switch = {
            RotationOrderEnum.rpy: rpy,
            RotationOrderEnum.ypr: ypr
        }

        return switch[self._order]()
    """******************************************** deprecated section ******************************************** """


# SphericalCoordinates
class SphericalCoordinates:
    """Point in spherical coordinates (roh, theta, phi). (immutable)"""

    # init
    def __init__(self, roh: float, theta: float, phi: float, unity: AngleUnityEnum = AngleUnityEnum.degree):
        """Roh (mm), theta (unity), phi (unity)."""
        # validate values
        assert isfinite(roh), f'Coordinates must be finite (rho = {rho}).'
        assert isfinite(theta), f'Coordinates must be finite (theta = {theta}).'
        assert isfinite(phi), f'Coordinates must be finite (phi = {phi}).'
        # check the unity
        assert unity != AngleUnityEnum.unknown, f'The angle unity cannot be unknown.'
        # assign attributes
        self.roh = roh
        self.theta = theta
        self.phi = phi
        self.unity = unity

    # get_tuple
    def get_tuple(self, unity: AngleUnityEnum = AngleUnityEnum.degree) -> Tuple[float, float, float]:
        """Return a tuple of (roh, theta, phi) with the angles in the given unity (degree by default)."""
        # check the unity
        assert unity != AngleUnityEnum.unknown, f'The angle unity cannot be unknown.'
        # same unitye
        if unity == self.unity:
            return self.roh, self.theta, self.phi
        # asked degree but is radian
        elif unity == AngleUnityEnum.degree and self.unity == AngleUnityEnum.radian:
            return self.roh, self.theta * 180 / pi, self.phi * 180 / pi
        # asked radian but is degree
        elif unity == AngleUnityEnum.radian and self.unity == AngleUnityEnum.degree:
            return self.roh, self.theta * pi / 180, self.phi * pi / 180
        # problem
        else:
            raise Exception('Could not define the correct unity.')

    # deepcopy
    def __deepcopy__(self, memodict={}):
        """TODO DOC THIS SHIT (DEBUG OF DEEPCOPY)"""
        dcp = SphericalCoordinates(
            roh=self.roh,
            theta=self.theta,
            phi=self.phi,
            unity=self.unity
        )
        return dcp


# SphericalCoordinateSystem
class SphericalCoordinateSystem:
    """Represent a spherical coordinate system located in a cartesian reference frame (origin and orientation)."""

    # init
    def __init__(self, center: Point, orientation: Orientation):
        """Just store the attributes."""
        self._center = center
        self._orientation = orientation

    # center
    @property
    def center(self) -> Point:
        """Copy of the system's center location."""
        return deepcopy(self._center)

    # orientation
    @property
    def orientation(self) -> Orientation:
        """Copy of the system's orientaion."""
        return deepcopy(self._orientation)

    """******************************************** deprecated section ******************************************** """
    @deprecated('Call the properties center and orientation.')
    def get_centre_et_ypr_angles(self):
        return self._center, self._orientation
    """******************************************** deprecated section ******************************************** """

    # to_cartesian
    @staticmethod
    def to_cartesian(spherical_coordianates: SphericalCoordinates) -> Vec3:
        """Transform a spherical coordinate relative to the system into a Vec3 in its own cartesian system."""
        # get the coords
        roh, theta, phi = spherical_coordianates.get_tuple(unity=AngleUnityEnum.radian)
        # x
        x = roh * cos(phi) * cos(theta)
        # y
        y = roh * cos(phi) * sin(theta)
        # z
        z = roh * sin(phi)
        # compute the vector in its own cartesian referential
        vec = Vec3(x, y, z)
        return vec

    # to_global_cartesian
    def to_global_cartesian(self, spherical_coordianates: SphericalCoordinates) -> Vec3:
        """
        Transform a spherical coordinate relative to the system into a Vec3 in
        the GLOBAL system (where the system is referenced.
        """
        # in its own referential
        v_ = self.to_cartesian(spherical_coordianates)
        # rot mat
        rot = self.orientation.rotation_matrix
        # center
        c = self.center
        # in the global's
        v = (rot * v_) + c
        return v

    # deepcopy
    def __deepcopy__(self, memodict={}):
        """TODO DOC THIS SHIT (DEBUG OF DEEPCOPY)"""
        dcp = SphericalCoordinateSystem(
            orientation=deepcopy(self._orientation),
            center=deepcopy(self._center)
        )


@deprecated('Use something from numpy!!!!!')
class SpaceRechercheAnglesLimites:
    # np.arange !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def __init__(self, intervalle_rho, intervalle_phi, intervalle_theta, unite):
        self.intervalle_rho = intervalle_rho
        self.intervalle_phi = intervalle_phi
        self.intervalle_theta = intervalle_theta
        self.unite = unite

    def get_intervalles(self):
        return self.intervalle_rho, self.intervalle_phi, self.intervalle_theta

