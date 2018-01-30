from src.calculs.simulation_angles_limites.setups import parametres_objets, parametres_ancrage

from src.calculs.setups import configuration_ancrage
from src.calculs.simulation_angles_limites.angles_limites import VerificateurAnglesLimites

chambre = parametres_objets.chambre

maisonette = parametres_objets.maisonette

dimensions_source = parametres_objets.dimensions_source

systeme_spherique_baie_vitree = parametres_objets.systeme_spherique_baie_vitree


def get_simple_haut_haut(configs_simulation):

    points_fixes = parametres_ancrage.Ideal.get_haut_haut()

    config_ancrage = configuration_ancrage.get_simple(points_fixes)

    verificateur = VerificateurAnglesLimites(
        dimensions_source=dimensions_source,
        maisonette=maisonette,
        chambre=chambre,
        config_ancrage=config_ancrage,
        systeme_spherique_baie_vitree=systeme_spherique_baie_vitree,
        configs_simulation=configs_simulation
    )

    return verificateur


def get_simple_haut_mid(configs_simulation):

    points_fixes = parametres_ancrage.Ideal.get_haut_mid()

    config_ancrage = configuration_ancrage.get_simple(points_fixes)

    verificateur = VerificateurAnglesLimites(
        dimensions_source=dimensions_source,
        maisonette=maisonette,
        chambre=chambre,
        config_ancrage=config_ancrage,
        systeme_spherique_baie_vitree=systeme_spherique_baie_vitree,
        configs_simulation=configs_simulation
    )

    return verificateur


def get_simple_haut_bas(configs_simulation):

    points_fixes = parametres_ancrage.Ideal.get_haut_bas()

    config_ancrage = configuration_ancrage.get_simple(points_fixes)

    verificateur = VerificateurAnglesLimites(
        dimensions_source=dimensions_source,
        maisonette=maisonette,
        chambre=chambre,
        config_ancrage=config_ancrage,
        systeme_spherique_baie_vitree=systeme_spherique_baie_vitree,
        configs_simulation=configs_simulation
    )

    return verificateur


def get_sh_sch_haut_haut(configs_simulation):

    points_fixes = parametres_ancrage.Ideal.get_haut_haut()

    config_ancrage = configuration_ancrage.get_tourne_sh_sch(points_fixes)

    verificateur = VerificateurAnglesLimites(
        dimensions_source=dimensions_source,
        maisonette=maisonette,
        chambre=chambre,
        config_ancrage=config_ancrage,
        systeme_spherique_baie_vitree=systeme_spherique_baie_vitree,
        configs_simulation=configs_simulation
    )

    return verificateur


def get_sh_sch_haut_mid(configs_simulation):

    points_fixes = parametres_ancrage.Ideal.get_haut_mid()

    config_ancrage = configuration_ancrage.get_tourne_sh_sch(points_fixes)

    verificateur = VerificateurAnglesLimites(
        dimensions_source=dimensions_source,
        maisonette=maisonette,
        chambre=chambre,
        config_ancrage=config_ancrage,
        systeme_spherique_baie_vitree=systeme_spherique_baie_vitree,
        configs_simulation=configs_simulation
    )

    return verificateur


def get_sh_sch_haut_bas(configs_simulation):

    points_fixes = parametres_ancrage.Ideal.get_haut_bas()

    config_ancrage = configuration_ancrage.get_tourne_sh_sch(points_fixes)

    verificateur = VerificateurAnglesLimites(
        dimensions_source=dimensions_source,
        maisonette=maisonette,
        chambre=chambre,
        config_ancrage=config_ancrage,
        systeme_spherique_baie_vitree=systeme_spherique_baie_vitree,
        configs_simulation=configs_simulation
    )

    return verificateur


