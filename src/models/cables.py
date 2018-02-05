from typing import List, Dict

from deprecated import deprecated

from src.enums import BoxVertexEnum
from src.math_entities import Point, Vec3
from src.models.boxes import Box
from src.toolbox.useful import solutions_formule_quadratique

DEFAULT_MINIMAL_TENSION = 10.
DEFAULT_MAXIMAL_TENSION = 100.


class CableEnds:
    """Describes the configuration of cable by having the ends to where that cable is attached."""

    def __init__(self, fixed_point: Point, source_vertex: BoxVertexEnum):
        self._source_vertex = source_vertex
        self._fixed_point = fixed_point

    @property
    def fixed_point(self) -> Point:
        return self._fixed_point

    @property
    def source_vertex(self) -> BoxVertexEnum:
        return self._source_vertex

    def __getitem__(self, key):
        if key == 'source_point':
            return self._source_vertex
        elif key == 'fixed_point':
            return self._fixed_point
        else:
            raise KeyError('source_point or fixed_point')


class CableLayout:
    """
    Describes the way that the cables are connected to the source.
    Does a mapping from Fixed Points X Source Vertices consisting of 8 cable ends.
    """

    def __init__(self, cables_ends: List[CableEnds]):
        if len(cables_ends) != 8:
            raise Exception('Exactly 8 cable ends must be given.')
        self._cables_ends = cables_ends


    def get_fixed_point(self, source_vertex: BoxVertexEnum) -> Point:
        """Return the respective fixed point of a certain soruce's vertex."""
        try:
            return next(ce.fixed_point for ce in self._cables_ends if ce.source_vertex == source_vertex)
        except StopIteration:
            raise KeyError(f"Problem with the given {type(source_point)} of value '{source_point}'")

    def get_source_vertex(self, fixed_point_name: str) -> BoxVertexEnum:
        """"""
        try:
            return next(ce.source_vertex for ce in self._cables_ends if ce.fixed_point.name == fixed_point_name)
        except StopIteration:
            raise KeyError(f"The fixed point of name '{fixed_point_name}' does not exist.")

    @deprecated
    def get_cables(self, source_vertices, diameter):
        return [
            Cable(
                source_point=vertex_name,
                fixed_point=self.get_fixed_point(vertex_name).fixed_point,
                source_point=source_vertices[vertex_name],
                diameter=diameter
            )
            for vertex_name in Box.noms_sommets_pave
        ]

    def generate_cables(self, source_vertices_points: Dict[BoxVertexEnum, Point], diameter):
        """Return a list of cables."""
        return [
            Cable(
                fixed_point=self.get_fixed_point(vertex),
                source_point=source_vertices_points[vertex],
                source_vertex=vertex,
                diameter=diameter
            )
            for vertex in BoxVertexEnum.list_vertices()
        ]

    def get_fixed_points(self):
        """Return a list of all fixed points."""
        return [ce.fixed_point for ce in self._cables_ends]

    def get_dict_fixed_points(self):
        return {ce.source_vertex: ce.fixed_point for ce in self._cables_ends}


class Cable:
    """Ideal representation of a cable that is attached at a fixed point and a source vertex."""

    def __init__(self, fixed_point: Point, source_point: Point, source_vertex: BoxVertexEnum,
                 diameter: float, tension_min: float = DEFAULT_MINIMAL_TENSION, tension_max: float = DEFAULT_MAXIMAL_TENSION):
        self.fixed_point = fixed_point
        self.source_point = source_point
        self.source_vertex = source_vertex
        self.diameter = diameter
        self.vector = self.fixed_point - self.source_point
        self.tension_min = tension_min
        self.tension_max = tension_max


    def get_source_point(self):
        return self.source_point

    def fixed_point(self):
        return self.fixed_point

    def get_tension_min(self):
        return self.tension_min

    def get_tension_max(self):
        return self.tension_max

    @deprecated
    def get_vecteur_unitaire(self):
        return self.vector / self.length()

    @property
    def direction_fixed_to_source(self) -> Vec3:
        return self.vector.direction

    @property
    def direction_source_to_fixed(self) -> Vec3:
        return - self.vector.direction

    @property
    def length(self):
        return self.vector.norm

    def get_generator_points_discretisation(self, nombre_points=300, inclure_sommet_ancrage=False,
                                            inclure_sommet_source=False):
        range_min = 0 if inclure_sommet_ancrage else 1
        range_max = nombre_points + (1 if inclure_sommet_source else 0)  # 1 pour compenser l'intervalle ouvert
        linear_range = range(range_min, range_max)
        return (self.fixed_point + (i / nombre_points) * self.vector for i in linear_range)

    def intersects_cable(self, cable2):

        origin = self.fixed_point
        direction = self.fixed_point - self.source_point
        direction = direction.direction()

        normale_plane1 = cable2.point_ancrage - cable2.sommet_source
        point_plane1 = cable2.point_ancrage

        normale_plane2 = cable2.sommet_source - cable2.point_ancrage
        point_plane2 = cable2.sommet_source

        axis = normale_plane2.direction()
        centre = point_plane1

        radius = cable2.diameter / 2 + self.diameter / 2

        a = direction.inner(direction) - direction.inner(axis) ** 2
        b = 2 * (direction.inner(origin - centre) - direction.inner(axis) * axis.inner(origin - centre))
        c = (origin - centre).inner(origin - centre) - axis.inner(origin - centre) ** 2 - radius ** 2

        if b ** 2 - 4 * a * c < 0:
            return False

        solution1, solution2 = solutions_formule_quadratique(a, b, c)
        point1 = origin + solution1 * direction
        point2 = origin + solution2 * direction

        if 0 <= solution1 <= self.length():
            if (normale_plane1.inner(point1 - point_plane1) <= 0) and (
                normale_plane2.inner(point1 - point_plane2) <= 0):
                return True

        if 0 <= solution2 <= self.length():
            if (normale_plane1.inner(point2 - point_plane1) <= 0) and (
                normale_plane2.inner(point2 - point_plane2) <= 0):
                return True

        return False

    def intersection_avec_pave(self, pave,
                               nombre_points_discretisation=100,
                               inclure_sommet_ancrage=False,
                               inclure_sommet_source=False):

        generateur_points = self.get_generator_points_discretisation(nombre_points=nombre_points_discretisation,
                                                                     inclure_sommet_ancrage=inclure_sommet_ancrage,
                                                                     inclure_sommet_source=inclure_sommet_source)
        appartient = [pave.point_appartient_pave(point) for point in generateur_points]
        return any(appartient)
        # return any(pave.point_appartient_pave(point) for point in generateur_points)

    @deprecated
    def entierement_dans_pave(self, pave,
                              nombre_points_discretisation=100,
                              inclure_sommet_ancrage=False,
                              inclure_sommet_source=False):

        generateur_points = self.get_generator_points_discretisation(nombre_points=nombre_points_discretisation,
                                                                     inclure_sommet_ancrage=inclure_sommet_ancrage,
                                                                     inclure_sommet_source=inclure_sommet_source)

        return all(pave.point_appartient_pave(point) for point in generateur_points)

    def is_inside_box(self, box: Box, ends_considered=False):
        if ends_considered:
            e1 = self.fixed_point
            e2 = self.source_point
        else:
            e1 = self.fixed_point + self.direction_fixed_to_source / 1000
            e2 = self.source_point + self.direction_source_to_fixed / 1000
        return box.point_appartient_pave(e1) and box.point_appartient_pave(e2)
