from src.enums import AngleUnityEnum


# ------------------------------------------------ Source ------------------------------------------------

class Source:

    # dimensions
    class Dimensions:
        length = 800  # mm
        width = 1600  # mm
        height = 1600  # mm

    class CenterOfMass:
        """Referenced from the source's center (XYZ with the same directions of the global frame)."""
        x = 0
        y = 0
        z = 0

