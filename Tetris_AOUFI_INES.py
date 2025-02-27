# Importation de toutes les librairies
import tkinter as tk
import numpy as np
import time
import random
from PIL import Image,ImageTk

# Je vais ensuite créer les différentes classes pour les différentes parties du jeu :
# 1) La classe du jeu en lui même où il y a par exemple toutes les initialisations du jeu et de la boucle principale
# 2) La classe tétromino parent "tetromino"
# 3) Une classe par tétromino (L, J, T, S, Z, I, O) pour que les données de chaque soit plus accessible

class game_board():
    '''
    game_board est la classe du jeu, où il y a basiquement toutes les actions.
    Premièrement je crée donc la matrice du jeu :
    Je dis que les "0" sont les emplacements libres, les "0,5" sont les murs et les tetros inactifs placés dans le jeu et les "1" sont les tetros en cours de jeu. 
    Tout cela donne un affichage très simple et minimaliste avec des 0 en noir, des 0.5 en gris et 1 en blanc. J'aurais pu assez facilement le mettre en couleur en changeant le 0.5 en nombre qui correspondent à un RGB, mais la ligne 83 est compliquée à utiliser et j'ai eu déjà beacoup de mal à le faire en noir et blanc, donc je n'ai pas voulu perdre plus de temps pour quelques couleurs. 
    Un jeu de tétris est un tableau de 10x20, en comptant les murs et le sol cela fait 12x21, je crée cependant un tableau de 12x23 car je veux laisser un emplacement au dessus du tetris qu'on voit pour faire apparaitre les pièce petit à petit.
    '''
    def __init__(self):
        self.board_dim = (23,12) # Définition des dimentions de la matrice
        self.tetris_array = np.zeros(self.board_dim) # Création de la matrice vide
        self.tetris_array[:,[0,-1]] = self.tetris_array[[0,-1]] = 0.5 # Définition des bords avec des 0.5
        self.tetris_array[0,1:11] = 0 # Puisque la ligne d'avant mettait tous les bords à 0.5, il faut que je fasse une ouverture pour le plafond
        self.piece_now = None # Initialisation de la pièce actuelle du jeu, en disant qu'il n'y a rien dedans pour que le jeu réagisse et en fasse apparaître une autre si le jeu est encore en cours
        self.game_state = True # Initialisation de l'état du jeu comme etant VRAI pour que le jeu se lance correctement la première fois
        
        self.root = tk.Tk() # Initialisation du self.root pour utiliser tkinter
        self.root.title('Tetris') # Je mets un titre à la fenêtre
        self.w = 300 # Initialisation de la dimension de la fenêtre pour qu'elle soit simplement modifiable 
        self.h = 525 # Je trouve la largeur(Width) et la hauteur(Height) exacte de l'affichage en prenant 12 ou 21*25(que j'ai défini ligne 82 dans la fonction update)
        self.canvas = tk.Canvas(self.root,width=self.w,height=self.h) # Création du canvas
        self.canvas.grid(row=0,column=0) # Je le place en fonction d'une grid en 0,0, j'aurais pu pack() mais ça aurait été plus compliqué pour organiser d'autres éléments autour

        self.root.resizable(width=False, height=False) # J'empêche la modification de la taille de la fenêtre
        self.root.after(1,self.clear_line) # Je lance toutes les fonctions du jeu
        self.root.after(1,self.game_play)
        self.root.after(1,self.update)
        self.root.mainloop() # Je lance la loop pour que le jeu reste en continu

    def clear_line(self):
        '''
        Cette fonction fait disaparaitre les lignes quand elles sont pleines.
        '''
        for i in range(self.tetris_array.shape[0]-1): # Je check pour toutes les lignes du tableau (en excluant les lignes)
            if np.all(self.tetris_array[i]==self.tetris_array[i][0]): # si tous les éléments de la ligne sont égaux
                self.tetris_array[i,1:11]= 0 # Je remplace donc la ligne i par 0
                self.tetris_array[1:i+1] = self.tetris_array[0:i] # et je décale tout ce qui est au dessus d'un cran en dessous

        self.root.after(1,self.update) # Je lanche update à chaque fin de fonction pour qu'il soit appelé dès qu'une action est fini pour qu'on voit toutes les actions instantanément
            
    def game_play(self):
        '''
        Cette fonction est celle du jeu principal, elle check si le jeu n'est pas perdu et fait apparaître des tetros dès qu'elle est posée
        '''
        if self.game_state: # Si le jeu est en cours
            for y in range(0,2): # si sur les 2 premières lignes (celles invisible par le joueur)
                for x in range(1,11): # un des élement (sans compter les murs bien sûr)
                    if self.tetris_array[y, x] == 0.5: # est égal à 0.5 (donc une pièce est posée)
                        self.game_state = False # le jeu est perdu

            if not self.piece_now: # S'il n'y a pas de pièce dans le jeu (alors que le jeu est lancé)
                self.piece_now = random.choice([tetro_I,tetro_O,tetro_L,tetro_J,tetro_Z,tetro_S,tetro_T]) # Je choisis une des pièces aléatoirement
                self.piece_now = self.piece_now(self) # et je l'apelle pour qu'elle se apparaisse
            self.piece_now.auto_move() # puis j'active le mouvement automatique vertical

            self.clear_line() # Je lance ensuite toutes les fonctions pour qu'elles soient toujours réactives
            self.root.after(1,self.update)
            self.root.after(1000,self.game_play) # Je lance ça toutes les secondes pour que le tetro décende à cet intervalle

        else: # Si le jeu est perdu/arreté 
            self.end = tk.Label(self.root,text="Game Over",bg='white',foreground='black') # J'affiche Game Over sur l'écran
            self.end.grid(row=0,column=0,) # Je le place au meme endroit que le tetris pour qu'il s'affiche au milieu
            print("Jeu perdu ! Redémarrez le pour recommencer.") # Je print que le jeu est perdu
            # Je n'ai pas de manière de relancer le jeu si on appuie sur un bouton, j'ai essayé mais tkinter esttrès compliqué à utiliser
        
    def update(self):
        '''
        Cette fonction sert à afficher le jeu, je transforme directement la matrice en image que j'affiche ensuite dans tkinter.
        '''
        self.tetris_array_display = np.kron(self.tetris_array[2:23,:],np.ones((25,25))) # J'utilise une fonction qui sert à agrandir la matrice, je multiplie donc chaque coté par 25 pour que ça reste proportionnel
        self.image_tetris = ImageTk.PhotoImage(Image.fromarray((self.tetris_array_display*255).astype('uint8'),mode='L')) # J'utilise une fonction qui transforme un array en image noir et blanc grâce à Pillow
        self.canvas.create_image(0,0,anchor='nw',image=self.image_tetris) # J'affiche ensuite l'image dans le canvas

class tetromino(game_board):
    '''
    La classe tétromino : un tétromino est une pièce de jeu de Tetris, dans cette classe je vais initialiser toutes les données pour les tetros et toutes les fonctions qui vont avec, c'est à dire :
    -Mouvement vertical automatique du tetro,
    -Tous les mouvements (gauche, droite, bas)
    -Toutes les rotations (horaire, anti-horaire)

    J'initialise cette classe (dans __init__) avec "self" et avec la classe du jeu que j'appelle "game" pour pouvoir échanger les données avec elle.

    "origin" et "pos" :
    Pour chaque pièce j'aurais deux données principale : l'origine et les coordonnées des 'briques' des tetros.
    Pour construire mon tetro je prends une origine par rapport à la matrice du jeu, c'est à dire où sera la pièce, ici 1,5 au début (ce qui correspond à 5,-1 si on dit que l'origine de l'axe est au coin haut-gauche) et je crée ma pièce autour de cela brique par brique.
    Chaque tetro possède 4 briques, et chacune de ces briques a donc une coordonnée par rapport à l'origine, pour le carré ça donnera donc : (0,0),(0,1),(-1,0),(-1,1), donc à chaque fois pour avoir les coordonnées de chaque brique sur la matrice du jeu, on fait origine + coordonnée.

    "offset" :
    L'offset ou décalage correspond au décalage que la pièce doit subir en fonction de sa rotation. A la base cela ne s'applique que pour le O et le I, mais il peut s'appliquer sur les autres dans certaines situations que je n'ai pas fait ici.

    J'aurais également pu rajouter ce qu'on appelle des "wall kick" mais c'était une liste énorme de if..else que je n'arrivais pas à mettre en place.
    Cette action permet de tourner les pièces quand elles sont contre les murs, car de base la pièce serait compté comme étant dans le mur si on essaiyait de la tourner et on le la laisserait donc pas faire cette action.
    '''
    def __init__(self, game):
        self.game = game
        self.origin = np.array([1,5]) # Initialisation de l'origine
        self.rotation = 0 # Initialisation de la rotation : il y a 4 positions de rotation différentes 0:rotation de base 1: une rotation horaire 2: deux rotations horaire ou anti-horaire 3: une rotation anti-horaire
        self.offset = np.array([[0,0],[0,0],[0,0],[0,0]]) # Initialisation de l'offset à 0 car toutes les pièces n'ont pas d'offset
        self.game.root.bind("<Left>", self.left)   # Je lie chaque action à une touche
        self.game.root.bind("<Right>", self.right)
        self.game.root.bind("<Down>", self.down)   
        self.game.root.bind("<x>", self.clockrot)        # "clockrot" pour clockwise rotation, ou rotation horaire
        self.game.root.bind("<w>", self.counterclockrot) # "counterclockrot" pour couterclockwise rotation, ou rotation anti-horaire
    
    def auto_move(self):
        '''
        "auto_move" correspond au mouvement vertical automatique des tetros.
        '''
        next_pos = self.pos+(self.origin+np.array([1,0])) # Je dis que la prochaine position potentiel est l'ancienne position "self.pos" + l'origine + (1,0) ce qui bouge la pièce d'un cran vers le bas

        if self.game.game_state: # Je vérifie toujours si le "game_state" = TRUE car c'est ce qui me dit si le jeu est toujours en cours.
            if 0.5 not in [self.game.tetris_array[y, x] for y, x in next_pos]: # Je vérifie si il n'y a pas un "0.5" (mur/tetro posé) dans la prochaine position dans la matrice tetris
                for y, x in self.pos + self.origin: # Pour la position précedente 
                    self.game.tetris_array[y, x] = 0 # Je supprime la pièce
                for y, x in next_pos: # Pour la prochaine position 
                    self.game.tetris_array[y, x] = 1 # Je créer la pièce
                self.origin += np.array([1,0]) # Puis je change l'orine, je la baisse de un pour qu'il capte qu'il ai bougé

            else: # S'il y a un "0.5" puisque c'est vertical, si la pièce touche une autre pièce par en dessous, la pièce devient inactive
                for y, x in self.pos + self.origin: # donc pour l'emplacement du tetro actuel
                    self.game.tetris_array[y, x] = 0.5 # je remplace tout par 0.5
                self.game.piece_now = None # et je dis qu'il n'y a plus de piece actuelle
            
    def left(self,event): # Pour que la fonction capte que la touche est appuyée je dois mettre "event"
        '''
        Toutes les fonctions de mouvement marchent quasiment pareil en théorie, sauf qu'elles ne serot pas directement désactivée puisque c'est uniquement si c'est touché par en bas que la pièce ne peux plus être controlée
        '''
        next_pos = self.pos+(self.origin+np.array([0,-1])) # Je décris la prochaine position potentiel comme l'ancienne mais en la décalant à gauche

        if self.game.game_state:
            if 0.5 not in [self.game.tetris_array[y, x] for y, x in next_pos]: # Même fonctionnement que précedemment
                for y, x in self.pos + self.origin:
                    self.game.tetris_array[y, x] = 0
                for y, x in next_pos:
                    self.game.tetris_array[y, x] = 1
                self.origin += np.array([0,-1])
        # Il n'y a pas de Else car si on ne peut pas déplacer le tetro on ne fait rien
        self.game.root.after(1,self.game.update) # Je lance toujours game.update à chaque action pour rafraichir l'affichage 
            
    def right(self,event):
        next_pos = self.pos+(self.origin+np.array([0,1]))
        
        if self.game.game_state:
            if 0.5 not in [self.game.tetris_array[y, x] for y, x in next_pos]:
                for y, x in self.pos + self.origin:
                    self.game.tetris_array[y, x] = 0
                for y, x in next_pos:
                    self.game.tetris_array[y, x] = 1
                self.origin += np.array([0,1])
        self.game.root.after(1,self.game.update)
            
    def down(self,event):
        next_pos = self.pos+(self.origin+np.array([1,0]))
        
        if self.game.game_state:
            if 0.5 not in [self.game.tetris_array[y, x] for y, x in next_pos]:
                for y, x in self.pos + self.origin:
                    self.game.tetris_array[y, x] = 0
                for y, x in next_pos:
                    self.game.tetris_array[y, x] = 1
                self.origin += np.array([1,0])

            else: # Ici il y a un else car on peut désactiver la pièce par en dessous comme expliqué plus tôt.
                for y, x in self.pos + self.origin:
                    self.game.tetris_array[y, x] = 0.5
                self.game.piece_now = None
        self.game.root.after(1,self.game.update)

    def clockrot(self,event):
        '''
        Cette fonction s'occupe des rotations horaires.
        '''
        clockwise = np.array([[0,1],[-1,0]]) # Je créer la matrice de rotation horaire
        next_coord = np.array([[0,0],[0,0],[0,0],[0,0]]) # Je creer une matrice vide de la position potentielle après la rotation pour pouvoir la modifier facilement plus tard
        
        if self.game.game_state:
            self.rotation = (self.rotation + 1) % 4 # J'ajoute 1 à la rotation en faisant en sorte qu'elle reste entre 0 et 3, car j'utiliserais le numéro de rotation plus tard pour l'offset par exemple
            
            # J'utilise la matrice de rotation pour faire tourner la pièce en fonction de son origine
            # Ce calcul pourrait être simplifié mais je préferais laisser pour bien voir le calcul théorique
            next_coord[0,0] = self.pos[0,0]*clockwise[0,0]+self.pos[0,1]*clockwise[0,1]
            next_coord[0,1] = self.pos[0,0]*clockwise[1,0]+self.pos[0,1]*clockwise[1,1]

            next_coord[1,0] = self.pos[1,0]*clockwise[0,0]+self.pos[1,1]*clockwise[0,1]
            next_coord[1,1] = self.pos[1,0]*clockwise[1,0]+self.pos[1,1]*clockwise[1,1]

            next_coord[2,0] = self.pos[2,0]*clockwise[0,0]+self.pos[2,1]*clockwise[0,1]
            next_coord[2,1] = self.pos[2,0]*clockwise[1,0]+self.pos[2,1]*clockwise[1,1]

            next_coord[3,0] = self.pos[3,0]*clockwise[0,0]+self.pos[3,1]*clockwise[0,1]
            next_coord[3,1] = self.pos[3,0]*clockwise[1,0]+self.pos[3,1]*clockwise[1,1]

            next_pos = next_coord + self.origin + self.offset[self.rotation] # Je définis donc la prochaine position potentielle en l'ajoutant à l'origine et l'offset en fonction d'à quel rotation il est (pour que le tetro O ne se décale pas par exemple)

            if 0.5 not in [self.game.tetris_array[y, x] for y, x in next_pos]: # Même fonctionnement pour voir s'il y a de la place où on veut se déplacer
                for y, x in self.pos + self.origin:
                    self.game.tetris_array[y, x] = 0
                for y, x in next_pos:
                    self.game.tetris_array[y, x] = 1
                self.origin += self.offset[self.rotation] # Je décale l'origine de l'offset que j'ai ajouté pour que la pièce entière se décale, au lieu de décaler chaque brique de tetro
                self.pos = next_coord # Ici je change la position du tetromino en elle meme aussi car il change complètement et ne se décale pas uniquement grâce à l'origine comme on le faisait précedemment

        self.game.root.after(1,self.game.update)

    def counterclockrot(self,event):
        '''
        Cette fonction marche exactement comme celle d'avant mais avec une matrice de rotation pour une rotation anti-horaire
        '''
        counter = np.array([[0,-1],[1,0]])
        next_coord = np.array([[0,0],[0,0],[0,0],[0,0]])
        
        if self.game.game_state:
            self.rotation = (self.rotation + 4 - 1) % 4

            next_coord[0,0] = self.pos[0,0]*counter[0,0]+self.pos[0,1]*counter[0,1]
            next_coord[0,1] = self.pos[0,0]*counter[1,0]+self.pos[0,1]*counter[1,1]
            
            next_coord[1,0] = self.pos[1,0]*counter[0,0]+self.pos[1,1]*counter[0,1]
            next_coord[1,1] = self.pos[1,0]*counter[1,0]+self.pos[1,1]*counter[1,1]
            
            next_coord[2,0] = self.pos[2,0]*counter[0,0]+self.pos[2,1]*counter[0,1]
            next_coord[2,1] = self.pos[2,0]*counter[1,0]+self.pos[2,1]*counter[1,1]

            next_coord[3,0] = self.pos[3,0]*counter[0,0]+self.pos[3,1]*counter[0,1]
            next_coord[3,1] = self.pos[3,0]*counter[1,0]+self.pos[3,1]*counter[1,1]
            
            next_pos = next_coord + self.origin + self.offset[self.rotation-1]

            if 0.5 not in [self.game.tetris_array[y, x] for y, x in next_pos]:
                for y, x in self.pos + self.origin:
                    self.game.tetris_array[y, x] = 0
                for y, x in next_pos:
                    self.game.tetris_array[y, x] = 1
                self.origin += self.offset[self.rotation-1]
        
                self.pos = next_coord

        self.game.root.after(1,self.game.update)

class tetro_O(tetromino):
    '''
    Je créer une classe par tétromino en leur donnant Tetromino en parent pour qu'ils échangent toutes les données.
    '''
    def __init__(self, game):
        super(tetro_O, self).__init__(game)
        self.pos = np.array([[0,0],[0,1],[-1,0],[-1,1]]) # Initialisation des positions de chaque brique
        self.rotation = 0 # Initialisation de la rotation à la position de base
        self.offset = np.array([[0,-1],[-1,0],[0,1],[1,0]]) # Je définis l'offset pour ceux qui en ont besoin

class tetro_I(tetromino):
    def __init__(self, game):
        super(tetro_I, self).__init__(game)
        self.pos = np.array([[0,-1],[0,0],[0,1],[0,2]])
        self.rotation = 0
        self.offset = np.array([[-1,0],[0,1],[1,0],[0,-1]])

class tetro_L(tetromino):
    def __init__(self, game):
        super(tetro_L, self).__init__(game)
        self.pos = np.array([[0,-1],[0,0],[0,1],[-1,1]])
        self.rotation = 0

class tetro_Z(tetromino):
    def __init__(self, game):
        super(tetro_Z, self).__init__(game)
        self.pos = np.array([[-1,-1],[-1,0],[0,0],[0,1]])
        self.rotation = 0

class tetro_S(tetromino):
    def __init__(self, game):
        super(tetro_S, self).__init__(game)
        self.pos = np.array([[0,-1],[0,0],[-1,0],[-1,1]])
        self.rotation = 0

class tetro_J(tetromino):
    def __init__(self, game):
        super(tetro_J, self).__init__(game)
        self.pos = np.array([[-1,-1],[0,-1],[0,0],[0,1]])
        self.rotation = 0

class tetro_T(tetromino):
    def __init__(self, game):
        super(tetro_T, self).__init__(game)
        self.pos = np.array([[-1,0],[0,-1],[0,0],[0,1]])
        self.rotation = 0

start = game_board() # Je créer donc une instance du jeu en l'appelant "start"
start.game_play() # Je lance le jeu.

# Le jeu a toutes les bases nécessaire pour jouer, j'arais cependant pu rajouter les points, les prochaines pièces qui apparaitront dans un coin, ou un bouton pour recommencer le jeu quand on perd.
# Il a cependant encore quelques bugs parfois mais très rarement.