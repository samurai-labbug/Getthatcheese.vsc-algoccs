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
        self.speed_boost = 0
        self.boost_timer = 0

    def update(self):
        keys = key.get_pressed()

        if self.speed_boost > 0:
            self.boost_timer -= 1
            if self.boost_timer <= 0:
                self.speed_boost = 0
        
        current_speed = self.speed + self.speed_boost
        if keys[K_d] and self.rect.x <= ANCHO - self.rect.w:
            self.image= self.derecha
            self.rect.x += current_speed
            
        elif keys[K_a] and self.rect.x >= 0:
            self.image= self.izquierda
            self.rect.x -= current_speed

        elif keys[K_s] and self.rect.y < ALTO - self.rect.h:
            self.image= self.original
            self.rect.y += current_speed

        elif keys[K_w] and self.rect.y > 0:
            self.image= self.arriba
            self.rect.y -= current_speed
            



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
        cord_x = randint(0,ANCHO- sprite_width)
        cord_y = randint(0,ALTO-sprite_height)
        super().__init__(sprite_img, cord_x, cord_y, sprite_width, sprite_height, 0)



# OBJETOS
inicio= transform.scale(image.load(INICIO_IMG),(ANCHO,ALTO))
background = transform.scale(image.load(BG_IMG), (ANCHO, ALTO))
player = Player(PLAYER_IMG, (ANCHO - 80) // 2, (ALTO - 100)//2, 70, 90, 5)
winner= transform.scale(image.load(WIN_IMG),(ANCHO,ALTO))
lose= transform.scale(image.load(LOSE_IMG),(ANCHO,ALTO))
font_1= font.Font(TEXT_FONT,30)

# trabajando con grupos:
all_sprites = sprite.Group()
enemies = sprite.Group()
items = sprite.Group()
cheeses = sprite.Group()

cheese_spawn_timer = 0  
enemy_spawn_timer = 0
item_spawn_timer = 0

#RESTART
def restart_game():
    global player,all_sprites,enemies, items, cheeses
    global points, lives, has_cheese,cheese_spawn_timer, enemy_spawn_timer, item_spawn_timer, finish

    all_sprites.empty()
    enemies.empty()
    items.empty()
    cheeses.empty()

    player = Player(PLAYER_IMG, (ANCHO - 80) // 2, (ALTO - 100)//2, 70, 90, 5)

    points=0
    lives=3
    cheese_spawn_timer=0
    enemy_spawn_timer=0
    item_spawn_timer=0
    has_cheese = False
    finish= False

# CICLO DE JUEGO
run = True
finish = False # ESTADO DE JUEGO
clock = time.Clock()
game_started = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False # bandera de estado
        if e.type == KEYDOWN:
            if e.key == K_r:
                restart_game()
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                game_started= True
        

    
        
    if not game_started:
        screen.blit(inicio, (0, 0))
        titulo = font.Font(None, 72).render("¡PRESIONA ESPACIO!", True, WHITE)
        instrucciones = font_1.render("para comenzar el juego", True, WHITE)
        
        screen.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//2 - 300))
        screen.blit(instrucciones, (ANCHO//2 - instrucciones.get_width()//2, ALTO//2 - 240))
        
        display.update()
        clock.tick(FPS)
        continue

    if not finish:
        screen.fill(BLACK)
        screen.blit(background, (0, 0))
        enemy_spawn_timer += 1
        item_spawn_timer += 1
        cheese_spawn_timer += 1

        if enemy_spawn_timer > ENEMY_SPAWN_RATE:
            new_enemy = Enemy(ENEMY_IMG, 80, 60, 3)
            all_sprites.add(new_enemy)
            enemies.add(new_enemy)
            enemy_spawn_timer = 0

        if item_spawn_timer > ITEM_SPAWN_RATE:
            new_item = Items(ITEM_IMG, 40, 40, 2)  
            all_sprites.add(new_item)
            items.add(new_item)
            item_spawn_timer = 0

        if cheese_spawn_timer > CHEESE_SPAWN_RATE and len(cheeses) == 0:
            new_cheese = Queso(CHEESE_IMG, 30, 30)
            all_sprites.add(new_cheese)
            cheeses.add(new_cheese)
            cheese_spawn_timer = 0

        for enemy in enemies:
            if sprite.collide_rect(player, enemy):
                enemy.kill()
                enemies.remove(enemy)
                all_sprites.remove(enemy)
                lives-=1


        for item in items:
            if sprite.collide_rect(player, item):
                player.speed_boost = item.bonus
                player.boost_timer = 180
                item.kill()
                items.remove(item)
                all_sprites.remove(item)
                lives+=1


        for cheese in cheeses:
            if sprite.collide_rect(player, cheese):
                cheese.kill()
                cheeses.remove(cheese)
                all_sprites.remove(cheese)
                has_cheese = True
                points+=1

        player.reset()
        player.update()
                
        all_sprites.update()
        all_sprites.draw(screen)

        puntaje_text= font_1.render(f'CHEESE {points}/20', 1 , WHITE)
        puntaje_vidas= font_1.render(f'Vidas= {lives}', 1 , (170,220,180))

        screen.blit(puntaje_vidas,(ANCHO-140,20))
        screen.blit(puntaje_text,(20,20))

        para_downs= font_1.render(f'PRESIONE R PARA REINICIAR', 1 , WHITE)


        if points==1:
            finish = True
            screen.fill(BLACK)
            screen.blit(winner,(0,0))
            screen.blit(para_downs,((ANCHO/2)-155,ALTO-100))

        if lives==0:
            finish = True
            screen.fill(BLACK)
            screen.blit(lose,(0,0))
            screen.blit(para_downs,(ANCHO/2,20))





    # NO TOCAR
    display.update()
    clock.tick(FPS)

quit()
