#from math import cos, sin, asin, atan2, pi
from src.calculs.modeles.entites_mathemathiques import *
from src.calculs.modeles.entites_systeme_minlight import *
from src.calculs.dynamique.miscellaneous import *
from src.calculs.setups import parametres_objets




class Trajectoire():

    '''
    :param date: String en format '29/07'
    :param latitude: string en format '63.2/N', ou '63.2/S'
    :param heure: string en format '18:48'
    :param orientation_nord: float entre 0.0 et 360.0
    :param orientation_zenit: float entre 0.0 et 90.0
    '''

    # provavelmente é melhor tirar heure_initiale, heure_finale e intervalle do construtor
    # e coloca-los como parametro dos metodos
    def __init__(self, date, latitude, heure_initiale, heure_finale,
                intervalle, ro, orientation_nord = 0.0, orientation_zenit=0.0):
        self.date = date
        self.latitude = latitude
        self.heure_initiale =heure_initiale
        self.heure_finale = heure_finale
        self.intervalle = intervalle
        #
        self.ro = ro
        #
        self.orientation_nord = orientation_nord
        self.orientation_zenit = orientation_zenit

# coord spheriques prenant y comme nord
    '''
    Fonction qui donne la position du soleil vue par un observeur sur Terre.

    
    :return: coordonnees [sol_azimut, sol_altitude] pour la position solaire vue.

    '''

    def position_soleil (self, heure):
        secs = 60 * (int(heure.split(':')[0]) * 60 + int(heure.split(':')[1]))
        return self.position_soleil_secondes(secs)

    def position_soleil_secondes (self, secs):

        dic_mois = \
             {
                 '01': 31,
                 '02': 28,
                 '03': 31,
                 '04': 30,
                 '05': 31,
                 '06': 30,
                 '07': 31,
                 '08': 31,
                 '09': 30,
                 '10': 31,
                 '11': 30,
                 '12': 31
             }

        # calcule le nombre n de jours dans la date (n=1 si date == '01/01')

        n = int(self.date.split('/')[0])

        for key in list(dic_mois.keys()):
            if key != self.date.split('/')[1]:
                n += dic_mois[key]
            else:
                break

        # recuperer la valeur de latitude

        if self.latitude.split('/')[1] == 'N':
            lat = pi/180*float(self.latitude.split('/')[0])
        else:
            lat = -1*pi/180*float(self.latitude.split('/')[0])


        # declin = angle de declinaison, calculé à partir de n
        declin = -pi / 180 * 23.45 * cos(2 * pi * (n + 10) / 365)


        # determiner la position [soleil_aizmut, soleil_altitude] du soleil:
        w_Terre = 2*pi/(24*60*60)  #en rad/seconde

        x = x_sph(declin, w_Terre*secs)
        y = y_sph(declin, w_Terre*secs) * sin(lat) + z_sph(declin) * cos(lat)
        z = -y_sph(declin, w_Terre*secs) * cos(lat) + z_sph(declin) * sin(lat)

        soleil_altitude = asin(z)*180/pi  # en degres
        soleil_azimut = point_azimut(x, y)

        return [soleil_azimut-self.orientation_nord + 180, soleil_altitude-self.orientation_zenit]


    def get_trajectoire (self):
        points_trajectoire = []

        n_points = int((secondes_dans_horaire(self.heure_finale)-secondes_dans_horaire(self.heure_initiale))/self.intervalle)
        for i in range(n_points):
            points_trajectoire.append(
                self.position_soleil_secondes(secondes_dans_horaire(self.heure_initiale) + i* self.intervalle));

            '''
            '''
        return points_trajectoire

    def get_configurations(self):
        lista_config = []
        for pos in self.get_trajectoire():
            config = Configuration(pos, self.ro)
            lista_config.append(config)
        return lista_config

class Configuration:
    def __init__(self, pair_theta_phi, ro):
        self.position_theta = pair_theta_phi[0]
        self.position_phi = pair_theta_phi[1]
        self.ro = ro
        self.set_centre_xyz(parametres_objets.systeme_spherique_baie_vitree)


    def set_centre_xyz(self, systeme_spherique):

      #  roh, theta, phi = coordonnees_spheriques.get_coordonnees_spheriques(unite_desiree=UniteAngleEnum.DEGRE)
        coordonnees_spheriques = CoordonnesSpherique(self.ro, self.position_theta, self.position_phi, UniteAngleEnum.DEGRE)
        # p = centre de la source pour le systeme cartesien à partir du quel le spherique est defini
        p = systeme_spherique.convertir_en_cartesien(coordonnees_spheriques)

        centre_systeme, ypr_angles_systeme = systeme_spherique.get_centre_et_ypr_angles()

        Rot = ypr_angles_systeme.get_tuple_angles_pour_inverser_rotation() \
            .get_matrice_rotation()

        res = Rot * p + centre_systeme

        # il faut faire ça sinon le retour est une matrice rot
        self.centre = Vecteur3D(res.__getitem__((0, 0)), res.__getitem__((1, 0)), res.__getitem__((2, 0)))

        self.ypr_angles = \
            TupleAnglesRotation(
                row=0,
                pitch=self.position_phi,
                yaw=self.position_theta,
                sequence=SequenceAnglesRotationEnum.YPR,
                unite=UniteAngleEnum.DEGRE  # !!!!!!!!!!!!!!!!!!!!!!!!
            )

    def get_angle(self):
        return self.ypr_angles

    def get_centre(self):
        return self.centre
        '''
    def get_coords(self):
        x =
        y =
        z =

        return Vecteur3D(),
        '''

# test

traj = Trajectoire('03/03', '60.3/N', '16:01', '20:00', 600, 2000)
a = traj.position_soleil('12:01')
print(a)

#print(traj.get_trajectoire())
print('')
#config = Configuration(a)
#print(config.get_centre())

print(traj.get_configurations())
