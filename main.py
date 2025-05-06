import pygame
import random

# init pygame
pygame.init()

# config
FPS_LIMIT = 144
MOVE_TIMER = 0
MOVE_INTERVAL = .1

HUNGER = 30

TILE_SIZE = 24 
WIDTH = 32
HEIGHT = 24
SCREEN_WIDTH = WIDTH * TILE_SIZE
SCREEN_HEIGHT = HEIGHT * TILE_SIZE

CHECKER_COLOR = (8,8,8)
CHECKER_ALTCOLOR = (0,0,0)
SNAKE_COLOR = (0,255,0)
FOOD_COLOR = (255, 0, 0)

FONT = pygame.font.SysFont("Lucida Console", 24, True)
TITLE = pygame.font.SysFont("Lucida Console", 48, True)
FONT_COLOR = (255,255,255)

# setup
screen = pygame.display.set_mode((TILE_SIZE * WIDTH, TILE_SIZE * HEIGHT))
pygame.display.set_caption("PySnake")

class Snake:
    def __init__(self):
           self.body = [(WIDTH // 2, HEIGHT // 2)]
           self.direction = (0,-1)
           self.new_direction = self.direction
           self.hunger = HUNGER
    
    def move(self):
        new_direction = self.new_direction
        if len(self.body)>1:
            head = self.body[0]
            second = self.body[1]
            new_head = (head[0] + new_direction[0], head[1] + new_direction[1])
            if new_head != second:
                self.direction = new_direction
        else:
            self.direction = new_direction
        
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        if not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
            return False  # crash
            
        self.body.insert(0, new_head)
        self.body.pop()
        
        return True
    
    def grow(self):
        self.body.append(self.body[-1])
        self.hunger = HUNGER # reset timer
    
    def change_direction(self, new_direction):
        self.new_direction = new_direction
    
    def check_collision(self):
        return self.body[0] in self.body[1:]

class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        return (random.randint(0, WIDTH -1), random.randint(0, HEIGHT - 1))

    def respawn(self, snake):
        while True:
            new_position = self.random_position()
            if new_position not in snake.body:
                self.position = new_position
                break

def draw_board():
    for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            if (x // TILE_SIZE + y // TILE_SIZE) % 2 == 0:
                color = CHECKER_COLOR
            else:
                color = CHECKER_ALTCOLOR

            pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))
            
def draw_snake(snake):
    for segment in snake.body:
        pygame.draw.rect(screen, SNAKE_COLOR, (segment[0] * TILE_SIZE, segment[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_food(food):
    pygame.draw.rect(screen, FOOD_COLOR, (food.position[0] * TILE_SIZE, food.position[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_score(score):
    text = FONT.render(f"{score}", True, FONT_COLOR)
    screen.blit(text, (TILE_SIZE, TILE_SIZE))

def game_over_screen(score):
    screen.fill(CHECKER_ALTCOLOR)
    over_text = TITLE.render("Game Over", True, FONT_COLOR)
    score_text = FONT.render(f"Score: {score}", True, FONT_COLOR)
    retry_text = FONT.render("Press any key to restart", True, FONT_COLOR)
    screen.blit(over_text, (SCREEN_WIDTH // 2 - over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# main
while True:
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    score = 0
    dt = 0

    running = True
    while running:
        dt = clock.tick(FPS_LIMIT) / 1000 
        MOVE_TIMER += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    snake.change_direction((1, 0))
           
        if MOVE_TIMER >= MOVE_INTERVAL:
            MOVE_TIMER = 0  # Reset the timer
            if not snake.move() or snake.check_collision() or len(snake.body) == 0:
                running = False
                game_over_screen(score)
                break

        if snake.body[0] == food.position:
            snake.grow()
            food.respawn(snake)
            score += 1
        
        draw_board()
        draw_snake(snake)
        draw_food(food)
        draw_score(score)
        pygame.display.flip()

