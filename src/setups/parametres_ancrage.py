from src.calculs.modeles.entites_mathemathiques import Vec3

from src.calculs.setups.parametres_objets import dimensions_chambre, distance_evaporateur_maisonette


'''
Paramètres 
'''


''' ************************ Points Fixes ************************ '''
# toutes les ancrages sont supposées dans les coins de la chambre
# donc, les coordonnées sont toujours, soit 0, soit la dimension de la chambre
# sauf la length qui s'arrete juste au niveau de la maisonette


class Ideal:

    # coordonnées d'ancrage
    x = distance_evaporateur_maisonette  # mm
    y = dimensions_chambre['width']    # mm
    z = dimensions_chambre['height']    # mm

    # la numérotation <<PF_xxx>> suit la logique des sommets des pavés
    # le <<xxx>> indique à quel "coin" de la chambre le point est fixé

    @staticmethod
    def get_haut_bas():
        return {
            'PF_000': Vec3(      0,       0,       0),  # PF_000
            'PF_100': Vec3(Ideal.x,       0,       0),  # PF_100
            'PF_010': Vec3(      0, Ideal.y,       0),  # PF_010
            'PF_110': Vec3(Ideal.x, Ideal.y,       0),  # PF_110
            'PF_001': Vec3(      0,       0, Ideal.z),  # PF_001
            'PF_101': Vec3(Ideal.x,       0, Ideal.z),  # PF_101
            'PF_011': Vec3(      0, Ideal.y, Ideal.z),  # PF_011
            'PF_111': Vec3(Ideal.x, Ideal.y, Ideal.z)   # PF_111
        }

    @staticmethod
    def get_haut_mid():
        return {
            'PF_000': Vec3(      0,       0, Ideal.z/2),  # PF_000
            'PF_100': Vec3(Ideal.x,       0, Ideal.z/2),  # PF_100
            'PF_010': Vec3(      0, Ideal.y, Ideal.z/2),  # PF_010
            'PF_110': Vec3(Ideal.x, Ideal.y, Ideal.z/2),  # PF_110
            'PF_001': Vec3(      0,       0, Ideal.z),    # PF_001
            'PF_101': Vec3(Ideal.x,       0, Ideal.z),    # PF_101
            'PF_011': Vec3(      0, Ideal.y, Ideal.z),    # PF_011
            'PF_111': Vec3(Ideal.x, Ideal.y, Ideal.z)     # PF_111
        }

    @staticmethod
    def get_haut_haut():
        return {
            'PF_000': Vec3(      0,       0, Ideal.z),  # PF_000
            'PF_100': Vec3(Ideal.x,       0, Ideal.z),  # PF_100
            'PF_010': Vec3(      0, Ideal.y, Ideal.z),  # PF_010
            'PF_110': Vec3(Ideal.x, Ideal.y, Ideal.z),  # PF_110
            'PF_001': Vec3(      0,       0, Ideal.z),  # PF_001
            'PF_101': Vec3(Ideal.x,       0, Ideal.z),  # PF_101
            'PF_011': Vec3(      0, Ideal.y, Ideal.z),  # PF_011
            'PF_111': Vec3(Ideal.x, Ideal.y, Ideal.z)   # PF_111
        }