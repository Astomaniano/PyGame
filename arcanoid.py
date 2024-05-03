import pygame
import random

pygame.init()

# Устанавливаем размеры окна
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Арканоид')

# Определяем цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Класс для платформы
class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 20
        self.x = (window_size[0] - self.width) / 2
        self.y = window_size[1] - self.height - 20
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 5

    def move(self, direction):
        if direction == 'left' and self.rect.left > 0:
            self.rect.x -= self.speed
        if direction == 'right' and self.rect.right < window_size[0]:
            self.rect.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

# Класс для мяча
class Ball:
    def __init__(self):
        self.radius = 10
        self.x = window_size[0] / 2
        self.y = window_size[1] / 2
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.speed_x = 3 * random.choice((1, -1))
        self.speed_y = 3 * random.choice((1, -1))

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Отскок от стен
        if self.rect.right >= window_size[0] or self.rect.left <= 0:
            self.speed_x *= -1
        if self.rect.top <= 0:
            self.speed_y *= -1

    def draw(self):
        pygame.draw.circle(screen, RED, self.rect.center, self.radius)

# Класс для кирпичика
class Brick:
    def __init__(self, x, y):
        self.width = 75
        self.height = 30
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)

# Добавляем кирпичики
bricks = []
for i in range(8):  # 8 кирпичиков в ряду
    for j in range(5):  # 5 рядов кирпичиков
        bricks.append(Brick(i * (75 + 10) + 70, j * (30 + 10) + 30))

# Создаем объекты платформы и мяча
paddle = Paddle()
ball = Ball()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Перемещение платформы
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move('left')
    if keys[pygame.K_RIGHT]:
        paddle.move('right')

    # Перемещение мяча
    ball.move()

    # Отскок мяча от платформы
    if ball.rect.colliderect(paddle.rect):
        ball.speed_y *= -1

    # Отскок мяча от кирпичиков
    for brick in bricks[:]:
        if ball.rect.colliderect(brick.rect):
            ball.speed_y *= -1
            bricks.remove(brick)  # Удаляем кирпичик при столкновении

    # Проверка на проигрыш
    if ball.rect.bottom >= window_size[1]:
        print('Вы проиграли!')
        run = False

    # Очистка экрана
    screen.fill(WHITE)

    # Рисуем объекты
    paddle.draw()
    ball.draw()
    for brick in bricks:
        brick.draw()

    # Обновление экрана
    pygame.display.flip()
    pygame.time.delay(10)

    #pygame.time.Clock().tick(60)

pygame.quit()