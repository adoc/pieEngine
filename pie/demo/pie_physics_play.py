"""

"""
import random
import math

import pygame
import pymunk
from pymunk import Vec2d

from pie.math import flip_rect_y_normals, flip_y_normals, vect_diff, vect_to_rad
from pie.base import MRunnable
from pie.entity.animated import SurfaceSelection
from pie.entity.background import ParallaxBackground
from pie.entity.composite import DistributedAnimated
from entity.primitive import Image
from pie.engine import Engine


class ShipPhysics:
    def __init__(self, space, body, poly):
        self.__screen_height = pygame.display.get_surface().get_height()
        self.__space = space
        self.__body = body
        self.__poly = poly
        self.__space.add(self.__body)

    @property
    def body_angle(self):
        return math.fmod(self.__body.angle, 2 * math.pi)

    @property
    def angle_deg(self):
         return math.fmod(self.body_angle * 180 / math.pi, 360)


    def __impulse(self, fv, mag, offset=(0, 0)):
        self.__body.apply_force(
            (Vec2d(*fv) * mag).rotated(self.__body.angle),
            Vec2d(offset).rotated(self.__body.angle))


    def forward_thrust(self, mag):
        self.__impulse((1, 0), mag)
        # self.__body.apply_impulse(
        #     (Vec2d(1, 0) * mag).rotated(self.body_angle))

    def reverse_thrust(self, mag):
        self.__impulse((-1, 0), mag)
        # self.__body.apply_impulse(
        #     (Vec2d(-1, 0) * mag).rotated(self.body_angle))

    #92, 37
    def fore_starboard_thrust(self, mag):
        self.__impulse((0, 1), mag, offset=(16, 0))
        # self.__body.apply_impulse(
        #     (Vec2d(0, 1) * mag).rotated(self.body_angle),self.__body.local_to_world(Vec2d(64, 0).rotated(self.body_angle)))

    def fore_port_thrust(self, mag):
        self.__impulse((-0, -1), mag, offset=(16, 0))
        # self.__body.apply_impulse(
        #     (Vec2d(0, -1) * mag).rotated(self.body_angle),Vec2d(64,0).rotated(self.body_angle))

    def aft_starboard_thrust(self, mag):
        self.__impulse((0, 1), mag, offset=(-16, 0))
        # self.__body.apply_impulse(
        #     (Vec2d(0, 1) * mag).rotated(self.body_angle),Vec2d(-64, 0).rotated(self.body_angle))

    def aft_port_thrust(self, mag):
        self.__impulse((-0, -1), mag, offset=(-16, 0))
        # self.__body.apply_impulse(
        #     (Vec2d(0, -1) * mag).rotated(self.body_angle),Vec2d(-64,0).rotated(self.body_angle))

    def rotate_to_starboard(self, mag):
        self.fore_port_thrust(mag)
        self.aft_starboard_thrust(mag)

    def rotate_to_port(self, mag):
        self.fore_starboard_thrust(mag)
        self.aft_port_thrust(mag)

    def update(self):
        self.__body.reset_forces()

        # Update object rect.
        viewport = flip_y_normals(self.__body.position, self.__screen_height)
        viewport = Vec2d(viewport[0], viewport[1]) #, viewport.size*2)
        self.rect.topleft = viewport

        # Physics stuff
        vect_to_destination = (self._destination -
                               (self.__body.position + (32,32))) # + (64, 64))) # 64x64 Offset to center of image.

        local_destination = vect_to_destination.rotated(self.__body.angle)

        local_angle_to_dest = vect_to_rad(local_destination)

        coef_to_dest = local_angle_to_dest / math.pi

        # print(ff)

        # print(coef_to_dest)

        # angle_to_destination = math.acos(vect_to_destination.normalized().dot(self.__body.rotation_vector.normalized()))

        # /
        # f = (math.pi - abs(abs(self.__body.angle - local_angle_to_dest) - math.pi))

        # /
        # body_angle = math.fmod(self.__body.angle, 2*math.pi)+2*math.pi
        # dest_angle = math.fmod(angle_to_destination, 2*math.pi)+2*math.pi
        # print(dest_angle - body_angle)

        # Rotation calcs
        ff = (local_destination[0] - local_destination[1])/self.__body.mass

        self.forward_thrust(ff)

        # Rotational
        mag = self.__body.mass*100
        dm = self.__body.mass*100

        print(coef_to_dest)

        f = coef_to_dest * mag
        dmp = -dm * abs(coef_to_dest) * self.__body.angular_velocity

        self.rotate_to_starboard(f)
        self.rotate_to_starboard(-dmp)

        self.aft_port_thrust(-f)
        self.aft_port_thrust(dmp)

        self.fore_port_thrust(-f)
        self.fore_port_thrust(dmp)


    def _reset(self):
        self.__body.reset_forces()
        self.__body.angle = 0
        self.__body.torque = 0
        self.__body.velocity = (0, 0)
        self.__body.position = (0, 0)


class Ship(SurfaceSelection, ShipPhysics):
    def __init__(self, space, rotation_seq, **rect_kwa):
        SurfaceSelection.__init__(self, rotation_seq, **rect_kwa)
        # Needed for coordinate conversions. (Hackish)
        self.__screen_height = pygame.display.get_surface().get_height()

        #print(flip_y_normals(self.rect,
        #                     self.__screen_height))

        mass = 1
        inertia = pymunk.moment_for_box(mass, 46, 18)# 92, 37)
        body = pymunk.Body(mass, inertia)
        body.position = Vec2d(flip_y_normals(self.rect, self.__screen_height))
        body.angular_velocity_limit = 1000
        body.velocity_limit = 1000

        poly = pymunk.Poly.create_box(body) #, offset=(34.25, 32.75))    #(68.5, 65.5)
        ShipPhysics.__init__(self, space, body, poly)

        self._destination = Vec2d(0, 0)

    def update(self):
        SurfaceSelection.update(self)
        self._destination = Vec2d(flip_y_normals(pygame.mouse.get_pos(), self.__screen_height))
        ShipPhysics.update(self)
        # Set rotation image frame.
        self.set_frame(self.angle_deg)


class PhysicsDemo(Engine):
    def __init__(self, *args, **kwa):
        Engine.__init__(self, *args, **kwa)

        self.bg_parallax = ParallaxBackground(
            viewport=pygame.Rect((0, 0), (1024, 512)))

        self.bg_parallax.add(
            Image(
            pygame.image.load("assets/composite/sf1_bg_med2.png").convert(),
            parallax_distance=3),
            Image(
            pygame.image.load("assets/composite/sf1_bg_far.png").convert(),
            blit_flags=pygame.BLEND_RGBA_ADD,
            parallax_distance=11),
            Image(
            pygame.image.load("assets/composite/sf1_bg_med1.png").convert(),
            blit_flags=pygame.BLEND_RGBA_ADD,
            parallax_distance=6),
            Image(
            pygame.image.load("assets/composite/sf1_bg_near.png").convert(),
            blit_flags=pygame.BLEND_RGBA_ADD,
            parallax_distance=1))

        self.add_render_plain(self.bg_parallax)

        # Physics
        self.__space = pymunk.Space()

        # Surprisingly fast load and transform of 360 PNG's for a ship animation.
        self.assets.animations.add_from_zip('ship1', "assets\\anim_ship1.zip", size=(64, 64))

        self.add_render_plain(Ship(self.__space,
                                   self.assets.animations['ship1'],
                                   center=(512, 256)))


    def update(self):
        Engine.update(self)

        self.__space.step(1/(self.fps))

        self.bg_parallax.viewport.topleft = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:
            self.add_render_plain(Ship(self.__space,
                                       self.assets.animations['ship1'],
                                       topleft=(random.randint(0, 1024),random.randint(0, 512))))

        print("FPS: ", self.fps)


# Keep this minimal.
if __name__ == "__main__":
    pygame.init()
    game = PhysicsDemo(pygame.display.set_mode((1024, 512), 0, 32),
                       non_static_background=True)

    game.start()