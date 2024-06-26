import pygame
import time

pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Тестовый проект')

image = pygame.image.load('PythonPic.png')
image_rect = image.get_rect()

image_2 = pygame.image.load('PyCharmPic.png')
image_rect_2 = image_2.get_rect()


run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = pygame.mouse.get_pos()
            image_rect.x = mouseX - 40
            image_rect.y = mouseY - 40

        if image_rect.colliderect(image_rect_2):
            print('произошло столкновение!')
            time.sleep(1)

    screen.fill((0, 0, 0))
    screen.blit(image, image_rect)
    screen.blit(image_2, image_rect_2)


    pygame.display.flip()

pygame.quit()