import numpy as np

from src.models.entite_cable_robot import CableRobotObserver


class HistoriqueValeur:

    def __init__(self, intervale, temps0=0):
        self._valeurs = list()
        self._temps = list()

        self._temps0 = temps0
        self._intervale = intervale
        self._i = 0

    def ajouter(self, valeur):
        self._valeurs.append(valeur)
        self._temps.append(self._temps0 + self._intervale * self._i)
        self._i = self._i + 1

    def get_temps(self):
        return self._temps

    def get_valeurs(self):
        return self._valeurs

    def get_couples_temps_valeur(self):
        return list(zip(self._temps, self._valeurs))

    def get_lists_temps_valeurs(self):
        return [self._temps, self._valeurs]

    def get_historique_differences(self):
        hist_diffs = HistoriqueValeur(intervale=self._intervale, temps0=self._temps0)

        for i in range(self._i - 1):
            hist_diffs.ajouter(self._valeurs[i+1] - self._valeurs[i])

        return hist_diffs

    def get_historique_transforme(self, transformation):
        hist_transf = HistoriqueValeur(intervale=self._intervale, temps0=self._temps0)

        for i in range(self._i):
            hist_transf.ajouter(transformation(self._valeurs[i]))

        return hist_transf


class ObserverLongueurCable(CableRobotObserver):

    def __init__(self, nom_cable, intervale):
        self._longueurs = HistoriqueValeur(intervale)
        self.nom_cable = nom_cable

    def notify(self, cable_robot):
        cable = cable_robot.get_cable(self.nom_cable)
        self._longueurs.ajouter(cable.longueur())

    def get_historique_longueurs(self):
        return self._longueurs

    def get_historique_vitesses(self):
        return self._longueurs.get_historique_differences()

    def get_historique_accelerations(self):
        return self._longueurs.get_historique_differences().get_historique_differences()


class ObserverLongueur8Cables:

    def __init__(self, cable_robot, intervale):
        self._dict_observers = dict()

        self._dict_observers['PF000'] = ObserverLongueurCable('PF000', intervale)
        self._dict_observers['PF001'] = ObserverLongueurCable('PF001', intervale)
        self._dict_observers['PF010'] = ObserverLongueurCable('PF010', intervale)
        self._dict_observers['PF011'] = ObserverLongueurCable('PF011', intervale)
        self._dict_observers['PF100'] = ObserverLongueurCable('PF100', intervale)
        self._dict_observers['PF101'] = ObserverLongueurCable('PF101', intervale)
        self._dict_observers['PF110'] = ObserverLongueurCable('PF110', intervale)
        self._dict_observers['PF111'] = ObserverLongueurCable('PF111', intervale)

        for observer in self._dict_observers.values():
            cable_robot.subscribe_observer(observer)

    def get_dict_historiques_longueurs(self):
        return {nom: observer.get_historique_longueurs() for nom, observer in self._dict_observers.items()}

    def get_dict_historique_vitesses(self):
        return {nom: observer.get_historique_vitesses() for nom, observer in self._dict_observers.items()}

    def get_dict_historique_accelerations(self):
        return {nom: observer.get_historique_accelerations() for nom, observer in self._dict_observers.items()}

    def get_historique_longueurs(self, nom_cable):
        return self._dict_observers[nom_cable].get_historique_longueurs()

    def get_historique_vitesses(self, nom_cable):
        return self._dict_observers[nom_cable].get_historique_vitesses()

    def get_historique_accelerations(self, nom_cable):
        return self._dict_observers[nom_cable].get_historique_accelerations()


class ObserverPoint3D(CableRobotObserver):

    @staticmethod
    def centre_accessor(cable_robot):
        source = cable_robot.get_source()
        centre = source.get_centre()
        return centre

    def __init__(self, intervale, accessor):
        self._points = HistoriqueValeur(intervale)
        self._accessor = accessor

    def notify(self, cable_robot):
        point = self._accessor(cable_robot)
        self._points.ajouter(point)

    def get_historique_points_3d(self):
        return self._points

    def get_historique_vitesses_3d(self):
        return self._points.get_historique_differences()

    def get_historique_vitesse(self):
        return self.get_historique_vitesses_3d().get_historique_transforme(lambda vec: np.linalg.norm(vec))

    def get_historique_accelerations_3d(self):
        return self.get_historique_vitesses_3d().get_historique_differences()

    def get_historique_accelerations(self):
        return self.get_historique_accelerations_3d().get_historique_transforme(lambda vec: np.linalg.norm(vec))

