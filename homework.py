import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Установка размеров окна
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Выживалово')

# Определение цветов
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 40
        self.height = 40
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(window_size[0] / 2, window_size[1] / 2))
        self.speed = 5
        self.lives = 3
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        # Ограничение движения в пределах окна
        self.rect.clamp_ip(screen.get_rect())

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 30
        self.height = 30
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)
        # Спавн врагов с краев экрана
        side = random.choice(['left', 'right', 'top', 'bottom'])
        if side == 'left':
            x = -self.width
            y = random.randint(0, window_size[1])
        elif side == 'right':
            x = window_size[0]
            y = random.randint(0, window_size[1])
        elif side == 'top':
            x = random.randint(0, window_size[0])
            y = -self.height
        else:  # bottom
            x = random.randint(0, window_size[0])
            y = window_size[1]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = random.randint(1, 3)

    def update(self, player):
        # Движение в сторону игрока
        direction = pygame.math.Vector2(player.rect.center) - self.rect.center
        direction.normalize_ip()
        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed

# Класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.Surface([4, 4])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=pos)
        self.speed = 10
        self.direction = direction

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        # Удалить пулю, если она покидает экран
        if not screen.get_rect().contains(self.rect):
            self.kill()

# Группы спрайтов
player = Player()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Стрельба пулей
            mouse_pos = pygame.mouse.get_pos()
            direction = pygame.math.Vector2(mouse_pos) - player.rect.center
            direction.normalize_ip()
            bullet = Bullet(player.rect.center, direction)
            bullets.add(bullet)

    # Обновление спрайтов
    player.update()
    enemies.update(player)
    bullets.update()

    # Проверка столкновений
    for enemy in enemies:
        if pygame.sprite.spritecollide(enemy, bullets, True):
            enemy.kill()  # Уничтожить врага при попадании
            player.score += 1  # Добавить очки за уничтожение врага
            if player.score % 30 == 0:
                player.lives += 1  # Дополнительная жизнь каждые 30 очков

    # Проверка столкновения игрока с врагами
    if pygame.sprite.spritecollide(player, enemies, True):
        player.lives -= 1  # Уменьшить количество жизней
        if player.lives == 0:
            print('Игра окончена! Ваш счет:', player.score)
            running = False

    # Спавн новых врагов
    if len(enemies) < 10:  # Поддерживаем число врагов на уровне 10
        enemies.add(Enemy())

    # Очистка экрана
    screen.fill(WHITE)

    # Рисование спрайтов
    screen.blit(player.image, player.rect)
    enemies.draw(screen)
    bullets.draw(screen)

    # Вывод счета и жизней
    font = pygame.font.SysFont(None, 36)
    score_text = font.render('Score: ' + str(player.score), True, GREEN)
    lives_text = font.render('Lives: ' + str(player.lives), True, GREEN)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    # Обновление экрана
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()