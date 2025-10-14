#!/usr/bin/env python3
"""
Snake Game - A real application to demonstrate system monitoring
This game uses CPU, Memory, and generates activity for SysInsight monitoring
"""

import pygame
import random
import sys
import time
from collections import deque

# Initialize Pygame
pygame.init()

# Game Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

# Game Speed
FPS = 10

class Snake:
    def __init__(self):
        self.length = 3
        self.positions = deque([((GRID_WIDTH // 2), (GRID_HEIGHT // 2))])
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + x) % GRID_WIDTH), (cur[1] + y) % GRID_HEIGHT)
        
        if len(self.positions) > 2 and new in list(self.positions)[2:]:
            return False  # Game Over
        else:
            self.positions.appendleft(new)
            if len(self.positions) > self.length:
                self.positions.pop()
        return True
    
    def reset(self):
        self.length = 3
        self.positions = deque([((GRID_WIDTH // 2), (GRID_HEIGHT // 2))])
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
    
    def render(self, surface):
        for p in self.positions:
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), 
                             (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1),
                        random.randint(0, GRID_HEIGHT - 1))
    
    def render(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, 
                          self.position[1] * GRID_SIZE),
                          (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)

# Direction vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def draw_grid(surface):
    """Draw grid lines"""
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, (40, 40, 40), (0, y), (WINDOW_WIDTH, y))
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, (40, 40, 40), (x, 0), (x, WINDOW_HEIGHT))

def draw_text(surface, text, size, x, y, color=WHITE):
    """Draw text on screen"""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def show_start_screen(screen):
    """Show start screen"""
    screen.fill(BLACK)
    draw_text(screen, "SNAKE GAME", 64, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4, GREEN)
    draw_text(screen, "Monitor CPU & Memory usage while playing!", 24, 
              WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40)
    draw_text(screen, "Use Arrow Keys to control", 30, 
              WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    draw_text(screen, "Press any key to start", 30, 
              WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40, YELLOW)
    draw_text(screen, "ESC to quit", 24, 
              WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                waiting = False

def show_game_over_screen(screen, score):
    """Show game over screen"""
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER!", 64, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4, RED)
    draw_text(screen, f"Final Score: {score}", 40, 
              WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20, YELLOW)
    draw_text(screen, "Press SPACE to play again", 30, 
              WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40)
    draw_text(screen, "ESC to quit", 24, 
              WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    waiting = False

def main():
    """Main game loop"""
    # Set up display
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Snake Game - SysInsight Demo')
    clock = pygame.time.Clock()
    
    # Show start screen
    show_start_screen(screen)
    
    # Game objects
    snake = Snake()
    food = Food()
    
    # Main game loop
    running = True
    while running:
        clock.tick(FPS)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT
        
        # Update snake
        if not snake.update():
            # Game over
            show_game_over_screen(screen, snake.score)
            snake.reset()
            food.randomize_position()
        
        # Check if snake ate food
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 10
            food.randomize_position()
            
            # Make sure food doesn't spawn on snake
            while food.position in snake.positions:
                food.randomize_position()
        
        # Drawing
        screen.fill(BLACK)
        draw_grid(screen)
        snake.render(screen)
        food.render(screen)
        
        # Draw score and info
        draw_text(screen, f"Score: {snake.score}", 30, 80, 10)
        draw_text(screen, "Watch dashboard: http://localhost:5001", 20, 
                 WINDOW_WIDTH - 200, 10, YELLOW)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    print("=" * 60)
    print("  SNAKE GAME - SysInsight Monitoring Demo")
    print("=" * 60)
    print("\n  This game runs in real-time and uses system resources.")
    print("  Monitor CPU, Memory, and activity on your dashboard!")
    print("\n  Dashboard: http://localhost:5001")
    print("  Controls: Arrow Keys | ESC to quit")
    print("=" * 60)
    print("\n  Starting game...\n")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame stopped by user.")
        pygame.quit()
        sys.exit()
