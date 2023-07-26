from constants import *
import pygame


class Piece():

    def __init__(self, shape_id: int, col_id: int):

        self.shape_id = shape_id
        self.col_id   = col_id

        self.colour = COLOURS[col_id]

        self.rect = pygame.Surface((SQR_SIZE-2, SQR_SIZE-2))
        self.rect.fill(self.colour)
        self.rect.set_alpha(120)


    def reset(self):

        self.placed = False
        self.selected = False

        self.shape = SHAPES[self.shape_id]
        self.x_pos, self.y_pos = START_POS[self.col_id][self.shape_id]

        b = '{0:02b}'.format(self.col_id-1)
        if int(b[0]): self.flip(-1)
        if int(b[1]): self.flip(1)

        self.width  = len(self.shape[0])
        self.height = len(self.shape)

        self.held = False

    
    def move(self, dx: int, dy: int):
        
        self.x_pos += dx
        self.y_pos += dy
        self.keep_in_bounds()


    def rotate(self, dir: int):

        # 1 = clockwise, -1 = counter-clockwise
        self.shape = rotate(self.shape, dir)

        self.width  = len(self.shape[0])
        self.height = len(self.shape)

        self.keep_in_bounds()


    def flip(self, dir: int):

        # 1 = flip about y-axis, -1 = flip about x-axis
        self.shape = flip(self.shape, dir)

    
    def keep_in_bounds(self):

        if self.x_pos < 0: self.x_pos = 0

        elif self.x_pos > WIDTH - self.width:
            self.x_pos = WIDTH - self.width

        if self.y_pos < 0: self.y_pos = 0

        elif self.y_pos > HEIGHT - self.height:
            self.y_pos = HEIGHT - self.height


    def pick_up(self, mouse_pos: tuple) -> bool:

        x,y = mouse_pos

        def create_pos_dict():

            self.pos_dict = {(0,0): (self.x_pos*SQR_SIZE-x,self.y_pos*SQR_SIZE-y)}

            for i in range(self.height):
                for j in range(self.width):
                
                    if self.shape[i][j] == 0: continue

                    dc = (self.x_pos+j)*SQR_SIZE - x
                    dr = (self.y_pos+i)*SQR_SIZE - y

                    self.pos_dict[(j,i)] = (dc,dr)

        for i in range(self.height):
            for j in range(self.width):
                
                if self.shape[i][j] == 0: continue

                left   = (self.x_pos+j)*SQR_SIZE+1
                right  = left+SQR_SIZE-2
                top    = (self.y_pos+i)*SQR_SIZE+1
                bottom = top+SQR_SIZE-2

                if (left <= x <= right and top <= y <= bottom):
                    create_pos_dict()
                    self.selected = True
                    self.held = True
                    return True
        
        return False
    

    def drop(self):

        x,y = pygame.mouse.get_pos()
        a,b = self.pos_dict[(0,0)]

        # Math to snap piece to grid
        self.x_pos = (x+a+SQR_SIZE//2)//SQR_SIZE
        self.y_pos = (y+b+SQR_SIZE//2)//SQR_SIZE
        
        self.held = False
        self.keep_in_bounds()


    def draw(self, screen):

        if self.held: x,y = pygame.mouse.get_pos()
        else: x,y = self.x_pos, self.y_pos

        for i in range(self.height):
            for j in range(self.width):
                
                if self.shape[i][j] == 0: continue

                if self.held: 
                    dc, dr = self.pos_dict[(j,i)]
                else: 
                    dc = (self.x_pos+j)*SQR_SIZE - x
                    dr = (self.y_pos+i)*SQR_SIZE - y

                rect = pygame.Rect(dc+x+1, dr+y+1, SQR_SIZE-2, SQR_SIZE-2) 

                if self.placed:
                    pygame.draw.rect(screen, self.colour, rect)
                else:
                    screen.blit(self.rect, (dc+x+1, dr+y+1))
                    if self.selected: pygame.draw.rect(screen, self.colour, rect, width=2)


def rotate(shape: list, dir: int) -> tuple:

    # 1 = clockwise, -1 = counter-clockwise
    return list(zip(*shape[::-dir]))[::dir]


def flip(shape: int, dir: int) -> list:

    # 1 = flip about y-axis, -1 = flip about x-axis
    if dir == 1: return [row[::-1] for row in shape]
    if dir ==-1: return rotate(flip(rotate(shape,1),1),-1)
