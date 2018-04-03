from datetime import datetime

from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import pygame
import pickle
import matplotlib.pyplot as plt

from src.math_entities import Vec3, TupleAnglesRotation, CoordonnesSpherique
from src.models.entites_systeme_minlight import Box

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1


class VerificateurAnglesLimites:
    def __init__(self, dimensions_source, maisonette, chambre, config_ancrage,
                 systeme_spherique_baie_vitree, configs_simulation):
        self.dimensions_source = dimensions_source
        self.maisonette = maisonette
        self.chambre = chambre
        self.config_ancrage = config_ancrage
        self.systeme_spherique_baie_vitree = systeme_spherique_baie_vitree
        self.diametre_cable = configs_simulation['diametre_cable']
        self.space_recherche = configs_simulation['space_recherche']
        self.n_discretisation_cables = configs_simulation['n_discretisation_cables']
        self.k_dicretisation_cubes = configs_simulation['k_dicretisation_cubes']
        self.verbose = configs_simulation['verbose']
        self.source = Box(
            centre=Vec3(0, 0, 0),
            ypr_angles=TupleAnglesRotation(0, 0, 0),
            dimensions=dimensions_source
        )
        self.limites = {}
        self._source_demo = self._get_source_demo_config_ancrage()
        self._cables_demo = self._get_cables_demo_config_ancrage()

    def trouver_angles_limites(self, sauvegarde_automatique=True, nom_fichier_sauvegarde='auto'):
        intervalle_rho, intervalle_phi, intervalle_theta = self.space_recherche.get_intervalles()
        unite_angles = self.space_recherche.unite
        for rho in intervalle_rho:
            if self.verbose:
                print('rho =', rho)

            couples_angles = []
            self.limites[rho] = couples_angles

            for phi in intervalle_phi:
                premier_theta_ok = False

                for theta in intervalle_theta:
                    theta_max = theta
                    self.source.changer_a_partir_de_coordonnes_spheriques(
                        coordonnees_spheriques=CoordonnesSpherique(rho, theta, phi, unite=unite_angles),
                        systeme_spherique=self.systeme_spherique_baie_vitree
                    )

                    if self.position_ok():
                        premier_theta_ok = True
                    else:
                        break

                couples_angles.append((phi, theta_max))

                if self.verbose:
                    print((phi, theta_max))

                if not premier_theta_ok:
                    break

            if self.verbose:
                print()

        if sauvegarde_automatique:
            self.sauvegarder_limites(nom_fichier_sauvegarde)

    def position_ok(self):
        sommets_source = self.source.get_dictionnaire_sommets()
        cables = self.config_ancrage.get_cables(sommets_source, diametre_cable=self.diametre_cable)

        if not self.cables_ok(cables):
            return False

        if self.source.is_coliding(self.maisonette,
                                                    k_discretisation=self.k_dicretisation_cubes):
            return False

        if not self.source.is_inside_box(self.chambre):
            return False

        return True

    def cables_ok(self, cables):
        for cable in cables:
            # maisonette
            if cable.intersection_avec_pave(self.maisonette, self.n_discretisation_cables):
                return False
            # source
            if cable.intersection_avec_pave(self.source, self.n_discretisation_cables):
                return False
            # chambre
            if not cable.entierement_dans_pave(self.chambre, self.n_discretisation_cables):
                return False
            # croisements
            for autre_cable in cables:
                if autre_cable == cable:
                    pass
                else:
                    if cable.intersects_cable(autre_cable):
                        return False
        return True

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!! creer une verification auto pour noms des fichier pour ne pas écrire dessus
    def sauvegarder_limites(self, nom_fichier='auto'):
        if nom_fichier == 'auto':
            format_ = '_%y_%m_%d_%H_%M_%S'
            nom_fichier = 'angles_limites' + datetime.now().strftime(format_)
        pickle_out = open(nom_fichier + '.pickle', "wb")
        pickle.dump(self.limites, pickle_out)
        pickle_out.close()

    def charger_fichier_limites(self, nom_fichier):
        pickle_in = open(nom_fichier + '.pickle', "rb")
        self.limites = pickle.load(pickle_in)
        pickle_in.close()

    def _generer_graphe(self, xlim=[0, 90], ylim=[0, 90]):
        fig = plt.figure()
        ax = fig.gca()

        for rho, couples in self.limites.items():
            phi, theta = zip(*couples)
            line, = ax.plot(theta, phi)
            line.set_label('Rho = ' + "{r:0.2f}".format(r=rho / 1000) + ' m')

        ax.set_title('Angles Limites')
        ax.set_xlabel('Theta [º]')
        ax.set_ylabel('Phi [º]')

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        ax.legend()

    def afficher_graphe_limites(self, xlim=[0, 90], ylim=[0, 90]):
        self._generer_graphe(xlim, ylim)
        plt.show()

    def sauvegarder_graphe_limites_png(self, xlim=[0, 90], ylim=[0, 90], nom_fichier='auto'):
        self._generer_graphe(xlim, ylim)

        if nom_fichier == 'auto':
            format_date = '_%y_%m_%d_%H_%M_%S'
            nom_fichier = 'angles_limites' + datetime.now().strftime(format_date)

        plt.savefig(nom_fichier + '.png', bbox_inches='tight')

    def _get_source_demo_config_ancrage(self):
        x_centre_source = sum(point.get_x() for point in self.config_ancrage.get_points_fixes()) / 8
        y_centre_source = sum(point.get_y() for point in self.config_ancrage.get_points_fixes()) / 8
        z_centre_source = self.chambre.dimensions['height'] / 2
        centre_demo = Vec3(x_centre_source, y_centre_source, z_centre_source)
        source_demo = Box(
            dimensions=self.dimensions_source,
            centre=centre_demo,
            ypr_angles=TupleAnglesRotation.ZERO()
        )
        return source_demo

    def _get_cables_demo_config_ancrage(self):
        sommets_source_demo = self._source_demo.get_dictionnaire_sommets()
        cables_demo = self.config_ancrage.get_cables(sommets_source_demo, self.diametre_cable)
        return cables_demo

    def draw_demo_config_ancrage(self):
        rotateX_CW = False
        rotateX_CCW = False
        rotateY_CW = False
        rotateY_CCW = False
        zoomIn = False
        zoomOut = False
        rotate_source_pitch = False

        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glLineWidth(2.0)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(0, 0, -5)
        source = self._get_source_demo_config_ancrage()
        cables = self._get_cables_demo_config_ancrage()
        origin = source.center
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN or event.type == KEYDOWN:
                    if event.key == pygame.K_p:
                        rotateX_CW = True
                    elif event.key == pygame.K_l:
                        rotateX_CCW = True
                    elif event.key == pygame.K_o:
                        rotateY_CW = True
                    elif event.key == pygame.K_k:
                        rotateY_CCW = True
                    elif event.key == pygame.K_w:
                        zoomIn = True
                    elif event.key == pygame.K_s:
                        zoomOut = True
                    elif event.key == pygame.K_m:
                        rotate_source_pitch = True

                elif event.type == pygame.KEYUP or event.type == KEYUP:
                    if event.key == pygame.K_p:
                        rotateX_CW = False
                    elif event.key == pygame.K_l:
                        rotateX_CCW = False
                    elif event.key == pygame.K_o:
                        rotateY_CW = False
                    elif event.key == pygame.K_k:
                        rotateY_CCW = False
                    elif event.key == pygame.K_w:
                        zoomIn = False
                    elif event.key == pygame.K_s:
                        zoomOut = False
            if rotateX_CW:
                glRotatef(3, 1, 0, 0)
            if rotateX_CCW:
                glRotatef(-3, 1, 0, 0)
            if rotateY_CW:
                glRotatef(3, 0, 1, 0)
            if rotateY_CCW:
                glRotatef(-3, 0, 1, 0)
            if rotateY_CCW:
                glRotatef(-3, 0, 1, 0)
            if zoomIn:
                glScalef(1.1, 1.1, 1.1)
            if zoomOut:
                glScalef(0.9, 0.9, 0.9)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            source.draw(origin, (0.95, 0.95, 0), True)
            self.chambre.draw(origin, (0, 0, 0), False)
            for cable in cables:
                cable.draw(origin)
            pygame.display.flip()
            pygame.time.wait(10)
