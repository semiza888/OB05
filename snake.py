import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 10

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Класс для отрисовки и управления змейкой
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = 'right'

    def move(self):
        head = self.body[0]
        x, y = head

        if self.direction == 'up':
            y -= 1
        elif self.direction == 'down':
            y += 1
        elif self.direction == 'left':
            x -= 1
        elif self.direction == 'right':
            x += 1

        # Проверка на столкновение с границами
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            # Изменяем направление движения
            if self.direction == 'up':
                self.direction = 'down'
            elif self.direction == 'down':
                self.direction = 'up'
            elif self.direction == 'left':
                self.direction = 'right'
            elif self.direction == 'right':
                self.direction = 'left'

            # Возвращаем координаты в пределы игрового поля
            x = max(0, min(x, GRID_WIDTH - 1))
            y = max(0, min(y, GRID_HEIGHT - 1))

        self.body.insert(0, (x, y))

        if self.body[0] == food.position:
            food.spawn()
        else:
            self.body.pop()

    def draw(self, screen):
        for segment in self.body:
            x, y = segment
            pygame.draw.rect(screen, GREEN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Класс для еды
class Food:
    def __init__(self):
        self.position = (random.randint(1, GRID_WIDTH - 1), random.randint(1, GRID_HEIGHT - 1))

    def spawn(self):
        self.position = (random.randint(1, GRID_WIDTH - 1), random.randint(1, GRID_HEIGHT - 1))

    def draw(self, screen):
        x, y = self.position
        pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Инициализация окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

snake = Snake()
food = Food()

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Обработка движения змейки
    snake.move()

    # Обработка движения мыши
    mouse_x, mouse_y = pygame.mouse.get_pos()
    snake_head_x, snake_head_y = snake.body[0]

    dx = mouse_x // CELL_SIZE - snake_head_x
    dy = mouse_y // CELL_SIZE - snake_head_y

    if abs(dx) > abs(dy):
        if dx > 0 and snake.direction != 'left':
            snake.direction = 'right'
        elif dx < 0 and snake.direction != 'right':
            snake.direction = 'left'
    else:
        if dy > 0 and snake.direction != 'up':
            snake.direction = 'down'
        elif dy < 0 and snake.direction != 'down':
            snake.direction = 'up'

    if snake.body[0] == food.position:
        food.spawn()
        snake.body.append(snake.body[-1])  # Увеличиваем длину змейки

    screen.fill(BLACK)
    snake.draw(screen)
    food.draw(screen)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()