from deprecated import deprecated
from numpy import arcsin, degrees, radians, cos, sin, sqrt

from src.enums import RotationOrderEnum, AngleUnityEnum, BoxVertexEnum
from src.math_entities import Vec3, Orientation, Point, MobilePoint, AbsMobilePointFollower


class BoxDimensions:
    """Length, width, height. Imutable."""

    def __init__(self, length: float, width: float, height: float):
        """Everythin in mm."""
        self._dimensions = {'length': length, 'width': width, 'height': height}

    def __getitem__(self, key):
        """Key e {length, width, height}."""
        return self._dimensions[key]

    def get_tuple(self):
        """Return the tuple (length, width, height)."""
        return self._dimensions['length'], self._dimensions['width'], self._dimensions['height']

    @property
    def length(self) -> float:
        return self._dimensions['length']

    @property
    def width(self) -> float:
        return self._dimensions['width']

    @property
    def height(self) -> float:
        return self._dimensions['height']


class Box(AbsMobilePointFollower):

    def _on_notify(self, p: MobilePoint):
        pass

    noms_sommets_pave = ('S000', 'S001', 'S010', 'S011', 'S100', 'S101', 'S110', 'S111')

    @staticmethod
    def point_appartient_pave_origine(point, dimensions: BoxDimensions) -> bool:
        """
        Fonction qui teste si un point est dans le volume d'un pavé localisé à l'origine.
        :param point:
        :param dimensions: (dictionnaire) length, width, height du pave de la source
        :return: False/True
        """
        long, larg, haut = dimensions.get_tuple()
        demi_long, demi_larg, demi_haut = long / 2, larg / 2, haut / 2
        x, y, z = point.get_tuple()

        return -demi_long <= x <= demi_long and \
               -demi_larg <= y <= demi_larg and \
               -demi_haut <= z <= demi_haut

    def __init__(self, centre: MobilePoint, ypr_angles: Orientation, dimensions: BoxDimensions):
        self.centre = centre
        self.ypr_angles = ypr_angles
        self.dimensions = dimensions
        self.sommets_origine = self.set_sommets_pave_origine()
        self.points = self.get_sommets_pave()

    def rotate(self, delta_yaw, delta_pitch, delta_row):
        self.ypr_angles.incrementer(delta_yaw, delta_pitch, delta_row)
        self.update_sommets()

    def translate(self, delta_x, delta_y, delta_z):
        self.centre += Vec3(delta_x, delta_y, delta_z)
        self.update_sommets()

    def set_position(self, centre):
        self.centre = centre
        self.update_sommets()

    def set_angles(self, ypr_angles):
        self.ypr_angles = ypr_angles
        self.update_sommets()

    def changer_systeme_repere_pave_vers_globale(self, point):
        # matrice de rotation
        Rot = self.ypr_angles.get_matrice_rotation()

        res = (Rot * point) + self.centre

        # il faut faire ça sinon le retour est une matrice rot
        return Vec3(res.__getitem__((0, 0)), res.__getitem__((1, 0)), res.__getitem__((2, 0)))

    def set_sommets_pave_origine(self):
        # dimensions
        long, larg, haut = self.dimensions.get_tuple()

        # points (coins) du pavé centré dans l'origine
        s000 = Vec3(- long / 2, - larg / 2, - haut / 2)
        s100 = Vec3(+ long / 2, - larg / 2, - haut / 2)
        s010 = Vec3(- long / 2, + larg / 2, - haut / 2)
        s110 = Vec3(+ long / 2, + larg / 2, - haut / 2)
        s001 = Vec3(- long / 2, - larg / 2, + haut / 2)
        s101 = Vec3(+ long / 2, - larg / 2, + haut / 2)
        s011 = Vec3(- long / 2, + larg / 2, + haut / 2)
        s111 = Vec3(+ long / 2, + larg / 2, + haut / 2)

        # points (coins) de la source repérés par rapport à son centre
        return [s000, s001, s010, s011, s100, s101, s110, s111]

    def sommets_pave_origine(self):
        return self.sommets_origine

    def get_centre(self):
        return self.centre

    def get_sommets_pave(self):
        """
        convention utilisé pour les rotations : z-y’-x″ (intrinsic rotations) = Yaw, pitch, and roll rotations
        http://planning.cs.uiuc.edu/node102.html
        http://planning.cs.uiuc.edu/node104.html
        https://en.wikipedia.org/wiki/Euler_angles#Tait.E2.80.93Bryan_angles
        https://en.wikipedia.org/wiki/Euler_angles#Rotation_matrix

        On suppose qu'on veut orienter le centre de la source par des angles
        et la position du centre, on calcule les positios des points (les coins de la source).
        :return: liste des points de la source par rapport au système de repère de la chambre
        """

        s_origine = self.sommets_pave_origine()
        return [self.changer_systeme_repere_pave_vers_globale(s) for s in s_origine]

    def sommets_pave(self):
        return self.points

    @deprecated
    def get_dictionnaire_sommets(self):
        return {nom: sommet for nom, sommet in zip(self.noms_sommets_pave, self.points)}

    def get_dict_vertex_point(self) -> bool:
        return {vertex: point for vertex, point in zip(BoxVertexEnum.list_vertices(), self.points)}

    def is_in_box(self, point: Point) -> bool:
        """Fonction qui teste si un point est dans le volume d'un pavé localisé à l'origine."""
        Rot = self.ypr_angles.get_tuple_angles_pour_inverser_rotation().get_matrice_rotation()

        point_repere_pave = Rot * (point - self.centre)

        # il faut faire ça parce que l'operation cidessus renvoie une matrice rotation
        point_repere_pave = Vec3(point_repere_pave.__getitem__((0, 0)),
                                 point_repere_pave.__getitem__((1, 0)),
                                 point_repere_pave.__getitem__((2, 0)))

        return self.point_appartient_pave_origine(point_repere_pave, self.dimensions)

    def test_colision_en_autre_pave(self, pave2, k_discretisation_arete=10):
        """
        Tests if there are points on pave1's faces inside pave2.
        the function needs to be called twice to be sure that there are no intersections
        pave1: dictionary with dimensions(dictionary),centre(matrix 3x1), ypr_angles(dictionary)
        k: (k+1)^2 = number of points to be tested on each face, the greater the k, the plus reliable the result.
        """

        k = k_discretisation_arete

        length, width, height = self.dimensions.get_tuple()

        points_to_be_tested = []

        for i in range(k + 1):
            for j in range(k + 1):
                x = i * length / k
                z = j * height / k
                points_to_be_tested.append(Vec3(x, 0, z))
                points_to_be_tested.append(Vec3(x, width, z))

                x = i * length / k
                y = j * width / k
                points_to_be_tested.append(Vec3(x, y, 0))
                points_to_be_tested.append(Vec3(x, y, height))

                y = i * width / k
                z = j * height / k
                points_to_be_tested.append(Vec3(0, y, z))
                points_to_be_tested.append(Vec3(length, y, z))

        for index in range(len(points_to_be_tested)):
            points_to_be_tested[index] = (self.ypr_angles.get_matrice_rotation()) * points_to_be_tested[index]

            # next line converts from 3d rotation matrix to vecteur3d
            points_to_be_tested[index] = Vec3(points_to_be_tested[index].__getitem__((0, 0)),
                                              points_to_be_tested[index].__getitem__((1, 0)),
                                              points_to_be_tested[index].__getitem__((2, 0)))

            points_to_be_tested[index] = points_to_be_tested[index] + self.centre - Vec3(length / 2, width / 2,
                                                                                         height / 2)

            if pave2.is_in_box(points_to_be_tested[index]):
                return True

        return False

    def intersection_avec_autre_pave(self, pave, k_discretisation_arete=10):

        """
        Tests if there are inserctions between pave1 and pave2,
        pave1: dictionary with dimensions(dictionary),centre(matrix 3x1), ypr_angles(dictionary)
        pave2: dictionary with dimensions(dictionary),centre(matrix 3x1), ypr_angles(dictionary)
        k: (k+1)^2 = number of points to be tested on each face, the greater the k, the more reliable the result
        return True if there are no intersections, returns False otherwise
        """
        if self.test_colision_en_autre_pave(pave, k_discretisation_arete):
            return True

        if pave.test_colision_en_autre_pave(self, k_discretisation_arete):
            return True

        return False
        # FIX POINT_APPARTIENT_PAVE AND POINT_3d

    def entierement_dans_autre_pave(self, autre):
        return all(autre.is_in_box(sommet) for sommet in self.sommets_pave())

    def changer_a_partir_de_coordonnes_spheriques(self, coordonnees_spheriques, systeme_spherique):
        '''
        source changed to self, not sure if it works
        '''
        roh, theta, phi = coordonnees_spheriques.get_coordonnees_spheriques(unite_desiree=AngleUnityEnum.degree)

        # p = centre de la source pour le systeme cartesien à partir du quel le spherique est defini
        p = systeme_spherique.convertir_en_cartesien(coordonnees_spheriques)

        centre_systeme, ypr_angles_systeme = systeme_spherique.get_centre_et_ypr_angles()

        Rot = ypr_angles_systeme.get_tuple_angles_pour_inverser_rotation() \
            .get_matrice_rotation()

        res = Rot * p + centre_systeme

        # il faut faire ça sinon le retour est une matrice rot
        self.centre = Vec3(res.__getitem__((0, 0)), res.__getitem__((1, 0)), res.__getitem__((2, 0)))

        self.ypr_angles = \
            Orientation(
                row=0,
                pitch=phi,
                yaw=theta,
                sequence=RotationOrderEnum.ypr,
                unite=AngleUnityEnum.degree  # !!!!!!!!!!!!!!!!!!!!!!!!
            )

    def update_sommets(self):
        newSommets = []
        Rot = self.ypr_angles.get_matrice_rotation()
        for sommet in self.sommets_origine:
            newPoint = (Rot * sommet) + self.centre
            newSommets.append(newPoint)
        for i in range(len(newSommets)):
            self.points[i].set_xyz(newSommets[i].item(0), newSommets[i].item(1), newSommets[i].item(2))

    @deprecated
    def draw(self):
        pass


class Source(Box):
    def __init__(self, centre, ypr_angles, dimensions):
        super().__init__(centre, ypr_angles, dimensions)
        self.create_parable()

    def get_light_radius(self):
        length, width, height = self.dimensions.get_tuple()
        return height / 2

    def get_light_centre(self):

        return (self.points[5] + self.points[7] + self.points[6] + self.points[
            4]) / 4  # 5,7,6,4 are the verticies of the light face

    def get_light_direction(self):
        return (self.get_light_centre() - self.centre).direction()

    def create_parable(self):  # creates visualization of the parable, must finish!!!!!!!
        length, width, height = self.dimensions.get_tuple()
        r = ((height * height / 4) + length * length) / (2 * length)
        self.angle_ouverture = degrees(arcsin(height / (2 * r)))
        self.points_parable_origin = []
        self.points_parable = []
        rotation = Orientation(0, 90, 0)
        self.points_per_level = 10
        self.angle_levels = 10
        matRot = rotation.get_matrice_rotation()
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
        self.update_sommets()

    def update_sommets(self):
        length, width, height = self.dimensions.get_tuple()
        newSommets = []
        newSommetsParable = []
        Rot = self.ypr_angles.get_matrice_rotation()
        for sommet in self.sommets_origine:
            newPoint = (Rot * sommet) + self.centre
            newSommets.append(newPoint)
        for i in range(len(newSommets)):
            self.points[i].set_xyz(newSommets[i].item(0), newSommets[i].item(1), newSommets[i].item(2))

        for sommet in self.points_parable_origin:
            newPoint = (Rot * sommet) + self.centre
            newSommetsParable.append(newPoint)
        for i in range(len(self.points_parable)):
            self.points_parable[i].set_xyz(newSommetsParable[i].item(0), newSommetsParable[i].item(1),
                                           newSommetsParable[i].item(2))

    deprecated
    def draw(self):
        pass

    @deprecated
    def draw_parable(self, origin):
        pass


class Maisonette(Box):

    def __init__(self, centre, ypr_angles, dimensions, window_dimensions, wall_width=150):
        super().__init__(centre, ypr_angles, dimensions)
        self.window_dimensions = window_dimensions
        self.wall_width = wall_width
        self.set_sommets_inside()

    def set_sommets_inside(self):
        S0 = self.points[0] - Vec3(-self.wall_width, -self.wall_width, -self.wall_width)
        S1 = self.points[1] - Vec3(-self.wall_width, -self.wall_width, self.wall_width)
        S2 = self.points[2] - Vec3(-self.wall_width, self.wall_width, -self.wall_width)
        S3 = self.points[3] - Vec3(-self.wall_width, self.wall_width, self.wall_width)

        S4 = self.points[4] - Vec3(self.wall_width, -self.wall_width, -self.wall_width)
        S5 = self.points[5] - Vec3(self.wall_width, -self.wall_width, self.wall_width)
        S6 = self.points[6] - Vec3(self.wall_width, self.wall_width, -self.wall_width)
        S7 = self.points[7] - Vec3(self.wall_width, self.wall_width, self.wall_width)

        S4 = self.points[4] - Vec3(self.wall_width, -self.wall_width, -self.wall_width)
        S5 = self.points[5] - Vec3(self.wall_width, -self.wall_width, self.wall_width)
        S6 = self.points[6] - Vec3(self.wall_width, self.wall_width, -self.wall_width)
        S7 = self.points[7] - Vec3(self.wall_width, self.wall_width, self.wall_width)

        length, width, height = self.dimensions.get_tuple()

        # window_inside_points

        S8 = self.points[1] - Vec3(-self.wall_width, -(width / 2 - self.window_dimensions['width'] / 2),
                                   (height / 2 - self.window_dimensions['height'] / 2))
        S9 = self.points[3] - Vec3(-self.wall_width, (width / 2 - self.window_dimensions['width'] / 2),
                                   (height / 2 - self.window_dimensions['height'] / 2))
        S10 = self.points[2] - Vec3(-self.wall_width, (width / 2 - self.window_dimensions['width'] / 2),
                                    -(height / 2 - self.window_dimensions['height'] / 2))
        S11 = self.points[0] - Vec3(-self.wall_width, -(width / 2 - self.window_dimensions['width'] / 2),
                                    -(height / 2 - self.window_dimensions['height'] / 2))

        #  window_outside_points

        S12 = self.points[1] - Vec3(0, -(width / 2 - self.window_dimensions['width'] / 2),
                                    (height / 2 - self.window_dimensions['height'] / 2))
        S13 = self.points[3] - Vec3(0, (width / 2 - self.window_dimensions['width'] / 2),
                                    (height / 2 - self.window_dimensions['height'] / 2))
        S14 = self.points[2] - Vec3(0, (width / 2 - self.window_dimensions['width'] / 2),
                                    -(height / 2 - self.window_dimensions['height'] / 2))
        S15 = self.points[0] - Vec3(0, -(width / 2 - self.window_dimensions['width'] / 2),
                                    -(height / 2 - self.window_dimensions['height'] / 2))

        S16 = self.points[0]
        S17 = self.points[1]
        S18 = self.points[2]
        S19 = self.points[3]

        self.sommets_extras = [S0, S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17, S18, S19]

    @deprecated
    def draw_inside(self, origin):
        pass

    @deprecated
    def draw(self, origin):
        pass
