from random import randint as rnd
import pygame as pg
import math as m


class Line:
    def __init__(self, settings):

        self.settings = settings

        self.height = rnd(5, 50)
        self.width = rnd(1, 2)

        self.basic_x = rnd(50, self.settings.win_width - 50)
        self.basic_y = rnd(50, self.settings.win_height - 50)

        self.x, self.y = self.basic_x, self.basic_y
        self.x_speed, self.y_speed = 0, 0
        self.back_x_speed, self.back_y_speed = 0, 0

        self.rect = None

        self.incline_color = self.settings.basic_lines_color
        # self.incline_color = (rnd(0, 255), rnd(0, 255), rnd(0, 255))
        self.color = self.incline_color[:]

        self.cur_angle = 90
        self.angle = 180

        self.incline_start_pos = 0
        self.incline_end_pos = 0

    def draw(self):
        # TEST RECTS
        # self.rect = pg.draw.line(self.settings.main_surf, self.color,
        #                          (self.x, self.y), (self.x, self.y + self.height), self.width)
        # self.rect = pg.draw.circle(self.settings.main_surf, (0, 0, 255), (int(self.x), int(self.y)), 5)

        cos_h = m.cos(m.radians(self.angle)) * self.height // 2
        sin_h = m.sin(m.radians(self.angle)) * self.height // 2

        self.incline_start_pos = (self.x + cos_h,
                                  self.y + self.height // 2 - sin_h)

        self.incline_end_pos = (self.x - cos_h,
                                self.y + self.height // 2 + sin_h)

        self.rect = pg.draw.aaline(self.settings.main_surf, self.color,
                                 self.incline_start_pos, self.incline_end_pos, self.width)

        if self.width == 2:
            self.incline_start_pos = (self.incline_start_pos[0] + 1, self.incline_start_pos[1])
            self.incline_end_pos = (self.incline_end_pos[0] + 1, self.incline_end_pos[1])

            self.rect = pg.draw.aaline(self.settings.main_surf, self.color,
                                     self.incline_start_pos, self.incline_end_pos, self.width)

    def update(self):

        self.x += self.x_speed
        self.y += self.y_speed

        if self.cur_angle != self.angle:
            self.angle += (self.cur_angle - self.angle) / 20

        if self.cur_angle != 90:
            self.cur_angle -= (self.angle - 90) / 20

        self.x += self.back_x_speed
        self.y += self.back_y_speed

        self.x_speed *= 0.9
        self.y_speed *= 0.9

        if abs(self.x_speed) < 0.1:
            self.x_speed = 0
        if abs(self.y_speed) < 0.1:
            self.y_speed = 0

        if abs(self.x_speed) + abs(self.y_speed) == 0:
            self.back_x_speed = (self.basic_x - self.x) / 200
            self.back_y_speed = (self.basic_y - self.y) / 200
