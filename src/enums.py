from enum import Enum


class AngleUnityEnum(Enum):
    """Unity used to measure angles."""
    unknown = 0
    radian = 1
    degree = 2


class RotationAngleEnum(Enum):
    """Row (body's x axis), pitch(body's y axis), yaw(body's z axis)."""
    unknown = 0
    row = 1
    pitch = 2
    yaw = 3


class RotationOrderEnum(Enum):
    """Sequence of the three rotation angles (ex: row, pitch, yaw)."""
    unknown = 0
    rpy = 1
    ypr = 2


class BoxVertexEnum(Enum):
    """Names of the vertices of a box in the system 's{x}{y}{z}'."""
    unknown = 0
    v000 = 1
    v100 = 2
    v010 = 3
    v110 = 4
    v001 = 5
    v101 = 6
    v011 = 7
    v111 = 8

    @staticmethod
    def list_vertices():
        return [
            BoxVertexEnum.v000,
            BoxVertexEnum.v100,
            BoxVertexEnum.v010,
            BoxVertexEnum.v110,
            BoxVertexEnum.v001,
            BoxVertexEnum.v101,
            BoxVertexEnum.v011,
            BoxVertexEnum.v111,
        ]

