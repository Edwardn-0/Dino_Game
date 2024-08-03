import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
grey = (169, 169, 169)
brown = (139, 69, 19)
red = (255, 0, 0)

pygame.display.set_caption('Dino_game')
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
starting = True
playing = False

font_title = pygame.font.Font(None, 83)
Title = font_title.render('<Dino Game>', True, black)
Title_rect = Title.get_rect(center=(400, 100))

font = pygame.font.Font(None, 74)

game_start = font.render('START', True, grey)
game_start_rect = game_start.get_rect(center=(400, 200))

game_over = font.render('Game Over', True, red)
game_over_rect = game_over.get_rect(center=(400, 200))

font_score = pygame.font.Font(None, 37)

font_scoreboard = pygame.font.Font(None, 35)

player = pygame.image.load('D:\system\문서\code\Image/Shyguy_-_Red2.png')
player = pygame.transform.scale(player, (100, 100))
player_rect = player.get_rect(midbottom=(100, 300))

player_speed = 5
jump = 15
gravity = 0.65
jumping = False
velocity_y = 0
jump_count = 0
max_jump = 2

ground_height = 20
ground_y = 300
ground_rect = pygame.Rect(0, ground_y, screen.get_width(), ground_height)

tree_width = 40
tree_height = 40
tree_y = ground_rect.top - tree_height
trees = [pygame.Rect(800, tree_y, tree_width, tree_height)]


score = 0
checked_score = 0

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

    screen.blit(Title, Title_rect)
    screen.blit(game_start, game_start_rect)

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
                score += 10

            if score // 50 > checked_score // 50:
                checked_score = score
                new_tree = pygame.Rect(random.randint(800, 2000), tree_y, tree_width, tree_height)
                trees.append(new_tree)


            if player_rect.colliderect(tree):
                player_speed = 0
                screen.blit(game_over, game_over_rect)

                score_up = font_score.render(f'Score: {score}', True, black)
                score_up_rect = score_up.get_rect(center=(400, 250))
                pygame.display.update()
                pygame.time.delay(1000)

                screen.blit(score_up, score_up_rect)
                pygame.display.update()
                pygame.time.delay(2000)

                playing = False
                starting = False



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