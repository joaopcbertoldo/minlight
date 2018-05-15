from numpy import cos, sin, matrix, sqrt
import numpy as np
from pprint import pprint


def point_3d(x, y, z):
    '''
    Retourne une matrice colonne 3x1 (numpy.matrix).
    [x, y, z]^T
    :return: matrice (numpy.matrix) colonne 3x1
    '''
    return matrix([[x], [y], [z]])


def get_coordonnees_point_3d(point):
    '''
    Prend un point_3d et retourne une tuple (x,y,z).
    :param point: matrice (numpy.matrix) colonne 3x1
    '''
    return point.item(0), point.item(1), point.item(2)


def vecteur_3d(x, y, z):
    '''
    Retourne une matrice colonne 3x1 (numpy.matrix).
    [x, y, z]^T
    :return: matrice (numpy.matrix) colonne 3x1
    '''
    return matrix([[x], [y], [z]])


def get_coordonnees_vecteur_3d(vecteur):
    '''
    Prend un point_3d et retourne une tuple (x,y,z).
    :param point: matrice (numpy.matrix) colonne 3x1
    '''
    return vecteur.item(0), vecteur.item(1), vecteur.item(2)


def rpy_angles(row, pitch, yaw):
    return {'yaw': yaw, 'pitch': pitch, 'row': row}


def get_ypr_angles(angles):
    return angles['yaw'], angles['pitch'], angles['row']


def get_rpy_angles(angles):
    return angles['row'], angles['pitch'], angles['yaw']


def dimensions_pave(length, width, height):
    return {'length': length, 'width': width, 'height': height}


def get_dimensions_pave(dimensions):
    return dimensions['length'], dimensions['width'], dimensions['height']


def vecteur_difference_2_points(depart, arrive):
    return arrive - depart


def norme_vecteur(vecteur):
    return sqrt(vecteur.T * vecteur)


def distance_2_points(A, B):
    '''
    Distance euclidiainne en 3D entre 2 vertices_points_list.
    :param A: matrice (numpy.matrix) colonne 3x1
    :param B: matrice (numpy.matrix) colonne 3x1
    '''
    return norme_vecteur(vecteur_difference_2_points(A, B))


def matrice_rotation_x(angle):
    s, c = sin(angle), cos(angle)
    return matrix([
        [1, 0, 0],
        [0, c, -s],
        [0, s, c]
    ])


def matrice_rotation_y(angle):
    s, c = sin(angle), cos(angle)
    return matrix([
        [c, 0, s],
        [0, 1, 0],
        [-s, 0, c]
    ])


def matrice_rotation_z(angle):
    s, c = sin(angle), cos(angle)
    return matrix([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ])


def matrice_rotation_z1_y2_x3(angles):
    yaw, pitch, row = get_ypr_angles(angles)
    return matrice_rotation_z(yaw) * matrice_rotation_y(pitch) * matrice_rotation_x(row)


def matrice_rotation_x1_y2_z3(angles):
    row, pitch, yaw = get_rpy_angles(angles)
    return matrice_rotation_x(row) * matrice_rotation_y(pitch) * matrice_rotation_z(yaw)


def generer_noms_sommets_pave():
    return ['S000', 'S100', 'S010', 'S110', 'S001', 'S101', 'S011', 'S111']


def generer_dictionnaire_sommets(sommets):
    return {nom: sommet for nom, sommet in zip(generer_noms_sommets_pave(), sommets)}


def get_points_ancrage_ordones(configs_ancrage):
    return [configs_ancrage[nom] for nom in generer_noms_sommets_pave()]


def sommets_pave_origine(dimensions):
    # dimensions
    long, larg, haut = get_dimensions_pave(dimensions)

    # sommets (coins) du pavé centré dans l'origine
    S000 = point_3d(+ long / 2, - larg / 2, - haut / 2)
    S100 = point_3d(- long / 2, - larg / 2, - haut / 2)
    S010 = point_3d(+ long / 2, + larg / 2, - haut / 2)
    S110 = point_3d(- long / 2, + larg / 2, - haut / 2)
    S001 = point_3d(+ long / 2, - larg / 2, + haut / 2)
    S101 = point_3d(- long / 2, - larg / 2, + haut / 2)
    S011 = point_3d(+ long / 2, + larg / 2, + haut / 2)
    S111 = point_3d(- long / 2, + larg / 2, + haut / 2)

    # sommets (coins) de la source repérés par rapport à son _center
    return [S000, S100, S010, S110, S001, S101, S011, S111]


def sommets_pave(centre, ypr_angles, dimensions):
    '''
    convention utilisé pour les rotations : z-y’-x″ (intrinsic rotations) = Yaw, pitch, and roll rotations
    http://planning.cs.uiuc.edu/node102.html
    http://planning.cs.uiuc.edu/node104.html
    https://en.wikipedia.org/wiki/Euler_angles#Tait.E2.80.93Bryan_angles
    https://en.wikipedia.org/wiki/Euler_angles#Rotation_matrix

    *** ancien 'anglesToPos' ***

    On suppose qu'on veut orienter le _center de la source par des angles
    et la position du _center, on calcule les positios des sommets (les coins de la source).
    :param centreSoleil: _center de la source dans le système de repère de la chambre
    :param theta: remplir...
    :param phi: remplir...
    :param dimensionsSource: (dictionnaire) length, width, height du pave de la source
    :return: liste des sommets de la source par rapport au système de repère de la chambre
    '''

    # Sommets
    # sommets (coins) de la source repérés par rapport à son _center
    S_origine = sommets_pave_origine(dimensions)

    # matrice de rotation
    Rot = matrice_rotation_z1_y2_x3(ypr_angles)

    # rotation
    S_origine_rot = [Rot * s for s in S_origine]

    # translation
    S = [s + centre for s in S_origine_rot]

    return S


def point_appartient_pave_origine(point, dimensions):
    '''
    Fonction qui teste si un point est dans le volume d'un pavé localisé à l'origine.
    :param dimensions: (dictionnaire) length, width, height du pave de la source
    :return: False/True
    '''
    long, larg, haut = get_dimensions_pave(dimensions)

    demi_long, demi_larg, demi_haut = long / 2, larg / 2, haut / 2

    x, y, z = get_coordonnees_point_3d(point)

    return -demi_long <= x <= demi_long and \
           -demi_larg <= y <= demi_larg and \
           -demi_haut <= z <= demi_haut


def point_appartient_pave(point, centre, ypr_angles, dimensions):
    '''
    Fonction qui teste si un point est dans le volume d'un pavé localisé à l'origine.
    :param dimensions: (dictionnaire) length, width, height du pave de la source
    :param centre: _center du pavé repéré dans le sys de coordonnées globale
    :return: False/True
    '''
    point_repere_translate = point - centre

    yaw, pitch, row = get_ypr_angles(ypr_angles)

    angles_opposes = rpy_angles(row=-row, pitch=-pitch, yaw=-yaw)

    rot = matrice_rotation_x1_y2_z3(angles_opposes)

    point_repere_pave = rot * point_repere_translate

    return point_appartient_pave_origine(point_repere_pave, dimensions)


def point_appartient_pave_droit_S000(point, centre, dimensions):
    '''
    Fonction qui teste si un point est dans le volume d'un pavé dont le point Mini est donné.
    :param dimensions: (dictionnaire) length, width, height du pave de la source
    :param centre: _center du pavé repéré dans le sys de coordonnées globale
    :return: False/True
    '''
    return point_appartient_pave_origine(point - centre, dimensions)


def direction_difference_2_points(depart, arrive):
    vec = vecteur_difference_2_points(depart, arrive)

    x, y, z = get_coordonnees_vecteur_3d(vec)

    norm = norme_vecteur(vec)

    xn, yn, zn = x / norm, y / norm, z / norm

    return vecteur_3d(xn, yn, zn)


def creer_vecteurs_cables(points_ancrage, sommets_source):
    return [vecteur_difference_2_points(pa, ss)
            for pa, ss
            in zip(points_ancrage, sommets_source)]


def longueurs_utiles_cables(les_vecteurs_cable):
    return [norme_vecteur(vc) for vc in les_vecteurs_cable]


def generator_points_discretisation_cable(point_ancrage, vecteur_cable, N):
    return (point_ancrage + (i / N) * vecteur_cable
            for i in range(1, N))


# pas encore utilisé
def tester_interdictions_points(generator_points, tests_interdictions):
    resultats = {t['nom']: t['message_ok'] for t in tests_interdictions}
    for p in generator_points:
        for t in tests_interdictions:
            fonction = t['fonction']
            args = t['args']
            if fonction.__call__(p, **args):
                resultats[t['nom']] = t['message_probleme']
    return resultats

"""
def verifier_cables(cables, maisonette, source, chambre, N_discretisation=300):
    centre_maisonette, dimensions_maisonette = maisonette['_center'], maisonette['dimensions']

    centre_source, ypr_angles_source, dimensions_source = source['_center'], source['_orientation'], source['dimensions']

    dimensions_room = chambre['dimensions']

    generators_points = {}
    for cable in cables:
        nom, point_ancrage, vecteur = cable['nom'], cable['point_ancrage'], cable['vecteur']

        generators_points[nom] = generator_points_discretisation_cable(point_ancrage, vecteur, N_discretisation)

    bilan = {}
    for nom, gen in generators_points.items():
        message = \
            {
                'maisonette': 'ok',
                'source': 'ok',
                'chambre': 'ok',
                'croisement': '?'
            }

        for point in gen:
            # maisonette
            if point_appartient_pave_droit_S000(point, centre_maisonette, dimensions_maisonette):
                message['maisonette'] = '!'

            # source
            if point_appartient_pave(point, centre_source, ypr_angles_source, dimensions_source):
                message['source'] = '!'

            # chambre
            if not point_appartient_pave_droit_S000(thisdir, point_3d(0, 0, 0), dimensions_room):
                message['chambre'] = '!'

                # ajouter les croisements

        bilan[nom] = message

    return bilan


def verifier_position(maisonette, source, chambre, configs_ancrage, print_results=False):
    sommets_source = sommets_pave(_center=source['_center'],
                                  _orientation=source['_orientation'],
                                  dimensions=source['dimensions'])

    points_ancrage = get_points_ancrage_ordones(configs_ancrage)

    vecteurs_cables = creer_vecteurs_cables(points_ancrage, sommets_source)

    cables = [{'nom': nom, 'point_ancrage': pa, 'vecteur': vec}
              for nom, pa, vec
              in zip(generer_noms_sommets_pave(), points_ancrage, vecteurs_cables)]

    bilan_cables = verifier_cables(cables, maisonette, source, chambre)

    # verifier si source touche murs
    # verifier si source touche maisonette
    # verifier si source touche evap

    if print_results:
        print('Bilan des résultats des cãbles')
        pprint(bilan_cables)


def maxTheta(r, phi, maisonette, source, chambre, configs_ancrag)
    # r : distance entre _center de la face de la maisonette et le _center de la source, r des coordonnes spheriques
    # phi : angle verticale , coordonnes spheriques
    # centreRotation:
    # maisonette
    # source
    # chambre


    wallCentre = creerPoint(LargCC / 2, LongM, HautM / 2)  # milieu du mur d'interet

    sourceCentreReference = creerPoint(LargCC / 2 + r, LongM, HautM / 2) - wallCentre

    maxTheta = [][]  # stores a max theta for each phi
    for i in range(90):
        for j in range(90):
            maxTheta[i][j] = 90

    for phiDegrees in range(90):
        for thetaDegrees in range(90):
            phi = math.radians(phiDegrees)
            theta = math.radians(thetaDegrees)
            rotationMatrixTheta = np.matrix([[1, 0, 0], [0, cos(theta), -sin(theta)], [0, sin(theta), cos(theta)]])
            rotationMatrixPhi = np.matrix([[cos(phi), -sin(phi), 0], [sin(phi), cos(phi), 0], [0, 0, 1]])
            sourceRotated = rotationMatrixTheta * rotationMatrixPhi * sourceCentreReference
            directionNormale = sourceRotated - wallCentres
            directionNormale = directionNormale / norme_vecteur(directionNormale)
            roll = arctan(directionNormale[1] / directionNormale[0])
            pitch = arctan(sqrt(directionNormale[0] ** 2 + directionNormale[1] ** 2) / directionNormale[2])
            if (verifySource(sourceCentre, roll, pitch))  # a faire
                continue
            maxTheta[phiDegrees] = thetaDegrees
            break
"""




