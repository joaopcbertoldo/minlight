from OpenGL.GL import glBegin, glColor4fv, glNormal3fv, glVertex3fv, glEnd
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_LINES

from src.models.cables import Cable


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

