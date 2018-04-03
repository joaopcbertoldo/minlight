from deprecated import deprecated
from copy import deepcopy
from numpy import arcsin, degrees, radians, cos, sin, sqrt, isfinite
from typing import Dict, Tuple, List

from src.enums import RotationOrderEnum, AngleUnityEnum, BoxVertexEnum, BoxVertexOrderEnum
from src.math_entities import Vec3, Orientation, Point, MobilePoint, SphericalCoordinates, SphericalCoordinateSystem
from src.toolbox.followables import AbsFollower
from src.configs import DefaultValues


# BoxDimensions
class BoxDimensions:
    """
    Length, width, height. Imutable.
    Dimensions are defined from a box set in origin and with all sides aligned along with XYZ axis.
        X: length
        Y: width
        Z: height
    """

    # ******************************************* initializaton *******************************************

    # init
    def __init__(self, length: float, width: float, height: float):
        """Everything in mm."""
        # store stuff
        self._dimensions = {'length': length, 'width': width, 'height': height}
        # validate the measures
        self._validate()

    # validate
    def _validate(self):
        """Validate the numeric values of the dimensions."""
        # get the values
        leng, wid, hei = self.get_tuple()
        # check if they are positive
        assert leng <= 0, f"Dimensions must be strictly positive (length = {leng})"
        assert wid <= 0, f"Dimensions must be strictly positive (width = {wid})."
        assert hei <= 0, f"Dimensions must be strictly positive (height = {hei})."
        # check if they are finite
        assert isfinite(leng), f"Dimensions must be finite (length = {leng})."
        assert isfinite(wid), f"Dimensions must be finite (width = {wid})."
        assert isfinite(hei), f"Dimensions must be finite (height = {hei})."

    # ******************************************* operators *******************************************

    # [] operator
    def __getitem__(self, key) -> float:
        """Key e {length, width, height}."""
        return self._dimensions[key]

    # ******************************************* properties *******************************************

    # length
    @property
    def length(self) -> float:
        """Dimension along with X axis when aligned with the reference frame. In mm."""
        return self._dimensions['length']

    # width
    @property
    def width(self) -> float:
        """Dimension along with Y axis when aligned with the reference frame. In mm."""
        return self._dimensions['width']

    # height
    @property
    def height(self) -> float:
        """Dimension along with Z axis when aligned with the reference frame. In mm."""
        return self._dimensions['height']

    # get_tuple
    def get_tuple(self) -> Tuple[float, float, float]:
        """Return the tuple (length, width, height)."""
        return self.length, self.width, self.height


# Box
class Box(AbsFollower):
    """(mutable) Represents a box object that has a 3D position, orientation and one can find its corners (vertices)."""
    # TODO: draw the vertices when box not in origin
    # TODO: define standard order in doc

    # ******************************************* special attributes *******************************************

    # vertices points
    _vertices_points: Dict[BoxVertexEnum, Point]

    # vertices points from self reference frame
    _vertices_points_from_self_ref: Dict[BoxVertexEnum, Point]

    # ******************************************* auxiliar logic *******************************************

    # _is_in_box_at_origin
    @staticmethod
    def _is_in_box_at_origin(point: Point, dimensions: BoxDimensions) -> bool:
        """Auxiliar function that checks if a given point is inside a box supposed in the origin."""
        # get halves of the dimensions
        long, larg, haut = dimensions.get_tuple()
        demi_long, demi_larg, demi_haut = long / 2, larg / 2, haut / 2
        # get the point
        x, y, z = point.get_tuple()
        # check if the point is between +/- the half-measures
        return -demi_long <= x <= demi_long and \
               -demi_larg <= y <= demi_larg and \
               -demi_haut <= z <= demi_haut

    # ******************************************* initialization *******************************************

    # init
    def __init__(self, center: MobilePoint, orientation: Orientation, dimensions: BoxDimensions):
        """Create a box that follows the _center as it moves around."""
        # abstract mobile point follower
        super(AbsFollower, self).__init__()
        # the center
        self._center = center
        # become a follower (to get notifs about changes)
        self._center.subscribe(self)
        # orientation
        self._orientation = orientation
        # become a follower (to get notifs about changes)
        self._orientation.subscribe(self)
        # dimensions
        self._dimensions = dimensions
        # vertices from self point of view
        self._vertices_points_from_self_ref = self._generate_vertex_points_from_self_reference()
        # in global
        self._vertices_points = self._generate_vertex_points_from_self_reference()
        # update them...
        self._update_vertices_points()

    # _generate_vertex_points_from_self_reference
    def _generate_vertex_points_from_self_reference(self) -> Dict[BoxVertexEnum, Point]:
        """(initialization) Dict of BoxVertexEnum -> Point as if they were seen from the box's own reference frame."""
        # dimensions
        l, w, h = self._dimensions.get_tuple()
        # points - corners of the box as if it was at origin
        # cf. doc/vertices_names_notation.pdf
        v000 = Vec3(-l/2, -w/2, -h/2)  # v000
        v100 = Vec3(+l/2, -w/2, -h/2)  # v100
        v010 = Vec3(-l/2, +w/2, -h/2)  # v010
        v110 = Vec3(+l/2, +w/2, -h/2)  # v110
        v001 = Vec3(-l/2, -w/2, +h/2)  # v001
        v101 = Vec3(+l/2, -w/2, +h/2)  # v101
        v011 = Vec3(-l/2, +w/2, +h/2)  # v011
        v111 = Vec3(+l/2, +w/2, +h/2)  # v111
        # the dict itself
        dic = {
            BoxVertexEnum.v000: v000,  # 000
            BoxVertexEnum.v100: v100,  # 100
            BoxVertexEnum.v010: v010,  # 010
            BoxVertexEnum.v110: v110,  # 110
            BoxVertexEnum.v001: v001,  # 001
            BoxVertexEnum.v101: v101,  # 101
            BoxVertexEnum.v011: v011,  # 011
            BoxVertexEnum.v111: v111,  # 111
        }
        return dic

    # ******************************************* properties *******************************************

    # orientation
    @property
    def orientation(self) -> Orientation:
        """Copy of the box's orientation."""
        return deepcopy(self._orientation)

    # dimensions
    @property
    def dimensions(self) -> BoxDimensions:
        """Copy of the box's dimensions."""
        return deepcopy(self._dimensions)

    # center
    @property
    def center(self) -> Point:
        """Copy of the box's center (as immutable point)."""
        x, y, z = self._center.get_tuple()
        return Point(x, y, z)

    # vertices_points_from_self_ref
    @property
    def vertices_points_from_self_ref(self) -> Dict[BoxVertexEnum, Point]:
        """Copy of a Dict of BoxVertexEnum -> Point of the Box's vertices points as seen from its self referential."""
        return deepcopy(self._vertices_points_from_self_ref)

    # vertices_points
    @property
    def vertices_points(self) -> Dict[BoxVertexEnum, Point]:
        """Copy of a Dict of BoxVertexEnum -> Point of the Box's vertices points (in global reference frame)."""
        return deepcopy(self._vertices_points)

    # vertices_points_list
    def vertices_points_list(self, order: BoxVertexOrderEnum) -> List[Point]:
        """List of the vertices points ordered in the given order. Cf BoxVertexOrderEnum."""
        # order of vertices
        vertices = BoxVertexEnum.list_vertices_ordered_as(order)
        # the box's points
        vertices_points = self.vertices_points
        # the list in the correct order
        ret = [vertices_points[vx] for vx in vertices]
        return ret

    # ******************************************* follower action *******************************************

    # _on_notify
    def _on_notify(self, center: MobilePoint):
        """Override on AbsFollower action method."""
        # update the box's points
        self._update_vertices_points()

    # update points
    def _update_vertices_points(self):
        """Recompute the vertices points."""
        #  get the rotation matrix
        Rot = self.orientation.rotation_matrix
        # iterate with the vertices points in origin
        for vertex, point_in_self_ref in self.vertices_points_from_self_ref.items():
            # compute the point
            point = (Rot * point_in_self_ref) + self.center.vec3
            # store it
            self._vertices_points[vertex] = point

    # ******************************************* dynamic changes methods *******************************************

    # rotate
    def rotate(self, delta_yaw: float, delta_pitch: float, delta_row: float):
        """Increment internal rotation. Unity must agree with Rotation object's unity."""
        # increment the rotation
        self._orientation.increment(delta_yaw, delta_pitch, delta_row)
        # _orientation (because the prop is a copy)
        # update the box's points on the orientation's notification

    # translate_center
    def translate_center(self, dx: float, dy: float, dz: float):
        """Increment the _center's coordinates."""
        # increment the mobile point
        self._center.increment(dx, dy, dz)
        # _center (because the prop is a copy)
        # update the box's points on the center's notification

    # set_center_position
    def set_center_position(self, position: Point):
        """Change the box's center position in space."""
        # get coordinates
        x, y, z = position.get_tuple()
        # set the mobile point's coordinates
        self._center.set_xyz(x, y, z)
        # _center (because the prop is a copy)
        # update is done with the notification

    # set_orientation
    def set_orientation(self, orientation: Orientation):
        """Change the box's orientation in space."""
        angles = orientation.angles
        # _orientation (because the prop is a copy)
        self._orientation.set_angles(angles)
        # update is done with the notification

    # set_from_sph_coordinates
    def set_from_sph_coordinates(self, sph_coordinates: SphericalCoordinates, sph_system: SphericalCoordinateSystem):
        """
        Change the boc`s position and orientation.
            Position: point given by the spherical coords.
            Orientation: such that the normal of the positif YZ face points to the system center.
            TODO document the faces names.
        """
        # get the coords
        roh, theta, phi = sph_coordinates.get_tuple(unity=AngleUnityEnum.degree)
        # point in the sph sys referetial
        p = sph_system.to_cartesian(sph_coordinates)
        # center and orientation of the system
        center = sph_system.center
        orientation = sph_system.orientation
        # rot mat
        rot = orientation.rotation_matrix
        # the point in the global ref
        res = (rot * p) + center.vec3
        # check it is a point TODO remove this assert
        assert isinstance(res, Point), 'type problem here'
        # move the box's center
        self.set_center_position(res)
        # temp orientation -- this is done not to deal with angle orders
        temp = Orientation(row=0, pitch=phi, yaw=theta, order=RotationOrderEnum.ypr, unity=self.orientation.unity)
        # rotate it
        self.orientation.set_angles(temp.angles)

    # ******************************************* colision logics *******************************************

    # is_in_box
    def is_in_box(self, point: Point) -> bool:
        """Says wether a given point is inside the box or not."""
        # inv rot mat
        rot_int = self.orientation.inversed_rotation_matrix
        # point from the box's center point of view
        point_from_box = rot_int * (point + (- self.center.vec3))
        # check the type TODO: remove this
        assert isinstance(point_from_box, Point)
        # logic
        return self._is_in_box_at_origin(point_from_box, self.dimensions)

    # _is_coliding (the logic)
    def _is_coliding(self, other_box: 'Box', k_discretisation=None) -> bool:
        """
        Tests if there are points on pave1's faces inside other_box.
        the function needs to be called twice to be sure that there are no intersections
        pave1: dictionary with dimensions(dictionary),_center(matrix 3x1), orientation(dictionary)
        k: (k+1)^2 = number of points to be tested on each face, the greater the k, the plus reliable the result.
        """
        # default value if needed
        k = k_discretisation if k_discretisation else DefaultValues.box_colision_k_dicretisation
        # dimensions
        length, width, height = self.dimensions.get_tuple()
        # points to test
        points_to_be_tested = []
        # create "points" on the faces
        for i in range(k + 1):
            for j in range(k + 1):
                # XZ faces
                x = i * length / k
                z = j * height / k
                points_to_be_tested.append(Vec3(x, 0, z))
                points_to_be_tested.append(Vec3(x, width, z))

                # XY faces
                x = i * length / k
                y = j * width / k
                points_to_be_tested.append(Vec3(x, y, 0))
                points_to_be_tested.append(Vec3(x, y, height))

                # YZ faces
                y = i * width / k
                z = j * height / k
                points_to_be_tested.append(Vec3(0, y, z))
                points_to_be_tested.append(Vec3(length, y, z))

        # test them
        for index in range(len(points_to_be_tested)):
            # rotate the point
            points_to_be_tested[index] = self.orientation.rotation_matrix * points_to_be_tested[index]

            # check type TODO: remove this assert
            assert isinstance(points_to_be_tested[index], Vec3), "problem here with vec3"
            # next line converts from 3d rotation matrix to vecteur3d
            # points_to_be_tested[index] = Vec3(points_to_be_tested[index].__getitem__((0, 0)),
            #                                   points_to_be_tested[index].__getitem__((1, 0)),
            #                                   points_to_be_tested[index].__getitem__((2, 0)))
            halves = Vec3(length / 2, width / 2, height / 2)
            points_to_be_tested[index] = points_to_be_tested[index] + self.center + (-halves)
            # check if the point is in the other
            if other_box.is_in_box(points_to_be_tested[index]):
                return True

        return False

    # is_coliding (the interface)
    def is_coliding(self, other_box: 'Box', k_discretisation=None) -> bool:
        """
        Tests if there are inserctions between pave1 and pave2,
        pave1: dictionary with dimensions(dictionary),_center(matrix 3x1), orientation(dictionary)
        pave2: dictionary with dimensions(dictionary),_center(matrix 3x1), orientation(dictionary)
        k: (k+1)^2 = number of points to be tested on each face, the greater the k, the more reliable the result
        return True if there are no intersections, returns False otherwise
        """
        return self._is_coliding(other_box, k_discretisation) or other_box._is_coliding(self, k_discretisation)

    # is_inside_box
    def is_inside_box(self, other_box: 'Box') -> bool:
        return all(other_box.is_in_box(p) for p in self.vertices_points_list(BoxVertexOrderEnum.standard()))

    """ *********** DEPRECATED *********** DEPRECATED *********** DEPRECATED *********** DEPRECATED *********** """

    @deprecated
    def changer_systeme_repere_pave_vers_globale(self, point):
        pass

    @deprecated('use vertices_points_from_self_ref')
    def set_sommets_pave_origine(self):
        pass

    @deprecated('use vertices_points_from_self_ref')
    def sommets_pave_origine(self):
        pass

    @deprecated('use vertices_points or vertices_points_list')
    def get_sommets_pave(self):
        pass

    @deprecated('use vertices_points_list with order ZYX or XYZ, cf enums and doc')
    def sommets_pave(self):
        pass

    @deprecated('use vertices_points')
    def get_dictionnaire_sommets(self):
        pass

    @deprecated('use the drawable object')
    def draw(self):
        pass


class Source(Box):
    def __init__(self, center, orientation, dimensions):
        super().__init__(center, orientation, dimensions)
        self.create_parable()

    def get_light_radius(self):
        length, width, height = self.dimensions.get_tuple()
        return height / 2

    def get_light_centre(self):
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # pontos da face YZ com X positivo
        points = self.vertices_points_list()
        return (points[5] + points[7] + points[6] + points[
            4]) / 4  # 5,7,6,4 are the verticies of the light face

    def get_light_direction(self):
        return (self.get_light_centre() - self._center).direction()

    def create_parable(self):  # creates visualization of the parable, must finish!!!!!!!
        length, width, height = self.dimensions.get_tuple()
        r = ((height * height / 4) + length * length) / (2 * length)
        self.angle_ouverture = degrees(arcsin(height / (2 * r)))
        self.points_parable_origin = []
        self.points_parable = []
        rotation = Orientation(0, 90, 0)
        self.points_per_level = 10
        self.angle_levels = 10
        matRot = rotation.rotation_matrix()
        for theta in range(0, int(self.angle_ouverture), self.angle_levels):
            for phi in range(0, 360, int(360 / self.points_per_level)):
                theta_rad = radians(theta)
                phi_rad = radians(phi)
                x0 = r * sin(theta_rad) * cos(phi_rad)
                y0 = r * sin(theta_rad) * sin(phi_rad)
                z0 = r * (1 - sqrt(1 - sin(theta_rad) * sin(theta_rad)))
                p = Vec3(x0, y0, z0)
                p = matRot * p - Vec3(length / 2, 0, 0)
                p = Vec3(p.item(0), p.item(1), p.item(2))
                p2 = Vec3(p.item(0), p.item(1), p.item(2))
                self.points_parable_origin.append(p)
                self.points_parable.append(p2)
        self.squares_edges = []
        # for()
        self._update_vertices_points()

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def _update_vertices_points(self):
        length, width, height = self.dimensions.get_tuple()
        newSommets = []
        newSommetsParable = []
        Rot = self.orientation.rotation_matrix()
        for sommet in self.vertices_points_from_self_ref:
            newPoint = (Rot * sommet) + self._center
            newSommets.append(newPoint)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        for i in range(len(newSommets)):
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # pontos da face YZ com X positivo
            self.vertices_points_list[i].set_xyz(newSommets[i].item(0), newSommets[i].item(1), newSommets[i].item(2))

        for sommet in self.points_parable_origin:
            newPoint = (Rot * sommet) + self._center
            newSommetsParable.append(newPoint)
        for i in range(len(self.points_parable)):
            self.points_parable[i].set_xyz(newSommetsParable[i].item(0), newSommetsParable[i].item(1),
                                           newSommetsParable[i].item(2))

    @deprecated
    def draw(self):
        pass

    @deprecated
    def draw_parable(self, origin):
        pass


class Maisonette(Box):

    def __init__(self, center, orientation, dimensions, window_dimensions, wall_width=150):
        super().__init__(center, orientation, dimensions)
        self.window_dimensions = window_dimensions
        self.wall_width = wall_width
        self.set_sommets_inside()

    def set_sommets_inside(self):
        points = self.vertices_points_list(BoxVertexOrderEnum.ZYX)
        S0 = points[0] - Vec3(-self.wall_width, -self.wall_width, -self.wall_width)
        S1 = points[1] - Vec3(-self.wall_width, -self.wall_width, self.wall_width)
        S2 = points[2] - Vec3(-self.wall_width, self.wall_width, -self.wall_width)
        S3 = points[3] - Vec3(-self.wall_width, self.wall_width, self.wall_width)

        S4 = points[4] - Vec3(self.wall_width, -self.wall_width, -self.wall_width)
        S5 = points[5] - Vec3(self.wall_width, -self.wall_width, self.wall_width)
        S6 = points[6] - Vec3(self.wall_width, self.wall_width, -self.wall_width)
        S7 = points[7] - Vec3(self.wall_width, self.wall_width, self.wall_width)

        length, width, height = self.dimensions.get_tuple()

        # window_inside_points

        S8 = points[1] - Vec3(-self.wall_width, -(width / 2 - self.window_dimensions['width'] / 2),
                                                    (height / 2 - self.window_dimensions['height'] / 2))
        S9 = points[3] - Vec3(-self.wall_width, (width / 2 - self.window_dimensions['width'] / 2),
                                                    (height / 2 - self.window_dimensions['height'] / 2))
        S10 = points[2] - Vec3(-self.wall_width, (width / 2 - self.window_dimensions['width'] / 2),
                                                     -(height / 2 - self.window_dimensions['height'] / 2))
        S11 = points[0] - Vec3(-self.wall_width, -(width / 2 - self.window_dimensions['width'] / 2),
                                                     -(height / 2 - self.window_dimensions['height'] / 2))

        #  window_outside_points

        S12 = points[1] - Vec3(0, -(width / 2 - self.window_dimensions['width'] / 2),
                                                     (height / 2 - self.window_dimensions['height'] / 2))
        S13 = points[3] - Vec3(0, (width / 2 - self.window_dimensions['width'] / 2),
                                                     (height / 2 - self.window_dimensions['height'] / 2))
        S14 = points[2] - Vec3(0, (width / 2 - self.window_dimensions['width'] / 2),
                                                     -(height / 2 - self.window_dimensions['height'] / 2))
        S15 = points[0] - Vec3(0, -(width / 2 - self.window_dimensions['width'] / 2),
                                                     -(height / 2 - self.window_dimensions['height'] / 2))

        S16 = points[0]
        S17 = points[1]
        S18 = points[2]
        S19 = points[3]

        self.sommets_extras = [S0, S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17, S18, S19]

    @deprecated
    def draw_inside(self, origin):
        pass

    @deprecated
    def draw(self, origin):
        pass
