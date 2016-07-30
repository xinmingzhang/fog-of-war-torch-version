import pygame as pg
from math import atan2
from math import pi as PI

from prepare import SCREEN_RECT,EYESIGHT


def get_angle(origin, destination):
    x_dist = destination[0] - origin[0]
    y_dist = destination[1] - origin[1]
    return atan2(-y_dist, x_dist) % (2 * PI)

class Fog(pg.sprite.Sprite):
    def __init__(self,game,*groups):
        super(Fog, self).__init__(*groups)
        self.game = game
        self.rect = SCREEN_RECT
        self.image = pg.Surface(self.rect.size).convert_alpha()
        self.image.fill((0,0,0,220))
        self.footprint = self.rect
        self.footprint.midbottom = self.rect.midbottom


    def update(self,pos):
        #player_surface = pg.Surface(self.rect.size).convert_alpha()
        self.image.fill((0,0,0,220))
        pg.draw.rect(self.image,(0,0,0,0),(pos[0]-EYESIGHT/2,pos[1]-EYESIGHT/2,EYESIGHT,EYESIGHT))

        for shadow in self.check_sprite_in_light(pos):
            pg.draw.polygon(self.image,(0,0,0,220),shadow)


        #self.image.blit(player_surface,(0,0),special_flags=pg.BLEND_RGBA_MIN)
        #pg.draw.circle(self.visible_area, (255, 0, 0), (int(pos[0]), int(pos[1])), 100)

    def check_sprite_in_light(self,pos):
        light_area = pg.sprite.Sprite()
        light_area.surface = pg.Surface((EYESIGHT,EYESIGHT))
        light_area.rect = light_area.surface.get_rect(center = pos)
        wolves_list = pg.sprite.spritecollide(light_area,self.game.outer,False)
        point_list = []
        for wolf in wolves_list:
            a = get_angle(pos,wolf.rect.center)
            b = []
            if 0 <= a < PI/2:
                b.append((pos[0]+EYESIGHT/2,pos[1]-EYESIGHT/2))
                b.append(self.get_boundary_point(pos, wolf.rect.bottomright))
                b.append(wolf.rect.bottomright)
                b.append(wolf.rect.topleft)
                b.append(self.get_boundary_point(pos, wolf.rect.topleft))
                point_list.append(b)
            elif PI/2 <= a < PI:
                b.append((pos[0]-EYESIGHT/2,pos[1]-EYESIGHT/2))
                b.append(self.get_boundary_point(pos, wolf.rect.topright))
                b.append(wolf.rect.topright)
                b.append(wolf.rect.bottomleft)
                b.append(self.get_boundary_point(pos, wolf.rect.bottomleft))
                point_list.append(b)
            elif PI <= a < 3*PI/2:
                b.append((pos[0]-EYESIGHT/2,pos[1]+EYESIGHT/2))
                b.append(self.get_boundary_point(pos, wolf.rect.bottomright))
                b.append(wolf.rect.bottomright)
                b.append(wolf.rect.topleft)
                b.append(self.get_boundary_point(pos, wolf.rect.topleft))
                point_list.append(b)
            elif 3*PI/2 <= a < 2*PI:
                b.append((pos[0]+EYESIGHT/2,pos[1]+EYESIGHT/2))
                b.append(self.get_boundary_point(pos, wolf.rect.topright))
                b.append(wolf.rect.topright)
                b.append(wolf.rect.bottomleft)
                b.append(self.get_boundary_point(pos, wolf.rect.bottomleft))
                point_list.append(b)

        return point_list

    @staticmethod
    def get_boundary_point(pos,point):
        a = get_angle(pos, point)
        try:
            k = (point[0]-pos[0])/(point[1]-pos[1])
            if PI/4 <= a < 3*PI/4:
                b = (k*(pos[1]-EYESIGHT/2-pos[1])+pos[0],pos[1]-EYESIGHT/2)
            elif 3*PI/4 <= a < 5*PI/4:
                b = (pos[0]-EYESIGHT/2,1/k*(pos[0]-EYESIGHT/2-pos[0])+pos[1])
            elif 5*PI/4 <= a < 7*PI/4:
                b = (k*(pos[1]+EYESIGHT/2-pos[1])+pos[0],pos[1]+EYESIGHT/2)
            else:
                b = (pos[0] + EYESIGHT/2, 1/ k * (pos[0] + EYESIGHT / 2 - pos[0]) + pos[1])
        except:
            if 3*PI/4 <= a < 5*PI/4:
                b = (pos[0]-EYESIGHT/2, pos[1])
            else:
                b = (pos[0]+EYESIGHT/2, pos[1])
        return b




    def draw(self,surface):
        surface.blit(self.image,self.rect)
