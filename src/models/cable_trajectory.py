from src.models.trajectoire import  *
#from src.models.cables import *
#from src.models.boxes import *
from src.models.observers import *
from src.models.system import *


class CableTrajectory:

    def __init__(self, robot : CableRobot, trajectory : Trajectoire, cable_observer : ObserverLongueur8Cables, interval):
        self.robot = robot
        self.trajectory = trajectory
        self.interval = interval

        cable_observer = ObserverLongueur8Cables(self.robot, self.interval)
        self.cable_observer = cable_observer

    def run_trajectory(self):
        config_list = self.trajectory.get_configurations()
        for config in config_list:
            self.robot.set_source_configuration(config.get_center(), config.get_angle())

    def get_delta_cables(self):
        return self.cable_observer.get_dict_historiques_longueurs()

    def write(self, file_name: str):
        # file_name = "src.trajectory_out.trajectory.txt"
        file = open(file_name, "w")

        file.write("Must implement the complete function!")
        file.write("And test it.")

        file.close()

## test
cable_traj = CableTrajectory()