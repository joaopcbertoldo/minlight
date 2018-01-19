import pygame
from pygame.locals import *
from src.calculs.modeles.entites_mathemathiques import Vecteur3D
from OpenGL.GL import *
from OpenGL.GLU import *
from src.calculs.setups.parametres_objets import dimensions_chambre
from numpy import tan
import time


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
        self.vertexList.append(Vecteur3D(dimensions_chambre['longueur']/2 ,pos_y + 0.5*dimensions_chambre['largeur'],pos_z + 0.5*dimensions_chambre['hauteur']))
        self.vertexList.append(Vecteur3D(dimensions_chambre['longueur']/2,pos_y + 0.5*dimensions_chambre['largeur'],pos_z - 0.5*dimensions_chambre['hauteur']))
        self.vertexList.append(Vecteur3D(dimensions_chambre['longueur']/2,pos_y  - 0.5*dimensions_chambre['largeur'],pos_z + 0.5*dimensions_chambre['hauteur']))
        self.vertexList.append(Vecteur3D(dimensions_chambre['longueur']/2,pos_y - 0.5*dimensions_chambre['largeur'],pos_z - 0.5*dimensions_chambre['hauteur']))

    def draw(self):
        triangles = (
            #    Surface((0,2,6,4),(0,0,1)), #ground
            (0,3,1), #ceiling
            (0,4,3), #back face
            (0,2,4), # left face looking from source
            (0,1,2)# right face looking from source
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
            glColor3fv((0.0,0.0,0.0))
            glNormal3fv((0.0,0.0,0.0))
            glVertex3fv(self.position)
            glColor3fv((0.0,0.0,0.0))
            glNormal3fv((0.0,0.0,0.0))
            glVertex3fv(vertex)
        glEnd()
