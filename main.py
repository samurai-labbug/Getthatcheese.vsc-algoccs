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
    def __init__(self, sprite_img, cord_x, cord_y, width, height, speed):
        super().__init__(sprite_img, cord_x, cord_y, width, height, speed)

        self.original= self.image
        self.derecha= transform.rotate(self.original,90)
        self.arriba= transform.rotate(self.original,180)
        self.izquierda= transform.rotate(self.original,270)
        

    def update(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x <= ANCHO - self.rect.w:
            self.image= self.derecha
            self.rect.x += self.speed
            
        elif keys[K_a] and self.rect.x >= 0:
            self.image= self.izquierda
            self.rect.x -= self.speed

        elif keys[K_s] and self.rect.y < ALTO - self.rect.h:
            self.image= self.original
            self.rect.y += self.speed

        elif keys[K_w] and self.rect.y > 0:
            self.image= self.arriba
            self.rect.y -= self.speed
            



class Enemy(GameSprite):
    def __init__(self, sprite_img, width, height, speed):
        
        direction = choice(['left', 'right', 'top', 'bottom'])
        
        if direction == 'left':
            x = -width
            y = randint(0, ALTO - height)
            self.dx = speed  
            self.dy = 0
        elif direction == 'right':
            x = ANCHO
            y = randint(0, ALTO - height)
            self.dx = -speed  
            self.dy = 0
        elif direction == 'top':
            x = randint(0, ANCHO - width)
            y = -height
            self.dx = 0
            self.dy = speed 
        else:  # bottom
            x = randint(0, ANCHO - width)
            y = ALTO
            self.dx = 0
            self.dy = -speed  
            
        super().__init__(sprite_img, x, y, width, height, speed)
        self.direction = direction
        self.dx, self.dy = self.dx, self.dy

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        if self.direction == 'left' and self.rect.x > ANCHO:
            self.kill()
        elif self.direction == 'right' and self.rect.x < -self.width:
            self.kill()
        elif self.direction == 'top' and self.rect.y > ALTO:
            self.kill()
        elif self.direction == 'bottom' and self.rect.y < -self.height:
            self.kill()


    

class Items(GameSprite):
    def __init__(self, sprite_img, sprite_width, sprite_height, bonus):
        cord_x = randint(0, ANCHO - sprite_width)
        cord_y = randint(0, ALTO - sprite_height)
        super().__init__(sprite_img, cord_x, cord_y, sprite_width, sprite_height, 0)
        self.bonus = bonus
        self.lifetime = 300  
        self.age = 0

    def update(self):
        self.age += 1
        if self.age > self.lifetime:
            self.kill()

class Queso(GameSprite):
    def __init__(self, sprite_img, sprite_width, sprite_height):
         
        cord_x = randint(0,ANCHO- sprite_height)
        cord_y = randint(0,ALTO-sprite_width)
        super().__init__(sprite_img, cord_x, cord_y, sprite_width, sprite_height, 0)

# OBJETOS
background = transform.scale(image.load(BG_IMG), (ANCHO, ALTO))
player = Player(PLAYER_IMG, (ANCHO - 80) // 2, ALTO - 70, 70, 90, 5)


# trabajando con grupos:
all_sprites = sprite.Group()
enemies = sprite.Group()
items = sprite.Group()


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
        enemy_spawn_timer += 1
        item_spawn_timer += 1

        if enemy_spawn_timer > ENEMY_SPAWN_RATE:
            new_enemy = Enemy(ENEMY_IMG, 80, 60, 3)
            all_sprites.add(new_enemy)
            enemies.add(new_enemy)
            enemy_spawn_timer = 0

        if item_spawn_timer > ITEM_SPAWN_RATE:
            new_item = Items(ITEM_IMG, 40, 40, 10)  
            all_sprites.add(new_item)
            items.add(new_item)
            item_spawn_timer = 0

        player.reset()
        player.update()
        
        all_sprites.update()
        all_sprites.draw(screen)
        



        # CONDICION VICTORIA
        # if victoria:
        #     finish = True
        #     screen.fill(BLACK)
        # CONDICION DERROTA



    # NO TOCAR
    display.update()
    clock.tick(FPS)

quit()
