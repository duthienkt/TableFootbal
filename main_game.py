from component import GameOver
from constant import *
from garfield import GActivity, garfield_load_image
from processing import Table, ScoreBoard


class MainGame(GActivity):
    def __init__(self, context):
        super().__init__(context)
        self.scoreBoard = ScoreBoard()
        self.table = Table(self.scoreBoard)

        self.isOver = False
        self.gameOver = GameOver(self.context)
        self.bg = garfield_load_image(PATH_BACKGROUND)

    def on_mouse_pressed(self, button, position):
        if self.gameOver.on_mouse_pressed(button, position):
            return True

        return super().on_mouse_pressed(button, position)

    def on_mouse_released(self, button, position):
        if self.gameOver.on_mouse_released(button, position):
            return True
        return super().on_mouse_released(button, position)

    def draw(self, delta_time, screen, position=(0, 0)):
        if self.scoreBoard.point1 + self.scoreBoard.point2 > 7:
            self.isOver = True
        if self.isOver:
            screen.blit(self.bg, position)
        (x, y) = position
        if not self.isOver:
            self.table.draw(delta_time, screen, (x, y + 150))

        if self.isOver:
            self.gameOver.draw(delta_time, screen, position)
            (xg, yg) = self.gameOver.position
            self.scoreBoard.draw(delta_time, screen, (x, max(yg + 195, y)))
        else:
            self.scoreBoard.draw(delta_time, screen)

    def on_key_pressed(self, key):
        if key == 27:
            if self.isOver:
                self.context.start_activity("menu")
            else:
                self.isOver = True
        if self.isOver:
            return False
        return self.table.on_key_pressed(key)

    def on_key_released(self, key):
        if self.isOver:
            return False
        return self.table.on_key_released(key)

    def on_mouse_move(self, position, rel, buttons):
        self.gameOver.on_mouse_move(position, rel, buttons)
        super().on_mouse_move(position, rel, buttons)
