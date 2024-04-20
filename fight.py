import pygame
import random

# Инициализация библиотеки Pygame
pygame.init()

# Определение констант
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ENEMY_SIZE = 20
PLAYER_SIZE = 20
WHITE = (255, 255, 255)
RED = (255, 0, 0)
SCORE_FONT_SIZE = 36

# Создание класса для игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.player_vertical_pos = 500  # Переменная для установления позиции игрока на экране

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.centerx = mouse_pos[0]  # Перемещение игрока только по горизонтали
        self.rect.centery = self.player_vertical_pos  # Фиксированное вертикальное положение игрока

# Создание класса для врага - круга
class EnemyCircle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)

# Создание класса для врага - треугольника
class EnemyTriangle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        pygame.draw.polygon(self.image, RED, [(0, ENEMY_SIZE), (ENEMY_SIZE // 2, 0), (ENEMY_SIZE, ENEMY_SIZE)])
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)

# Создание класса для врага - квадрата
class EnemySquare(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Survival Game')

# Создание спрайтов
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Инициализация скорости и счетчика столкновений
game_speed = 5.0
collisions_count = 0

# Создание шрифта для отображения сообщения
font = pygame.font.SysFont(None, SCORE_FONT_SIZE)

# Функция для добавления врагов разных типов
def add_enemy():
    enemy_type = random.choice([EnemyCircle, EnemyTriangle, EnemySquare])
    enemy = enemy_type(game_speed)
    all_sprites.add(enemy)
    enemies.add(enemy)

# Функция для отрисовки врагов разных типов
def draw_enemies():
    for enemy in enemies:
        if isinstance(enemy, EnemyCircle):
            pygame.draw.circle(screen, RED, enemy.rect.center, ENEMY_SIZE // 2)
        elif isinstance(enemy, EnemyTriangle):
            pygame.draw.polygon(screen, RED, [(enemy.rect.centerx, enemy.rect.top),
                                              (enemy.rect.right, enemy.rect.bottom),
                                              (enemy.rect.left, enemy.rect.bottom)])
        elif isinstance(enemy, EnemySquare):
            screen.blit(enemy.image, enemy.rect)

# Основной игровой цикл
running = True
clock = pygame.time.Clock()
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Добавление врагов
    if len(enemies) < 10:
        add_enemy()

    # Обновление всех спрайтов
    all_sprites.update()

    # Проверка на столкновение игрока с врагом
    collisions = pygame.sprite.spritecollide(player, enemies, True)
    if collisions:
        collisions_count += 1
        if collisions_count % 5 == 0:  # Новый враг добавляется каждый раз, когда игрок столкнулся с 5 врагами
            add_enemy()
            game_speed += 1
            collisions_count = 0

    # Отображение количества столкновений и скорости игры на экране
    text = font.render(f'Collisions: {collisions_count}  Speed: {game_speed}', True, WHITE)
    screen.blit(text, (10, 10))

    draw_enemies()

    pygame.draw.rect(screen, WHITE, player.rect)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()