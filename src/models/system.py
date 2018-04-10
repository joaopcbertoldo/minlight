import copy
from abc import ABCMeta, abstractmethod

from src.models.boxes import Box, Maisonette
from src.models.cables import CableLayout


# Cable Robot
class CableRobot:

    # init
    def __init__(self, chambre: Box, maisonette: Maisonette, source: , diametre_cables, config_ancrage: CableLayout):
        """ """
        self._chambre = copy.deepcopy(chambre)
        self._maisonette = copy.deepcopy(maisonette)
        self._source = copy.deepcopy(source)
        self._diametre_cables = diametre_cables
        self._config_ancrage = copy.deepcopy(config_ancrage)

        # create cables
        sommets_source = self._source.vertices_points
        self._cables = self._config_ancrage.generate_cables(sommets_source, diameter=self._diametre_cables)

        self._observers = list()

    def draw(self, origin, draw_maisonette):
        for cable in self._cables:
            cable.draw(origin)
        self._chambre.draw(origin)
        if draw_maisonette:
            self._maisonette.draw(origin)
        self._source.draw(origin)

    def rotate_source(self, delta_yaw=0, delta_pitch=0, delta_roll=0, notify=True):
        self._source.rotate(delta_yaw, delta_pitch, delta_roll)
        self._notify_observers(notify)

    def translate_source(self, delta_x=0, delta_y=0, delta_z=0, notify=True):
        self._source.translate_center(delta_x, delta_y, delta_z)
        self._notify_observers(notify)

    def set_source_position(self, centre, notify=True):
        self._source.set_center_position(centre)
        self._notify_observers(notify)

    def set_source_angles(self, angles, notify=True):
        self._source.set_orientation(angles)
        self._notify_observers(notify)

    def set_source_configuration(self, centre, angles, notify=True):
        self.set_source_position(centre, notify=False)
        self.set_source_angles(angles, notify=False)
        self._notify_observers(notify)

    def light_center(self):
        return self._source.light_center

    def get_light_direction(self):
        return self._source.light_direction

    def get_light_radius(self):
        return self._source.light_radius

    def get_centre(self):
        return self._chambre.center()

    def subscribe_observer(self, observer):
        self._observers.append(observer)

    def _notify_observers(self, enable):
        if enable:
            for observer in self._observers:
                observer.notify(self)

    def get_cable(self, nom_cable):
        return (copy.deepcopy(cable) for cable in self._cables if cable.nom_sommet_source == nom_cable).next()

    def get_source(self):
        return copy.deepcopy(self._source)


class CableRobotObserver:
    __metaclass__ = ABCMeta

    @abstractmethod
    def notify(self, cable_robot):
        pass
