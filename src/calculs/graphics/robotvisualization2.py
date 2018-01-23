import pygame
from pygame.locals import *
from src.calculs.graphics.trackball import Trackball
from OpenGL.GL import *
from OpenGL.GLU import *
import time
from src.calculs.control.keyboard_controlers import SourceKeyboardController, ViewKeyboardController
from src.calculs.control.pygame_view_controlable import PygameViewControlable


class RobotVisualization2:

    def __init__(self, cable_robot, source_controlable):
        print("Initializing cable robot.")
        self._cable_robot = cable_robot
        # self.reset_mvt_variables()
        self.light_off()
        self.window_height = 800
        self.window_width = 1200
        self.reset_mvt_variables()
        self.trackball = Trackball(self.window_width, self.window_height)
        self.mouse_position = (0, 0)
        self._view_controlable = PygameViewControlable()
        self._source_controlable = source_controlable
        self._keyboard_source_controller = SourceKeyboardController(source_controlable=self._source_controlable)
        self._keyboard_view_controller = ViewKeyboardController(view_controlable=self._view_controlable)

    def light_on(self):
        self.use_shaders = True

    def light_off(self):
        self.use_shaders = False

    def set_display_dimensions(self, height, width):
        print("Setting display dimensions.")
        self.window_height = height
        self.window_width = width

    def set_uniforms(self):
        print("Setting shaders.")
        self.light_position_uniform = glGetUniformLocation(self.gl_program, "light_position")
        self.light_direction_uniform = glGetUniformLocation(self.gl_program, "light_direction")
        self.light_radius_uniform = glGetUniformLocation(self.gl_program, "light_radius")

    def update_uniforms(self):
        glUniform4fv(self.light_position_uniform, 1, self._cable_robot.get_light_centre() - self._cable_robot.get_centre() + (1,))
        glUniform4fv(self.light_direction_uniform, 1, self._cable_robot.get_light_direction() + (0,))
        glUniform1fv(self.light_radius_uniform, 1, self._cable_robot.get_light_radius())

    def create_window(self):
        print("Creating window.")
        pygame.display.set_mode((self.window_width, self.window_height), DOUBLEBUF | OPENGL | RESIZABLE)
        glClearColor(1.0, 1.0, 1.0, 1.0)

    def set_opengl_parameters(self):
        print("Setting opengl parameters.")
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        # setting line smooth parameters
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA_SATURATE, GL_ONE)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glLineWidth(1.5)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        print("opengl parameters set.")

    def set_shaders(self):
        print("Setting shaders.")
        v = glCreateShader(GL_VERTEX_SHADER)
        f = glCreateShader(GL_FRAGMENT_SHADER)

        with open("graphics/shaders/simpleshader.frag", "r") as myfile:
            ftext = myfile.readlines()

        with open("graphics/shaders/simpleshader.vert", "r") as myfile:
            vtext = myfile.readlines()

        glShaderSource(v, vtext)
        glShaderSource(f, ftext)

        glCompileShader(v)
        glCompileShader(f)

        p = glCreateProgram()
        glAttachShader(p, v)
        glAttachShader(p, f)

        glLinkProgram(p)
        glUseProgram(p)

        self.gl_program = p

    def close_window(self):
        print("Closing window.")
        pygame.quit()
        quit()

    def reset_mvt_variables(self):
        print("Resetting mvt variables.")
        self.rotateX_CW = False
        self.rotateX_CCW = False
        self.rotateY_CW = False
        self.rotateY_CCW = False
        self.zoomIn = False
        self.zoomOut = False
        self.translate_source_X_pos = False
        self.translate_source_X_neg = False
        self.translate_source_Z_pos = False
        self.translate_source_Z_neg = False
        self.rotate_source_yaw_neg = False
        self.rotate_source_yaw_pos = False
        self.rotate_source_pitch_neg = False
        self.rotate_source_pitch_pos = False
        self.rotate_source_row_neg = False
        self.rotate_source_row_pos = False

    def reset_viewer_matrix(self):
        glLoadIdentity()
        gluPerspective(45, (self.window_width / self.window_height), 0.1, 50.0)
        glTranslatef(0, 0, -15)
    #    glRotatef(-90, 1, 0, 0)
        glScalef(0.001, 0.001, 0.001)

    def manage_events(self):
        for event in pygame.event.get():
            self._keyboard_source_controller.manage_event(event)
            self._keyboard_view_controller.manage_event(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                self.trackball.startRotation(x, y)
                print("clicou")

            elif event.type == pygame.MOUSEBUTTONUP:
                self.trackball.stopRotation()
                print("soltou")

            elif event.type == pygame.MOUSEMOTION:
                a,b,c = event.buttons
                x,y = event.pos
                if(a or b or c):
                    self.trackball.updateRotation(x, y)

            elif event.type == pygame.KEYDOWN or event.type == KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_viewer_matrix()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

    def show(self):
        print("start drawing....")
        self.create_window()
        self.set_opengl_parameters()
        if self.use_shaders:
            self.set_shaders()
            self.set_uniforms()
        origin = self._cable_robot.get_centre()

        self.reset_viewer_matrix()

        self._keyboard_source_controller.plug()

        while True:
            self.manage_events()
            if self.use_shaders:
                self.update_uniforms()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self._cable_robot.draw(origin, True)
            pygame.display.flip()
            #pygame.time.wait(10)

    def draw_trajectory(self, trajectory, time_step, speed):
        print("start drawing....")
        self.create_window()
        self.set_opengl_parameters()
        if(self.use_shaders):
            self.set_shaders()
            self.set_uniforms()
        origin = self._cable_robot.get_centre()
        self.reset_viewer_matrix()
        initial_time = time.time()

        while True:
            self.manage_events()
            if(self.use_shaders):
                self.update_uniforms()
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            i = int((time.time() - initial_time)/time_step)
            self._cable_robot.set_source_position(trajectory[i].position)
            self._cable_robot.set_source_angles(trajectory[i].angles)

            self._cable_robot.draw(origin)
            pygame.display.flip()
            pygame.time.wait(10)
