import pygame
import sys

from gameMechanics import Snake, Food


# global variables
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH/GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT/GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

pygame.init()
pygame.display.set_caption('Snake Game')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
surface = pygame.Surface(screen.get_size())
surface = surface.convert()


def drawGrid(surface, score):

    if (score < 10):  # blue
        lightColor = [153, 230, 255]
        darkColor = [128, 223, 255]
    elif(score < 20):  # yellow
        lightColor = [255, 214, 153]
        darkColor = [255, 204, 128]
    elif(score < 35):  # red
        lightColor = [255, 153, 153]
        darkColor = [255, 128, 128]
    elif(score < 50):  # purple
        lightColor = [236, 179, 255]
        darkColor = [230, 153, 255]
    elif(score < 75):  # black
        lightColor = [194, 194, 214]
        darkColor = [163, 163, 194]

    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x+y) % 2 == 0:
                r = pygame.Rect((x*GRID_SIZE, y*GRID_SIZE),
                                (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(
                    surface, (lightColor[0], lightColor[1], lightColor[2]), r)
            else:
                rr = pygame.Rect((x*GRID_SIZE, y*GRID_SIZE),
                                 (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(
                    surface, (darkColor[0], darkColor[1], darkColor[2]), rr)


def mainMenu():

    font = pygame.font.Font('freesansbold.ttf', 26)
    font1 = pygame.font.Font('freesansbold.ttf', 16)
    font2 = pygame.font.SysFont('arial', 16)
    text_main_menu = font.render("Snake", 1, (140, 255, 102))

    click = False
    run = True
    while run:

        mouse_x, mouse_y = pygame.mouse.get_pos()

        screen.fill((0, 0, 0))

        screen.blit(text_main_menu, (int(SCREEN_WIDTH/2-(text_main_menu.get_width()) /
                                         2), int((SCREEN_WIDTH/3))))

        button_play = pygame.Rect((int(SCREEN_WIDTH/2-150/2), 200, 150, 40))
        pygame.draw.rect(screen, (225, 0, 0), button_play)

        text_play = font.render("Play", True, (225, 225, 225))
        text_rect = text_play.get_rect()

        screen.blit(text_play, (int(240-text_rect.width/2), 210, 150, 40))

        # levels legend
        color1 = pygame.Rect(192, 294, 15, 15)
        color2 = pygame.Rect(192, 314, 15, 15)
        color3 = pygame.Rect(192, 334, 15, 15)
        color4 = pygame.Rect(192, 354, 15, 15)
        color5 = pygame.Rect(192, 374, 15, 15)
        pygame.draw.rect(screen, (128, 223, 255), color1)
        pygame.draw.rect(screen, (255, 204, 128), color2)
        pygame.draw.rect(screen, (255, 128, 128), color3)
        pygame.draw.rect(screen, (230, 153, 255), color4)
        pygame.draw.rect(screen, (163, 163, 194), color5)

        text_levels = font1.render("Levels", True, (225, 225, 225))
        text_level1 = font2.render("Score < 10", True, (225, 225, 225))
        text_level2 = font2.render("Score < 20", True, (225, 225, 225))
        text_level3 = font2.render("Score < 35", True, (225, 225, 225))
        text_level4 = font2.render("Score < 50", True, (225, 225, 225))
        text_level5 = font2.render("Score < 75", True, (225, 225, 225))

        screen.blit(text_levels, (215, 270, 150, 40))
        screen.blit(text_level1, (220, 292, 150, 40))
        screen.blit(text_level2, (220, 312, 150, 40))
        screen.blit(text_level3, (220, 332, 150, 40))
        screen.blit(text_level4, (220, 352, 150, 40))
        screen.blit(text_level5, (220, 372, 150, 40))

        if button_play.collidepoint((mouse_x, mouse_y)):
            button_play = pygame.Rect(
                (int(SCREEN_WIDTH/2-150/2), 200, 150, 40))
            pygame.draw.rect(screen, (255, 51, 51), button_play)

            screen.blit(text_play, (int(240-text_rect.width/2), 210, 150, 40))

            if click:
                run = False
                return False, True, False

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()


def game():
    temp = SCREEN_HEIGHT

    clock = pygame.time.Clock()

    snake = Snake()
    food = Food()
    drawGrid(surface, snake.score)
    myfont = pygame.font.Font('freesansbold.ttf', 26)

    game_run = True
    pause = False
    while (game_run):
        clock.tick(10+snake.score*0.5)
        snake.handle_keys()
        drawGrid(surface, snake.score)

        game_reset = snake.move()
        if(game_reset):
            game_run = False
            pygame.time.delay(1000)
            while(temp != 0):
                clock.tick(100)
                rect_rollup = pygame.Rect(
                    (0, temp, SCREEN_WIDTH, SCREEN_HEIGHT))
                pygame.draw.rect(screen, (0, 0, 0), rect_rollup)
                temp = temp-15
                pygame.display.flip()

        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        text = myfont.render("Score: {0}".format(snake.score), 1, (0, 0, 0))
        screen.blit(text, (10, 15))
        pygame.display.update()
    return snake.score


def endGame(score):
    font = pygame.font.Font('freesansbold.ttf', 26)
    click = False
    run = True
    while(run):

        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.fill((0, 0, 0))
        text_lost = font.render("You Lost", True, (225, 225, 225))
        text_rect = text_lost.get_rect()
        screen.blit(text_lost, (int(SCREEN_WIDTH/2-(text_lost.get_width()) /
                                    2), int((SCREEN_WIDTH/3)), 150, 40))
        text = font.render("Score: {0}".format(score), 1, (255, 255, 255))
        screen.blit(text, (10, 15))

        button_replay = pygame.Rect((int(SCREEN_WIDTH/2-150/2), 200, 150, 40))
        pygame.draw.rect(screen, (225, 0, 0), button_replay)

        text_replay = font.render("Replay", True, (225, 225, 225))
        text_rect = text_replay.get_rect()

        screen.blit(text_replay, (int(240-text_rect.width/2),
                                  button_replay.y+10, 150, 40))

        button_mm = pygame.Rect((int(SCREEN_WIDTH/2-150/2), 250, 150, 40))
        pygame.draw.rect(screen, (225, 0, 0), button_mm)

        text_mm = font.render("Menu", True, (225, 225, 225))
        text_rect = text_mm.get_rect()

        screen.blit(text_mm, (int(240-text_rect.width/2),
                              button_mm.y+10, 150, 40))

        if button_replay.collidepoint((mouse_x, mouse_y)):
            if click:
                run = False
                return False, True, False
        elif button_mm.collidepoint((mouse_x, mouse_y)):
            if click:
                run = False
                return True, False, False
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()


def main():
    load_menu = True
    load_game = False
    load_end = False
    score = 0
    while(True):
        if (load_menu == True and load_game == False and load_end == False):
            load_menu, load_game, load_end = mainMenu()
        elif(load_menu == False and load_game == True and load_end == False):
            score = game()
            load_menu, load_game, load_end = False, False, True
        else:
            load_menu, load_game, load_end = endGame(score)


main()
