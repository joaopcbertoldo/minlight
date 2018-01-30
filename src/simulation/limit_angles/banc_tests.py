# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
import matplotlib

from src.calculs.modeles.entites_mathemathiques import \
    SpaceRechercheAnglesLimites, \
    IntervalleLineaire
from src.calculs.modeles.enums import UniteAngleEnum
from src.calculs.setups import faux
from src.calculs.simulation_angles_limites import angles_limites_factory

matplotlib.use('Agg')


''' ************************ Configs Simulation ************************ '''

# space de recherche
intervalle_rho = IntervalleLineaire(min=500, max=3001, pas=250)  # mm

intervalle_phi = IntervalleLineaire(min=0, max=90, pas=1)        # degres

intervalle_theta = IntervalleLineaire(min=0, max=90, pas=1)      # degres

space_recherche = \
    SpaceRechercheAnglesLimites(
        intervalle_rho=intervalle_rho,
        intervalle_phi=intervalle_phi,
        intervalle_theta=intervalle_theta,
        unite=UniteAngleEnum.DEGRE
    )

# diameter des câbles
diametre_cable = 10  # mm

# discretisation des câbles
n_discretisation_cables = 30  # point/câble

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


''' ************************ Selection ************************ '''

selection = {
    'faux': {
        'calculer': False,
        'sauvegarder_graphe': False,
        'afficher_graphe': False,
        'afficher_demo_config': False
    },

    'simple_haut_haut': {
        'calculer': True,
        'sauvegarder_graphe': True,
        'afficher_graphe': False,
        'afficher_demo_config': False
    },

    'simple_haut_mid': {
        'calculer': True,
        'sauvegarder_graphe': True,
        'afficher_graphe': False,
        'afficher_demo_config': False
    },

    'simple_haut_bas': {
        'calculer': True,
        'sauvegarder_graphe': True,
        'afficher_graphe': False,
        'afficher_demo_config': False
    },

    'sh_sch_haut_haut': {
        'calculer': True,
        'sauvegarder_graphe': True,
        'afficher_graphe': False,
        'afficher_demo_config': False
    },

    'sh_sch_haut_mid': {
        'calculer': True,
        'sauvegarder_graphe': True,
        'afficher_graphe': False,
        'afficher_demo_config': False
    },

    'sh_sch_haut_bas': {
        'calculer': True,
        'sauvegarder_graphe': True,
        'afficher_graphe': False,
        'afficher_demo_config': False
    }
}


''' ************************ faux ************************ '''
if selection['faux']['calculer']:
    faux.verificateur.trouver_angles_limites(
        sauvegarde_automatique=True,
        nom_fichier_sauvegarde='./resultats_limites/faux'
    )

if selection['faux']['sauvegarder_graphe']:
    faux.verificateur.sauvegarder_graphe_limites_png(nom_fichier='./graphes/faux')

if selection['faux']['afficher_graphe']:
    faux.verificateur.afficher_graphe_limites()

if selection['faux']['afficher_demo_config']:
    faux.verificateur.draw_demo_config_ancrage()


''' ************************ simple haut-haut ************************ '''

simple_haut_haut = angles_limites_factory.get_simple_haut_haut(configs_simulation=configs_simulation)

if selection['simple_haut_haut']['calculer']:
    simple_haut_haut.trouver_angles_limites(
        sauvegarde_automatique=True,
        nom_fichier_sauvegarde='./resultats_limites/simple_haut_haut'
    )

if selection['simple_haut_haut']['sauvegarder_graphe']:
    simple_haut_haut.sauvegarder_graphe_limites_png(nom_fichier='./graphes/simple_haut_haut')

if selection['simple_haut_haut']['afficher_graphe']:
    simple_haut_haut.afficher_graphe_limites()

if selection['simple_haut_haut']['afficher_demo_config']:
    simple_haut_haut.draw_demo_config_ancrage()


''' ************************ simple haut-mid ************************ '''

simple_haut_mid = angles_limites_factory.get_simple_haut_mid(configs_simulation=configs_simulation)

if selection['simple_haut_mid']['calculer']:
    simple_haut_mid.trouver_angles_limites(
        sauvegarde_automatique=True,
        nom_fichier_sauvegarde='./resultats_limites/simple_haut_mid'
    )

if selection['simple_haut_mid']['sauvegarder_graphe']:
    simple_haut_mid.sauvegarder_graphe_limites_png(nom_fichier='./graphes/simple_haut_mid')

if selection['simple_haut_mid']['afficher_graphe']:
    simple_haut_mid.afficher_graphe_limites()

if selection['simple_haut_mid']['afficher_demo_config']:
    simple_haut_mid.draw_demo_config_ancrage()


''' ************************ simple haut-bas ************************ '''

simple_haut_bas = angles_limites_factory.get_simple_haut_bas(configs_simulation=configs_simulation)

if selection['simple_haut_bas']['calculer']:
    simple_haut_bas.trouver_angles_limites(
        sauvegarde_automatique=True,
        nom_fichier_sauvegarde='./resultats_limites/simple_haut_bas'
    )

if selection['simple_haut_bas']['sauvegarder_graphe']:
    simple_haut_bas.sauvegarder_graphe_limites_png(nom_fichier='./graphes/simple_haut_bas')

if selection['simple_haut_bas']['afficher_graphe']:
    simple_haut_bas.afficher_graphe_limites()

if selection['simple_haut_bas']['afficher_demo_config']:
    simple_haut_bas.draw_demo_config_ancrage()


''' ************************ sh sch haut-haut ************************ '''

sh_sch_haut_haut = angles_limites_factory.get_sh_sch_haut_haut(configs_simulation=configs_simulation)

if selection['sh_sch_haut_haut']['calculer']:
    sh_sch_haut_haut.trouver_angles_limites(
        sauvegarde_automatique=True,
        nom_fichier_sauvegarde='./resultats_limites/sh_sch_haut_haut'
    )

if selection['sh_sch_haut_haut']['sauvegarder_graphe']:
    sh_sch_haut_haut.sauvegarder_graphe_limites_png(nom_fichier='./graphes/sh_sch_haut_haut')

if selection['sh_sch_haut_haut']['afficher_graphe']:
    sh_sch_haut_haut.afficher_graphe_limites()

if selection['sh_sch_haut_haut']['afficher_demo_config']:
    sh_sch_haut_haut.draw_demo_config_ancrage()


''' ************************ sh sch haut-mid ************************ '''

sh_sch_haut_mid = angles_limites_factory.get_sh_sch_haut_mid(configs_simulation=configs_simulation)

if selection['sh_sch_haut_mid']['calculer']:
    sh_sch_haut_mid.trouver_angles_limites(
        sauvegarde_automatique=True,
        nom_fichier_sauvegarde='./resultats_limites/sh_sch_haut_mid'
    )

if selection['sh_sch_haut_mid']['sauvegarder_graphe']:
    sh_sch_haut_mid.sauvegarder_graphe_limites_png(nom_fichier='./graphes/sh_sch_haut_mid')

if selection['sh_sch_haut_mid']['afficher_graphe']:
    sh_sch_haut_mid.afficher_graphe_limites()

if selection['sh_sch_haut_mid']['afficher_demo_config']:
    sh_sch_haut_mid.draw_demo_config_ancrage()


''' ************************ sh sch haut-bas ************************ '''

sh_sch_haut_bas = angles_limites_factory.get_sh_sch_haut_bas(configs_simulation=configs_simulation)

if selection['sh_sch_haut_bas']['calculer']:
    sh_sch_haut_bas.trouver_angles_limites(
        sauvegarde_automatique=True,
        nom_fichier_sauvegarde='./resultats_limites/sh_sch_haut_bas'
    )

if selection['sh_sch_haut_bas']['sauvegarder_graphe']:
    sh_sch_haut_bas.sauvegarder_graphe_limites_png(nom_fichier='./graphes/sh_sch_haut_bas')

if selection['sh_sch_haut_bas']['afficher_graphe']:
    sh_sch_haut_bas.afficher_graphe_limites()

if selection['sh_sch_haut_bas']['afficher_demo_config']:
    sh_sch_haut_bas.draw_demo_config_ancrage()
