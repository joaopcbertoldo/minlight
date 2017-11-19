
from src.calculs.modeles.enums import UniteAngleEnum

from src.calculs.modeles.entites_mathemathiques import \
    Vecteur3D,                                \
    TupleAnglesRotation,                      \
    SpaceRechercheAnglesLimites,              \
    IntervalleLineaire,                       \
    SystemeRepereSpherique

from src.calculs.modeles.entites_systeme_minlight import \
    DimensionsPave,                             \
    Pave,                                       \
    ConfigurationAncrage,                       \
    ConfigurationCable,                         \
    Source,                                     \
    Chambre


'''
Paramètres
'''

''' ************************ Chambre ************************ '''

# dimensions
dimensions_chambre = \
    DimensionsPave(
        # on considere le sisteme à partir de l'évaporateur
        longueur=8500,  # mm
        largeur=5000,   # mm
        hauteur=4000    # mm
    )

# centre
centre_chambre = \
    Vecteur3D(
        x=dimensions_chambre['longueur'] / 2,  # mm
        y=dimensions_chambre['largeur' ] / 2,  # mm
        z=dimensions_chambre['hauteur' ] / 2   # mm
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
    DimensionsPave(
        longueur=5000,  # mm
        largeur=2500,   # mm
        hauteur=2900    # mm
    )

# centre
centre_maisonette = \
    Vecteur3D(
        x=distance_evaporateur_maisonette + dimensions_maisonette['longueur'] / 2,
        y=dimensions_chambre['largeur'] / 2,
        z=dimensions_maisonette['hauteur'] / 2
    )

# pave
maisonette = \
    Pave(
        centre=centre_maisonette,
        ypr_angles=TupleAnglesRotation.ZERO(),
        dimensions=dimensions_maisonette
    )


''' ************************ Source ************************ '''

# dimensions
dimensions_source = \
    DimensionsPave(
        longueur=1000,  # mm
        largeur=1600,   # mm
        hauteur=1600    # mm
    )

centre_source = \
    Vecteur3D(
        x=dimensions_chambre['longueur'] / 2,  # mm
        y=dimensions_chambre['largeur' ] / 2,  # mm
        z=dimensions_chambre['hauteur' ] / 2   # mm
    )

source = \
    Source(
        centre = centre_source,
        ypr_angles = TupleAnglesRotation.ZERO(),
        dimensions = dimensions_source
    )

''' ************************ Systeme Spherique Baie Vitrée ************************ '''

# centre - supposé dans le centre de la face d'intérêt de la maisonette
centre_systeme_spherique = \
    Vecteur3D(
        x=distance_evaporateur_maisonette,
        y=dimensions_chambre['largeur'] / 2,
        z=dimensions_maisonette['hauteur'] / 2
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
