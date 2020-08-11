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


def drawGrid(surface, score):

    if (score < 10):
        lightColor = [1, 225, 154]
        darkColor = [1, 209, 154]
    elif(score < 20):
        lightColor = [93, 216, 228]
        darkColor = [84, 194, 205]
    elif(score < 35):
        lightColor = [240, 221, 0]
        darkColor = [240, 198, 0]

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


pygame.init()
pygame.display.set_caption('Snake Game')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
surface = pygame.Surface(screen.get_size())
surface = surface.convert()


def main():
    load_menu = True
    load_game = False
    load_end = False
    while(True):
        if (load_menu == True and load_game == False and load_end == False):
            load_menu, load_game, load_end = mainMenu()
        elif(load_menu == False and load_game == True and load_end == False):
            game()
            load_menu, load_game, load_end = False, False, True
        else:
            load_menu, load_game, load_end = endGame()


def mainMenu():

    font = pygame.font.Font('freesansbold.ttf', 26)
    text_main_menu = font.render("Main Menu", 1, (255, 255, 255))

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

        if button_play.collidepoint((mouse_x, mouse_y)):
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
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        text = myfont.render("score {0}".format(snake.score), 1, (0, 0, 0))
        screen.blit(text, (5, 10))
        pygame.display.update()


def endGame():
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


main()
