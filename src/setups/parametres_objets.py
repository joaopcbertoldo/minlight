from src.enums import AngleUnityEnum

from src.math_entities import Vec3, Orientation, SphericalCoordinateSystem, Point, MobilePoint
from src.models.boxes import BoxDimensions, Box, Source, Maisonette

'''
Paramètres
'''

''' ************************ Chambre ************************ '''

# dimensions
dimensions_room = \
    BoxDimensions(
        # on considere le sisteme à partir de l'évaporateur
        length=8500.,  # mm
        width=5000.,   # mm
        height=3800.    # mm
    )

# _center
centre_room = \
    MobilePoint(
        name="Room's center.",
        x=dimensions_room['length'] / 2,  # mm
        y=dimensions_room['width'] / 2,  # mm
        z=dimensions_room['height'] / 2   # mm
    )

# pavé
room = Box(
        center=centre_room,
        orientation=Orientation.zero(),
        dimensions=dimensions_room
    )


''' ************************ Maisonette ************************ '''

distance_evaporateur_maisonette = 3500  # mm

# dimensions
dimensions_maisonette = \
    BoxDimensions(
        length=5000,  # mm
        width=2500,   # mm
        height=2900    # mm
    )

# _center
centre_maisonette = \
    MobilePoint(
        name="Maisonette's center.",
        x=distance_evaporateur_maisonette + dimensions_maisonette['length'] / 2,
        y=dimensions_room['width'] / 2,
        z=dimensions_maisonette['height'] / 2
    )

# window dimensions
window_dimensions = {
    'width': 1200,  # mm
    'height': 2150  # mm
}

# pave
maisonette = \
    Maisonette(
        center=centre_maisonette,
        orientation=Orientation.zero(),
        dimensions=dimensions_maisonette,
        window_dimensions=window_dimensions
    )


''' ************************ Source ************************ '''

# dimensions
dimensions_source = \
    BoxDimensions(
        length=800,  # mm
        width=1600,  # mm
        height=1600  # mm
    )

centre_source = \
    MobilePoint(
        name="Source's center",
        x=dimensions_room['length'] / 5,  # mm
        y=dimensions_room['width'] / 2,  # mm
        z=dimensions_room['height'] / 2   # mm
    )

source = \
    Source(
        center=centre_source,
        orientation=Orientation.zero(),
        dimensions=dimensions_source
    )

''' ************************ Systeme Spherique Baie Vitrée ************************ '''

# _center - supposé dans le _center de la face d'intérêt de la maisonette
centre_systeme_spherique = \
    Point(
        x=distance_evaporateur_maisonette,
        y=dimensions_room['width'] / 2,
        z=dimensions_maisonette['height'] / 2
    )

# rotation
rotation_systeme_spherique = \
    Orientation(
        yaw=180,  # degrés
        pitch=0,  # degrés
        row=0,    # degrés
        unity=AngleUnityEnum.degree,
    )

# systeme sphérique
systeme_spherique_baie_vitree = SphericalCoordinateSystem(
    center=centre_systeme_spherique,
    orientation=rotation_systeme_spherique
)

''' ************************ Camera ************************ '''
camera_direction = Vec3(
        x=0,
        y=0,
        z=0
)

# position
camera_position1 = Vec3(
        x=-dimensions_room['length']/2,  # mm
        y=-0.25*dimensions_room['width'],  # mm
        z=-0.1*dimensions_room['height']  # mm
)

camera_position2 = Vec3(
        x=-dimensions_room['length']/2,  # mm
        y=-0.25*dimensions_room['width'],  # mm
        z=0.25*dimensions_room['height']  # mm
)

camera_position3 = Vec3(
        x=-dimensions_room['length']/2,  # mm
        y=0.25*dimensions_room['width'],  # mm
        z=-0.25*dimensions_room['height']  # mm
)

camera_position4 = Vec3(
        x=-dimensions_room['length']/2,  # mm
        y=0.25*dimensions_room['width'],  # mm
        z=0.25*dimensions_room['height']  # mm
)


def __main__():
    print('parametres_objets chargés')
    print('Objets crées : ')
    print(dimensions_room)
    print(centre_room)
    print(room)
    print(dimensions_maisonette)
    print(centre_maisonette)
    print(room)
    print(dimensions_source)
    print(centre_systeme_spherique)
    print(rotation_systeme_spherique)
    print(systeme_spherique_baie_vitree)
