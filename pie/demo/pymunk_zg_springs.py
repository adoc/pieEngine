"""This example showcase an arrow pointing or aiming towards the cursor.
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import sys
import random
import math

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk
from pymunk import Vec2d
import pymunk.pygame_util

# fixme: This fails soo... fuck physics! :P
def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    clock = pygame.time.Clock()
    running = True
    
    ### Physics stuff
    space = pymunk.Space()
    ps = [(80,0),(0,20),(0,-20)]
    moment = pymunk.moment_for_poly(1, ps)

    ship1_body = pymunk.Body(1, moment)
    ship1_body.position = (random.randint(0,600), random.randint(0,300))
    ship1_body.angle = (random.random() * math.pi * 2) - math.pi
    ship1_shape = pymunk.Poly(ship1_body, ps)
    ship1_shape.color = THECOLORS['red']

    ship2_body = pymunk.Body(1, moment)
    ship2_body.position = (random.randint(600,1200), random.randint(300,600))
    ship2_body.angle = (random.random() * math.pi * 2) - math.pi
    ship2_shape = pymunk.Poly(ship2_body, ps)
    ship2_shape.color = THECOLORS['blue']

    ship1_body.velocity_limit = 100
    ship1_body.angular_velocity_limit = 100
    ship2_body.velocity_limit = 100
    ship2_body.angular_velocity_limit = 100

    def setup_constraints(body1, body2):
        rot_stiff = 100000
        rot_damp = 1000

        fol_stiff = 10000
        fol_damp = 1000

        # rotary_spring = pymunk.constraint.DampedRotarySpring(body2, body1, 0, rot_stiff, rot_damp)
        damped_spring = pymunk.constraint.DampedSpring(body1, body2, (0, 0), (0, 20), 10, fol_stiff, fol_damp)
        damped_spring2 = pymunk.constraint.DampedSpring(body1, body2, (0, 0), (0, -20), 10, fol_stiff, fol_damp)
        damped_spring3 = pymunk.constraint.DampedSpring(body1, body2, (0, 0), (80, 0), 0, 10, 1)

        # space.add(damped_spring, damped_spring2, damped_spring3, rotary_spring)
        space.add(damped_spring, damped_spring2, damped_spring3)

    space.add(ship1_body, ship2_body, ship1_shape, ship2_shape)

    setup_constraints(ship1_body, ship2_body)
    setup_constraints(ship2_body, ship1_body)

    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(screen, "aiming.png")
            elif event.type == pygame.MOUSEMOTION:
                pass
                # mouse_pos = pymunk.pygame_util.get_mouse_pos(screen)
                # ship2_body.position = mouse_pos
                # ship2_body.angle = (ship2_body.position - ship1_body.position).angle

            # to easily find good values for the damped rortary spring
            # as with most simulations done with pymunk, the imporant thing
            # is that it looks good, not the exact parameters
            elif event.type == KEYDOWN and event.key == K_q:
                rotary_spring.stiffness *= .5
                # print rotary_spring.stiffness, rotary_spring.damping
            elif event.type == KEYDOWN and event.key == K_w:
                rotary_spring.stiffness *= 2
                # print rotary_spring.stiffness, rotary_spring.damping
            elif event.type == KEYDOWN and event.key == K_a:
                rotary_spring.damping *= .5
                # print rotary_spring.stiffness, rotary_spring.damping
            elif event.type == KEYDOWN and event.key == K_s:
                rotary_spring.damping *= 2
                # print rotary_spring.stiffness, rotary_spring.damping
                
        ### Clear screen
        screen.fill(THECOLORS["white"])
        
        ### Draw stuff
        pymunk.pygame_util.draw(screen, space)

        ### Update physics
        #ship1_body.apply_impulse((pymunk.Vec2d(100, 0)).rotated(ship1_body.angle))
        #ship2_body.apply_impulse((pymunk.Vec2d(100, 0)).rotated(ship2_body.angle))


        dt = 1.0/60.0
        for x in range(20):
            space.step(dt)

        ### Flip screen
        pygame.display.flip()
        clock.tick(60)
        
if __name__ == '__main__':
    sys.exit(main())
