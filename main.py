from constants import *
from game import Game
import pygame


pygame.display.set_caption('Blokus by Nick Sciarretta')
screen = pygame.display.set_mode((WIDTH*SQR_SIZE, HEIGHT*SQR_SIZE))


game = Game()
running = True


while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT: 
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            game.select_piece()

        elif event.type == pygame.MOUSEBUTTONUP:

            if game.selected_piece is not None:
                game.selected_piece.drop()

        elif event.type == pygame.KEYDOWN:

            piece = game.selected_piece
            keys = pygame.key.get_pressed()
            shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

            if event.key == pygame.K_ESCAPE:
                game.title_screen_active = not game.title_screen_active

            elif game.title_screen_active: pass

            elif event.key == pygame.K_n and shift:
                game.new_game()

            elif event.key == pygame.K_TAB:
                game.next_player()

            elif piece is None: pass

            elif piece.held: pass

            elif event.key == pygame.K_UP:
                piece.move(0,-1)

            elif event.key == pygame.K_DOWN:
                piece.move(0, 1)

            elif event.key == pygame.K_LEFT:
                piece.move(-1, 0)

            elif event.key == pygame.K_RIGHT:
                piece.move(1, 0)

            elif event.key == pygame.K_a:
                piece.rotate(-1)

            elif event.key == pygame.K_d:
                piece.rotate(1)

            elif event.key == pygame.K_w:
                piece.flip(-1)

            elif event.key == pygame.K_s:
                piece.flip(1)

            elif event.key == pygame.K_RETURN:
                game.place_piece()

        elif event.type == pygame.KEYUP: 
            button_pressed = hold = False

    game.draw(screen)
    pygame.display.update()
    

pygame.quit()