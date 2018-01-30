from abc import ABCMeta, abstractmethod


class SourceControlable:
    __metaclass__ = ABCMeta

    @abstractmethod
    def x_plus(self):
        pass

    @abstractmethod
    def x_minus(self):
        pass

    @abstractmethod
    def y_plus(self):
        pass

    @abstractmethod
    def y_minus(self):
        pass

    @abstractmethod
    def z_plus(self):
        pass

    @abstractmethod
    def z_minus(self):
        pass

    @abstractmethod
    def roll_plus(self):
        pass

    @abstractmethod
    def roll_minus(self):
        pass

    @abstractmethod
    def pitch_plus(self):
        pass

    @abstractmethod
    def pitch_minus(self):
        pass

    @abstractmethod
    def yaw_plus(self):
        pass

    @abstractmethod
    def yaw_minus(self):
        pass


class ViewControlable:

    @abstractmethod
    def rotate_x_cw(self):
        pass

    @abstractmethod
    def rotate_x_ccw(self):
        pass

    @abstractmethod
    def rotate_y_cw(self):
        pass

    @abstractmethod
    def rotate_y_ccw(self):
        pass

    @abstractmethod
    def rotate_z_cw(self):
        pass

    @abstractmethod
    def rotate_z_ccw(self):
        pass

    @abstractmethod
    def zomm_in(self):
        pass

    @abstractmethod
    def zomm_out(self):
        pass