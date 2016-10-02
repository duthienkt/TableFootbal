import math

from constant import *
from garfield import GActivity, GDrawable
from garfield import garfield_load_image, garfield_font


class ScoreBoard(GDrawable):
    def __init__(self, player_1_name="Player 1", player_2_name="Player 2"):
        self.bg = garfield_load_image(PATH_SCORE_BOARD_BG)
        self.font = garfield_font(PATH_FONT, 30)
        self.player1Name = player_1_name
        self.player2Name = player_2_name
        self.player1Text = self.font.render(self.player1Name, True, COLOR_WHILE)
        self.player2Text = self.font.render(self.player2Name, True, COLOR_WHILE)
        self.point1 = 0
        self.point2 = 0
        self.point1Text = self.font.render(str(self.point1), True, COLOR_WHILE)
        self.point2Text = self.font.render(str(self.point2), True, COLOR_WHILE)

    def draw(self, delta_time, screen, position=(0, 0)):
        screen.blit(self.bg, position)
        (x, y) = position
        screen.blit(self.player1Text, (x + 80, y + 23))
        screen.blit(self.player2Text, (screen.get_width() - 80 - self.player2Text.get_width(), y + 23))
        screen.blit(self.point1Text, (x + 180, y + 80))
        screen.blit(self.point2Text, (screen.get_width() - 180 - self.point2Text.get_width(), y + 80))

    def inc_point2(self):
        self.point1 += 1
        self.point1Text = self.font.render(str(self.point1), True, COLOR_WHILE)

    def inc_point1(self):
        self.point2 += 1
        self.point2Text = self.font.render(str(self.point2), True, COLOR_WHILE)


COLUMNS = [[(58, 249)],  # 0
           [(184, 159),  # 1
            (184, 339)],  # 2
           [(310, 114),  # 3
            (310, 249),  # 4
            (310, 384)],  # 5
           [(436, 69),  # 6
            (436, 159),  # 7
            (436, 249),  # 8
            (436, 339),  # 9
            (436, 429)],  # 10
           [(564, 69),  # 11
            (564, 159),  # 12
            (564, 249),  # 13
            (564, 339),  # 14
            (564, 429)],  # 15
           [(690, 114),  # 16
            (690, 249),  # 17
            (690, 384)],  # 18
           [(816, 159),  # 19
            (816, 339)],  # 20
           [(942, 249)]]  # 21
COLUMN_DELTA_LIMIT = [90, 130, 84, 39, 39, 48, 150, 90]
COLUMN_PLAYER_ID = [0, 0, 1, 0, 1, 0, 1, 1]
COLUMN_PLAYER_ID_KEY = [99, 118, 117, 98, 105, 110, 111, 112]
PLAYER_MOVE_KEY = [(119, 115, 97, 100), (273, 274, 276, 275)]
PLAYER_W = 27
PLAYER_H = 43
PLAYER_H_BEGIN = 7
PLAYER_H_END = 49
PLAYER_DRAW_Y = -7.5

Y_LIMIT = 50


def up_case(key):
    if key < 97 or key > 122:
        return key
    return key - 32


class RectBound:
    def __init__(self, position, size, v=(0, 0)):
        (self.x, self.y) = position
        (self.w, self.h) = size
        (self.dx, self.dy) = v


class Column(GDrawable):
    def __init__(self, player_index, positions, id_key, keys, y_limit):
        self.player_index = player_index
        self.positions = positions
        self.image = garfield_load_image(PATH_PLAYERS[player_index])
        self.deltaY = 0
        self.vv = 0
        self.grad = 0
        self.idKey = id_key
        (self.upKey, self.downKey, self.leftKey, self.rightKey) = keys
        self.x = 0
        self.y = 0
        self.yLimit = y_limit
        self.active = False
        self.bounds = []

    def draw(self, delta_time, screen, position=(0, 0)):
        (x0, y0) = position
        self.y += delta_time / 1000.0 * self.deltaY
        if not self.active:
            self.deltaY = 0

        self.grad += delta_time / 1000.0 * self.vv
        if abs(self.grad) >= 3.14:
            self.grad = 0
            self.vv = 0
        self.x = math.sin(self.grad) * 50
        if self.deltaY < 0:
            if self.y < -self.yLimit:
                self.deltaY = 0
                self.y = -self.yLimit
        if self.deltaY > 0:
            if self.y > self.yLimit:
                self.deltaY = 0
                self.y = self.yLimit
        self.bounds = []
        for (x, y) in self.positions:
            self.bounds.append(RectBound((x + self.x - 13, y + self.y), (27, 42),
                                         (math.cos(self.grad) * 50, self.deltaY)))
            screen.blit(self.image, (x + x0 + self.x - 13, y + y0 + PLAYER_DRAW_Y + self.y))

    def on_key_released(self, key):
        if key == self.upKey:
            if self.deltaY < 0:
                self.deltaY = 0
            return True
        elif key == self.downKey:
            if self.deltaY > 0:
                self.deltaY = 0
            return True

    def on_key_pressed(self, key):
        if key == self.upKey:
            self.deltaY = -150
            return True
        elif key == self.downKey:
            self.deltaY = 150
            return True
            # elif key == self.leftKey:
            #     if self.grad <= 0.2:
            #         self.vv = -3.14
            # elif key == self.rightKey:
            #     if self.grad >= -0.2:
            #         self.vv = 3.14

    def set_active(self, active):
        self.active = active


class Table(GActivity):
    def __init__(self, score_board):
        self.yardImage = garfield_load_image(PATH_YARD)
        self.width = self.yardImage.get_width()
        self.height = self.yardImage.get_height()
        self.ball = Ball(self, (500, 270), (60, 0))
        self.scoreBoard = score_board
        self.columns = []
        for i in range(len(COLUMNS)):
            self.columns.append(
                Column(COLUMN_PLAYER_ID[i], COLUMNS[i], COLUMN_PLAYER_ID_KEY[i], PLAYER_MOVE_KEY[COLUMN_PLAYER_ID[i]],
                       COLUMN_DELTA_LIMIT[i]))
        self.colActivated = [0, 7]
        self.columns[0].set_active(True)
        self.columns[7].set_active(True)

    def draw(self, delta_time, screen, position=(0, 0)):
        screen.blit(self.yardImage, position)
        self.ball.draw(delta_time, screen, position)
        for c in self.columns:
            c.draw(delta_time, screen, position)

    def new_score(self, code):
        if code == 1:
            self.scoreBoard.inc_point1()
        if code == 2:
            self.scoreBoard.inc_point2()
        if code > 0:
            if (self.scoreBoard.point1 + self.scoreBoard.point2) % 2 == 0:
                self.ball = Ball(self, (500, 270), (260, 0))
            else:
                self.ball = Ball(self, (500, 270), (-260, 0))

    def on_key_released(self, key):

        if self.columns[self.colActivated[0]].on_key_released(key):
            return True
        if self.columns[self.colActivated[1]].on_key_released(key):
            return True

        return super().on_key_released(key)

    def on_mouse_pressed(self, button, position):
        return super().on_mouse_pressed(button, position)

    def on_key_pressed(self, key):

        for i in range(len(self.columns)):
            p = self.columns[i]
            if p.idKey == key:
                if not self.colActivated[p.player_index] == i:
                    self.columns[self.colActivated[p.player_index]].set_active(False)
                self.colActivated[p.player_index] = i
                self.columns[i].set_active(True)
                return True
        if self.columns[self.colActivated[0]].on_key_pressed(key):
            return True
        if self.columns[self.colActivated[1]].on_key_pressed(key):
            return True
        return super().on_key_pressed(key)

    def on_mouse_released(self, button, position):
        return super().on_mouse_released(button, position)

    def on_mouse_move(self, position, rel, buttons):
        super().on_mouse_move(position, rel, buttons)


class Player(GActivity):
    def __init__(self, context, table):
        super().__init__(context)
        self.table = table

    def on_mouse_released(self, button, position):
        return super().on_mouse_released(button, position)

    def on_mouse_pressed(self, button, position):
        return super().on_mouse_pressed(button, position)

    def draw(self, delta_time, screen, position=(0, 0)):
        super().draw(delta_time, screen, position)

    def on_key_pressed(self, key):
        return super().on_key_pressed(key)

    def on_key_released(self, key):
        return super().on_key_released(key)

    def on_mouse_move(self, position, rel, buttons):
        super().on_mouse_move(position, rel, buttons)


class Ball(GDrawable):
    def __init__(self, table, position, velocity0=(0, 0)):
        self.position = position
        self.image = garfield_load_image(PATH_BALL)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rad = self.width / 2.0
        self.table = table
        self.velocity = velocity0

    def draw(self, delta_time, screen, position=(0, 0)):
        for c in self.table.columns:
            rec = c.bounds
            self.contact(rec, delta_time)

        (x0, y0) = position
        (x, y) = self.position
        (dx, dy) = self.velocity
        x += dx * (delta_time / 1000.0)
        y += dy * (delta_time / 1000.0)
        if x < self.rad:
            x = 2 * self.rad - x
            if dx < 0:
                dx = -dx
        if y < self.rad:
            y = 3 * self.rad - y
            if dy < 0:
                dy = -dy
        if x > self.table.width - self.rad:
            x = 2 * (self.table.width - self.rad) - x
            if dx > 0:
                dx = -dx

        if y > self.table.height - self.rad:
            y = 2 * (self.table.height - self.rad) - y
            if dy > 0:
                dy = -dy
        # dy *= 1 - (delta_time / 100000)
        # dx *= 1 - (delta_time / 100000)

        self.velocity = (dx, dy)
        self.position = (x, y)

        screen.blit(self.image, (x0 + x - self.rad, y0 + y - self.rad))
        self.table.new_score(self.player_score_code())

    def player_score_code(self):
        (x, y) = self.position
        if y < 180 or y > 360:
            return -1
        if x < 26:
            return 1
        if x > 973:
            return 2
        return -1

    def contact(self, bounds, delta_time):
        (x, y) = self.position
        (dx, dy) = self.velocity
        for e in bounds:
            # print(bounds)
            (l, t) = (e.x, e.y)
            (b, r) = (e.h, e.w)
            b += t
            r += l
            # if x >= r + self.rad or x <= l - self.rad or y >= b + self.rad or y <= t - self.rad:
            #     continue
            #
            # if y > t - self.rad and dy > 0:
            #     dy = -dy
            #     dy += e.dy
            # elif y < b + self.rad and dy < 0:
            #     dy = -dy
            #     dy += e.dy

            if x >= r + self.rad or x <= l - self.rad or y >= b + self.rad or y <= t - self.rad:
                continue

            if dx < 0 and x < r + self.rad:
                dx = -dx
                if abs(dx) < 300:
                    dx *= 1.1
                x = r + self.rad
                dy += e.dy

            elif dx > 0 and x > l - self.rad:
                dx = -dx
                if abs(dx) < 300:
                    dx *= 1.1
                x = l - self.rad
                dy += e.dy

                # dy += e.dy
                # if dy < 0 and y + dy * delta_time / 1000.0 < b + self.rad:
                #     dy = -dy
                #     y = b + self.rad
                # elif dy > 0 and y + dy * delta_time / 1000.0 > t - self.rad:
                #     dy = -dy
                #     y = t - self.rad

        if dx * dx + dy * dy >= 100:
            self.velocity = (dx * 0.99999, dy * 0.99999)
        else:
            self.velocity = (dx, dy)

        self.position = (x, y)
