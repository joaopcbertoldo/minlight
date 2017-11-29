import pygame,sys
from pygame.locals import *
from modeles.entite_cable_robot import *
from src.calculs.graphics.trackball import Trackball
from OpenGL.GL import *
from OpenGL.GLU import *
import operator

class Robot_Visualization:

    def __init__(self,cable_robot):
        print("initializing cable robot.....")
        self._cable_robot = copy.deepcopy(cable_robot)
        self.reset_mvt_variables()
        self.light_off()
        self.height = 800
        self.width = 1200
        self.reset_mvt_variables()
        self.trackball = Trackball(self.width,self.height)
        self.mouse_position = (0,0)
    def light_on(self):

        self.use_shaders = True

    def light_off(self):

        self.use_shaders = False

    def set_display_dimensions(self,height,width):
        print("setting display dimensions.....")
        self.height = height
        self.width = width

    def set_uniforms(self):
        print("setting shaders.....")
        self.light_position_uniform = glGetUniformLocation(self.gl_program,"light_position")
        self.light_direction_uniform = glGetUniformLocation(self.gl_program,"light_direction")
        self.light_radius_uniform = glGetUniformLocation(self.gl_program,"light_radius")

    def update_uniforms(self):

        glUniform4fv(self.light_position_uniform,1, self._cable_robot.get_light_centre() - self._cable_robot.get_centre()+ (1,))
        glUniform4fv(self.light_direction_uniform,1, self._cable_robot.get_light_direction() + (0,))
        glUniform1fv(self.light_radius_uniform,1, self._cable_robot.get_light_radius())

    def create_window(self):
        print("creating window.....")
        pygame.display.set_mode((self.width,self.height), DOUBLEBUF|OPENGL|RESIZABLE)
        glClearColor(1.0, 1.0, 1.0, 1.0)

    def set_opengl_parameters(self):
        print("setting opengl parameters....")
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        #setting line smooth parameters
        glEnable (GL_LINE_SMOOTH)
        glEnable (GL_BLEND)
        glBlendFunc (GL_SRC_ALPHA_SATURATE, GL_ONE)
        glHint (GL_LINE_SMOOTH_HINT, GL_NICEST)
        glLineWidth (1.5)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        print("opengl parameters set.")

    def set_shaders(self):
        print("setting shaders....")
        v = glCreateShader(GL_VERTEX_SHADER)
        f = glCreateShader(GL_FRAGMENT_SHADER)

        with open ("graphics/shaders/simpleshader.frag", "r") as myfile:
            ftext=myfile.readlines()
        with open ("graphics/shaders/simpleshader.vert", "r") as myfile:
            vtext=myfile.readlines()

        glShaderSource(v, vtext)
        glShaderSource(f, ftext)

        glCompileShader(v)
        glCompileShader(f)

        p = glCreateProgram()
        glAttachShader(p,v)
        glAttachShader(p,f)

        glLinkProgram(p)
        glUseProgram(p)

        self.gl_program = p

    def close_window(self):
        print("closing window......")
        pygame.quit()
        quit()

    def reset_mvt_variables(self):
        print("resetting mvt variables.....")
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
        gluPerspective(45, (self.width/self.height), 0.1, 50.0)
        glTranslatef(0,0,-15)
    #    glRotatef(-90, 1, 0, 0)
        glScalef(0.001,0.001,0.001)


    def manage_events(self):

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                self.trackball.startRotation(x,y)
                print("clicou")
            elif event.type == pygame.MOUSEBUTTONUP:
                self.trackball.stopRotation()
                print("soltou")
            elif event.type == pygame.MOUSEMOTION:
                a,b,c = event.buttons
                x,y = event.pos
                if(a or b or c):
                    self.trackball.updateRotation(x,y)
            elif event.type == pygame.KEYDOWN or event.type == KEYDOWN:
                if event.key == pygame.K_p:
                    self.rotateX_CW = True
                elif event.key == pygame.K_l:
                    self.rotateX_CCW = True
                elif event.key == pygame.K_o:
                    self.rotateY_CW = True
                elif event.key == pygame.K_k:
                    self.rotateY_CCW = True
                elif event.key == pygame.K_z:
                    self.zoomIn = True
                elif event.key == pygame.K_x:
                    self.zoomOut = True
                elif event.key == pygame.K_m:
                    self.rotate_source_pitch= True
                elif event.key == pygame.K_w:
                    self.translate_source_X_pos= True
                elif event.key == pygame.K_s:
                    self.translate_source_X_neg= True
                elif event.key == pygame.K_a:
                    self.translate_source_Z_pos = True
                elif event.key == pygame.K_d:
                    self.translate_source_Z_neg = True
                elif event.key == pygame.K_i:
                    self.rotate_source_yaw_pos = True
                elif event.key == pygame.K_j:
                    self.rotate_source_yaw_neg = True
                elif event.key == pygame.K_u:
                    self.rotate_source_pitch_pos = True
                elif event.key == pygame.K_h:
                    self.rotate_source_pitch_neg = True
                elif event.key == pygame.K_y:
                    self.rotate_source_row_pos = True
                elif event.key == pygame.K_g:
                    self.rotate_source_row_neg = True
                elif event.key == pygame.K_r:
                    self.reset_viewer_matrix()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()


            elif event.type == pygame.KEYUP or event.type == KEYUP:
                if event.key == pygame.K_p:
                    self.rotateX_CW = False
                elif event.key == pygame.K_l:
                    self.rotateX_CCW = False
                elif event.key == pygame.K_o:
                    self.rotateY_CW = False
                elif event.key == pygame.K_k:
                    self.rotateY_CCW = False
                elif event.key == pygame.K_z:
                    self.zoomIn = False
                elif event.key == pygame.K_x:
                    self.zoomOut = False
                elif event.key == pygame.K_w:
                    self.translate_source_X_pos= False
                elif event.key == pygame.K_s:
                    self.translate_source_X_neg= False
                elif event.key == pygame.K_a:
                    self.translate_source_Z_pos= False
                elif event.key == pygame.K_d:
                    self.translate_source_Z_neg= False
                elif event.key == pygame.K_m:
                    self.rotate_source_pitch = False
                elif event.key == pygame.K_i:
                    self.rotate_source_yaw_pos = False
                elif event.key == pygame.K_j:
                    self.rotate_source_yaw_neg = False
                elif event.key == pygame.K_u:
                    self.rotate_source_pitch_pos = False
                elif event.key == pygame.K_h:
                    self.rotate_source_pitch_neg = False
                elif event.key == pygame.K_y:
                    self.rotate_source_row_pos = False
                elif event.key == pygame.K_g:
                    self.rotate_source_row_neg = False

    def execute_transformations(self):

            if(self.rotateX_CW == True):
                glRotatef(2, 1, 0, 0)
            elif(self.rotateX_CCW == True):
                glRotatef(-2, 1, 0, 0)
            elif(self.rotateY_CW == True):
                glRotatef(2, 0, 0, 1)
            elif(self.rotateY_CCW == True):
                glRotatef(-2, 0, 0, 1)
            elif(self.zoomIn == True):
                glScalef(1.1,1.1,1.1)
            elif(self.zoomOut == True):
                glScalef(0.9,0.9,0.9)

            elif(self.translate_source_X_neg == True):
                self._cable_robot.translate_source(-5,0,0)
            elif(self.translate_source_X_pos == True):
                self._cable_robot.translate_source(5,0,0)
            elif(self.translate_source_Z_neg == True):
                self._cable_robot.translate_source(0,0,-5)
            elif(self.translate_source_Z_pos == True):
                self._cable_robot.translate_source(0,0,5)

            elif(self.rotate_source_yaw_pos == True):
                self._cable_robot.rotate_source(1,0,0)
            elif(self.rotate_source_yaw_neg == True):
                self._cable_robot.rotate_source(-1,0,0)
            elif(self.rotate_source_pitch_pos == True):
                self._cable_robot.rotate_source(0,1,0)
            elif(self.rotate_source_pitch_neg == True):
                self._cable_robot.rotate_source(0,-1,0)
            elif(self.rotate_source_row_pos == True):
                self._cable_robot.rotate_source(0,0,1)
            elif(self.rotate_source_row_neg == True):
                self._cable_robot.rotate_source(0,0,-1)

    def show(self):
        print("start drawing....")
        self.create_window()
        self.set_opengl_parameters()
        if(self.use_shaders):
            self.set_shaders()
            self.set_uniforms()
        origin = self._cable_robot.get_centre()

        self.reset_viewer_matrix()

        while True:
            self.manage_events()
            self.execute_transformations()
            if(self.use_shaders):
                self.update_uniforms()
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            self._cable_robot.draw(origin)
            pygame.display.flip()
            pygame.time.wait(10)
