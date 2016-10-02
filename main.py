import random

from component import NormalCursor
from constant import *
from garfield import Garfield, garfield_music_is_busy, garfield_add_music
from main_game import MainGame
from menu_game import MenuGame


class Main(Garfield):
    def __init__(self):
        super().__init__()
        self.cursor = NormalCursor("assets/cursor.png", 5)
        pygame.mouse.set_visible(False)
        self.powerOff = None
        self.activity = None

    def setup(self):
        self.frame_rate(FRAME_RATE)
        self.activity = MenuGame(self)
        self.trigger_music()
        pass

    def on_mouse_move(self, position, rel, buttons):
        self.cursor.on_mouse_move(position, rel, buttons)
        self.activity.on_mouse_move(position, rel, buttons)
        pass

    def on_mouse_pressed(self, button, position):
        self.trigger_music()
        self.cursor.on_mouse_pressed(button, position)
        self.activity.on_mouse_pressed(button, position)
        pass

    def on_key_pressed(self, key):
        self.trigger_music()
        self.activity.on_key_pressed(key)

    def on_key_released(self, key):
        self.activity.on_key_released(key)

    def setting(self):
        self.size(SIZE_SCREEN)
        pass

    def on_mouse_released(self, button, position):
        self.activity.on_mouse_released(button, position)
        self.cursor.on_mouse_released(button, position)

    def draw(self, delta_time, screen=None, position=(0, 0)):
        self.activity.draw(delta_time, screen, position)
        self.cursor.draw(delta_time, self.screen)
        pass

    def set_cursor(self, cursor):
        self.cursor = cursor

    def start_activity(self, activity_command):
        if activity_command == "exit":
            self.exit()
        if activity_command == "menu":
            self.activity = MenuGame(self)
        if activity_command == "play":
            self.activity = MainGame(self)
        pass

    def trigger_music(self):
        if not garfield_music_is_busy():
            garfield_add_music(PATH_MUSIC[random.randint(0,  len(PATH_MUSIC)-1)])


Main().__main__()
