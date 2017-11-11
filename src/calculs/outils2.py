from numpy import cos, sin, pi, matrix, sqrt
from numpy.linalg import pinv
import numpy as np
from pprint import pprint

from entites import *

import shapely.geometry as geom


def point_appartient_pave_origine(point, dimensions):
    '''
    Fonction qui teste si un point est dans le volume d'un pavé localisé à l'origine.
    :param dimensions: (dictionnaire) longueur, largeur, hauteur du pave de la source
    :return: False/True
    '''
    long, larg, haut = dimensions.get_tuple_dimensions()

    demi_long, demi_larg, demi_haut = long / 2, larg / 2, haut / 2

    x, y, z = point.get_coordonnes()

    return -demi_long <= x <= demi_long and \
           -demi_larg <= y <= demi_larg and \
           -demi_haut <= z <= demi_haut


def point_appartient_pave(point, pave):
    '''
    Fonction qui teste si un point est dans le volume d'un pavé localisé à l'origine.
    :param dimensions: (dictionnaire) longueur, largeur, hauteur du pave de la source
    :param centre: centre du pavé repéré dans le sys de coordonnées globale
    :return: False/True
    '''
    point_repere_translate = point - pave.centre

    Rot = pave.ypr_angles \
              .get_tuple_angles_pour_inverser_rotation() \
              .get_matrice_rotation()

    point_repere_pave = Rot * point_repere_translate

    return point_appartient_pave_origine(point_repere_pave, pave.dimensions)



def verifier_cables(cables, maisonette, source, dimensions_chambre, N_discretisation=300):

    chambre = Pave(
        centre     = Vecteur3D(0, 0, 0),
        ypr_angles = TupleAnglesRotation(0, 0, 0),
        dimensions = dimensions_chambre
    )

    generators_points = {}

    bilan = {}
    for cable in cables:
        message = \
            {
                'maisonette': 'ok',
                'source': 'ok',
                'chambre': 'ok',
                'croisement': '?'
            }

        for point in cable.get_generator_points_discretisation(N_discretisation):
            # maisonette
            if point_appartient_pave(point, maisonette):
                message['maisonette'] = '!'

            # source
            if point_appartient_pave(point, source):
                message['source'] = '!'

            # chambre
            if not point_appartient_pave(point, chambre):
                message['chambre'] = '!'

            # ajouter les croisements

        bilan[cable.nom_sommet_source] = message

    return bilan


def verifier_position(maisonette, source, chambre, config_ancrage, print_results=False):
    sommets_source = source.get_dictionnaire_sommets()

    cables = config_ancrage.get_cables(sommets_source)

    bilan_cables = verifier_cables(cables, maisonette, source, chambre)

    # verifier si source touche murs
    # verifier si source touche maisonette
    # verifier si source touche evap

    if print_results:
        print('Bilan des résultats des cãbles')
        pprint(bilan_cables)

    return any(str == '!' for str in list(bilan_cables.values()))


def changer_source_a_partir_des_coordonnes_spheriques(source, coordonnees_spheriques, systeme_spherique):
    roh, theta, phi = coordonnees_spheriques.get_coordonnees_spheriques()

    # p = centre de la source pour le systeme cartesien à partir du quel le spherique est defini
    p = systeme_spherique.convertir_en_cartesien(coordonnees_spheriques)

    centre_systeme, ypr_angles_systeme = systeme_spherique.get_centre_et_ypr_angles()

    Rot = ypr_angles_systeme.get_tuple_angles_pour_inverser_rotation()

    source.centre = Rot * p + centre_systeme

    source.ypr_angles = \
        TupleAnglesRotation(
            row      = 0,
            pitch    = phi,
            yaw      = theta,
            sequence = SequenceAnglesRotationEnum.YPR,
            unite    = UniteAngleEnum.DEGRE  # !!!!!!!!!!!!!!!!!!!!!!!!
        )


def trouver_angles_limites(space_recherche, maisonette, dimensions_source, chambre, config_ancrage, systeme_spherique_baie_vitree):

    intervalle_rho, intervalle_phi, intervalle_theta = space_recherche.get_intervalles()

    resultats = {}

    source = Pave(
        centre     = Vecteur(0,0,0),
        ypr_angles = TupleAnglesRotation(0,0,0),
        dimensions = dimensions_source
    )

    for rho in intervalle_rho:
        couples = []

        resultats[rho] = couples

        premier_phi_ok = False

        for phi in intervalle_phi:

            for theta in intervalle_theta:
                theta_max = theta

                changer_source_a_partir_des_coordonnes_spheriques(
                    source                 = source,
                    coordonnees_spheriques = CoordonnesSpherique(rho, theta, phi),
                    systeme_spherique      = systeme_spherique_baie_vitree
                )

                if verifier_position(maisonette, source, chambre, config_ancrage):
                    premier_phi_ok = True
                else:
                    break

            couples.append((phi, theta_max))

            if not premier_phi_ok:
                break

def solutions_formule_quadratique(a,b,c):
    return ((-b - sqrt(b*b - 4*a*c))/(2*a),(-b + sqrt(b*b - 4*a*c))/(2*a))


'''
def maxTheta(r, phi, maisonette,source,chambre,configs_ancrag)
#r : distance entre centre de la face de la maisonette et le centre de la source, r des coordonnes spheriques
#phi : angle verticale , coordonnes spheriques
#centreRotation:
#maisonette
#source
#chambre


    wallCentre = creerPoint(LargCC/2,LongM,HautM/2) # milieu du mur d'interet

    sourceCentreReference = creerPoint(LargCC/2 + r,LongM,HautM/2) - wallCentre

    maxTheta = [][] #stores a max theta for each phi
    for i in range(90):
        for j in range(90):
            maxTheta[i][j] = 90

    for phiDegrees in range(90):
        for thetaDegrees in range(90):
                phi = math.radians(phiDegrees)
                theta = math.radians(thetaDegrees)
                rotationMatrixTheta = np.matrix([[1,0,0],[0,cos(theta),-sin(theta)],[0,sin(theta),cos(theta)]])
                rotationMatrixPhi = np.matrix([[cos(phi),-sin(phi),0],[sin(phi),cos(phi),0],[0,0,1]])
                sourceRotated = rotationMatrixTheta*rotationMatrixPhi*sourceCentreReference
                directionNormale = sourceRotated - wallCentres
                directionNormale = directionNormale/norme_vecteur(directionNormale)
                roll = arctan(directionNormale[1]/directionNormale[0])
                pitch = arctan(sqrt(directionNormale[0]**2  + directionNormale[1]**2 )/directionNormale[2])
                if(verifySource(sourceCentre,roll,pitch))#a faire
                    continue
                maxTheta[phiDegrees] = thetaDegrees
                break

'''