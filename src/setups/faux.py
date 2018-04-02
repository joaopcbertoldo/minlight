from src.enums import AngleUnityEnum

from src.math_entities import \
    Vec3, \
    TupleAnglesRotation, \
    SpaceRechercheAnglesLimites, \
    IntervalleLineaire, \
    SphericalCoordinateSystem

from src.models.entites_systeme_minlight import \
    BoxDimensions, \
    Box, \
    CableLayout, \
    CableConfiguration

from src.simulation.limit_angles.angles_limites import VerificateurAnglesLimites

'''
    Setup d'un faux systeme.
    Destiné juste à faire des debugs avec des valeurs plus simples.
'''

''' ************************ Maisonette ************************ '''
# centre
centre_maisonette = \
    Vec3(
        x=7500,  # mm
        y=5000,  # mm
        z=5000  # mm
    )

# dimensions
dimensions_maisonette = \
    BoxDimensions(
        length=5000,  # mm
        width=10000,  # mm
        height=10000  # mm
    )

# pave
maisonette = \
    Box(
        centre=centre_maisonette,
        ypr_angles=TupleAnglesRotation.ZERO(),
        dimensions=dimensions_maisonette
    )

''' ************************ Source ************************ '''

# dimensions
dimensions_source = \
    BoxDimensions(
        length=1000,  # mm
        width=1000,  # mm
        height=1000  # mm
    )

''' ************************ Chambre ************************ '''

# centre
centre_chambre = \
    Vec3(
        x=5000,  # mm
        y=5000,  # mm
        z=5000  # mm
    )

# dimensions
dimensions_chambre = \
    BoxDimensions(
        length=10000,  # mm
        width=10000,  # mm
        height=10000  # mm
    )

# pavé
chambre = \
    Box(
        centre=centre_chambre,
        ypr_angles=TupleAnglesRotation.ZERO(),
        dimensions=dimensions_chambre
    )

''' ************************ Ancrage ************************ '''

''' ****** Points Fixes ****** '''
# toutes les ancrages sont supposées dans les coins de la chambre
# donc, les coordonnées sont toujours, soit 0, soit la dimension de la chambre
# sauf la length qui s'arrete juste au niveau de la maisonette

# coordonnées d'ancrage
x = 5000  # mm
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

cc_000 = CableConfiguration(source_vertex_name='S000', fixed_point=PF_000)  # cc_000
cc_100 = CableConfiguration(source_vertex_name='S100', fixed_point=PF_100)  # cc_100
cc_010 = CableConfiguration(source_vertex_name='S010', fixed_point=PF_010)  # cc_010
cc_110 = CableConfiguration(source_vertex_name='S110', fixed_point=PF_110)  # cc_110
cc_001 = CableConfiguration(source_vertex_name='S001', fixed_point=PF_001)  # cc_001
cc_101 = CableConfiguration(source_vertex_name='S101', fixed_point=PF_101)  # cc_101
cc_011 = CableConfiguration(source_vertex_name='S011', fixed_point=PF_011)  # cc_011
cc_111 = CableConfiguration(source_vertex_name='S111', fixed_point=PF_111)  # cc_111

''' ****** Configurations des Câbles ****** '''
config_ancrage = CableLayout(
    configs_cables=[cc_000, cc_100, cc_010, cc_110, cc_001, cc_101, cc_011, cc_111]
)

''' ************************ Systeme Spherique Baie Vitrée ************************ '''

# centre - supposé dans le centre de la face d'intérêt de la maisonette
centre_systeme_spherique = \
    Vec3(
        x=5000,  # mm
        y=5000,  # mm
        z=5000  # mm
    )

# rotation
rotation_systeme_spherique = \
    TupleAnglesRotation(
        yaw=180,  # degrés
        pitch=0,  # degrés
        row=0,  # degrés
        unite=AngleUnityEnum.degree,
    )

# systeme sphérique
systeme_spherique_baie_vitree = SphericalCoordinateSystem(
    centre=centre_systeme_spherique,
    ypr_angles=rotation_systeme_spherique
)

''' ************************ Configs Simulation ************************ '''

# space de recherche
space_recherche = \
    SpaceRechercheAnglesLimites(
        intervalle_rho=IntervalleLineaire(min=1000, max=1501, pas=250),  # mm
        intervalle_phi=IntervalleLineaire(min=0, max=180, pas=6),  # degres
        intervalle_theta=IntervalleLineaire(min=0, max=180, pas=6),  # degres
        unite=AngleUnityEnum.degree
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
    'space_recherche': space_recherche,
    'diametre_cable': diametre_cable,
    'n_discretisation_cables': n_discretisation_cables,
    'k_dicretisation_cubes': k_dicretisation_cubes,
    'verbose': verbose
}

''' ************************ VerificateurAnglesLimites ************************ '''

verificateur = VerificateurAnglesLimites(
    dimensions_source=dimensions_source,
    maisonette=maisonette,
    chambre=chambre,
    config_ancrage=config_ancrage,
    systeme_spherique_baie_vitree=systeme_spherique_baie_vitree,
    configs_simulation=configs_simulation
)


def __main__():
    print('faux a été importé')
    print(verificateur)  # overwrite str function
