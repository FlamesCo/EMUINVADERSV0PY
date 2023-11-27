import os
import datetime
import random
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
ENEMY_WIDTH = 30
ENEMY_HEIGHT = 30
BULLET_WIDTH = 5
BULLET_HEIGHT = 15
PLAYER_SPEED = 2
ENEMY_SPEED = 0.5
BULLET_SPEED = 2
ENEMY_COUNT = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont(None, 36)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Save Game Function
def save_game(score):
    documents_folder = os.path.join(os.path.expanduser('~'), 'Documents')
    filename = f"space_invaders_save_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}.txt"
    file_path = os.path.join(documents_folder, filename)
    with open(file_path, 'w') as file:
        file.write(f"Score: {score}\n")
    print(f"Game saved to {file_path}")

# Start Menu Function
def start_menu():
    screen.fill(BLACK)
    title_text = FONT.render('Space Invaders', True, WHITE)
    start_text = FONT.render('Press ENTER to Start', True, WHITE)
    quit_text = FONT.render('Press Q to Quit', True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True  # Start game
                elif event.key == pygame.K_q:
                    return False  # Quit game
            elif event.type == pygame.QUIT:
                return False

# Game Loop Function
def game_loop():
    player = pygame.Rect(400, 500, PLAYER_WIDTH, PLAYER_HEIGHT)
    enemies = [pygame.Rect(random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH), random.randint(50, 300), ENEMY_WIDTH, ENEMY_HEIGHT) for _ in range(ENEMY_COUNT)]
    bullets = []
    score = 0
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(30)  # 30 frames per second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, score

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player.right < SCREEN_WIDTH:
            player.x += PLAYER_SPEED
        if keys[pygame.K_SPACE]:
            bullet = pygame.Rect(player.centerx - BULLET_WIDTH // 2, player.top, BULLET_WIDTH, BULLET_HEIGHT)
            bullets.append(bullet)

        for bullet in bullets:
            bullet.y -= BULLET_SPEED
        bullets = [bullet for bullet in bullets if bullet.y > 0]

        for enemy in enemies:
            enemy.y += ENEMY_SPEED
            for bullet in bullets:
                if enemy.colliderect(bullet):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10
                    new_enemy = pygame.Rect(random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH), 0, ENEMY_WIDTH, ENEMY_HEIGHT)
                    enemies.append(new_enemy)

        for enemy in enemies:
            if player.colliderect(enemy):
                save_game(score)
                return True, score  # Player died, offer continue

        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, player)
        for enemy in enemies:
            pygame.draw.rect(screen, WHITE, enemy)
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        score_text = FONT.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

    return False, score

# Continue Screen Function
def continue_screen(score):
    screen.fill(BLACK)
    continue_text = FONT.render('CONTINUE? (Y/N)', True, WHITE)
    score_text = FONT.render(f'Your Score: {score}', True, WHITE)
    screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True  # Continue game
                elif event.key == pygame.K_n:
                    return False  # End game
            elif event.type == pygame.QUIT:
                return False

# Main Game Function
def main():
    if start_menu():  # Show the start menu
        continue_game = True
        final_score = 0

        while continue_game:
            game_over, score = game_loop()
            if game_over:
                continue_game = continue_screen(score)
                final_score = score if continue_game else final_score
            else:
                continue_game = False

        print(f"Final Score: {final_score}")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
