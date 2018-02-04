from numpy import tan

from OpenGL.GL import *

from src.math_entities import Vec3
from src.setups.parametres_objets import dimensions_chambre


class CameraOpening:

    def __init__(self,position,direction,opening):
        self.position = position
        self.direction = direction
        self.opening = opening
        self.vertexList = []
        self.calculatePoints()

    def calculatePoints(self):
        pos_x = -self.position.get_x()
        pos_y = -self.position.get_y()
        pos_z = -self.position.get_z()

        self.vertexList.append(self.position)
        self.vertexList.append(Vec3(self.position.get_x() + 0.25*dimensions_chambre['length'],self.position.get_y() + 0.25*dimensions_chambre['length']*tan(self.opening/2),self.position.get_z() + 0.25*dimensions_chambre['length']*tan(self.opening/2)))
        self.vertexList.append(Vec3(self.position.get_x() + 0.25*dimensions_chambre['length'],self.position.get_y() + 0.25*dimensions_chambre['length']*tan(self.opening/2),self.position.get_z()- 0.25*dimensions_chambre['length']*tan(self.opening/2)))
        self.vertexList.append(Vec3(self.position.get_x() + 0.25*dimensions_chambre['length'],self.position.get_y()  -0.25*dimensions_chambre['length']*tan(self.opening/2),self.position.get_z() + 0.25*dimensions_chambre['length']*tan(self.opening/2)))
        self.vertexList.append(Vec3(self.position.get_x() + 0.25*dimensions_chambre['length'],self.position.get_y()  -0.25*dimensions_chambre['length']*tan(self.opening/2),self.position.get_z()-0.25*dimensions_chambre['length']*tan(self.opening/2)))

    def draw(self):
        triangles = (
            (0,3,1),
            (0,4,3),
            (0,2,4),
            (0,1,2)
            )

        glBegin(GL_TRIANGLES)
        for triangle in triangles:
            for vertex in triangle:
                glColor4fv((0.6,0.,0.9,0.3))
                glNormal3fv((0.0,0.0,0.0))
                glVertex3fv(self.vertexList[vertex])
        glEnd()

        glBegin(GL_LINES)
        for vertex in self.vertexList:
            glColor3fv((0.6,0.,0.9))
            glNormal3fv((0.0,0.0,0.0))
            glVertex3fv(self.position)
            glColor3fv((0.6,0.,0.9))
            glNormal3fv((0.0,0.0,0.0))
            glVertex3fv(vertex)
        glEnd()
