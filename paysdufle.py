# coding: utf-8

import sys
import time
import glob
import pygame
import logging
import pygame_menu
from moviepy.editor import *

# VARIABLES
TITLE = "Pays du FLE - L'anniversaire magique"
PSEUDO_SECRET_KEY = 'bEokH7susW'
WIDTH = 800
HEIGHT = 600
MENU_TITLE = "Pays du FLE"
MENU_WIDTH = 600
MENU_HEIGHT = 400
FPS = 60
TEMPS_PAR_PORTE=5
TEMPS_RESTANT_VOCABULAIRE=TEMPS_PAR_PORTE
TEMPS_RESTANT_GRAMMAIRE=TEMPS_PAR_PORTE
CODE_VOCABULAIRE = 0
CODE_GRAMMAIRE = 0
DIFFICULTE = 1
CODE_VOCABULAIRE_TROUVE = False
CODE_GRAMMAIRE_TROUVE = False

# INITIALISATION
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# IMAGES
splashscreen = pygame.image.load('data/images/splashscreen.png').convert()
coffre = pygame.image.load('data/images/coffre.png').convert()
vocabulaire = pygame.image.load('data/images/portes/vocabulaire.jpg').convert()
grammaire = pygame.image.load('data/images/portes/grammaire.jpg').convert()

# VIDEOS
video_introduction_1 = VideoFileClip("data/videos/introduction/1.mp4")
video_introduction_2 = VideoFileClip("data/videos/introduction/2.mp4")

# POLICES
police_petit = pygame.font.Font("data/polices/berylium.ttf", 20)
police = pygame.font.Font("data/polices/berylium.ttf", 40)

def fadeOut(width, height): 
    fade = pygame.Surface((width, height))
    fade.fill((0, 0, 0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(1)

# Permet d'afficher l'écran d'accueil
def display_splashscreen():
    screen.blit(splashscreen, (100, 150))
    pygame.event.pump()
    pygame.display.update()
    time.sleep(2)
    fadeOut(WIDTH, HEIGHT)

display_splashscreen()

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

# Permet d'afficher un texte multi lignes à l'écran
def display_text(file):
    f = open('data/textes/' + file + '.txt', mode="r", encoding="utf-8")
    lines = f.read()
    f.close()
    screen.fill(pygame.Color("#abc1cc"))
    blit_text(screen, lines, (20, 20), police)
    pygame.display.update()

# Permet d'afficher l'introduction au jeu
def display_intro():
    display_text('introduction/1')
    break_ = False
    while True:
        if break_:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fadeOut(WIDTH, HEIGHT)
                    screen.fill(pygame.Color("#abc1cc"))
                    video_introduction_1.resize((WIDTH, HEIGHT)).preview()
                    break_ = True
                    break
    display_text('introduction/2')
    break_ = False
    while True:
        if break_:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fadeOut(WIDTH, HEIGHT)
                    screen.fill(pygame.Color("#abc1cc"))
                    video_introduction_2.resize((WIDTH, HEIGHT)).preview()
                    break_ = True
                    break
    display_text('introduction/3')
    break_ = False
    while True:
        if break_:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fadeOut(WIDTH, HEIGHT)
                    break_ = True
                    break

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

def display_questions(category):
    for filename in glob.glob('data/textes/questions/' + DIFFICULTE + '/' + category + '/*.txt'):
        with open(os.path.join(os.cwd(), filename), 'r') as f: # open in readonly mode
            # do your stuff

    f = open('data/textes/questions/' + DIFFICULTE + '/' + category + '*.txt', mode="r", encoding="utf-8")
    lines = f.read()
    f.close()
    screen.fill(pygame.Color("#abc1cc"))
    blit_text(screen, lines, (20, 20), police)
    pygame.display.update()

def display_game():

    start_ticks = pygame.time.get_ticks()

    while True:
        
        seconds = int(round((pygame.time.get_ticks() - start_ticks) / 1000))

        if seconds > 10:
            sys.exit()

        screen.fill((0,0,0))

        coffre_rect = coffre.get_rect(topleft=(350, 100))
        vocabulaire_rect = vocabulaire.get_rect(topleft=(50, 400))
        grammaire_rect = grammaire.get_rect(topleft=(300, 400))

        screen.blit(coffre, coffre_rect)
        screen.blit(vocabulaire, vocabulaire_rect)
        screen.blit(grammaire, grammaire_rect)
        
        if CODE_VOCABULAIRE_TROUVE:
            coffre_vocabulaire_text_string = "Code vocabulaire : %s" % (CODE_VOCABULAIRE)
            coffre_vocabulaire_text = police_petit.render(str(coffre_vocabulaire_text_string), 1, (255,255,255))
            coffre_vocabulaire_text_rect = coffre_vocabulaire_text.get_rect(topleft=(310, 200))
            screen.blit(coffre_vocabulaire_text, coffre_vocabulaire_text_rect)
        if CODE_GRAMMAIRE_TROUVE:
            coffre_grammaire_text_string = "Code grammaire : %s" % (CODE_GRAMMAIRE)
            coffre_grammaire_text = police_petit.render(str(coffre_grammaire_text_string), 1, (255,255,255))
            coffre_grammaire_text_rect = coffre_grammaire_text.get_rect(topleft=(310, 230))
            screen.blit(coffre_grammaire_text, coffre_grammaire_text_rect)

        vocabulaire_text = police_petit.render('Vocabulaire', 1, (255,255,255))
        vocabulaire_text_rect = vocabulaire_text.get_rect(topleft=(60, 350))
        screen.blit(vocabulaire_text, vocabulaire_text_rect)

        grammaire_text = police_petit.render('Grammaire', 1, (255,255,255))
        grammaire_text_rect = grammaire_text.get_rect(topleft=(310, 350))
        screen.blit(grammaire_text, grammaire_text_rect)

        counting_string = "%s" % (seconds)
        counting_text = police_petit.render(str(counting_string), 1, (255,255,255))
        counting_rect = counting_text.get_rect(center = screen.get_rect().center)
        screen.blit(counting_text, counting_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if vocabulaire_rect.collidepoint(x, y):
                    logging.warning('Click vocabulaire')
                elif grammaire_rect.collidepoint(x, y):
                    logging.warning('Click grammaire')

        pygame.display.update()
        clock.tick(FPS)
    
    fadeOut(WIDTH, HEIGHT)

# Boucle du jeu
def start_the_game():

    while True:

        # Si l'utilisateur n'a pas modifié le numéro de groupe
        if CODE_VOCABULAIRE == 0:
            # On génère les codes pour le numéro de groupe 01
            compute_codes("01")
        
        display_intro()

        display_game()

        pygame.quit()
        sys.exit(0)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit(0)

menu = pygame_menu.Menu(MENU_HEIGHT, MENU_WIDTH, MENU_TITLE, theme=pygame_menu.themes.THEME_BLUE)

menu.add_selector('Numéro de groupe : ', [('01', 1), ('02', 2), ('03', 3), ('04', 4), ('05', 5), ('06', 6), ('07', 7), ('08', 8), ('09', 9), ('10', 10)], onchange=set_group)
menu.add_selector('Difficulté : ', [('A1', 'a1'), ('A2', 'a2')], onchange=set_difficulty)
menu.add_button('Jouer', start_the_game)
menu.add_button('Quitter', pygame_menu.events.EXIT)

menu.mainloop(screen)