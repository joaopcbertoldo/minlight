from enum import Enum


class UniteAngleEnum(Enum):
    """Indicates the unity used to measure angle."""
    INCONU = 0
    RADIAN = 1
    DEGRE = 2


class AngleRotationEnum(Enum):
    INCONU = 0
    ROW = 1
    PITCH = 2
    YAW = 3


class SequenceAnglesRotationEnum(Enum):
    INCONU = 0
    RPY = 1
    YPR = 2
