import sys
import time
import pygame
import logging
import pygame_menu

TITLE = "Pays du FLE - L'anniversaire magique"
PSEUDO_SECRET_KEY = 'bEokH7susW'
WIDTH = 1024
HEIGHT = 768
MENU_TITLE = "Pays du FLE"
MENU_WIDTH = 700
MENU_HEIGHT = 500
FPS = 60
TEMPS_PAR_PORTE=5
TEMPS_RESTANT_VOCABULAIRE=TEMPS_PAR_PORTE
TEMPS_RESTANT_GRAMMAIRE=TEMPS_PAR_PORTE
CODE_VOCABULAIRE = 0
CODE_GRAMMAIRE = 0
DIFFICULTE = 1

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
splashscreen = pygame.image.load('images/splashscreen.png')
introGirlImg = pygame.image.load('images/intro_girl.jpg')
clock = pygame.time.Clock()

screen.blit(splashscreen, (140, 170))
pygame.event.pump()
pygame.display.update()
time.sleep(0)

# Cf. : https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame?answertab=active#tab-top
def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

# Permet d'obtenir les codes pour le cadenas
def compute_codes(group):
    global CODE_VOCABULAIRE
    global CODE_GRAMMAIRE
    hashCodes = str(abs(hash(PSEUDO_SECRET_KEY + str(group))))
    n = 4
    codes = [hashCodes[i:i+n] for i in range(0, len(hashCodes), n)]
    CODE_VOCABULAIRE = codes[0]
    CODE_GRAMMAIRE = codes[1]

# Permet de définir le niveau de difficulté
def set_difficulty(value, difficulty):
    global DIFFICULTE
    DIFFICULTE = difficulty

# Permet de définir le numéro de groupe
def set_group(value, group):
    compute_codes(group)

# Boucle du jeu
def start_the_game():
    f = open("introduction.txt", "r")
    lines = f.read()
    f.close()

    clock = pygame.time.Clock()

    while True:
        time = clock.tick(FPS)

        if CODE_VOCABULAIRE == 0:
            compute_codes("01")

        police = pygame.font.Font("polices/berylium.ttf", 40)
        
        screen.fill(pygame.Color("#abc1cc"))
        blit_text(screen, lines, (20, 20), police)
        pygame.display.update()

        # screen.fill(pygame.Color("#abc1cc"))
        # screen.blit(introGirlImg, (140, 170))
        # pygame.event.pump()
        # pygame.display.update()
        # pygame.time.wait(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit(0)

menu = pygame_menu.Menu(MENU_HEIGHT, MENU_WIDTH, MENU_TITLE, theme=pygame_menu.themes.THEME_BLUE)

menu.add_selector('Numéro de groupe : ', [('01', 1), ('02', 2), ('03', 3), ('04', 4), ('05', 5), ('06', 6), ('07', 7), ('08', 8), ('09', 9), ('10', 10)], onchange=set_group)
menu.add_selector('Difficulté : ', [('A1', 1), ('A2', 2)], onchange=set_difficulty)
menu.add_button('Jouer', start_the_game)
menu.add_button('Quitter', pygame_menu.events.EXIT)

menu.mainloop(screen)