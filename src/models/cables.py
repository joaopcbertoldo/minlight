from typing import List, Dict, Generator
from copy import deepcopy
from deprecated import deprecated

from numpy import isfinite

from src.enums import BoxVertexEnum
from src.math_entities import Point, Vec3, MobilePoint
from src.models.boxes import Box
from src.toolbox.useful import solutions_formule_quadratique
from src.configs import DefaultValues
from src.toolbox.followables import AbsFollower


# CableEnds
class CableEnds:
    """Describes the configuration of cable by having the ends to where that cable is attached."""

    # init
    def __init__(self, fixed_point: Point, source_vertex: BoxVertexEnum):
        """Assign internal attributes. Fixed point is the one attached to the room and the vertex is to the source."""
        self._source_vertex = source_vertex
        self._fixed_point = fixed_point

    # fixed_point
    @property
    def fixed_point(self) -> Point:
        """Return the fixed point (no need of copy cuz points are immutable)."""
        return self._fixed_point

    # source_vertex
    @property
    def source_vertex(self) -> BoxVertexEnum:
        """Return the source's vertex."""
        return self._source_vertex

    # [] operator
    def __getitem__(self, key):
        """Return one of the two attributes."""
        # source_point
        if key == 'source_point':
            return self._source_vertex
        # fixed_point
        elif key == 'fixed_point':
            return self._fixed_point
        # problem
        else:
            raise KeyError('source_point or fixed_point')


# CableLayout
class CableLayout:
    """
    Describes the way that the cables are connected to the source.
    Does a mapping from Fixed Points X Source Vertices consisting of 8 cable ends.
    """

    # init
    def __init__(self, cables_ends: List[CableEnds], diameter: float = None):
        """"""
        # validations
        assert len(cables_ends) == 8, 'Exactly 8 cable ends must be given.'
        assert all(type(ce) == CableEnds for ce in cables_ends), f'cable ends must be of type {CableEnds.__name__}.'
        if diameter:
            assert isfinite(diameter) and diameter > 0, f'invalid diameter ({diameter})'
        # assign attributes
        self._cables_ends = cables_ends
        self._diameter = diameter if diameter else DefaultValues.cable_diameter

    # get_fixed_point
    def get_fixed_point(self, source_vertex: BoxVertexEnum) -> Point:
        """Return the respective fixed point of a certain soruce's vertex."""
        try:
            # find it
            return next(ce.fixed_point for ce in self._cables_ends if ce.source_vertex == source_vertex)
        except StopIteration:
            raise KeyError(f"Problem with the given {type(source_vertex).__name__} of value '{source_vertex}'")

    # get_source_vertex
    def get_source_vertex(self, fixed_point_name: str) -> BoxVertexEnum:
        """TODO doc str"""
        try:
            # find it
            return next(ce.source_vertex for ce in self._cables_ends if ce.fixed_point.name == fixed_point_name)
        except StopIteration:
            raise KeyError(f"The fixed point of name '{fixed_point_name}' does not exist.")

    # generate_cables
    def generate_cables(self, source_vertices_points: Dict[BoxVertexEnum, Point],
                        diameter: float = None) -> List['Cable']:
        """Return a list of cables connection the cable layout to the given source vertices (with diameter in mm)."""
        if diameter:
            assert isfinite(diameter) and diameter > 0, f'invalid diameter ({diameter})'
        # ensure a value
        diameter = diameter if diameter else self._diameter
        # ret
        return [
            Cable(
                fixed_point=self.get_fixed_point(vertex),
                source_point=source_vertices_points[vertex],
                source_vertex=vertex,
                diameter=diameter
            )
            for vertex in BoxVertexEnum.list_vertices()
        ]

    # get_fixed_points
    def get_fixed_points(self) -> List[Point]:
        """Return a list of all fixed points. TODO to property"""
        return [ce.fixed_point for ce in self._cables_ends]

    # get_dict_fixed_points
    def get_dict_fixed_points(self):
        """Return a dict that maps source vertices to fixed points. TODO to property"""
        return {ce.source_vertex: ce.fixed_point for ce in self._cables_ends}

    @deprecated('use generate cables')
    def get_cables(self, source_points, diameter):
        pass


# Cable
class Cable(AbsFollower):
    """Ideal representation of a cable that is attached at a fixed point and a source vertex."""
    default_discretisation_number_of_points_box_intersection = 100

    # init
    def __init__(self, fixed_point: Point, source_point: MobilePoint, source_vertex: BoxVertexEnum,
                 diameter: float = None, tension_min: float = None, tension_max: float = None):
        """TODO doc str"""
        # super
        AbsFollower.__init__(self)
        # super(AbsFollower, self).__init__()
        # TODO validate cable's init
        # assign attributes
        self._fixed_point = fixed_point
        self._source_mobile_point = source_point
        self._source_vertex = source_vertex
        self._diameter = diameter if diameter else DefaultValues.cable_diameter
        self._tension_min = tension_min if tension_min else DefaultValues.minimal_tention
        self._tension_max = tension_max if tension_max else DefaultValues.maximal_tention
        # compute its vector
        self._vector = self.fixed_point - self.source_point
        # subscribe to the mobile point
        self._source_mobile_point.subscribe(self)

    # _on_notify (follower action)
    def _on_notify(self, p: MobilePoint):
        """Update the internal vector of its direction."""
        self._vector = self.fixed_point - self.source_point

    # diameter
    @property
    def diameter(self) -> float:
        """Cable's diameter in mm."""
        return self._diameter

    # source_point
    @property
    def source_point(self) -> Point:
        """Return a deepcopy of the source point."""
        return deepcopy(self._source_mobile_point)

    # source_vertex
    @property
    def source_vertex(self) -> BoxVertexEnum:
        """Return the source vertex."""
        return self._source_vertex

    # fixed_point
    @property
    def fixed_point(self) -> Point:
        """Return a deepcopy of the fixed point."""
        return deepcopy(self._fixed_point)

    # tension_min
    @property
    def tension_min(self) -> float:
        """Minimal tension needed in the cable (in Newtons)."""
        return self._tension_min

    # tension_max
    @property
    def tension_max(self) -> float:
        """Maximal tension needed in the cable (in Newtons)."""
        return self._tension_max

    # direction_fixed_to_source
    @property
    def direction_fixed_to_source(self) -> Vec3:
        """Unitary _vector in the direction fixed point -> source point."""
        return self._vector.direction

    # direction_source_to_fixed
    @property
    def direction_source_to_fixed(self) -> Vec3:
        """Unitary _vector in the direction source point -> fixed point."""
        return Vec3.zero() - self._vector.direction

    # length
    @property
    def length(self) -> float:
        """Distance from the fixed point and the source point."""
        return self._vector.norm

    # get_discretisation
    def get_discretisation(self, nb_points: int = None,
                           include_fixed_point=False, include_source_point=False) -> Generator[Point]:
        """Return an iterable of points that are along the cables' line. TODO review method"""
        # check nb_points
        if nb_points:
            assert type(nb_points) == int and nb_points > 0, "nb_points must be an int and > 0."
        nb_points = nb_points if nb_points else DefaultValues.cable_discretisation_nb_points
        # include ends or not
        range_min = 0 if include_fixed_point else 1
        range_max = nb_points + (1 if include_source_point else 0)  # 1 pour compenser l'intervalle ouvert
        # range
        linear_range = range(range_min, range_max)
        # ret the generator
        return (self.fixed_point + (i / nb_points) * self._vector for i in linear_range)

    # intersects_cable
    def intersects_cable(self, cable2: 'Cable') -> bool:
        """Returns whether a cable 2 intersects self. TODO review method"""
        origin = self.fixed_point
        direction = self.fixed_point - self.source_point
        direction = direction.direction

        normale_plane1 = cable2.fixed_point - cable2.source_point
        point_plane1 = cable2.fixed_point

        normale_plane2 = cable2.source_point - cable2.fixed_point
        point_plane2 = cable2.source_point

        axis = normale_plane2.direction
        centre = point_plane1

        radius = cable2.diameter / 2 + self._diameter / 2

        a = direction.inner(direction) - direction.inner(axis) ** 2
        b = 2 * (direction.inner(origin - centre) - direction.inner(axis) * axis.inner(origin - centre))
        c = (origin - centre).inner(origin - centre) - axis.inner(origin - centre) ** 2 - radius ** 2

        if b ** 2 - 4 * a * c < 0:
            return False

        solution1, solution2 = solutions_formule_quadratique(a, b, c)
        point1 = origin + solution1 * direction
        point2 = origin + solution2 * direction

        if 0 <= solution1 <= self.length:
            if (normale_plane1.inner(point1 - point_plane1) <= 0) \
                    and (normale_plane2.inner(point1 - point_plane2) <= 0):
                return True

        if 0 <= solution2 <= self.length:
            if (normale_plane1.inner(point2 - point_plane1) <= 0) \
                    and (normale_plane2.inner(point2 - point_plane2) <= 0):
                return True

        return False

    # intersects_box
    def intersects_box(self, box: Box, nb_points: int = None, include_fixed_point=False, include_source_point=False) \
            -> bool:
        """Wheter a cable intersects a box. Verification done by discretizing the cable in many points. TODO review method"""
        # check nb_points
        if nb_points:
            assert type(nb_points) == int and nb_points > 0, "nb_points must be an int and > 0."
        nb_points = nb_points if nb_points else DefaultValues.cable_discretisation_nb_points_box_intersection

        dicretisation = self.get_discretisation(nb_points=nb_points,
                                                include_fixed_point=include_fixed_point,
                                                include_source_point=include_source_point)
        appartient = (box.is_in_box(point) for point in dicretisation)
        return any(appartient)

    # is_inside_box
    def is_inside_box(self, box: Box, ends_considered=False) -> bool:
        """Wheter a cable is entirely inside a box."""
        if ends_considered:
            e1 = self.fixed_point
            e2 = self.source_point
        else:
            e1 = self.fixed_point + self.direction_fixed_to_source / 1000
            e2 = self.source_point + self.direction_source_to_fixed / 1000
        return box.is_in_box(e1) and box.is_in_box(e2)

    @deprecated('use is_inside_box')
    def entierement_dans_pave(self, pave,
                              nombre_points_discretisation=100,
                              inclure_sommet_ancrage=False,
                              inclure_sommet_source=False):

        generateur_points = self.get_discretisation(nb_points=nombre_points_discretisation,
                                                    include_fixed_point=inclure_sommet_ancrage,
                                                    include_source_point=inclure_sommet_source)

        return all(pave.is_in_box(point) for point in generateur_points)

    @deprecated
    def get_vecteur_unitaire(self):
        pass
