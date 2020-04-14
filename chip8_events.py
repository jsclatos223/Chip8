# This is the class blueprint for a Events Object.
import pygame
import sys
pygame.init()


class EVENTS():
    def __init__(self):
        # Construct System Event Controls
        self.cpu = 0
        self.events = pygame.event.get()            # Keeps track of any events that happen while application is running.
        self.event_type = -1
        self.keys = [
                        pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                        pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r,
                        pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f,
                        pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v
                    ]


    def get_key_event(self):
        self.events = pygame.event.get()
        for event in self.events:
            self.event_type = -1
            if event.type == pygame.QUIT():
                sys.exit(0)
            elif event.type == pygame.KEYUP:
                self.event_type = 0
            elif event.type == pygame.KEYDOWN:
                self.event_type = 1

            if self.event_type == 0 or se;f.event_type == 1:
                if event.key in self.keys:
                    i = self.keys.index(event.key)
                    self.cpu.keys[i] = self.event_type
