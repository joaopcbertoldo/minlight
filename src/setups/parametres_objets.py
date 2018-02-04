from src.enums import UniteAngleEnum

from src.math_entities import \
    Vec3,                                \
    TupleAnglesRotation,                      \
    SystemeRepereSpherique

from src.models.entites_systeme_minlight import \
    BoxDimensions,                             \
    CableConfiguration,                         \
    Source,                                     \
    Chambre,                                     \
    Maisonette


'''
Paramètres
'''

''' ************************ Chambre ************************ '''

# dimensions
dimensions_chambre = \
    BoxDimensions(
        # on considere le sisteme à partir de l'évaporateur
        length=8500,  # mm
        width=5000,   # mm
        height=3800    # mm
    )

# centre
centre_chambre = \
    Vec3(
        x=dimensions_chambre['length'] / 2,  # mm
        y=dimensions_chambre['width'] / 2,  # mm
        z=dimensions_chambre['height'] / 2   # mm
    )

# pavé
chambre = \
    Chambre(
        centre=centre_chambre,
        ypr_angles=TupleAnglesRotation.ZERO(),
        dimensions=dimensions_chambre
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

# centre
centre_maisonette = \
    Vec3(
        x=distance_evaporateur_maisonette + dimensions_maisonette['length'] / 2,
        y=dimensions_chambre['width'] / 2,
        z=dimensions_maisonette['height'] / 2
    )

# window dimensions
window_dimensions = {
    'width': 1200,
    'height': 2150
}


# pave
maisonette = \
    Maisonette(
        centre=centre_maisonette,
        ypr_angles=TupleAnglesRotation.ZERO(),
        dimensions=dimensions_maisonette,
        window_dimensions=window_dimensions
    )


''' ************************ Source ************************ '''

# dimensions
dimensions_source = \
    BoxDimensions(
        length=800,  # mm
        width=1600,   # mm
        height=1600    # mm
    )

centre_source = \
    Vec3(
        x=dimensions_chambre['length'] / 5,  # mm
        y=dimensions_chambre['width'] / 2,  # mm
        z=dimensions_chambre['height'] / 2   # mm
    )

source = \
    Source(
        centre=centre_source,
        ypr_angles=TupleAnglesRotation.ZERO(),
        dimensions=dimensions_source
    )

''' ************************ Systeme Spherique Baie Vitrée ************************ '''

# centre - supposé dans le centre de la face d'intérêt de la maisonette
centre_systeme_spherique = \
    Vec3(
        x=distance_evaporateur_maisonette,
        y=dimensions_chambre['width'] / 2,
        z=dimensions_maisonette['height'] / 2
    )

# rotation
rotation_systeme_spherique = \
    TupleAnglesRotation(
        yaw=180,  # degrés
        pitch=0,  # degrés
        row=0,    # degrés
        unite=UniteAngleEnum.DEGRE,
    )

# systeme sphérique
systeme_spherique_baie_vitree = SystemeRepereSpherique(
    centre=centre_systeme_spherique,
    ypr_angles=rotation_systeme_spherique
)

''' ************************ Camera ************************ '''
camera_direction = Vec3(
        x=0,
        y=0,
        z=0
)

# position
camera_position1 = Vec3(
        x=-dimensions_chambre['length']/2,  # mm
        y=-0.25*dimensions_chambre['width'],  # mm
        z=-0.1*dimensions_chambre['height']  # mm
)

camera_position2 = Vec3(
        x=-dimensions_chambre['length']/2,  # mm
        y=-0.25*dimensions_chambre['width'],  # mm
        z=0.25*dimensions_chambre['height']  # mm
)

camera_position3 = Vec3(
        x=-dimensions_chambre['length']/2,  # mm
        y=0.25*dimensions_chambre['width'],  # mm
        z=-0.25*dimensions_chambre['height']  # mm
)

camera_position4 = Vec3(
        x=-dimensions_chambre['length']/2,  # mm
        y=0.25*dimensions_chambre['width'],  # mm
        z=0.25*dimensions_chambre['height']  # mm
)


def __main__():
    print('parametres_objets chargés')
    print('Objets crées : ')
    print(dimensions_chambre)
    print(centre_chambre)
    print(chambre)
    print(dimensions_maisonette)
    print(centre_maisonette)
    print(chambre)
    print(dimensions_source)
    print(centre_systeme_spherique)
    print(rotation_systeme_spherique)
    print(systeme_spherique_baie_vitree)
