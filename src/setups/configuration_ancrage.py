from enum import Enum
from pprint import pprint

from src.models.entites_systeme_minlight import CableLayout, CableConfiguration


''' ************************ Configurations des Câbles ************************ '''
# la numérotation <<cc_xxx>> suit la logique des sommets des pavés
# le <<xxx>> indique à quel sommet le cable sera rataché DANS LA SOURCE


''' ************************ Directions et Plans ************************ '''


class DirectionEnum(Enum):
    unknown = 0
    X = 1
    Y = 2
    Z = 3

    def get_lettre(self):
        return self.name.lower()


class PlanEnum(Enum):
    unknown = 0
    XY = 1
    XZ = 2
    YZ = 3

    def get_direction_manquante(self):
        return DirectionEnum.X if self == self.YZ else \
               DirectionEnum.Y if self == self.XZ else \
               DirectionEnum.Z if self == self.XY else \
               DirectionEnum.unknown


''' ************************ Sous Configurations des Câbles ************************ '''


class SousConfigCableEnum(Enum):
    unknown = 0
    SIMPLE = 1
    CROISE_UP_DOWN = 2
    CROISE_LEFT_RIGHT = 3
    TOURNE_SENS_HORLOGE = 4
    TOURNE_SENS_CONTRE_HORLOGE = 5


class Sequence3emeDirectionEnum(Enum):
    unknown = 0
    CONSTANTE = 1
    DEUX_A_DEUX = 2
    INTERMITANTE = 3

    def get_sequence(self, valeur):

        if self == Sequence3emeDirectionEnum.CONSTANTE:
            return [valeur] * 4

        elif self == Sequence3emeDirectionEnum.DEUX_A_DEUX:
            return [valeur] * 2 + [int(not valeur)] * 2

        elif self == Sequence3emeDirectionEnum.INTERMITANTE:
            return [valeur, int(not valeur)] * 2

        else:
            raise Exception('direction_fixe doit être Sequence3emeDirectionEnum')


''' ************************ Sous Configuration de Plan ************************ '''
"""
"""


class SousConfigCable:
    """
    """

    ''' ****** Simple ****** '''
    # YZ
    simple_yz = {
        'PF_x00': 'Sx00',
        'PF_x10': 'Sx10',
        'PF_x01': 'Sx01',
        'PF_x11': 'Sx11'
    }

    # XZ
    simple_xz = {
        'PF_0y0': 'S0y0',
        'PF_1y0': 'S1y0',
        'PF_0y1': 'S0y1',
        'PF_1y1': 'S1y1'
    }

    # XY
    simple_xy = {
        'PF_00z': 'S00z',
        'PF_10z': 'S10z',
        'PF_01z': 'S01z',
        'PF_11z': 'S11z'
    }

    ''' ****** Croisé UP-DOWN ****** '''
    # YZ
    croise_up_down_yz = {
        'PF_x00': 'Sx10',
        'PF_x10': 'Sx00',
        'PF_x01': 'Sx11',
        'PF_x11': 'Sx01'
    }

    # XZ
    croise_up_down_xz = {
        'PF_0y0': 'S1y0',
        'PF_1y0': 'S0y0',
        'PF_0y1': 'S1y1',
        'PF_1y1': 'S0y1'
    }

    # XY
    croise_up_down_xy = {
        'PF_00z': 'S10z',
        'PF_10z': 'S00z',
        'PF_01z': 'S11z',
        'PF_11z': 'S01z'
    }

    ''' ****** Croisé LEFT-RIGHT ****** '''
    # YZ
    croise_left_right_yz = {
        'PF_x00': 'Sx01',
        'PF_x10': 'Sx11',
        'PF_x01': 'Sx00',
        'PF_x11': 'Sx10'
    }

    # XZ
    croise_left_right_xz = {
        'PF_0y0': 'S0y1',
        'PF_1y0': 'S1y1',
        'PF_0y1': 'S0y0',
        'PF_1y1': 'S1y0'
    }

    # XY
    croise_left_right_xy = {
        'PF_00z': 'S01z',
        'PF_10z': 'S11z',
        'PF_01z': 'S00z',
        'PF_11z': 'S10z'
    }

    ''' ****** Tourné Sens Horloge ****** '''
    # YZ
    tourne_sens_horloge_yz = {
        'PF_x00': 'Sx01',
        'PF_x10': 'Sx00',
        'PF_x01': 'Sx11',
        'PF_x11': 'Sx10'
    }

    # XZ
    tourne_sens_horloge_xz = {
        'PF_0y0': 'S1y0',
        'PF_1y0': 'S1y1',
        'PF_0y1': 'S0y0',
        'PF_1y1': 'S0y1'
    }

    # XY
    tourne_sens_horloge_xy = {
        'PF_00z': 'S01z',
        'PF_10z': 'S00z',
        'PF_01z': 'S11z',
        'PF_11z': 'S10z'
    }

    ''' ****** Tourné Sens Contre Horloge ****** '''
    # YZ
    tourne_sens_contre_horloge_yz = {
        'PF_x00': 'Sx10',
        'PF_x10': 'Sx11',
        'PF_x01': 'Sx00',
        'PF_x11': 'Sx01'
    }

    # XZ
    tourne_sens_contre_horloge_xz = {
        'PF_0y0': 'S0y1',
        'PF_1y0': 'S0y0',
        'PF_0y1': 'S1y1',
        'PF_1y1': 'S1y0'
    }

    # XY
    tourne_sens_contre_horloge_xy = {
        'PF_00z': 'S10z',
        'PF_10z': 'S11z',
        'PF_01z': 'S00z',
        'PF_11z': 'S01z'
    }

    ''' ****** Dictionnaire des configs X plans ****** '''
    configs_plans = {
        SousConfigCableEnum.SIMPLE: {
            PlanEnum.YZ: simple_yz,
            PlanEnum.XZ: simple_xz,
            PlanEnum.XY: simple_xy
        },

        SousConfigCableEnum.CROISE_UP_DOWN: {
            PlanEnum.YZ: croise_up_down_yz,
            PlanEnum.XZ: croise_up_down_xz,
            PlanEnum.XY: croise_up_down_xy
        },

        SousConfigCableEnum.CROISE_LEFT_RIGHT: {
            PlanEnum.YZ: croise_left_right_yz,
            PlanEnum.XZ: croise_left_right_xz,
            PlanEnum.XY: croise_left_right_xy
        },

        SousConfigCableEnum.TOURNE_SENS_HORLOGE: {
            PlanEnum.YZ: tourne_sens_horloge_yz,
            PlanEnum.XZ: tourne_sens_horloge_xz,
            PlanEnum.XY: tourne_sens_horloge_xy
        },

        SousConfigCableEnum.TOURNE_SENS_CONTRE_HORLOGE: {
            PlanEnum.YZ: tourne_sens_contre_horloge_yz,
            PlanEnum.XZ: tourne_sens_contre_horloge_xz,
            PlanEnum.XY: tourne_sens_contre_horloge_xy
        },
    }

    ''' ****** Methodes ****** '''

    def __init__(self, sous_config, plan):

        if sous_config != SousConfigCableEnum.SIMPLE and \
           sous_config != SousConfigCableEnum.CROISE_UP_DOWN and \
           sous_config != SousConfigCableEnum.CROISE_LEFT_RIGHT and \
           sous_config != SousConfigCableEnum.TOURNE_SENS_HORLOGE and \
           sous_config != SousConfigCableEnum.TOURNE_SENS_CONTRE_HORLOGE:
            raise Exception('direction_fixe doit être SousConfigPlanEnum')

        if plan != PlanEnum.XY and plan != PlanEnum.XZ and plan != PlanEnum.YZ:
            raise Exception('direction_fixe doit être PlanEnum')

        self.sous_config = sous_config

        self.plan = plan

    def get_dictionnaire_de_config(self):
        return self.configs_plans[self.sous_config][self.plan]

    def __str__(self):
        return self.sous_config.name + '-' + self.plan.name

    def get_dictionnaire_de_config_rempli(self, sequence_pf, sequence_s):
        dict_sous_cru = self.get_dictionnaire_de_config()

        direction = self.plan.get_direction_manquante().get_lettre()

        def remplacer_direction(string, valeur):
            return string.replace(direction, str(valeur))

        config = {}

        for i, (pf, s) in enumerate(dict_sous_cru.items()):
            pf_rempli = remplacer_direction(pf, sequence_pf[i])

            s_rempli = remplacer_direction(s, sequence_s[i])

            config[pf_rempli] = s_rempli

        return config

    @staticmethod
    def merge_dicts(un, autre):
        complet = {}
        complet.update(un)
        complet.update(autre)
        return complet


''' ************************ Configurations d'Ancrage Factory ************************ '''


class Aux:
    sous_config_cable_0 = None
    sequence_pf_0 = None
    sequence_s_0 = None

    sous_config_cable_1 = None
    sequence_pf_1 = None
    sequence_s_1 = None

    dict_config_complet = None

    points_fixes = None


def _creer_config_ancrage():
    dict_partiel_0 = Aux.sous_config_cable_0.get_dictionnaire_de_config_rempli(sequence_pf=Aux.sequence_pf_0,
                                                                               sequence_s=Aux.sequence_s_0)

    dict_partiel_1 = Aux.sous_config_cable_1.get_dictionnaire_de_config_rempli(sequence_pf=Aux.sequence_pf_1,
                                                                               sequence_s=Aux.sequence_s_1)

    Aux.dict_config_complet = SousConfigCable.merge_dicts(dict_partiel_0, dict_partiel_1)

    noms_points_fixes = list(Aux.dict_config_complet.keys())

    configs_cables = [CableConfiguration(Aux.points_fixes[pf], Aux.dict_config_complet[pf])
                      for pf in noms_points_fixes]

    config_ancrage = CableLayout(configs_cables)

    return config_ancrage


def get_simple(points_fixes):
    """
    
    :param points_fixes: dictionnaire des points fixes d'ancrage
    :return: 
    """
    Aux.sous_config_cable_0 = SousConfigCable(SousConfigCableEnum.SIMPLE, PlanEnum.XY)
    Aux.sequence_pf_0 = Sequence3emeDirectionEnum.CONSTANTE.get_sequence(0)
    Aux.sequence_s_0 = Sequence3emeDirectionEnum.CONSTANTE.get_sequence(0)
    Aux.sous_config_cable_1 = SousConfigCable(SousConfigCableEnum.SIMPLE, PlanEnum.XY)
    Aux.sequence_pf_1 = Sequence3emeDirectionEnum.CONSTANTE.get_sequence(1)
    Aux.sequence_s_1 = Sequence3emeDirectionEnum.CONSTANTE.get_sequence(1)
    Aux.points_fixes = points_fixes
    return _creer_config_ancrage()


def get_tourne_sh_sch(points_fixes):
    """
    :param points_fixes: dictionnaire des points fixes d'ancrage
    :return: 
    """
    Aux.sous_config_cable_0 = SousConfigCable(SousConfigCableEnum.TOURNE_SENS_HORLOGE, PlanEnum.XY)
    Aux.sequence_pf_0 = Sequence3emeDirectionEnum.CONSTANTE.get_sequence(0)
    Aux.sequence_s_0 = Sequence3emeDirectionEnum.CONSTANTE.get_sequence(0)
    Aux.sous_config_cable_1 = SousConfigCable(SousConfigCableEnum.TOURNE_SENS_CONTRE_HORLOGE, PlanEnum.XY)
    Aux.sequence_pf_1 = Sequence3emeDirectionEnum.CONSTANTE.get_sequence(1)
    Aux.sequence_s_1 = Sequence3emeDirectionEnum.CONSTANTE.get_sequence(1)
    Aux.points_fixes = points_fixes
    return _creer_config_ancrage()


def get_tourne_sch_sh(points_fixes):
    """
    :param points_fixes: dictionnaire des points fixes d'ancrage
    :return: 
    """
    Aux.sous_config_cable_0 = SousConfigCable(SousConfigCableEnum.TOURNE_SENS_CONTRE_HORLOGE, PlanEnum.XY)
    Aux.sequence_pf_0 = Sequence3emeDirectionEnum.CONSTANTE.get_sequence(0)
    Aux.sequence_s_0 = Sequence3emeDirectionEnum.CONSTANTE.get_sequence(0)
    Aux.sous_config_cable_1 = SousConfigCable(SousConfigCableEnum.TOURNE_SENS_HORLOGE, PlanEnum.XY)
    Aux.sequence_pf_1 = Sequence3emeDirectionEnum.CONSTANTE.get_sequence(1)
    Aux.sequence_s_1 = Sequence3emeDirectionEnum.CONSTANTE.get_sequence(1)
    Aux.points_fixes = points_fixes
    return _creer_config_ancrage()


''' ************************ Tests ************************ '''


scs = [SousConfigCableEnum.TOURNE_SENS_CONTRE_HORLOGE,
       SousConfigCableEnum.TOURNE_SENS_HORLOGE,
       SousConfigCableEnum.CROISE_LEFT_RIGHT,
       SousConfigCableEnum.CROISE_UP_DOWN,
       SousConfigCableEnum.SIMPLE]

plans = [PlanEnum.XY, PlanEnum.XZ, PlanEnum.XY]

scps = [SousConfigCable(sous_config=sc, plan=p) for sc in scs for p in plans]


def __main__():
    for scp in scps:
        print(scp)
        pprint(scp.get_dictionnaire_de_config(), width=1)
        print()


''' ************************ Configurations Rien Croisé ************************ '''

"""
# Description
def get_config_ancrage_rien_croise():
    cc_000 = CableConfiguration(source_vertex_name='S000', fixed_point=PF_000)  # cc_000 = PF_000 --> S000
    cc_100 = CableConfiguration(source_vertex_name='S100', fixed_point=PF_100)  # cc_100 = PF_100 --> S100
    cc_010 = CableConfiguration(source_vertex_name='S010', fixed_point=PF_010)  # cc_010 = PF_010 --> S010
    cc_110 = CableConfiguration(source_vertex_name='S110', fixed_point=PF_110)  # cc_110 = PF_110 --> S110
    cc_001 = CableConfiguration(source_vertex_name='S001', fixed_point=PF_001)  # cc_001 = PF_001 --> S001
    cc_101 = CableConfiguration(source_vertex_name='S101', fixed_point=PF_101)  # cc_101 = PF_101 --> S101
    cc_011 = CableConfiguration(source_vertex_name='S011', fixed_point=PF_011)  # cc_011 = PF_011 --> S011
    cc_111 = CableConfiguration(source_vertex_name='S111', fixed_point=PF_111)  # cc_111 = PF_111 --> S111

    config_ancrage = CableLayout(
        configs_cables=[cc_000, cc_100, cc_010, cc_110, cc_001, cc_101, cc_011, cc_111]
    )

    return config_ancrage


def get_config_ancrage_xy_croise_sens_horloge_en_bas():
    cc_000 = CableConfiguration(source_vertex_name='S010', fixed_point=PF_000)  # cc_000 = PF_000 --> S010
    cc_100 = CableConfiguration(source_vertex_name='S000', fixed_point=PF_100)  # cc_100 = PF_100 --> S000
    cc_010 = CableConfiguration(source_vertex_name='S110', fixed_point=PF_010)  # cc_010 = PF_010 --> S110
    cc_110 = CableConfiguration(source_vertex_name='S100', fixed_point=PF_110)  # cc_110 = PF_110 --> S100
    cc_001 = CableConfiguration(source_vertex_name='S101', fixed_point=PF_001)  # cc_001 = PF_001 --> S101
    cc_101 = CableConfiguration(source_vertex_name='S111', fixed_point=PF_101)  # cc_101 = PF_101 --> S111
    cc_011 = CableConfiguration(source_vertex_name='S001', fixed_point=PF_011)  # cc_011 = PF_011 --> S001
    cc_111 = CableConfiguration(source_vertex_name='S011', fixed_point=PF_111)  # cc_111 = PF_111 --> S011

    config_ancrage = CableLayout(
        configs_cables=[cc_000, cc_100, cc_010, cc_110, cc_001, cc_101, cc_011, cc_111]
    )

    return config_ancrage

def get_config_ancrage_xy_croise_sens_horloge_en_haut():
    cc_000 = CableConfiguration(source_vertex_name='S100', fixed_point=PF_000)  # cc_000 = PF_000 --> S100
    cc_100 = CableConfiguration(source_vertex_name='S110', fixed_point=PF_100)  # cc_100 = PF_100 --> S110
    cc_010 = CableConfiguration(source_vertex_name='S000', fixed_point=PF_010)  # cc_010 = PF_010 --> S000
    cc_110 = CableConfiguration(source_vertex_name='S010', fixed_point=PF_110)  # cc_110 = PF_110 --> S010
    cc_001 = CableConfiguration(source_vertex_name='S011', fixed_point=PF_001)  # cc_001 = PF_001 --> S011
    cc_101 = CableConfiguration(source_vertex_name='S001', fixed_point=PF_101)  # cc_101 = PF_101 --> S001
    cc_011 = CableConfiguration(source_vertex_name='S111', fixed_point=PF_011)  # cc_011 = PF_011 --> S111
    cc_111 = CableConfiguration(source_vertex_name='S101', fixed_point=PF_111)  # cc_111 = PF_111 --> S101

    config_ancrage = CableLayout(
        configs_cables=[cc_000, cc_100, cc_010, cc_110, cc_001, cc_101, cc_011, cc_111]
    )

    return config_ancrage
"""
