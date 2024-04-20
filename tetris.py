import pygame
import random

# Определение цветов
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Определение размеров окна и блоков
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 600
BLOCK_SIZE = 30

# Определение фигур
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],
]


class TetrisBlock:
    def __init__(self, color):
        self.color = color

    def draw(self, surface, x, y):
        pygame.draw.rect(surface, self.color, (x, y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(surface, BLACK, (x, y, BLOCK_SIZE, BLOCK_SIZE), 3)


class TetrisGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[None] * (WINDOW_WIDTH // BLOCK_SIZE) for _ in range(WINDOW_HEIGHT // BLOCK_SIZE)]
        self.current_block = self.new_block()
        self.current_x = 0
        self.current_y = 0
        self.fall_time = 0
        self.score = 0

    def new_block(self):
        shape = random.choice(tetris_shapes)
        color = random.choice([CYAN, MAGENTA, YELLOW, GREEN, RED, BLUE])
        return TetrisBlock(color), shape

    def draw_grid(self):
        for y in range(WINDOW_HEIGHT // BLOCK_SIZE):
            for x in range(WINDOW_WIDTH // BLOCK_SIZE):
                block = self.grid[y][x]
                if block:
                    block.draw(self.screen, x * BLOCK_SIZE, y * BLOCK_SIZE)

    def draw_current_block(self):
        for y, row in enumerate(self.current_block[1]):
            for x, col in enumerate(row):
                if col:
                    self.current_block[0].draw(self.screen, (x + self.current_x) * BLOCK_SIZE,
                                               (y + self.current_y) * BLOCK_SIZE)

    def move_down(self):
        self.current_y += 1
        if self.check_collision():
            self.current_y -= 1
            self.add_to_grid()
            self.remove_completed_lines()
            self.current_block = self.new_block()
            self.current_x = 0
            self.current_y = 0

    def move_sideways(self, dx):
        new_x = self.current_x + dx
        if 0 <= new_x <= WINDOW_WIDTH // BLOCK_SIZE - len(self.current_block[1][0]):
            self.current_x = new_x
            if self.check_collision():
                self.current_x -= dx

    def rotate(self):
        self.current_block = self.current_block[0], [list(row)[::-1] for row in zip(*self.current_block[1])]

    def check_collision(self):
        for y, row in enumerate(self.current_block[1]):
            for x, col in enumerate(row):
                if col:
                    if (x + self.current_x < 0 or x + self.current_x >= len(self.grid[0]) or
                            y + self.current_y >= len(self.grid) or
                            self.grid[y + self.current_y][x + self.current_x]):
                        return True
        return False

    def add_to_grid(self):
        for y, row in enumerate(self.current_block[1]):
            for x, col in enumerate(row):
                if col:
                    self.grid[y + self.current_y][x + self.current_x] = self.current_block[0]

    def remove_completed_lines(self):
        lines_to_remove = []
        for y in range(len(self.grid)):
            if None not in self.grid[y]:
                lines_to_remove.append(y)
        for y in lines_to_remove:
            del self.grid[y]
            self.grid.insert(0, [None] * (WINDOW_WIDTH // BLOCK_SIZE))
            self.score += 10

    def run(self):
        running = True
        while running:
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_current_block()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_sideways(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.move_sideways(1)
                    elif event.key == pygame.K_DOWN:
                        self.move_down()
                    elif event.key == pygame.K_SPACE:
                        self.rotate()

            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()
            if self.fall_time / 1000 >= 1:
                self.move_down()
                self.fall_time = 0

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    game = TetrisGame()
    game.run()