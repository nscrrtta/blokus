from title_screen import TitleScreen
from random import randint
from piece import Piece
from constants import *
import pygame


class Game:

    def __init__(self):

        self.pieces = {
            1: [Piece(i,1) for i in range(21)], # Red
            2: [Piece(i,2) for i in range(21)], # Blue
            3: [Piece(i,3) for i in range(21)], # Green
            4: [Piece(i,4) for i in range(21)], # Yellow
        }
        
        self.board_tile = pygame.Surface((SQR_SIZE-2, SQR_SIZE-2))
        self.board_tile.fill((200,200,200))
        self.board_tile.set_alpha(120)

        self.title_screen = TitleScreen()
        self.title_screen_active = True

        self.new_game()
        

    def new_game(self):

        # 0 = empty square
        # 1 = red square
        # 2 = blue square
        # 3 = green square
        # 4 = yellow square

        self.board = [[0 for _ in range(20)] for _ in range(20)]
        self.selected_piece = None
        
        for i, pieces in self.pieces.items():
            for piece in pieces: piece.reset()

        # Randomly choose who goes first
        self.active_player = randint(1,4)
        

    def next_player(self):

        if self.selected_piece is not None:
            self.selected_piece.reset()
            self.selected_piece = None

        self.active_player = (self.active_player)%4 + 1


    def select_piece(self):

        x,y = pygame.mouse.get_pos()

        if self.selected_piece is not None:
            if self.selected_piece.pick_up((x,y)):
                return
            self.selected_piece.reset()
            self.selected_piece = None
        
        for piece in self.pieces[self.active_player]:
            if piece.pick_up((x,y)):
                self.selected_piece = piece
                break

    
    def place_piece(self):

        if self.selected_piece is None: return
        if not self.valid_spot(): return

        for i in range(self.selected_piece.height):
            for j in range(self.selected_piece.width):

                if self.selected_piece.shape[i][j] == 0: continue

                x = j+self.selected_piece.x_pos-LEFT//SQR_SIZE
                y = i+self.selected_piece.y_pos-TOP//SQR_SIZE

                self.board[y][x] = self.selected_piece.col_id

        self.selected_piece.placed = True
        self.selected_piece = None
        self.next_player()


    def valid_spot(self) -> bool:

        valid = False
        first_piece = True

        for piece in self.pieces[self.active_player]:
            if piece.placed: first_piece = False; break

        for i in range(self.selected_piece.height):
            for j in range(self.selected_piece.width):

                if self.selected_piece.shape[i][j] == 0: continue

                x = j+self.selected_piece.x_pos-LEFT//SQR_SIZE
                y = i+self.selected_piece.y_pos-TOP//SQR_SIZE

                # Check if out of bounds
                if not (0 <= x < 20 and 0 <= y < 20): return False
                
                # Check if first piece touches corner
                if first_piece and (x,y) == CORNERS[self.active_player]: 
                    valid = True
                
                # Check if overlapping another piece
                if self.board[y][x] > 0: return False

                # Check if touching edge of friendly piece
                for x2, y2 in [(x,y+1), (x,y-1), (x+1,y), (x-1,y)]:
                    if not (0 <= x2 < 20 and 0 <= y2 < 20): continue
                    if self.board[y2][x2] == self.active_player: return False

                # Check if touching corner of friendly piece
                for x2, y2 in [(x+1,y+1), (x-1,y+1), (x-1,y-1), (x+1,y-1)]:
                    if not (0 <= x2 < 20 and 0 <= y2 < 20): continue
                    if self.board[y2][x2] == self.active_player: valid = True

        if valid: return True
        return False

    
    def draw(self, screen):

        screen.fill((50,50,50))
    
        # Draw square around board to show whose turn it is
        rect = pygame.Rect(LEFT-3, TOP-3, SQR_SIZE*20+6, SQR_SIZE*20+6)
        pygame.draw.rect(screen, COLOURS[self.active_player], rect, width=2)

        # Draw board
        for i in range(20):
            for j in range(20):

                left = 1+j*SQR_SIZE+LEFT
                top  = 1+i*SQR_SIZE+TOP
                screen.blit(self.board_tile, (left, top))

        # Draw pieces
        for i, pieces in self.pieces.items():
            if i == self.active_player: continue
            for piece in pieces: piece.draw(screen)

        for piece in self.pieces[self.active_player]: piece.draw(screen)

        if self.title_screen_active: self.title_screen.draw(screen)
