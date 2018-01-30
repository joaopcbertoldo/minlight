from src.calculs.modeles.entite_cable_robot import CableRobot
from src.calculs.graphics.robotvisualization2 import *
from src.calculs.setups import parametres_ancrage, configuration_ancrage
from src.calculs.setups.parametres_objets import source, maisonette, chambre
from src.calculs.control.cable_robot_source_controlable import CableRobotSourceControlable

points_fixes = parametres_ancrage.Ideal.get_haut_haut()

config_ancrage = configuration_ancrage.get_simple(points_fixes)


def main():
    my_robot = CableRobot(chambre, maisonette, source, 5, config_ancrage)

    source_ctrl = CableRobotSourceControlable(my_robot)
    my_drawer = RobotVisualization2(my_robot, source_ctrl)
    # my_drawer.light_on()
    my_drawer.show()

main()
