from component import FlyButton
from constant import *
from garfield import garfield_load_image, GActivity


class MenuGame(GActivity):
    def __init__(self, context):
        self.background = garfield_load_image(PATH_BACKGROUND)
        self.menuButton = [PlayNewgame(context), PlayHelp(context), PlayExit(context), PlayLogo(context)]
        self.playerLeft = PlayPlayerLeft(context)
        self.playerRight = PlayPlayerRight(context)
        self.logo = PlayLogo(context)
        super().__init__(context)

    def draw(self, delta_time, screen, position=(0, 0)):
        screen.blit(self.background, position)
        self.logo.draw(delta_time, screen, position)
        self.playerLeft.draw(delta_time, screen, position)
        self.playerRight.draw(delta_time, screen, position)

        for b in self.menuButton:
            b.draw(delta_time, screen, position)
        super().draw(delta_time, screen, position)

    def on_mouse_pressed(self, button, position):
        for b in self.menuButton:
            if b.on_mouse_pressed(button, position):
                return True
        return super().on_mouse_pressed(button, position)

    def on_mouse_move(self, position, rel, buttons):
        for b in self.menuButton:
            b.on_mouse_move(position, rel, buttons)

        super().on_mouse_move(position, rel, buttons)

    def on_mouse_released(self, button, position):
        for b in self.menuButton:
            if b.on_mouse_released(button, position):
                return True
        return super().on_mouse_released(button, position)

    def on_key_pressed(self, key):
        return super().on_key_pressed(key)

    def on_key_released(self, key):
        return super().on_key_released(key)


class PlayNewgame(FlyButton):
    def __init__(self, context):
        super().__init__(context, (context.width / 2 - 175, 800), (context.width / 2 - 175, 350),
                         PATH_BUTTONS[0][0], PATH_BUTTONS[0][1])

    def on_click(self):
        self.context.start_activity("play")


class PlayHelp(FlyButton):
    def __init__(self, context):
        super().__init__(context, (context.width / 2 - 175, 900), (context.width / 2 - 175, 450),
                         PATH_BUTTONS[1][0], PATH_BUTTONS[1][1])

    def on_click(self):
        self.context.start_activity("play")


class PlayExit(FlyButton):
    def __init__(self, context):
        super().__init__(context, (context.width / 2 - 175, 1000), (context.width / 2 - 175, 550),
                         PATH_BUTTONS[2][0], PATH_BUTTONS[2][1])

    def on_click(self):
        self.context.start_activity("exit")


class PlayLogo(FlyButton):
    def __init__(self, context):
        super().__init__(context, (context.width / 2 - 325, -500), (context.width / 2 - 325, 20),
                         PATH_LOGO, PATH_LOGO)


class PlayPlayerLeft(FlyButton):
    def __init__(self, context):
        super().__init__(context, (-592, context.height / 2 +100), (18, context.height / 2 +100),
                         PATH_PLAYER_LEFT, PATH_PLAYER_LEFT)


class PlayPlayerRight(FlyButton):
    def __init__(self, context):
        super().__init__(context, (1290, context.height / 2 +100), (690, context.height / 2 +100),
                         PATH_PLAYER_RIGHT, PATH_PLAYER_RIGHT)
