from pygame import *
from config import *
from random import *
init()

# FUNCIONALIDAD

# TRABAJO CON FUENTES
font.init()


# MAIN WINDOW
screen = display.set_mode((ANCHO, ALTO))
display.set_caption(TITULO)

# CLASE PRINCIPAL
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, cord_x, cord_y, width, height, speed=0):
        super().__init__()
        self.width = width
        self.height = height
        self.image = transform.scale(image.load(sprite_img), (self.width, self.height))
        # Creamos una superficie para la imagen
        self.rect = self.image.get_rect()
        self.rect.x = cord_x
        self.rect.y = cord_y
        self.speed = speed

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x <= ANCHO - self.rect.w:
            self.rect.x += self.speed
        elif keys[K_a] and self.rect.x >= 0:
            self.rect.x -= self.speed


class Enemy(GameSprite):
    pass


# OBJETOS
background = transform.scale(image.load(BG_IMG), (ANCHO, ALTO))

player = Player(PLAYER_IMG, (ANCHO - 80) // 2, ALTO - 70, 80, 60, 5)
# trabajando con grupos:


# CICLO DE JUEGO
run = True
finish = False # ESTADO DE JUEGO
clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False # bandera de estado
        if e.type == KEYDOWN:
            if e.key == K_r:
                finish = False

    if not finish:
        screen.blit(background, (0, 0))
        player.reset()
        player.update()
            
        # CONDICION VICTORIA
        # if victoria:
        #     finish = True
        #     screen.fill(BLACK)
        # CONDICION DERROTA



    # NO TOCAR
    display.update()
    clock.tick(FPS)

quit()
