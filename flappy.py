import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Colors
WHITE = (255, 255, 255)
DARK_GREEN = (0, 100, 0) 
RED = (255, 0, 0)

bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_radius = 15
gravity = 0.3
bird_velocity = 0
jump_strength = -6 
flap_strength = -10

# Pipe properties
pipe_width = 70
pipe_gap = 150
pipe_velocity = 4
pipes = []

# Score
score = 0
font = pygame.font.SysFont('Arial', 30)

clock = pygame.time.Clock()

def create_pipe():
    height = random.randint(100, SCREEN_HEIGHT - 100 - pipe_gap)
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, height + pipe_gap, pipe_width, SCREEN_HEIGHT - height - pipe_gap)
    return top_pipe, bottom_pipe

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = flap_strength
  
    bird_velocity += gravity
    bird_y += bird_velocity
    
    # Move pipes and check for collisions
    for pipe in pipes:
        pipe[0].x -= pipe_velocity
        pipe[1].x -= pipe_velocity
    
    pipes = [pipe for pipe in pipes if pipe[0].x + pipe_width > 0]
    
    for top_pipe, bottom_pipe in pipes:
        if (bird_x + bird_radius > top_pipe.x and bird_x - bird_radius < top_pipe.x + pipe_width and
            (bird_y - bird_radius < top_pipe.height or bird_y + bird_radius > bottom_pipe.y)):
            running = False
    
    if bird_y + bird_radius > SCREEN_HEIGHT or bird_y - bird_radius < 0:
        running = False
    
    if random.randint(0, 100) < 2:
        pipes.append(create_pipe())

    for top_pipe, bottom_pipe in pipes:
        if bird_x + bird_radius > top_pipe.x and bird_x - bird_radius < top_pipe.x + pipe_width and bird_y > top_pipe.height:
            score += 1
    
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (bird_x, int(bird_y)), bird_radius)
    
    for top_pipe, bottom_pipe in pipes:
        pygame.draw.rect(screen, DARK_GREEN, top_pipe)
        pygame.draw.rect(screen, DARK_GREEN, bottom_pipe)
    
    # Display score
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
