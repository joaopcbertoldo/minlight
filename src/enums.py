from enum import Enum
from typing import List


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


class BoxVertexOrderEnum(Enum):
    """
    Logic for the order of the vertices of a box.
    XYZ -> X vary firs, then Y, then Z (000, 100, 010, 110,...)
    ZYX -> Z vary firs, then Y, then X (000, 001, 010, 011,...)
    """
    unknown = 0
    XYZ = 1
    ZYX = 2


class BoxVertexEnum(Enum):
    """Names of the vertices of a box in the system 's{x}{y}{z}'. Cf. doc/vertices_names_notation.pdf"""
    unknown = 0
    v000 = 1
    v100 = 2
    v010 = 3
    v110 = 4
    v001 = 5
    v101 = 6
    v011 = 7
    v111 = 8

    # list_vertices (standard order X Y Z)
    @staticmethod
    def list_vertices() -> List['BoxVertexEnum']:
        """Vertices names in our standard order (XYZ). Cf. doc/vertices_names_notation.pdf"""
        # TODO: doc the standard somewhere
        return BoxVertexEnum.list_vertices_ordered_as(BoxVertexOrderEnum.XYZ)

    # list_vertices_ordered_as
    @staticmethod
    def list_vertices_ordered_as(order: BoxVertexOrderEnum) -> List['BoxVertexEnum']:
        """Vertices names in given order. Cf. doc/vertices_names_notation.pdf"""
        # X Y Z
        if order == BoxVertexOrderEnum.XYZ:
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
        # Z Y X
        elif order == BoxVertexOrderEnum.ZYX:
            return [
                BoxVertexEnum.v000,
                BoxVertexEnum.v001,
                BoxVertexEnum.v010,
                BoxVertexEnum.v011,
                BoxVertexEnum.v100,
                BoxVertexEnum.v101,
                BoxVertexEnum.v110,
                BoxVertexEnum.v111,
            ]
        # problem
        else:
            raise Exception('Unknonw order.')