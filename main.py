import pygame as pg
import os
import math as m
from settings import Settings
from lines import Line
from random import randint as rnd

print(m.log(50, 50 ** (1/5)))


pg.init()

settings = Settings()

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (-1500, 10)

screen = pg.display.set_mode(settings.win_size, flags=pg.DOUBLEBUF | pg.NOFRAME)
surf = pg.Surface(settings.win_size)
surf.set_alpha(200)

settings.screen = screen
settings.main_surf = surf

clock = pg.time.Clock()

font = pg.font.SysFont('Times New Roman', 16)

lines = []
for k in range(settings.lines_num):
    line = Line(settings)
    line.draw()
    lines.append(line)

while True:
    surf.fill(settings.win_bg)

    clock.tick(settings.win_fps)

    mouse_rad_rect = pg.draw.circle(settings.main_surf, (255, 0, 0), settings.mouse_pos, settings.mouse_rad, 1)

    for line_ind in settings.mouse_rect.collidelistall([k.rect for k in lines]):
        line = lines[line_ind]
        if settings.mouse_pos[1] <= line.y:
            y = line.y
        elif settings.mouse_pos[1] >= line.y + line.height:
            y = line.y + line.height
        else:
            y = settings.mouse_pos[1]

        x = line.x - settings.mouse_pos[0]
        y = settings.mouse_pos[1] - y

        dist = m.sqrt(x**2 + y**2)

        if settings.text_alpha > 0:
            settings.text_alpha -= 1
        else:
            settings.text_alpha = 0

        if settings.text_size >= 61:
            settings.text_size -= 0.1

        if dist <= settings.mouse_rad:

            if y == 0:
                test_angle = -settings.mouse_pos[1] + line.y + line.height // 2
            elif y < 0:
                test_angle = line.height // 2
            else:
                test_angle = -line.height // 2

            if x > 0:
                test_angle *= -1
            line.cur_angle = test_angle / line.height * 200 + 90

            line.color = (255, 0, 0)

            force = m.log(settings.mouse_rad + 1 - dist, 50 ** (1 / 25))

            if x == 0:
                force_x = 0
                force_y = force * (1 if y < 0 else -1)
            elif y == 0:
                force_x = force * (1 if x > 0 else -1)
                force_y = 0
            else:
                koef_x = x / (abs(x) + abs(y))
                koef_y = -y / (abs(x) + abs(y))

                force_x = force * koef_x
                force_y = force * koef_y

            line.x_speed = force_x
            line.y_speed = force_y

    for line in lines:
        line.update()
        line.draw()
        if line.color != settings.basic_lines_color:
            koef = 50
            line.color = (int(line.color[0] - (line.color[0] - line.incline_color[0]) / koef),
                          int(line.color[1] - ((line.color[1] - line.incline_color[1]) / koef)),
                          int(line.color[2] - ((line.color[2] - line.incline_color[2]) / koef)))

    # rad_font = pg.font.SysFont('Times New Roman', int(settings.text_size))

    text_fps = font.render(str(round(clock.get_fps(), 1)), True, (255, 0, 0))
    # rad_text = rad_font.render(f"Mouse rad is {settings.mouse_rad}", True, (255, 0, 0))

    # rad_surf = pg.Surface(rad_text.get_size(), pg.SRCALPHA)
    # rad_surf.fill((255, 255, 255, settings.text_alpha))
    # rad_text.blit(rad_surf, (0, 0), special_flags=pg.BLEND_RGBA_MULT)

    surf.blit(text_fps, (10, 20))
    # surf.blit(rad_text, rad_text.get_rect(center=(400, 300)))

    screen.blit(surf, (0, 0))

    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == 27:
                print("<<< EXIT >>>")
                exit()
            elif event.key == 32:
                test_line = Line(settings)
        elif event.type == pg.MOUSEMOTION:
            settings.mouse_pos = pg.mouse.get_pos()
            settings.mouse_rect = pg.Rect(settings.update_mouse_rect(settings.mouse_pos, settings.mouse_rad))

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:
                settings.mouse_rad += 20
                settings.text_alpha = 255
                settings.text_size = 70

                settings.mouse_pos = pg.mouse.get_pos()
                settings.mouse_rect = pg.Rect(settings.update_mouse_rect(settings.mouse_pos, settings.mouse_rad))

            elif event.button == 5:
                settings.mouse_rad -= 20
                if settings.mouse_rad <= 0:
                    settings.mouse_rad = 5
                settings.text_alpha = 255
                settings.text_size = 70

                settings.mouse_pos = pg.mouse.get_pos()
                settings.mouse_rect = pg.Rect(settings.update_mouse_rect(settings.mouse_pos, settings.mouse_rad))

            elif event.button == 1:
                for line in lines:
                    line.basic_x = rnd(50, settings.win_width - 50)
                    line.basic_y = rnd(50, settings.win_height - 50)

    pg.display.update()