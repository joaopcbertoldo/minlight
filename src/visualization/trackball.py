from numpy import sqrt, arccos

from OpenGL.GL import *

from src.math_entities import Vec3


class Trackball:
    def __init__(self, w, h):
        self.ballRadius = 600
        self.isRotating = False
        self.width = w
        self.height = h
        self.reset()

    def setWidthHeight(self, w, h):
        self.width = w
        self.height = h
        self.ballRadius = min((w / 2), (h / 2))

    # * \ingroup GLVisualization
    # * Set the radius of the ball (a typical radius for a 1024x768 window is 600
    # * \param newRadius The radius of the spherical dragging area

    def setRadius(self, newRadius):
        self.ballRadius = newRadius

    def startRotation(self, _x, _y):
        x = ((_x) - (self.width / 2))
        y = ((self.height / 2) - _y)

        self.startRotationVector = self.convertXY(x, y)
        self.startRotationVector = self.startRotationVector.get_direction()

        self.currentRotationVector = self.startRotationVector;
        self.isRotating = True

    def updateRotation(self, _x, _y):
        x = ((_x) - (self.width / 2))
        y = ((self.height / 2) - _y)

        self.currentRotationVector = self.convertXY(x, y)
        self.currentRotationVector = self.currentRotationVector.get_direction()
        self.applyRotationMatrix()

    def applyRotationMatrix(self):
        if (self.isRotating):
            if ((self.currentRotationVector - self.startRotationVector).norm() > 1E-6):
                rotationAxis = self.currentRotationVector.cross(self.startRotationVector)
                rotationAxis = rotationAxis.get_direction()
                val = self.currentRotationVector.transpose().dot(self.startRotationVector)
                if (val > (1 - 0.0000000001)):
                    val = 1.0
                else:
                    val = val
                rotationAngle = arccos(val) * 180.0 / 3.14159
                # // rotate around the current position
                self.applyTranslationMatrix(True)
                glRotatef(rotationAngle * 0.05, -rotationAxis.get_x(), -rotationAxis.get_y(), -rotationAxis.get_z())
                self.applyTranslationMatrix(False)
        glMultMatrixf(self.startMatrix)

    def stopRotation(self):

        self.isRotating = False

    def applyTranslationMatrix(self, reverse):
        if (reverse):
            factor = -1.0
        else:
            factor = 1.0

        tx = self.transX + (self.currentTransX - self.startTransX) * 0.01
        ty = self.transY + (self.currentTransY - self.startTransY) * 0.01
        glTranslatef(factor * tx, factor * (-ty), 0)

    def convertXY(self, x, y):
        d = x * x + y * y
        radiusSquared = self.ballRadius * self.ballRadius
        if (d > radiusSquared):
            return Vec3(x, y, 0)

        else:
            return Vec3(x, y, sqrt(radiusSquared - d))

    def reset(self):
        fov = 30
        #  // reset matrix
        self.startMatrix = [0] * 16
        self.startMatrix[0] = 1
        self.startMatrix[1] = 0
        self.startMatrix[2] = 0
        self.startMatrix[3] = 0
        self.startMatrix[4] = 0
        self.startMatrix[5] = 1
        self.startMatrix[6] = 0
        self.startMatrix[7] = 0
        self.startMatrix[8] = 0
        self.startMatrix[9] = 0
        self.startMatrix[10] = 1
        self.startMatrix[11] = 0
        self.startMatrix[12] = 0
        self.startMatrix[13] = 0
        self.startMatrix[14] = 0
        self.startMatrix[15] = 1
        self.transX = self.transY = 0
        self.startTransX = self.startTransY = self.currentTransX = self.currentTransY = 0
