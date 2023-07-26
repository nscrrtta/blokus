from constants import *
import pygame


pygame.init()


class Text():

    def __init__(self, text: str, x_pos: int, y_pos: int, font_size: int, center: bool):

        font = pygame.font.Font(None, int((font_size/28)*SQR_SIZE))
        self.text = font.render(text, True, (250,250,250))
        self.rect = self.text.get_rect()

        if center: self.rect.center  = (x_pos, y_pos)
        else: self.rect.topleft = (x_pos, y_pos)


class TitleScreen:

    def __init__(self):

        self.text = [
            Text('Welcome to',         WIDTH*SQR_SIZE/2, TOP+1*SQR_SIZE, 42, True),
            Text('By Nick Sciarretta', WIDTH*SQR_SIZE/2, TOP+8*SQR_SIZE, 42, True)
        ]

        for i, (fnc, btn) in enumerate([
            ('Play/Pause',      'Escape'),
            ('New Game',        'Shift+N'),
            ('Switch Player',   'Tab'),
            ('Move',            'Arrow Keys'),
            ('Rotate',          'A or D'),
            ('Flip Horizontal', 'S'),
            ('Flip Vertical',   'W'),
            ('Place On Board',  'Return')
        ]):
            self.text.append(Text(fnc, LEFT+ 4*SQR_SIZE, TOP+(11+i)*SQR_SIZE, 35, False))
            self.text.append(Text(btn, LEFT+12*SQR_SIZE, TOP+(11+i)*SQR_SIZE, 35, False))


    def draw(self, screen):
        
        # Draw title screen
        rect = pygame.Rect(LEFT-3, TOP-3, SQR_SIZE*20+6, SQR_SIZE*20+6)
        pygame.draw.rect(screen, (100,100,100), rect)

        # Fun graphic
        for i, row in enumerate([
            [2,0,0,0,1,0,0,0,0,0,4,0,3,0,0,0,0,0,1,1],
            [2,0,0,0,1,0,0,0,0,0,4,0,3,0,0,0,0,0,1,0],
            [2,2,2,0,1,0,3,4,4,0,4,3,0,0,2,0,2,0,1,1],
            [2,0,2,0,1,0,3,0,4,0,4,0,3,0,2,0,2,0,0,1],
            [2,2,2,0,1,0,3,3,4,0,4,0,3,0,2,2,2,0,1,1]
        ]):
            for j, value in enumerate(row):
                if value == 0: continue
                colour = COLOURS[value]

                left = j*SQR_SIZE+LEFT+1
                top  = (i+2)*SQR_SIZE+TOP+1

                rect = pygame.Rect(left, top, SQR_SIZE-2, SQR_SIZE-2)
                pygame.draw.rect(screen, colour, rect)

        for text in self.text: screen.blit(text.text, text.rect)
