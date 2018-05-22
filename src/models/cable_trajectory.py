from src.models.trajectoire import *
from src.models.cables import *
from src.models.boxes import *
from src.models.observers import *
from src.models.system import *
from src.math_entities import *


class CableTrajectory:

    def __init__(self, robot : CableRobot, trajectory : Trajectory, interval):
        self.robot = robot
        self.trajectory = trajectory
        self.interval = interval

        self.cable_observer = ObserverLongueur8Cables(self.robot, self.interval)
        # maquette dimensions hardcoded for now
        self.translator = TrajectoryTranslator(self.trajectory, 20, 40, 80, 40, 0.5)

    def run_trajectory(self):
        config_list = self.translator.get_config_list()
        for config in config_list:
            self.robot.set_source_configuration(config[0], config[1])

    def get_delta_cables(self):
        return self.cable_observer.get_dict_historiques_longueurs()

    def write(self, file_name: str):
        # file_name = "src.trajectory_out.trajectory.txt"
        file = open(file_name, "w")

        file.write("Must implement the complete function!")
        file.write("And test it.")

        file.close()

######## test #########
# initialization of the bunch of classes representing the system

# maquette dimensions:
maq_L = 390# must be careful with this one, it may change the coord transformation
maq_H = 270
maq_W = 240
maquette = Box(MobilePoint(maq_L/2, maq_H/2, maq_W/2), Orientation(0.0, 0.0, 0.0), BoxDimensions(maq_L, maq_W, maq_H))

# maisonette, completely useless in this case
dic = {'width':1.0, 'height':1.0} # does not matter, just for instanciating a Maisonette
maisonnete = Maisonette(Point(100000.0, 1000000.0, 1000000.0), Orientation(0.0, 0.0, 0.0), BoxDimensions(1.0, 1.0, 1.0),dic)

# source:
pos_init = MobilePoint(maq_L/2, maq_H/2, maq_W/2) # may be changed
orient_init = Orientation(0.0, 0.0, 0.0)
src_L = 30.0
src_H = 60.0
src_W = 25.0
source_dim = BoxDimensions(src_L, src_W, src_H)
source = Source(pos_init, orient_init, source_dim)

# cables
cable_diam = 1.0 # may change

fixed_points = []
fixed_points.append(Point(0.0, 50.0, 20.0))
fixed_points.append(Point(270.0, 0.0, 20.0))
fixed_points.append(Point(340.0, 240.0, 20.0))
fixed_points.append(Point(0.0, 175.0, 20.0))
fixed_points.append(Point(95.0, 0.0, 250.0))
fixed_points.append(Point(290.0, 0.0, 250.0))
fixed_points.append(Point(280.0, 240.0, 250.0))
fixed_points.append(Point(98.0, 240.0, 250.0))

cable_ends = []
cable_ends.append(CableEnds(fixed_points[0], BoxVertexEnum(1)))
cable_ends.append(CableEnds(fixed_points[1], BoxVertexEnum(2)))
cable_ends.append(CableEnds(fixed_points[2], BoxVertexEnum(4)))
cable_ends.append(CableEnds(fixed_points[3], BoxVertexEnum(3)))
cable_ends.append(CableEnds(fixed_points[4], BoxVertexEnum(5)))
cable_ends.append(CableEnds(fixed_points[5], BoxVertexEnum(6)))
cable_ends.append(CableEnds(fixed_points[6], BoxVertexEnum(8)))
cable_ends.append(CableEnds(fixed_points[7], BoxVertexEnum(7)))

cable_layout = CableLayout(cable_ends)

## CableRobot:
cable_robot = CableRobot(maquette, maisonnete, source, cable_diam, cable_layout)

## Trajecory:
trajectory = Trajectory('03/03', '60.3/N', '10:00', '14:00', 20)

## interval:
interval = 20 # must confirm

### Cable trajectory
cable_traj = CableTrajectory(cable_robot, trajectory, interval)