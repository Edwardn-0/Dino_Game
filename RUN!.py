import pygame
import random
import os
import sys

def resource_path(relpath):
    try:
        abspath = sys._MEIPASS
    except Exception:
        abspath = os.path.abspath(".")
    return os.path.join(abspath, relpath)

def trees_height_setting(l, w, h):
    global tree_y, trees
    tree_y = ground_rect.top - h
    trees = [pygame.Rect(l, tree_y, w, h)]


pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
grey = (169, 169, 169)
brown = (139, 69, 19)
red = (255, 0, 0)

pygame.display.set_caption('RUN!')
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
starting = True
playing = False

font_title = pygame.font.Font(None, 83)
Title = font_title.render('<RUN!>', True, black)
Title_rect = Title.get_rect(center=(400, 100))

font = pygame.font.Font(None, 74)

game_start = font.render('START', True, grey)
game_start_rect = game_start.get_rect(center=(400, 200))

game_over = font.render('Game Over', True, red)
game_over_rect = game_over.get_rect(center=(400, 200))

font_score = pygame.font.Font(None, 37)

font_scoreboard = pygame.font.Font(None, 35)

image = resource_path("image/Shyguy_-_Red2.png")
player = pygame.image.load(image)
player = pygame.transform.scale(player, (100, 100))
player_rect = player.get_rect(midbottom=(100, 300))

START = 'starting'
PLAY = 'playing'
game_state = START

while starting:
    clock.tick(60)
    screen.fill(white)

    for event_first in pygame.event.get():
        if event_first.type == pygame.QUIT:       
            starting = False
        if event_first.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if game_start_rect.collidepoint(mouse_pos):
                playing = True
                game_state = PLAY

    screen.blit(Title, Title_rect)
    screen.blit(game_start, game_start_rect)

    if game_state == PLAY:
            player_rect = player.get_rect(midbottom=(100, 300))
            player_speed = 5
            jump = 15.5
            gravity = 0.65
            jumping = False
            velocity_y = 0
            jump_count = 0
            max_jump = 1

            ground_height = 20
            ground_y = 300
            ground_rect = pygame.Rect(0, ground_y, screen.get_width(), ground_height)

            trees_height_setting(800, 35, 70)

            score = 0
            checked_score = 0

    while playing:
        clock.tick(60)
        screen.fill(white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                starting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if jump_count < max_jump:
                        if not jumping or (jumping and jump_count < max_jump):
                            jumping = True
                            velocity_y = -jump
                            jump_count += 1
        
        if jumping:
            player_rect.y += velocity_y
            velocity_y += gravity
            if player_rect.bottom >= 300:
                player_rect.bottom = 300
                jumping = False
                jump_count = 0
            if player_rect.top <= 0:
                player_rect.top = 0

        for tree in trees:
            tree.x -= player_speed
            if tree.right < 0:
                tree.x = 800
                score += 1

            if score // 5 > checked_score // 5:
                checked_score = score
                trees_height_setting(550, 45, 90)
            elif score // 7 > checked_score // 7:
                checked_score = score
                trees_height_setting(800, 35, 70)
            elif score // 12 > checked_score // 12:
                checked_score = score
                trees_height_setting(1100, 75, 125)

            if score // 2 > checked_score // 2:
                checked_score = score
                player_speed += 1.5


            if player_rect.colliderect(tree):
                player_speed = 0
                screen.blit(game_over, game_over_rect)

                score_up = font_score.render(f'Score: {score}', True, black)
                score_up_rect = score_up.get_rect(center=(400, 250))
                pygame.display.update()
                pygame.time.delay(500)

                screen.blit(score_up, score_up_rect)
                pygame.display.update()
                pygame.time.delay(1500)

                scoreboard = open('scoreboard.txt', 'a+')
                scoreboard.write(str(score)+'\n')
                scoreboard.close()

                playing = False
                game_state = START



        screen.blit(player, player_rect)

        scoreboard = font_scoreboard.render(f'score: {score}', True, black)
        scoreboard_rect = scoreboard.get_rect(center=(720, 25))
        screen.blit(scoreboard, scoreboard_rect)

        pygame.draw.rect(screen, black, ground_rect)
        for tree in trees:
            pygame.draw.rect(screen, brown, tree)

            

        pygame.display.update()

    pygame.display.update()


pygame.quit()