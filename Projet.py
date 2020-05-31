import pygame
import sys
from pygame.locals import *
pygame.init()

taille_sprite = 20
nombre_sprite_cote = 40


class Jeu:
    """Class du jeu de la vie"""

    def __init__(self, fichier):
        """ classe créant l'interface du jeu et controlant sa matrice """
        self.fichier = fichier
        self.structure = []

    def generer(self):
        """Méthode permettant de générer le niveau en fonction du fichier.
        On crée une liste générale, contenant une liste par ligne à afficher"""
        # On ouvre le fichier
        with open(self.fichier, "r") as fichier:
            structure_niveau = []
            # On parcourt les lignes du fichier
            for ligne in fichier:
                ligne_niveau = []
                # On parcourt les sprites (lettres) contenus dans le fichier
                for sprite in ligne:
                    # On ignore les "\n" de fin de ligne
                    if sprite != '\n':
                        # On ajoute le sprite à la liste de la ligne
                        ligne_niveau.append(sprite)
                # On ajoute la ligne à la liste du niveau
                structure_niveau.append(ligne_niveau)
            # On sauvegarde cette structure
            self.structure = structure_niveau

    def afficher(self, interface):
        """ Créer l'interface de case vide/plein """
        carre_plein = pygame.image.load("carre_plein.png").convert()
        carre_vide = pygame.image.load("carre_vide.png").convert()

        num_ligne = 0
        for ligne in self.structure:
            num_case = 0
            for sprite in ligne:
                # On calcule la position réelle en pixels
                x = num_case * taille_sprite
                y = num_ligne * taille_sprite
                if sprite == '0':  # 0=case vide
                    interface.blit(carre_vide, (x, y))
                if sprite == '1':  # 1 =carre plein
                    interface.blit(carre_plein, (x, y))
                num_case += 1
            num_ligne += 1


class Joueur:
    """déplacement du joueur/ controle du curseur """

    def __init__(self, curseur, niveau):
        self.curseur = pygame.image.load(curseur).convert_alpha()
        self.case_x = 0
        self.case_y = 0
        self.x = 0
        self.y = 0
        self.etat_niveau = {}
        self.niveau = niveau

    def deplacer(self, direction):
        """outil permettant de déplacer le curseur"""

        if direction == 'droite':
            # on ne veut pas que le curseur sorte de l'écran
            if self.case_x < (nombre_sprite_cote - 1):
                # on le déplace vers la droite
                self.case_x += 1
                self.x = self.case_x * taille_sprite
        if direction == 'gauche':
            # on déplace vers la gauche
            if self.case_x > 0:
                self.case_x -= 1
                self.x = self.case_x * taille_sprite
        if direction == 'haut':
            # on déplace vers le haut
            if self.case_y > 0:
                self.case_y -= 1
                self.y = self.case_y * taille_sprite
        if direction == 'bas':
            # on déplace vers le bas
            if self.case_y < (nombre_sprite_cote - 1):
                self.case_y += 1
                self.y = self.case_y * taille_sprite

    def deposer(self):
        """outil permettant de changer une case vide par une case pleine
                            et inversement"""
        # On cherche l'index de la matrice de notre niveau qui correspond a la position du curseur
        # puis on modifie la valeur présente dans l'index coresspondant
        if self.niveau.structure[self.case_y][self.case_x] == '1':
            self.niveau.structure[self.case_y][self.case_x] = '0'
        elif self.niveau.structure[self.case_y][self.case_x] == '0':
            self.niveau.structure[self.case_y][self.case_x] = '1'

    def regles(self):
        """ Outil permettant de calculer le nombre de voisin de chaque case"""
        b = 0

        while b != nombre_sprite_cote:
            a = 0
            while a != nombre_sprite_cote:
                # on s'occupe des cas particuliers
                # coin en haut a gauche
                if a == 0 and b == 0:
                    voisin = 0
                    if self.niveau.structure[a + 1][b] == '1':
                        voisin += 1
                    if self.niveau.structure[a][b + 1] == '1':
                        voisin += 1
                    if self.niveau.structure[a + 1][b + 1] == '1':
                        voisin += 1
                    self.etat_niveau[a, b] = voisin
                # coin en haut a droite
                elif a == 0 and b == nombre_sprite_cote - 1:
                    voisin = 0
                    if self.niveau.structure[a + 1][b] == '1':
                        voisin += 1
                    if self.niveau.structure[a][b - 1] == '1':
                        voisin += 1
                    if self.niveau.structure[a + 1][b - 1] == '1':
                        voisin += 1
                    self.etat_niveau[a, b] = voisin
                # coin en bas a gauche
                elif a == nombre_sprite_cote - 1 and b == 0:
                    voisin = 0
                    if self.niveau.structure[a - 1][b] == '1':
                        voisin += 1
                    if self.niveau.structure[a][b + 1] == '1':
                        voisin += 1
                    if self.niveau.structure[a - 1][b + 1] == '1':
                        voisin += 1
                    self.etat_niveau[a, b] = voisin
                # coin en bas a droite
                elif a == nombre_sprite_cote - 1 and b == nombre_sprite_cote - 1:
                    voisin = 0
                    if self.niveau.structure[a - 1][b] == '1':
                        voisin += 1
                    if self.niveau.structure[a][b - 1] == '1':
                        voisin += 1
                    if self.niveau.structure[a - 1][b - 1] == '1':
                        voisin += 1
                    self.etat_niveau[a, b] = voisin
                # bord gauche
                elif 0 < a < nombre_sprite_cote - 1 and b == 1 - 1:
                    voisin = 0
                    if self.niveau.structure[a + 1][b] == '1':
                        voisin += 1
                    if self.niveau.structure[a - 1][b] == '1':
                        voisin += 1
                    if self.niveau.structure[a][b + 1] == '1':
                        voisin += 1
                    if self.niveau.structure[a + 1][b + 1] == '1':
                        voisin += 1
                    if self.niveau.structure[a - 1][b + 1] == '1':
                        voisin += 1
                    self.etat_niveau[a, b] = voisin
                # bord haut
                elif a == 0 and 0 < b < nombre_sprite_cote - 1:
                    voisin = 0
                    if self.niveau.structure[a][b + 1] == '1':
                        voisin += 1
                    if self.niveau.structure[a][b - 1] == '1':
                        voisin += 1
                    if self.niveau.structure[a + 1][b] == '1':
                        voisin += 1
                    if self.niveau.structure[a + 1][b + 1] == '1':
                        voisin += 1
                    if self.niveau.structure[a + 1][b - 1] == '1':
                        voisin += 1
                    self.etat_niveau[a, b] = voisin
                # bord droit
                elif 0 < a < nombre_sprite_cote - 1 and b == nombre_sprite_cote - 1:
                    voisin = 0
                    if self.niveau.structure[a - 1][b] == '1':
                        voisin += 1
                    if self.niveau.structure[a - 1][b - 1] == '1':
                        voisin += 1
                    if self.niveau.structure[a + 1][b - 1] == '1':
                        voisin += 1
                    if self.niveau.structure[a + 1][b] == '1':
                        voisin += 1
                    if self.niveau.structure[a][b - 1] == '1':
                        voisin += 1
                    self.etat_niveau[a, b] = voisin
                # bord bas
                elif a == nombre_sprite_cote - 1 and 0 < b < nombre_sprite_cote - 1:
                    voisin = 0
                    if self.niveau.structure[a - 1][b] == '1':
                        voisin += 1
                    if self.niveau.structure[a - 1][b - 1] == '1':
                        voisin += 1
                    if self.niveau.structure[a - 1][b + 1] == '1':
                        voisin += 1
                    if self.niveau.structure[a][b + 1] == '1':
                        voisin += 1
                    if self.niveau.structure[a][b - 1] == '1':
                        voisin += 1
                    self.etat_niveau[a, b] = voisin
                # cas général
                else:
                    voisin = 0
                    if self.niveau.structure[a - 1][b] == '1':
                        voisin += 1
                    if self.niveau.structure[a + 1][b] == '1':
                        voisin += 1
                    if self.niveau.structure[a][b - 1] == '1':
                        voisin += 1
                    if self.niveau.structure[a][b + 1] == '1':
                        voisin += 1
                    if self.niveau.structure[a + 1][b + 1] == '1':
                        voisin += 1
                    if self.niveau.structure[a + 1][b - 1] == '1':
                        voisin += 1
                    if self.niveau.structure[a - 1][b + 1] == '1':
                        voisin += 1
                    if self.niveau.structure[a - 1][b - 1] == '1':
                        voisin += 1
                    self.etat_niveau[a, b] = voisin
                a += 1
            b += 1

    def redessinage(self):
        """ on applique les règles du jeu de la vie """

        axe_x = 0
        while axe_x != nombre_sprite_cote:
            axe_y = 0
            while axe_y != nombre_sprite_cote:
                # règle pour les cases vides
                if self.niveau.structure[axe_y][axe_x] == '0':
                    if self.etat_niveau[axe_y, axe_x] == 3:
                        self.niveau.structure[axe_y][axe_x] = '1'
                # règle pour les cases pleines
                if self.niveau.structure[axe_y][axe_x] == '1':
                    if self.etat_niveau[axe_y, axe_x] > 3:
                        self.niveau.structure[axe_y][axe_x] = '0'
                if self.niveau.structure[axe_y][axe_x] == '1':
                    if self.etat_niveau[axe_y, axe_x] == 3 or 2:
                        self.niveau.structure[axe_y][axe_x] = '1'
                if self.niveau.structure[axe_y][axe_x] == '1':
                    if self.etat_niveau[axe_y, axe_x] < 2:
                        self.niveau.structure[axe_y][axe_x] = '0'
                axe_y += 1
            axe_x += 1


continuer = 1
while continuer == 1:
    # on charge les images que l'ont utilisera
    page = pygame.display.set_mode((1000, 750))
    acceuil = pygame.image.load("acceuil.png").convert()
    son_on = pygame.image.load("son_actif.png").convert()
    son_off = pygame.image.load("son_mute.png").convert()
    page.blit(acceuil, (0, 0))
    page.blit(son_on, (800, 80))
    credit = pygame.image.load("credit.png").convert()
    regles = pygame.image.load("regles.png").convert()
    tutoriel = pygame.image.load("tutoriel.png").convert()
    tutoriel1 = pygame.image.load("tutoriel1.png").convert()
    son = pygame.mixer.music.load("chopin-waltz-op-64-no-2-rubinstein.wav")
    # permet de jauger la vitesse de notre future curseur
    pygame.key.set_repeat(5, 170)

    # rafraichit l'image, obligatoire pour afficher une interface
    pygame.display.flip()
    # variables
    continuer_jeu = 1
    continuer_acceuil = 1

    niveauName = ""
    interfaceName = 0
    choix = 0
    play = 0
    joue = 0
    while continuer_acceuil:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)
                # Permet d'accéder aux règles
                elif event.key == pygame.K_r:
                    continuer_acceuil = 0
                    choix = 2
                # Permet d'accéder au tutoriel
                elif event.key == pygame.K_t:
                    continuer_acceuil = 0
                    choix = 3
                # Permet d'accéder au jeu
                elif event.key == pygame.K_j:
                    continuer_acceuil = 0
                    choix = 4
                    niveauName = "t1"
                # Permet d'accèder au crédit
                elif event.key == pygame.K_c:
                    continuer_acceuil = 0
                    choix = 5

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and 500 < event.pos[1] < 600 and 300 < event.pos[0] < 450:
                    if play == 0:
                        pygame.mixer.music.play()
                        play = 1
                    else:
                        pygame.mixer.music.unpause()
                if event.button == 1 and 500 < event.pos[1] < 600 and 500 < event.pos[0] < 650:
                    pygame.mixer.music.pause()
                if event.button == 1 and 80 < event.pos[1] < 145 and 800 < event.pos[0] < 880:
                    if joue == 1:
                        pygame.mixer.music.set_volume(1)
                        page.blit(son_on, (800, 80))
                        pygame.display.flip()
                        joue = 0
                    elif joue == 0:
                        pygame.mixer.music.set_volume(0.0)
                        page.blit(son_off, (800, 80))
                        pygame.display.flip()
                        joue = 1


    pygame.display.flip()
    # Affiche la page des règles
    while choix == 2:

        page.blit(regles, (0, 0))

        pygame.display.flip()

        while choix:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        choix = 0
                if event.type == pygame.QUIT:
                    sys.exit(0)
    # Affiche les crédits
    while choix == 5:

        page.blit(credit, (0, 0))

        pygame.display.flip()
        while choix:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        choix = 0
                if event.type == pygame.QUIT :
                    sys.exit(0)
    # Affiche le tutoriel (1ère page)
    while choix == 3:
        page.blit(tutoriel, (0, 0))
        pygame.display.flip()
        while choix == 3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                # Permet d'accéder a la deuxième page du tutoriel
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        choix = 6
                    if event.key == pygame.K_ESCAPE:
                        choix = 0
    # affiche la deuxième page du tutoriel
    while choix == 6:
        page.blit(tutoriel1, (0, 0))
        pygame.display.flip()
        while choix == 6:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                # Permet d'accéder au  jeu avec le modéle du tutoriel choisi
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_2:
                        choix = 4
                        niveauName = "t2"
                    if event.key == pygame.K_1:
                        choix = 4
                        niveauName = "t3"
                    if event.key == pygame.K_3:
                        choix = 4
                        niveauName = "t4"
                    # retour au menue
                    if event.key == pygame.K_ESCAPE:
                        choix = 0
    # Affiche le jeu
    if choix == 4:
        # Résolution de l'interface
        interfaceName = pygame.display.set_mode(
            (nombre_sprite_cote * taille_sprite, nombre_sprite_cote * taille_sprite))
        # création du jeu
        niveau = Jeu(niveauName)
        niveau.generer()
        niveau.afficher(interfaceName)
        # création du curseur
        curseur = Joueur("lock.png", niveau)

        while continuer_jeu:
            # Limitation de vitesse de la boucle
            pygame.time.Clock().tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        continuer_jeu = 0
                    # déplacement curseur
                    elif event.key == pygame.K_RIGHT:
                        curseur.deplacer('droite')
                    elif event.key == pygame.K_LEFT:
                        curseur.deplacer('gauche')
                    elif event.key == pygame.K_UP:
                        curseur.deplacer('haut')
                    elif event.key == pygame.K_DOWN:
                        curseur.deplacer('bas')
                    # Permet de placer/enlever une case vide/pleine
                    elif event.key == pygame.K_o:
                        curseur.deposer()
                    # Lance les règles du jeu
                    elif event.key == pygame.K_s:
                        test = Joueur("lock.png", niveau)
                        test.regles()
                        test.redessinage()

            # affiche le niveau/curseur après modification
            niveau.afficher(interfaceName)
            interfaceName.blit(curseur.curseur, (curseur.x, curseur.y))
            pygame.display.flip()
