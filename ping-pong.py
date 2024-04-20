import pygame

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Ping Pong')
font = pygame.font.SysFont(None, 50)

class Ball:
    def __init__(self):
        self.radius = 10
        self.color = BLUE
        self.speed_x = 5
        self.speed_y = 5
        self.position = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def move(self):
        self.position[0] += self.speed_x
        self.position[1] += self.speed_y

        if self.position[0] <= 0 or self.position[0] >= WINDOW_WIDTH:
            self.speed_x *= -1
        if self.position[1] <= 0 or self.position[1] >= WINDOW_HEIGHT:
            self.speed_y *= -1

class Paddle:
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.color = WHITE
        self.position = [x, y]

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], self.width, self.height))

    def move(self, y):
        if 0 <= y <= WINDOW_HEIGHT - self.height:
            self.position[1] = y

class Game:
    def __init__(self):
        self.player_score = 0
        self.ai_score = 0
        self.misses = 0
        self.max_misses = 10

    def increase_player_score(self):
        self.player_score += 1

    def increase_ai_score(self):
        self.ai_score += 1

    def reset_misses(self):
        self.misses = 0

    def increase_misses(self):
        self.misses += 1

    def is_game_over(self):
        return self.misses >= self.max_misses

game = Game()
ball = Ball()
player_paddle = Paddle(10, WINDOW_HEIGHT // 2 - 35, 10, 70)
ai_paddle = Paddle(WINDOW_WIDTH - 20, WINDOW_HEIGHT // 2 - 35, 10, 70)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEMOTION:
            player_paddle.move(event.pos[1])  # Update player paddle position with mouse movement

    ball.move()
    ai_paddle.move(ball.position[1])

    if ball.position[0] - ball.radius <= player_paddle.position[0] + player_paddle.width:
        if player_paddle.position[1] <= ball.position[1] <= player_paddle.position[1] + player_paddle.height:
            ball.speed_x *= -1
            game.increase_player_score()
        else:
            game.increase_misses()
            ball.position = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]

    if ball.position[0] + ball.radius >= ai_paddle.position[0]:
        if ai_paddle.position[1] <= ball.position[1] <= ai_paddle.position[1] + ai_paddle.height:
            ball.speed_x *= -1
            game.increase_ai_score()

    if game.is_game_over():
        screen.fill(BLACK)
        game_over_text = font.render("Game Over. Play again? (Y/N)", True, WHITE)
        screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2))

        pygame.display.flip()

        continue_game = False
        while not continue_game:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        game.reset_misses()
                        game.player_score = 0
                        game.ai_score = 0
                        continue_game = True
                    elif event.key == pygame.K_n:
                        running = False
                        continue_game = True

    screen.fill(BLACK)
    ball.draw(screen)
    player_paddle.draw(screen)
    ai_paddle.draw(screen)

    player_score_text = font.render(f"Player: {game.player_score}", True, WHITE)
    ai_score_text = font.render(f"AI: {game.ai_score}", True, WHITE)
    screen.blit(player_score_text, (20, 20))
    screen.blit(ai_score_text, (WINDOW_WIDTH - ai_score_text.get_width() - 20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()