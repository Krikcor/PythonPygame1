import os
import pygame
import time
from random import randint

pygame.init()
pygame.mixer.init()
LARGEUR, HAUTEUR = 800, 400
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Krikcor Pong")
pygame.display.set_icon(pygame.image.load('tennis.png'))
FPS = 60
clock = pygame.time.Clock()

son_joueur = pygame.mixer.Sound(os.path.join("assets", "pong_joueur.wav"))
son_mur = pygame.mixer.Sound(os.path.join("assets", "pong_mur.wav"))
son_point = pygame.mixer.Sound(os.path.join("assets", "pong_point.wav"))

separateurs = []
N = 10
LARGEUR_SEP = 2
HAUTEUR_SEP = HAUTEUR/N
OFFSET = 20

for i in range(N):
    x = (LARGEUR - LARGEUR_SEP)/2
    y = i*HAUTEUR_SEP + OFFSET/2
    separateurs.append(pygame.Rect(x, y, LARGEUR_SEP, HAUTEUR_SEP - OFFSET))

VITESSE_BOULE = 5
VITESSE_BOULE_LENT = 2

class Joueur:
    LARGEUR = 15
    HAUTEUR = 50
    VITESSE = 5
    FONT = pygame.font.SysFont(None, 100)

    def __init__(self, pos=(0, 0)):
        self.rect = pygame.Rect(pos[0], pos[1], Joueur.LARGEUR, Joueur.HAUTEUR)
        self.score = 0

    def deplacer_haut(self):
        self.rect.y -= Joueur.VITESSE

    def deplacer_bas(self):
        self.rect.y += Joueur.VITESSE

    def score_surface(self):
        return Joueur.FONT.render(str(self.score), True, 'white')

def direction_y_boule(x):
    return x*0.3

def gerer_collisions(boule, boule_dir, joueur_g, joueur_d):
    if boule.colliderect(joueur_g.rect):
        changer_vitesse_boule(boule_dir, VITESSE_BOULE)
        boule_dir.x = -boule_dir.x
        boule_dir.y = direction_y_boule(boule.center[1] - joueur_g.rect.center[1])
        son_joueur.play()
    
    if boule.colliderect(joueur_d.rect):
        changer_vitesse_boule(boule_dir, VITESSE_BOULE)
        boule_dir.x = -boule_dir.x
        boule_dir.y = direction_y_boule(boule.center[1] - joueur_d.rect.center[1])
        son_joueur.play()

def initialiser_boule(boule, boule_dir):
    boule.x = LARGEUR/2
    boule.y = randint(int(HAUTEUR/4), int(HAUTEUR - HAUTEUR/4))
    changer_vitesse_boule(boule_dir, VITESSE_BOULE_LENT)

def changer_vitesse_boule(boule_dir, vitesse):
    boule_dir.x = vitesse if boule_dir.x > 0 else -vitesse
    boule_dir.y = vitesse if boule_dir.y > 0 else -vitesse

def deplacer_boule(boule, boule_dir):
    if boule.x <= 0:
        joueur_d.score += 1
        initialiser_boule(boule, boule_dir)
        son_point.play()

    if boule.x + DIM_BOULE >= LARGEUR:
        joueur_g.score += 1
        initialiser_boule(boule, boule_dir)
        son_point.play()

    if boule.y <= 0  or boule.y + DIM_BOULE >= HAUTEUR:
        boule_dir.y = -boule_dir.y
        son_mur.play()
    

    boule.x += boule_dir.x
    boule.y += boule_dir.y

font = pygame.font.Font(None, 36)
texte_z = font.render("z", True, pygame.Color('white'))
texte_s = font.render("s", True, pygame.Color('white'))
texte_haut = font.render("flèche haut", True, pygame.Color('white'))
texte_bas = font.render("flèche bas", True, pygame.Color('white'))

fleche_haut = pygame.Surface((20, 20))
fleche_haut.fill(pygame.Color('white'))
fleche_bas = pygame.Surface((20, 20))
fleche_bas.fill(pygame.Color('white'))

def dessiner(joueur_d, joueur_g, boule, afficher_aide):
    fenetre.fill('black')

    for sep in separateurs:
        pygame.draw.rect(fenetre, 'white', sep)

    pygame.draw.rect(fenetre, 'white', joueur_g.rect)
    pygame.draw.rect(fenetre, 'white', joueur_d.rect)
    pygame.draw.rect(fenetre, 'white', boule)

    fenetre.blit(joueur_g.score_surface(), (int(LARGEUR/2 - 100), 10))
    score_surf = joueur_d.score_surface()
    fenetre.blit(score_surf, (int(LARGEUR/2 + 100 - score_surf.get_width()), 10))

    if afficher_aide:

        fenetre.blit(fleche_haut, (50, 50))
        fenetre.blit(texte_z, (75, 50))
        fenetre.blit(fleche_bas, (50, 100))
        fenetre.blit(texte_s, (75, 100))


        fenetre.blit(fleche_haut, (LARGEUR - 200, 50))
        fenetre.blit(texte_haut, (LARGEUR - 175, 50))
        fenetre.blit(fleche_bas, (LARGEUR - 200, 100))
        fenetre.blit(texte_bas, (LARGEUR - 175, 100))

    pygame.display.update()

joueur_g = Joueur((5, (HAUTEUR - Joueur.HAUTEUR)/2))
joueur_d = Joueur((LARGEUR - Joueur.LARGEUR - 5, (HAUTEUR - Joueur.HAUTEUR)/2))

DIM_BOULE = 10
boule = pygame.Rect(LARGEUR/2, HAUTEUR/2, DIM_BOULE, DIM_BOULE)
boule_dir = boule.copy()

FONT = pygame.font.SysFont(None, 50)
BUTTON_FONT = pygame.font.SysFont(None, 50)

def afficher_message_victoire(message):
    texte = FONT.render(message, True, (255, 255, 255))
    rect = texte.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 50))
    fenetre.blit(texte, rect)

    bouton_rejouer = pygame.Rect(LARGEUR // 2 - 100, HAUTEUR // 2 + 50, 200, 50)
    pygame.draw.rect(fenetre, (0, 255, 0), bouton_rejouer)
    texte_bouton = BUTTON_FONT.render("Rejouer", True, (0, 0, 0))
    fenetre.blit(texte_bouton, (bouton_rejouer.x + 50, bouton_rejouer.y + 10))

    pygame.display.flip()

    return bouton_rejouer


def main():
    executer = True
    jeu_actif = True
    initialiser_boule(boule, boule_dir)
    bouton_rejouer = None
    clock = pygame.time.Clock()
    start_time = time.time()

    running = True
    
    while executer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                executer = False
            if event.type == pygame.MOUSEBUTTONDOWN and bouton_rejouer:
                if bouton_rejouer.collidepoint(event.pos):
                    joueur_g.score = 0
                    joueur_d.score = 0
                    initialiser_boule(boule, boule_dir)
                    bouton_rejouer = None
                    jeu_actif = True
        
        touches = pygame.key.get_pressed()
        if touches[pygame.K_z] and joueur_g.rect.y > 0:
            joueur_g.deplacer_haut()
        if touches[pygame.K_s]  and joueur_g.rect.y + Joueur.HAUTEUR < HAUTEUR:
            joueur_g.deplacer_bas()
        if touches[pygame.K_UP] and joueur_d.rect.y > 0:
            joueur_d.deplacer_haut()
        if touches[pygame.K_DOWN]  and joueur_d.rect.y + Joueur.HAUTEUR < HAUTEUR:
            joueur_d.deplacer_bas()

        current_time = time.time()
        afficher_aide = current_time - start_time < 4


        if jeu_actif == True:
            gerer_collisions(boule, boule_dir, joueur_g, joueur_d)
            deplacer_boule(boule, boule_dir)
            dessiner(joueur_d, joueur_g, boule, afficher_aide)
            if joueur_g.score >= 10:
                bouton_rejouer = afficher_message_victoire("Le joueur de gauche a gagné!")
                jeu_actif = False
            elif joueur_d.score >= 10:
                bouton_rejouer = afficher_message_victoire("Le joueur de droite a gagné!")
                jeu_actif = False
        
        
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

