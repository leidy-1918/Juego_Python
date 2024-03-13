import pygame
import sys
import random
from bullet import Bullet  # Importa la clase Bullet desde el archivo bullet.py

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fuente para el texto
font = pygame.font.Font(None, 36)

# Función para mostrar menú
def show_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "play"
                elif event.key == pygame.K_2:
                    return "exit"

        screen.fill(BLACK)
        draw_text("Space Invaders", font, WHITE, screen, SCREEN_WIDTH // 2, 100)
        draw_text("1. Play", font, WHITE, screen, SCREEN_WIDTH // 2, 250)
        draw_text("2. Exit", font, WHITE, screen, SCREEN_WIDTH // 2, 300)
        pygame.display.flip()

# Función para dibujar texto en la pantalla
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Función para crear enemigos
def create_enemies(level):
    enemies = pygame.sprite.Group()
    for row in range(3):
        for col in range(8):
            enemy = Enemy(100 + col * 80, 50 + row * 60)
            enemies.add(enemy)
    return enemies

# Clase para el jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

# Clase para los enemigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1  # Reducir la velocidad de los enemigos a 1 píxel por fotograma

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)

# Función principal del juego
def main():
    while True:
        # Mostrar menú
        choice = show_menu()
        if choice == "play":
            run_game()
        elif choice == "exit":
            pygame.quit()
            sys.exit()

# Función para ejecutar el juego
def run_game():
    # Inicialización de variables
    player = Player()
    level = 1
    enemies = create_enemies(level)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(enemies)
    bullets = pygame.sprite.Group()  # Grupo para almacenar los disparos

    # Tiempo de juego en segundos
    play_time = 60  # Por ejemplo, 60 segundos

    # Puntaje inicial del jugador
    score = 0

    # Bucle principal del juego
    clock = pygame.time.Clock()  # Crear un objeto Clock para controlar la velocidad de fotogramas
    start_time = pygame.time.get_ticks()  # Obtener el tiempo de inicio del juego
    while True:
        # Limitar la velocidad de fotogramas
        clock.tick(60)  # Limitar a 60 fotogramas por segundo

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Disparar al presionar la tecla de espacio
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullets.add(bullet)
                    all_sprites.add(bullet)

        # Actualización de los sprites
        all_sprites.update()

        # Detección de colisiones entre los disparos y los enemigos
        for bullet in bullets:
            hits = pygame.sprite.spritecollide(bullet, enemies, True)
            for hit in hits:
                bullet.kill()
                # Incrementar el puntaje al destruir un enemigo
                score += 10

        # Detección de colisiones entre el jugador y los enemigos
        if pygame.sprite.spritecollide(player, enemies, True):
            # Aquí puedes manejar la colisión entre el jugador y los enemigos (por ejemplo, perder una vida)
            pass

        # Verificación de nivel completado
        if len(enemies) == 0:
            level += 1
            enemies = create_enemies(level)
            all_sprites.add(enemies)

        # Verificar si se ha agotado el tiempo de juego
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        remaining_time = max(play_time - elapsed_time, 0)
        if remaining_time == 0:
            # La partida ha terminado
            # Aquí puedes mostrar el puntaje final y cualquier otra acción de finalización del juego
            print("Tiempo agotado. Puntaje final:", score)
            pygame.quit()
            sys.exit()

        # Dibujado de la pantalla
        screen.fill(BLACK)
        all_sprites.draw(screen)
        # Mostrar el tiempo restante y el puntaje en la pantalla
        draw_text("Tiempo: " + str(remaining_time) + "s", font, WHITE, screen, 70, 20)
        draw_text("Puntaje: " + str(score), font, WHITE, screen, SCREEN_WIDTH - 100, 20)
        pygame.display.flip()

# Ejecución del juego
if __name__ == "__main__":
    main()

