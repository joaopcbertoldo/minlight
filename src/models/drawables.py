# from OpenGL.GL import *
from OpenGL.GL import glBegin, glColor4fv, glNormal3fv, glVertex3fv, glEnd
from OpenGL.raw.GL.ARB.tessellation_shader import GL_QUADS
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_LINES

from src.models.cables import Cable
from src.models.boxes import Box, Source, Maisonette
from src.toolbox.useful import get_plane_normal
from src.visualization.outils import Surface


class DrawableCable(Cable):

    def draw(self, origin):
        edge = (0, 1)
        verticies = (
            self.source_point - origin, self.fixed_point - origin
        )
        glBegin(GL_LINES)
        for vertex in edge:
            glColor4fv((0.5, 0.5, 0.3, 1.0))
            glNormal3fv((0.0, 0.0, 0.0))
            glVertex3fv(verticies[vertex])
        glEnd()


class DrawableBox(Box):
    def draw(self, origin, color=(0.45, 0.45, 0.45, 1.0), drawFaces=True):
        edges = (
            (0, 1),
            (0, 2),
            (0, 4),
            (1, 3),
            (1, 5),
            (7, 3),
            (7, 5),
            (7, 6),
            (6, 2),
            (6, 4),
            (3, 2),
            (5, 4)
        )
        surfaces = (
            (0, 2, 6, 4),
            (5, 7, 3, 1),
            (4, 6, 7, 5),
            (1, 3, 2, 0),
            (6, 2, 3, 7),
            (1, 0, 4, 5)
        )

        verticies = self.sommets_pave()
        verticiesInOrigin = []

        for v in verticies:
            verticiesInOrigin.append(v - origin)

        if drawFaces:
            glBegin(GL_QUADS)
            for surface in surfaces:
                normal = get_plane_normal(surface, self.vertices_points_as_list, self._center)
                normal_tuple = normal.get_tuple()
                for vertex in surface:
                    glColor4fv(color)
                    glNormal3fv(normal_tuple)
                    glVertex3fv(verticiesInOrigin[vertex])
            glEnd()

        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glColor4fv((0.0, 0.0, 0.0, 1.0))
                glNormal3fv((0.0, 0.0, 0.0))
                glVertex3fv(verticiesInOrigin[vertex])
        glEnd()


class Chambre(Box):
    def __init__(self, center, orientation, dimensions):
        super().__init__(center, orientation, dimensions)

    def draw(self, origin, color=(0.2, 0.2, 0.2, 1.0), drawFaces=True):
        edges = (
            (0, 1),
            (0, 2),
            (0, 4),
            (1, 3),
            (1, 5),
            (7, 3),
            (7, 5),
            (7, 6),
            (6, 2),
            (6, 4),
            (3, 2),
            (5, 4)
        )
        ground = (4, 6, 2, 0)

        normal = get_plane_normal(ground, self.vertices_points_as_list, -self._center)
        normal_tuple = normal.get_tuple()

        glBegin(GL_QUADS)
        for vertex in ground:
            glColor4fv(color)
            glNormal3fv(normal_tuple)
            glVertex3fv(self.vertices_points_as_list[vertex] - origin)
        glEnd()

        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glColor4fv((0.0, 0.0, 0.0, 1.0))
                glNormal3fv((0.0, 0.0, 0.0))
                glVertex3fv(self.vertices_points_as_list[vertex] - origin)
        glEnd()


class DrawableSource(Source):
    def draw_parable(self, origin):
        number_levels = int(self.angle_ouverture / self.angle_levels)
        #    self.points_per_level = len(self.points_parable)
        glBegin(GL_QUADS)
        for j in range(number_levels - 2):
            for i in range(self.points_per_level):
                glColor4fv((0.95, 0.95, 0, 1.0))
                glNormal3fv((0.0, 0.0, 0.0))
                glVertex3fv(self.points_parable[i % self.points_per_level + (j + 1) * self.points_per_level] - origin)
                glVertex3fv(self.points_parable[i + 1 + (j + 1) * self.points_per_level] - origin)
                glVertex3fv(self.points_parable[(i + 1) % self.points_per_level + j * self.points_per_level] - origin)
                glVertex3fv(self.points_parable[i + j * self.points_per_level] - origin)
        glEnd()
        glBegin(GL_LINES)
        for j in range(number_levels):
            for i in range(self.points_per_level):
                glColor4fv((0.5, 0.5, 0.5, 1.0))
                glNormal3fv((0.0, 0.0, 0.0))
                glVertex3fv(self.points_parable[i + j * self.points_per_level] - origin)
                glVertex3fv(self.points_parable[(i + 1) % self.points_per_level + j * self.points_per_level] - origin)
        glEnd()

        glBegin(GL_LINES)
        for i in range(len(self.points_parable) - self.points_per_level):
            for j in (i, i + self.points_per_level):
                glColor4fv((0.5, 0.5, 0.5, 1.0))
                glNormal3fv((0.0, 0.0, 0.0))
                glVertex3fv(self.points_parable[j] - origin)
        glEnd()

    def draw(self, origin):
        self.draw_parable(origin)
        edges = (
            (0, 1),
            (0, 2),
            (0, 4),
            (1, 3),
            (1, 5),
            (7, 3),
            (7, 5),
            (7, 6),
            (6, 2),
            (6, 4),
            (3, 2),
            (5, 4)
        )

        #    edges = ()
        surfaces = (
            (1, 3, 2, 0),
            (1, 0, 4, 5),
            (0, 2, 6, 4),
            (1, 3, 7, 5),
            (7, 3, 2, 6)
        )

        light = (1, 3, 2, 0)

        normal = get_plane_normal(light, self.vertices_points_as_list, self._center)
        normal_tuple = normal.get_tuple()
        glBegin(GL_QUADS)
        for vertex in light:
            glNormal3fv(normal_tuple)
            glColor4fv((1.0, 1.0, 1.0, 1.0))
            glVertex3fv(self.vertices_points_as_list[vertex] - origin)
        glEnd()

        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glColor4fv((0.0, 0.0, 0.0, 1.0))
                glNormal3fv((0.0, 0.0, 0.0))
                glVertex3fv(self.vertices_points_as_list[vertex] - origin)
        glEnd()


class DrawableMaisonette(Maisonette):
    def draw_inside(self, origin):
        edges = (
            (0, 1),
            (0, 2),
            (0, 4),
            (1, 3),
            (1, 5),
            (7, 3),
            (7, 5),
            (7, 6),
            (6, 2),
            (6, 4),
            (3, 2),
            (5, 4),
            # windows inside
            (8, 9),
            (9, 10),
            (10, 11),
            (11, 8),
            # window outside
            (12, 13),
            (13, 14),
            (14, 15),
            (15, 12),
            # wall between windows
            (8, 12),
            (9, 13),
            (10, 14),
            (11, 15)

        )
        surfaces_inside = (
            #####inside
            Surface((5, 7, 6, 4), (-1, 0, 0)),
            Surface((5, 4, 0, 1), (0, 1, 0)),
            Surface((7, 3, 2, 6), (0, -1, 0)),
            Surface((4, 6, 2, 0), (0, 0, 1)),
            Surface((1, 3, 7, 5), (0, 0, 1))
        )
        surfaces_outside = (
            #####outside front face
            Surface((16, 17, 12, 15), (-1, 0, 0)),
            Surface((19, 13, 12, 17), (-1, 0, 0)),
            Surface((13, 19, 18, 14), (-1, 0, 0)),
            Surface((16, 15, 14, 18), (-1, 0, 0)),
            #####
            Surface((8, 11, 15, 12), (0, -1, 0)),
            Surface((12, 13, 9, 8), (0, 0, -1)),
            Surface((13, 14, 10, 9), (0, 1, 0)),
            Surface((14, 15, 11, 10), (0, 0, 1))
        )
        verticies = self.sommets_extras
        verticiesInOrigin = []
        for v in verticies:
            verticiesInOrigin.append(v - origin)
        glBegin(GL_QUADS)
        for surface in surfaces_outside:
            for vertex in surface.edges:
                glColor4fv((0.4, 0.4, 0.4, 1.0))
                glNormal3fv(surface.normal)
                glVertex3fv(verticiesInOrigin[vertex])
        for surface in surfaces_inside:
            for vertex in surface.edges:
                glColor4fv((0.6, 0.6, 0.6, 1.0))
                glNormal3fv(surface.normal)
                glVertex3fv(verticiesInOrigin[vertex])
        glEnd()
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glColor4fv((0.0, 0.0, 0.0, 1.0))
                glNormal3fv((0.0, 0.0, 0.0))
                glVertex3fv(verticiesInOrigin[vertex])
        glEnd()

    def draw(self, origin):
        self.draw_inside(origin)
        edges = (
            (0, 1),
            (0, 2),
            (0, 4),
            (1, 3),
            (1, 5),
            (7, 3),
            (7, 5),
            (7, 6),
            (6, 2),
            (6, 4),
            (3, 2),
            (5, 4)
        )
        surfaces = (
            #    Surface((0,2,6,4),(0,0,1)), #ground
            Surface((5, 7, 3, 1), (0, 0, 1)),  # ceiling
            Surface((4, 6, 7, 5), (1, 0, 0)),  # back face
            Surface((6, 2, 3, 7), (0, 1, 0)),  # left face looking from source
            Surface((1, 0, 4, 5), (0, -1, 0))  # right face looking from source

        )

        verticies = self.sommets_pave()
        verticiesInOrigin = []
        for v in verticies:
            verticiesInOrigin.append(v - origin)

        glBegin(GL_QUADS)
        for surface in surfaces:
            for vertex in surface.edges:
                glColor4fv((0.4, 0.4, 0.4, 1.0))
                glNormal3fv(surface.normal)
                glVertex3fv(verticiesInOrigin[vertex])
        glEnd()

        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glColor4fv((0.0, 0.0, 0.0, 1.0))
                glNormal3fv((0.0, 0.0, 0.0))
                glVertex3fv(verticiesInOrigin[vertex])
        glEnd()