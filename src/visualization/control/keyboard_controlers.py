import pygame as pg
from pygame.locals import *
from enum import IntEnum
from threading import Thread
import time


class KeysEnum(IntEnum):
    A = pg.K_a
    B = pg.K_b
    C = pg.K_c
    D = pg.K_d
    E = pg.K_e
    F = pg.K_f
    G = pg.K_g
    H = pg.K_h
    I = pg.K_i
    J = pg.K_j
    K = pg.K_k
    L = pg.K_l
    M = pg.K_m
    N = pg.K_n
    O = pg.K_o
    P = pg.K_p
    Q = pg.K_q
    R = pg.K_r
    S = pg.K_s
    T = pg.K_t
    U = pg.K_u
    V = pg.K_v
    X = pg.K_x
    W = pg.K_w
    Y = pg.K_y
    Z = pg.K_z
    PAGEUP = pg.K_PAGEUP
    PAGEDOWN = pg.K_PAGEDOWN
    UP = pg.K_UP
    DOWN = pg.K_DOWN
    LEFT = pg.K_LEFT
    RIGHT = pg.K_RIGHT
    PLUS = pg.K_KP_PLUS
    MINUS = pg.K_KP_MINUS


class KeyboardController:

    def __init__(self, actions, key_map, wait_time_miliseconds=10, parallel=True):
        self._actions = actions
        self._key_map = key_map
        self._booleans_switch = self._create_booleans()
        if parallel:
            self._wait_time = wait_time_miliseconds
            self._condition = False
            self._thread = Thread(target=self._worker, daemon=True)
            self._thread.start()

    def _create_booleans(self):
        return {int(val): False for key, val in self._key_map.items()}

    def manage_event(self, event):
        if event.type == pg.KEYDOWN or event.type == KEYDOWN:
            if event.key in self._booleans_switch.keys():
                self._booleans_switch[event.key] = True

        elif event.type == pg.KEYUP or event.type == KEYUP:
            if event.key in self._booleans_switch.keys():
                self._booleans_switch[event.key] = False

    def _apply_actions(self):
        for key, boolean in self._booleans_switch.items():
            if boolean:
                self._actions[key]()

    def _worker(self):
        while True:
            if self._condition:
                self._apply_actions()
                time.sleep(self._wait_time / 1000)

    def plug(self):
        self._condition = True

    def unplug(self):
        self._condition = False


class SourceKeyboardController(KeyboardController):
    default_key_map = {
        'x_plus': KeysEnum.R,
        'x_minus': KeysEnum.F,
        'y_plus': KeysEnum.E,
        'y_minus': KeysEnum.D,
        'z_plus': KeysEnum.W,
        'z_minus': KeysEnum.S,
        'roll_plus': KeysEnum.U,
        'roll_minus': KeysEnum.J,
        'pitch_plus': KeysEnum.I,
        'pitch_minus': KeysEnum.K,
        'yaw_plus': KeysEnum.O,
        'yaw_minus': KeysEnum.L,
    }

    @staticmethod
    def _create_action_switch(key_map, source_controlable):
        switch = dict()
        switch[key_map['x_plus']] = source_controlable.x_plus
        switch[key_map['x_minus']] = source_controlable.x_minus
        switch[key_map['y_plus']] = source_controlable.y_plus
        switch[key_map['y_minus']] = source_controlable.y_minus
        switch[key_map['z_plus']] = source_controlable.z_plus
        switch[key_map['z_minus']] = source_controlable.z_minus
        switch[key_map['roll_plus']] = source_controlable.roll_plus
        switch[key_map['roll_minus']] = source_controlable.roll_minus
        switch[key_map['pitch_plus']] = source_controlable.pitch_plus
        switch[key_map['pitch_minus']] = source_controlable.pitch_minus
        switch[key_map['yaw_plus']] = source_controlable.yaw_plus
        switch[key_map['yaw_minus']] = source_controlable.yaw_minus
        return switch

    def __init__(self, source_controlable, key_map=None, wait_time_miliseconds=10):
        key_map = SourceKeyboardController.default_key_map if not key_map else key_map
        actions = SourceKeyboardController._create_action_switch(key_map, source_controlable)
        super().__init__(actions, key_map, wait_time_miliseconds)


class ViewKeyboardController(KeyboardController):
    # TODO : check if threads can share sources so that this can run in //

    default_key_map = {
        'rotate_x_cw': KeysEnum.PAGEUP,
        'rotate_x_ccw': KeysEnum.LEFT,
        'rotate_y_cw': KeysEnum.UP,
        'rotate_y_ccw': KeysEnum.DOWN,
        'rotate_z_cw': KeysEnum.PAGEDOWN,
        'rotate_z_ccw': KeysEnum.RIGHT,
        'zomm_in': KeysEnum.PLUS,
        'zomm_out': KeysEnum.MINUS,
    }

    @staticmethod
    def _create_action_switch(key_map, view_controlable):
        switch = dict()
        switch[key_map['rotate_x_cw']] = view_controlable.rotate_x_cw
        switch[key_map['rotate_x_ccw']] = view_controlable.rotate_x_ccw
        switch[key_map['rotate_y_cw']] = view_controlable.rotate_y_cw
        switch[key_map['rotate_y_ccw']] = view_controlable.rotate_y_ccw
        switch[key_map['rotate_z_cw']] = view_controlable.rotate_z_cw
        switch[key_map['rotate_z_ccw']] = view_controlable.rotate_z_ccw
        switch[key_map['zomm_in']] = view_controlable.zomm_in
        switch[key_map['zomm_out']] = view_controlable.zomm_out
        return switch

    def __init__(self, view_controlable, key_map=None, wait_time_miliseconds=0):
        key_map = ViewKeyboardController.default_key_map if not key_map else key_map
        actions = ViewKeyboardController._create_action_switch(key_map, view_controlable)
        super().__init__(actions, key_map, wait_time_miliseconds, parallel=False)

    def manage_event(self, event):
        super(self.__class__, self).manage_event(event)
        super(self.__class__, self)._apply_actions()
