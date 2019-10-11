import pygame
(width, height) = (500, 500)
screen = pygame.display.set_mode((width, height))

black_square = pygame.transform.scale((pygame.image.load('img/square_gray_dark.png')), (width//8, height//8))
white_square = pygame.transform.scale((pygame.image.load('img/square_gray_light.png')), (width//8, height//8))