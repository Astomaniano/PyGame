import pygame
pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Тестовый проект')

image = pygame.image.load('PythonPic.png')
image_rect = image.get_rect()

image_2 = pygame.image.load('PyCharmPic.png')
image_rect_2 = image_2.get_rect()

speed = 1



run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        image_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        image_rect.x += speed
    if keys[pygame.K_UP]:
        image_rect.y -= speed
    if keys[pygame.K_DOWN]:
        image_rect.y += speed

    screen.fill((0, 0, 0))
    screen.blit(image, image_rect)
    screen.blit(image_2, image_rect_2)


    pygame.display.flip()

pygame.quit()