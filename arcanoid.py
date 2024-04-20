import pygame
import sys
import random
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Размеры блока
BLOCK_WIDTH = 50
BLOCK_HEIGHT = 20

# Список цветов для кирпичиков
BLOCK_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]


class Ball:
    def __init__(self):
        self.radius = 10
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.dx = 5
        self.dy = -5

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)


class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 20
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = SCREEN_HEIGHT - self.height - 10
        self.speed = 10

    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed

    def update_position(self, mouse_x):
        if mouse_x < self.width // 2:
            self.x = 0
        elif mouse_x > SCREEN_WIDTH - self.width // 2:
            self.x = SCREEN_WIDTH - self.width
        else:
            self.x = mouse_x - self.width // 2

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))


class Block:
    def __init__(self, x, y):
        self.width = BLOCK_WIDTH
        self.height = BLOCK_HEIGHT
        self.x = x
        self.y = y
        self.visible = True
        self.color = random.choice(BLOCK_COLORS)

    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


# Создание объектов
ball = Ball()
paddle = Paddle()
blocks = []
for row in range(5):
    for col in range(16):
        blocks.append(Block(col * (BLOCK_WIDTH + 5) + 30, row * (BLOCK_HEIGHT + 5) + 50))

# Инициализация экрана и часов
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simple Arkanoid')
clock = pygame.time.Clock()

# Главный цикл игры
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Обработка движения мыши
    mouse_x, _ = pygame.mouse.get_pos()
    paddle.update_position(mouse_x)

    screen.fill((0, 0, 0))

    ball.move()
    if ball.x <= ball.radius or ball.x >= SCREEN_WIDTH - ball.radius:
        ball.dx *= -1
    if ball.y <= ball.radius:
        ball.dy *= -1

    if ball.y >= SCREEN_HEIGHT - ball.radius:
        game_over = True

    if paddle.x < ball.x < paddle.x + paddle.width and paddle.y < ball.y < paddle.y + paddle.height:
        ball.dy *= -1

    for block in blocks:
        if block.visible and block.x < ball.x < block.x + BLOCK_WIDTH and block.y < ball.y < block.y + BLOCK_HEIGHT:
            block.visible = False
            ball.dy *= -1

    ball.draw(screen)
    paddle.draw(screen)

    for block in blocks:
        block.draw(screen)

    pygame.display.update()

    clock.tick(60)  # Устанавливаем 60 кадров в секунду

    if game_over:
        # После завершения игры предложим пользователю продолжить
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over. Press any key to continue...", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.update()

        # Ожидание нажатия любой клавиши для продолжения игры
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP:
                    blocks = [Block(col * (BLOCK_WIDTH + 5) + 30, row * (BLOCK_HEIGHT + 5) + 50) for row in range(5) for
                              col in range(16)]
                    ball = Ball()
                    game_over = False
                    wait = False