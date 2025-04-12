import pygame
import sys
import os

pygame.init()

background_colour = (24, 24, 24)

width, height = 300, 300
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption('Gravity Ball Simulator')

def resource_path(relative_path):
    """Get the absolute path to the resource, works for dev and bundled."""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

icon_path = resource_path('assets/GravityGame.png')
ball_image_path = resource_path('assets/ball.png')

icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)

ball_image = pygame.image.load(ball_image_path)

ball_radius = 40
ball_image = pygame.transform.scale(ball_image, (ball_radius * 2, ball_radius * 2))

ball_pos = [width // 2, height // 2]
ball_velocity = [0, 0]
dragging = False
drag_offset = [0, 0]

gravity = 0.5
bounce_factor = 0.9  
friction = 0.99

pygame.display.flip()

running = True
while running:
    screen.fill(background_colour)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if (ball_pos[0] - ball_radius < event.pos[0] < ball_pos[0] + ball_radius) and (ball_pos[1] - ball_radius < event.pos[1] < ball_pos[1] + ball_radius):
                dragging = True
                drag_offset = [ball_pos[0] - event.pos[0], ball_pos[1] - event.pos[1]]

        if event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                dragging = False
                mouse_x, mouse_y = event.pos

                ball_velocity = [(mouse_x - ball_pos[0]) * 0.5, (mouse_y - ball_pos[1]) * 0.5]

        if event.type == pygame.VIDEORESIZE:
            width, height = event.size
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    if dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        ball_pos = [mouse_x + drag_offset[0], mouse_y + drag_offset[1]]
        ball_velocity = [0, 0]

    ball_velocity[1] += gravity
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    if ball_pos[0] - ball_radius < 0:
        ball_pos[0] = ball_radius  
        ball_velocity[0] = -ball_velocity[0] * bounce_factor
    elif ball_pos[0] + ball_radius > width:
        ball_pos[0] = width - ball_radius  
        ball_velocity[0] = -ball_velocity[0] * bounce_factor

    if ball_pos[1] - ball_radius < 0:
        ball_pos[1] = ball_radius 
        ball_velocity[1] = -ball_velocity[1] * bounce_factor
    elif ball_pos[1] + ball_radius > height:
        ball_pos[1] = height - ball_radius 
        ball_velocity[1] = -ball_velocity[1] * bounce_factor

    ball_velocity[0] *= friction
    ball_velocity[1] *= friction

    screen.blit(ball_image, (ball_pos[0] - ball_radius, ball_pos[1] - ball_radius))

    pygame.display.update()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
