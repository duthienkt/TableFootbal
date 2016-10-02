import math

from animation import Animation
from constant import *
from garfield import MouseInteractive
from garfield import garfield_load_image, GActivity, garfield_pick_color


class NormalCursor(Animation, MouseInteractive):
    def __init__(self, image_path, frame_count, interval_time=300):
        super().__init__(image_path, frame_count, interval_time)
        self.position = (0, 0)

    def on_mouse_move(self, position, rel, buttons):
        self.position = position

    def draw(self, delta_time, screen, position=(0, 0)):
        super().draw(delta_time, screen, self.position)

    def on_mouse_released(self, button, position):
        return False

    def on_mouse_pressed(self, button, position):
        return False


class Button(GActivity):
    def __init__(self, context, position, path1, path2):
        super().__init__(context)
        self.mouseOutsideImage = garfield_load_image(path1)
        self.mouseInsideImage = garfield_load_image(path2)
        self.currentImage = self.mouseOutsideImage
        self.position = position

    def draw(self, delta_timte, screen, position=(0, 0)):
        screen.blit(self.currentImage, self.position)

    def on_mouse_pressed(self, button, position):
        (x, y) = position
        (x0, y0) = self.position
        c = garfield_pick_color(self.currentImage, (x - x0, y - y0))
        if c is not None:
            (r, g, b, a) = c
            if a > 50:
                self.currentImage = self.mouseInsideImage
                return True
        return False

    def on_mouse_released(self, button, position):
        if not self.currentImage == self.mouseInsideImage:
            return
        self.currentImage = self.mouseOutsideImage
        (x, y) = position
        (x0, y0) = self.position
        c = garfield_pick_color(self.currentImage, (x - x0, y - y0))
        if c is not None:
            (r, g, b, a) = c
            if a > 50:
                return True
        return False

    def on_mouse_move(self, position, rel, buttons):
        (x, y) = position
        (x0, y0) = self.position
        c = garfield_pick_color(self.currentImage, (x - x0, y - y0))
        if c is not None:
            (r, g, b, a) = c
            if a > 50:
                self.currentImage = self.mouseInsideImage
                return
        self.currentImage = self.mouseOutsideImage


class ClickAbleButton(Button):
    def __init__(self, context, position, path1, path2):
        super().__init__(context, position, path1, path2)
        self.pressed = False

    def on_mouse_pressed(self, button, position):
        if super().on_mouse_pressed(button, position):
            self.pressed = True
            return True
        return False

    def on_mouse_released(self, button, position):
        if super().on_mouse_released(button, position):
            if self.pressed:
                self.on_click()
            return True
        return False

    def on_click(self):
        pass


class FlyButton(ClickAbleButton):
    def __init__(self, context, position0, position1, path1, path2):
        super().__init__(context, position0, path1, path2)
        self.position0 = position0
        self.position1 = position1
        self.clicked = False

    def draw(self, delta_time, screen, position=(0, 0)):
        (vx0, vy0) = self.position
        (vx1, vy1) = self.position1
        dx = vx1 - vx0
        dy = vy1 - vy0
        l = math.sqrt(dx * dx + dy * dy)

        if self.clicked and l < 1:
            self.clicked = False
            self.on_click()
        elif l >= 1:

            dx /= l
            dy /= l
            l = delta_time / 20.0 * math.log(1 + l / 5.0)
            dx *= l
            dy *= l
            self.position = (vx0 + dx, vy0 + dy)
        super().draw(delta_time, screen, self.position)


class ExitButton(FlyButton):
    def on_click(self):
        self.context.start_activity("exit")


class GameOver(FlyButton):
    def on_click(self):
        self.context.start_activity("play")

    def __init__(self, context):
        super().__init__(context, (context.width / 2 - 351, -500), (context.width / 2 - 351, 100), PATH_GAME_OVER[0],
                         PATH_GAME_OVER[1])
