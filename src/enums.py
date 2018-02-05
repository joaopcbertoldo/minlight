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
    s000 = 1
    s100 = 2
    s010 = 3
    s110 = 4
    s001 = 5
    s101 = 6
    s011 = 7
    s111 = 8

    @staticmethod
    def list_vertices():
        return [
            BoxVertexEnum.s000,
            BoxVertexEnum.s100,
            BoxVertexEnum.s010,
            BoxVertexEnum.s110,
            BoxVertexEnum.s001,
            BoxVertexEnum.s101,
            BoxVertexEnum.s011,
            BoxVertexEnum.s111,
        ]
