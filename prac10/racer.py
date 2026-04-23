import pygame
import random

# Инициализация
pygame.init()

# Размер окна
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()

# Машина игрока (прямоугольник)
player = pygame.Rect(180, 500, 40, 60)

# Враг
enemy = pygame.Rect(random.randint(0, WIDTH-40), -60, 40, 60)
enemy_speed = 5

running = True
while running:
    screen.fill((255, 255, 255))  # белый фон

    # Закрытие окна
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5

    # Движение врага
    enemy.y += enemy_speed

    # Если враг вышел за экран — появляется сверху
    if enemy.y > HEIGHT:
        enemy.y = -60
        enemy.x = random.randint(0, WIDTH-40)

    # Столкновение
    if player.colliderect(enemy):
        print("Game Over")
        running = False

    # Рисуем
    pygame.draw.rect(screen, (0, 0, 0), player)
    pygame.draw.rect(screen, (255, 0, 0), enemy)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()