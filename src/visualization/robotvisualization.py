from numpy import radians
import time

from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import pygame

from src.models.entite_cable_robot import *
from src.visualization.trackball import Trackball
from src.visualization.cameraOpening import CameraOpening
from src.setups.parametres_objets import camera_position1, camera_position2, camera_position3, camera_position4, \
                                         camera_direction


class RobotVisualization:
      """
    draws a trajectory
    usage: draw_trajectory(...) to draw a trajectory
            show() to draw a single position
    :param cable_robot: CableRobot object to be drawn
    :param draw_maisonette: bool, true=maisonette will be drawn
    """
    
    def __init__(self, cable_robot,draw_maisonette ):
        print("Initializing cable robot.")
        self._cable_robot = copy.deepcopy(cable_robot)
        # self.reset_mvt_variables()
        # light is turned off to avoid some errors with the shaders, should work in most cases
        self.light_off()
        #setting window size
        self.window_height = 800
        self.window_width = 1200
        #makes sure that the source and the viewer are not moving
        self.reset_mvt_variables()
        #initializes a trackball to rotate the camera using mouse
        self.trackball = Trackball(self.window_width, self.window_height)
        self.mouse_position = (0, 0)
        self.draw_maisonette = draw_maisonette

    def light_on(self):
    '''  
    turns the sun's light on
    '''
        self.use_shaders = True

    def light_off(self):
    '''
    turns the sun's light off
    '''
        self.use_shaders = False

    def set_display_dimensions(self, height, width):
        print("Setting display dimensions.")
        self.window_height = height
        self.window_width = width

    def set_uniforms(self):
    '''
    Initializes uniforms and stores their locations.
    '''
    
        print("Setting shaders.")
        self.light_position_uniform = glGetUniformLocation(self.gl_program, "light_position")
        self.light_direction_uniform = glGetUniformLocation(self.gl_program, "light_direction")
        self.light_radius_uniform = glGetUniformLocation(self.gl_program, "light_radius")
        self.window_limit_top = glGetUniformLocation(self.gl_program,"window_limit_top")
        self.window_limit_bottom = glGetUniformLocation(self.gl_program, "window_limit_bottom")

    def update_uniforms(self):
    '''
    Updates the information given to the shaders through the uniforms.
    '''
    
        glUniform4fv(self.light_position_uniform, 1, self._cable_robot.light_center - self._cable_robot.get_centre() + (1,))
        glUniform4fv(self.light_direction_uniform, 1, self._cable_robot.light_direction() + (0,))
        glUniform1fv(self.light_radius_uniform, 1, self._cable_robot.light_radius)
        #glUniform1fv(self.window_limit_bottom, 1, )
        #glUniform1fv(self.window_limit_top,1, )


    def create_window(self):
    '''
    Creates a window context for the visualization
    '''
        print("Creating window.")
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), DOUBLEBUF | OPENGL | RESIZABLE | OPENGLBLIT)
        glClearColor(1.0, 1.0, 1.0, 1.0)
        pygame.init()

    def set_opengl_parameters(self):
    '''
    Sets some opengl consts.
    '''
        print("Setting opengl parameters.")
        #enables z coordinate testing
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
        glRotatef(-90, 1, 0, 0)

    def set_shaders(self):
    '''
    Initializes the shaders, this function won't be used if the lights are off
    '''
    
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
    '''
    #resets/initializes all the mvt variables to make sure there isn't anything moving
    #CW = clockwise
    #CCW = counter clockwise
    #pos = positive
    #neg = negative
    '''
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
    '''
    resets the camera to the initial position and rotation,
    very useful  when trackball does crazy things
    '''
    
        glLoadIdentity()
        gluPerspective(45, (self.window_width / self.window_height), 0.1, 50.0)
        glTranslatef(0, 0, -15)
        glRotatef(-90, 1, 0, 0)
        glScalef(0.001, 0.001, 0.001)

    def manage_events(self):
    ''' 
    Function to manage the keyboard/mouse events. 
    It is responsible for changing the mvt variables when an event is detected
    '''
    
        #iterate over all the events detected by pygame and changes the mvt variable that corresponds to the event 
        for event in pygame.event.get():
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

            #if a key is pressed, the movement begins
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
                    
            #if the key is released, the movement ends
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
    #execute transformations that are "activated"
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
                self._cable_robot.translate_source(-5, 0, 0)
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
    """
    draws a static cable robot
    """
        print("start drawing....")
        self.create_window()
        self.set_opengl_parameters()
        if(self.use_shaders):
            self.set_shaders()
            self.set_uniforms()
        origin = self._cable_robot.get_centre()

        self.reset_viewer_matrix()

#         my_camera_opening1 = CameraOpening(camera_position1,camera_direction, radians(100))
#         my_camera_opening2 = CameraOpening(camera_position2,camera_direction, radians(100))
#         my_camera_opening3 = CameraOpening(camera_position3,camera_direction, radians(100))
#         my_camera_opening4 = CameraOpening(camera_position4,camera_direction, radians(100))



        while True:
            self.manage_events()
            self.execute_transformations()
            if(self.use_shaders):
                self.update_uniforms()
            #clear the buffers before drawing
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            #draws the new frame
            self._cable_robot.draw(origin,self.draw_maisonette)
        #    my_camera_opening1.draw()
        #    my_camera_opening2.draw()
        #    my_camera_opening3.draw()
        #    my_camera_opening4.draw()
            #switches the framebuffers
            pygame.display.flip()
            #a pause between two frames
            pygame.time.wait(10)

    def draw_trajectory(self,trajectory, time_step,speed):
    """
    draws a trajectory
    :param trajectory: Trajectory object
    :param time_step: time_step: time in ms between two position in the trajectory
    :param speed: speed of the trajectory, i.e. how many ms of trajectory will be shown in 1 ms
    """
    
        print("start drawing trajectory....")
        print("step + " + str(time_step))
        self.create_window()
        self.set_opengl_parameters()
        if(self.use_shaders):
            self.set_shaders()
            self.set_uniforms()
        origin = self._cable_robot.get_centre()
        self.reset_viewer_matrix()
        initial_time = time.time()
        i = 0

#         my_camera_opening1 = CameraOpening(camera_position1,camera_direction, radians(100))
#         my_camera_opening2 = CameraOpening(camera_position2,camera_direction, radians(100))
#         my_camera_opening3 = CameraOpening(camera_position3,camera_direction, radians(100))
#         my_camera_opening4 = CameraOpening(camera_position4,camera_direction, radians(100))

        while True:
            self.manage_events()
            self.execute_transformations()
            if(self.use_shaders):
                self.update_uniforms()
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            i = (time.time() - initial_time)
            i = i/time_step
            i = int(i*speed)
            self._cable_robot.set_source_position(trajectory[int(i% len(trajectory))].get_centre())
            self._cable_robot.set_source_angles(trajectory[int(i% len(trajectory))].get_angle())
            self._cable_robot.draw(origin,self.draw_maisonette)
#             my_camera_opening1.draw()
#             my_camera_opening2.draw()
#             my_camera_opening3.draw()
#             my_camera_opening4.draw()
            pygame.display.flip()
            pygame.time.wait(10)
