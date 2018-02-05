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
