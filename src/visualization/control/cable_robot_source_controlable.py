from src.calculs.control.controlable import SourceControlable


class CableRobotSourceControlable(SourceControlable):

    def __init__(self, cable_robot, translation_step=5, rotation_step=1):
        self._cable_robot = cable_robot
        self._translation_step = translation_step
        self._rotation_step = rotation_step

    def x_plus(self):
        self._cable_robot.translate_source(self._translation_step, 0, 0)

    def x_minus(self):
        self._cable_robot.translate_source(-self._translation_step, 0, 0)

    def y_plus(self):
        self._cable_robot.translate_source(0, self._translation_step, 0)

    def y_minus(self):
        self._cable_robot.translate_source(0, -self._translation_step, 0)

    def z_plus(self):
        self._cable_robot.translate_source(0, 0, self._translation_step)

    def z_minus(self):
        self._cable_robot.translate_source(0, 0, -self._translation_step)

    def roll_plus(self):
        self._cable_robot.rotate_source(delta_roll=self._rotation_step)

    def roll_minus(self):
        self._cable_robot.rotate_source(delta_roll=-self._rotation_step)

    def pitch_plus(self):
        self._cable_robot.rotate_source(delta_pitch=self._rotation_step)

    def pitch_minus(self):
        self._cable_robot.rotate_source(delta_pitch=-self._rotation_step)

    def yaw_plus(self):
        self._cable_robot.rotate_source(delta_yaw=self._rotation_step)

    def yaw_minus(self):
        self._cable_robot.rotate_source(delta_yaw=-self._rotation_step)


