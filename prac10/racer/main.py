import pygame
import random

# Инициализация
pygame.init()

car_img = pygame.image.load("car.png")
car_img = pygame.transform.scale(car_img, (60, 90))
enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (60, 90))
coins = []
coin_timer = 0
coin_count = 0

# Размер окна
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()

# Машина игрока (прямоугольник)
player = pygame.Rect(180, 500, 60, 90)

# Враг
enemy = pygame.Rect(random.randint(0, WIDTH-60), -90, 60, 90)
enemy_speed = 5

running = True
while running:
    screen.fill((128, 128, 128))  # темно-серый
    
    # линия по центру дороги
    for i in range(0, HEIGHT, 40):
     pygame.draw.rect(screen, (255, 255, 255), (WIDTH//2 - 5, i, 10, 20))

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
        
    # Ограничение по границам экрана
    if player.x < 0:
        player.x = 0
    if player.x > WIDTH - player.width:
        player.x = WIDTH - player.width  

    # Движение врага
    enemy.y += enemy_speed
    
    # создание монет
    coin_timer += 1
    if coin_timer > 60:  # каждые ~1 сек (60 FPS)
     coin_x = random.randint(0, WIDTH - 20)
     coin = pygame.Rect(coin_x, -20, 20, 20)
     coins.append(coin)
     coin_timer = 0
     
    # движение монет
    for coin in coins[:]:
     coin.y += 5

    # сбор монеты
     if player.colliderect(coin):
         coins.remove(coin)
         coin_count += 1

    # удаление если ушла вниз
     elif coin.y > HEIGHT:
         coins.remove(coin)

    # Если враг вышел за экран — появляется сверху
    if enemy.y > HEIGHT:
        enemy.y = -90
        enemy.x = random.randint(0, WIDTH-60)

    # Столкновение
    if player.colliderect(enemy):
        print("Game Over")
        running = False

    # Рисуем
    screen.blit(car_img, (player.x, player.y))
    screen.blit(enemy_img, (enemy.x, enemy.y))
    # рисуем монеты
    for coin in coins:
     pygame.draw.circle(screen, (255, 215, 0), coin.center, 10)

    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Coins: {coin_count}", True, (0, 0, 0))
    screen.blit(text, (WIDTH - 120, 10))
    
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()