from pygame.locals import *
from garfield import *

pygame.init()


class Animation(GDrawable):
    def __init__(self, url, frame_count, elapse_time, is_loop=True, size=None):
        self.sprites = []
        self.isLoop = is_loop
        self.frameCount = frame_count
        self.elapseTime = elapse_time
        self.frameId = 0
        self.accTime = 0

        im = garfield_load_image(url)
        self.width = im.get_width() / frame_count
        self.height = im.get_height()
        for i in range(frame_count):
            sub_image = im.subsurface(Rect(self.width * i, 0, self.width, self.height))
            if size is not None:
                sub_image = pygame.transform.scale(sub_image, size)
            self.sprites.append(sub_image)
        if size is not None:
            (self.width, self.height) = size

    def draw(self, delta_time, screen, position=(0, 0)):
        self.accTime += delta_time
        if self.accTime > self.elapseTime:
            self.frameId += self.accTime // self.elapseTime
            self.accTime = self.accTime % self.elapseTime
        if self.isLoop:
            self.frameId %= self.frameCount
        if self.frameId < self.frameCount:
            screen.blit(self.sprites[self.frameId], position)

    def pick_color(self, position):
        if not self.is_alive():
            return None
        return garfield_pick_color(self.sprites[self.frameId], position)

    def is_alive(self):
        return self.frameId < self.frameCount

    def restart(self):
        self.accTime = 0
        self.frameId = 0
