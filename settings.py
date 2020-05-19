import pygame as pg

class Settings:
    def __init__(self):
        self.win_width = 800
        self.win_height = 600
        self.win_size = (self.win_width, self.win_height)

        self.win_bg = (210, 210, 210)
        self.win_fps = 30

        self.screen = None
        self.main_surf = None

        self.mouse_rad = 60
        self.mouse_pos = (0, 0)
        self.mouse_rect = (int(self.mouse_pos[0] - self.mouse_rad), int(self.mouse_pos[1] - self.mouse_rad),
                          int(self.mouse_rad), int(self.mouse_rad))
        self.mouse_rect = pg.Rect(self.mouse_rect)
        self.update_mouse_rect = lambda pos, rad: (int(pos[0] - rad), int(pos[1] - rad), int(rad * 2), int(rad * 2))

        self.lines_num = 5000

        self.text_alpha = 255
        self.text_size = 60

        self.basic_lines_color = (55, 55, 55)