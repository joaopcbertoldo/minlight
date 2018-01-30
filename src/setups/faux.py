from ..modeles.enums import UniteAngleEnum

from src.calculs.modeles.entites_mathemathiques import \
    Vec3,                                \
    TupleAnglesRotation,                      \
    SpaceRechercheAnglesLimites,              \
    IntervalleLineaire,                       \
    SystemeRepereSpherique

from src.calculs.modeles.entites_systeme_minlight import \
    BoxDimensions,                             \
    Box,                                       \
    CableLayout,                       \
    ConfigurationCable

from src.calculs.simulation_angles_limites.angles_limites import VerificateurAnglesLimites

'''
    Setup d'un faux systeme.
    Destiné juste à faire des debugs avec des valeurs plus simples.
'''

''' ************************ Maisonette ************************ '''
# centre
centre_maisonette = \
    Vec3(
        x = 7500,  # mm
        y = 5000,  # mm
        z = 5000   # mm
    )

# dimensions
dimensions_maisonette = \
    BoxDimensions(
        longueur =  5000,  # mm
        largeur  = 10000,  # mm
        hauteur  = 10000   # mm
    )

# pave
maisonette = \
    Box(
        centre     = centre_maisonette,
        ypr_angles = TupleAnglesRotation.ZERO(),
        dimensions = dimensions_maisonette
)


''' ************************ Source ************************ '''

# dimensions
dimensions_source = \
    BoxDimensions(
        longueur = 1000,  # mm
        largeur  = 1000,  # mm
        hauteur  = 1000   # mm
    )


''' ************************ Chambre ************************ '''

# centre
centre_chambre = \
    Vec3(
        x = 5000,  # mm
        y = 5000,  # mm
        z = 5000   # mm
    )

# dimensions
dimensions_chambre = \
    BoxDimensions(
        longueur = 10000,  # mm
        largeur  = 10000,  # mm
        hauteur  = 10000   # mm
    )

# pavé
chambre = \
    Box(
        centre     = centre_chambre,
        ypr_angles = TupleAnglesRotation.ZERO(),
        dimensions = dimensions_chambre
    )


''' ************************ Ancrage ************************ '''

''' ****** Points Fixes ****** '''
# toutes les ancrages sont supposées dans les coins de la chambre
# donc, les coordonnées sont toujours, soit 0, soit la dimension de la chambre
# sauf la longueur qui s'arrete juste au niveau de la maisonette

# coordonnées d'ancrage
x = 5000   # mm
y = 10000  # mm
z = 10000  # mm

# la numérotation <<PF_xxx>> suit la logique des sommets des pavés
# le <<xxx>> indique à quel "coin" de la chambre le point est fixé

PF_000 = Vec3(0, 0, 0)  # PF_000
PF_100 = Vec3(x, 0, 0)  # PF_100
PF_010 = Vec3(0, y, 0)  # PF_010
PF_110 = Vec3(x, y, 0)  # PF_110
PF_001 = Vec3(0, 0, z)  # PF_001
PF_101 = Vec3(x, 0, z)  # PF_101
PF_011 = Vec3(0, y, z)  # PF_011
PF_111 = Vec3(x, y, z)  # PF_111


''' ****** Configurations des Câbles ****** '''
# la numérotation <<cc_xxx>> suit la logique des sommets des pavés
# le <<xxx>> indique à quel sommet le cable sera rataché DANS LA SOURCE

cc_000 = ConfigurationCable(nom_sommet_source='S000', point_ancrage= PF_000)  # cc_000
cc_100 = ConfigurationCable(nom_sommet_source='S100', point_ancrage= PF_100)  # cc_100
cc_010 = ConfigurationCable(nom_sommet_source='S010', point_ancrage= PF_010)  # cc_010
cc_110 = ConfigurationCable(nom_sommet_source='S110', point_ancrage= PF_110)  # cc_110
cc_001 = ConfigurationCable(nom_sommet_source='S001', point_ancrage= PF_001)  # cc_001
cc_101 = ConfigurationCable(nom_sommet_source='S101', point_ancrage= PF_101)  # cc_101
cc_011 = ConfigurationCable(nom_sommet_source='S011', point_ancrage= PF_011)  # cc_011
cc_111 = ConfigurationCable(nom_sommet_source='S111', point_ancrage= PF_111)  # cc_111


''' ****** Configurations des Câbles ****** '''
config_ancrage = CableLayout(
    configs_cables=[cc_000, cc_100, cc_010, cc_110, cc_001, cc_101, cc_011, cc_111]
)


''' ************************ Systeme Spherique Baie Vitrée ************************ '''

# centre - supposé dans le centre de la face d'intérêt de la maisonette
centre_systeme_spherique = \
    Vec3(
        x = 5000,  # mm
        y = 5000,  # mm
        z = 5000   # mm
    )

# rotation
rotation_systeme_spherique = \
    TupleAnglesRotation(
        yaw   = 180,  # degrés
        pitch = 0,    # degrés
        row   = 0,    # degrés
        unite = UniteAngleEnum.DEGRE,
    )

# systeme sphérique
systeme_spherique_baie_vitree = SystemeRepereSpherique(
    centre     = centre_systeme_spherique,
    ypr_angles = rotation_systeme_spherique
)


''' ************************ Configs Simulation ************************ '''

# space de recherche
space_recherche = \
    SpaceRechercheAnglesLimites(
        intervalle_rho   = IntervalleLineaire(min= 1000, max= 1501, pas=  250),  # mm
        intervalle_phi   = IntervalleLineaire(min=    0, max=  180, pas=    6),  # degres
        intervalle_theta = IntervalleLineaire(min=    0, max=  180, pas=    6),  # degres
        unite = UniteAngleEnum.DEGRE
)

# diameter des câbles
diametre_cable = 10  # mm

# discretisation des câbles
n_discretisation_cables = 20  # point/câble

# discretisation des cubes
k_dicretisation_cubes = 3  # division/arête --> nb points/face = (k+1)^2

# verbose
verbose = True

# dictionnaire de configs
configs_simulation = {
    'space_recherche'         : space_recherche,
    'diametre_cable'          : diametre_cable,
    'n_discretisation_cables' : n_discretisation_cables,
    'k_dicretisation_cubes'   : k_dicretisation_cubes,
    'verbose'                 : verbose
}


''' ************************ VerificateurAnglesLimites ************************ '''

verificateur = VerificateurAnglesLimites(
    dimensions_source             = dimensions_source,
    maisonette                    = maisonette,
    chambre                       = chambre,
    config_ancrage                = config_ancrage,
    systeme_spherique_baie_vitree = systeme_spherique_baie_vitree,
    configs_simulation            = configs_simulation
)

def __main__():
    print('faux a été importé')
    print(verificateur)  # overwrite str function
