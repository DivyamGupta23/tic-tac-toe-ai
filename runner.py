import pygame
import sys
import time

import tictactoe as ttt

pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tic-Tac-Toe")
mediumFont = pygame.font.Font("Montserrat-Medium.ttf", 41)
largeFont = pygame.font.Font("Montserrat-Bold.ttf", 60)
moveFont = pygame.font.Font("Montserrat-Bold.ttf", 41)

user = None
board = ttt.initial_state()
ai_turn = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(pygame.Color(45, 46, 49))

    # Let user choose a player.
    if user is None:

        # Draw title
        title = largeFont.render(
            "Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)

        title_shadow = largeFont.render(
            "Tic-Tac-Toe", True, pygame.Color(32, 33, 36))
        title_shadowRect = title.get_rect()
        title_shadowRect.center = ((width / 2) - 7, 57)

        screen.blit(title_shadow, title_shadowRect)
        screen.blit(title, titleRect)

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2.5), width / 3, 120)
        playXButtonShadow = pygame.Rect(
            (width / 8)-7, (height / 2.5)+7, width / 3, 120)
        playX = mediumFont.render(" X ", True, white)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, pygame.Color(22, 23, 26), playXButtonShadow,
                         border_bottom_right_radius=20, border_top_left_radius=20)

        pygame.draw.rect(screen, pygame.Color(32, 33, 36),
                         playXButton, border_bottom_right_radius=20, border_top_left_radius=20)

        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(
            4*(width / 8), (height / 2.5), width / 3, 120)
        playOButtonShadow = pygame.Rect(
            4*(width / 8)+7, (height / 2.5)+7, width / 3, 120)
        playO = mediumFont.render(" 0 ", True, pygame.Color(32, 33, 36))
        playORect = playO.get_rect()
        playORect.center = playOButton.center

        pygame.draw.rect(screen, pygame.Color(22, 23, 26), playOButtonShadow,
                         border_top_right_radius=20, border_bottom_left_radius=20)

        pygame.draw.rect(screen, white, playOButton,
                         border_top_right_radius=20, border_bottom_left_radius=20)
        screen.blit(playO, playORect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O

    else:

        # Draw game board
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)

                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        # Show title
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == player:
            title = f"{user}'s Turn"
        else:
            title = f"CPU({player}) is thinking.."
        title = moveFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 4, height - 65, width / 2, 50)
            again = mediumFont.render(
                "Play Again", True, pygame.Color(32, 33, 36))
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton,
                             border_bottom_right_radius=20, border_top_left_radius=20)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False

    pygame.display.flip()
