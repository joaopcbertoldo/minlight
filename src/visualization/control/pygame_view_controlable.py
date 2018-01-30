from OpenGL.GL import *
from src.calculs.control.controlable import ViewControlable


class PygameViewControlable(ViewControlable):

    def __init__(self, angle_step=2, zoom_scale_step=0.1):
        self._angle_step = angle_step
        self._zoom_scale_step = zoom_scale_step

    def rotate_x_cw(self):
        glRotate(self._angle_step, 1, 0, 0)

    def rotate_x_ccw(self):
        glRotate(-self._angle_step, 1, 0, 0)

    def rotate_y_cw(self):
        glRotate(self._angle_step, 0, 1, 0)

    def rotate_y_ccw(self):
        glRotate(-self._angle_step, 0, 1, 0)

    def rotate_z_cw(self):
        glRotate(self._angle_step, 0, 0, 1)

    def rotate_z_ccw(self):
        glRotate(-self._angle_step, 0, 0, 1)

    def zomm_in(self):
        scale = 1 + self._zoom_scale_step
        glScale(scale, scale, scale)

    def zomm_out(self):
        scale = 1 - self._zoom_scale_step
        glScale(scale, scale, scale)
