import pygame
import serial

# Initialize Pygame
pygame.init()

# Initialize Serial Communication with Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)  # Adjust 'COM3' as per your system

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Catch the Falling Objects')

# Load images
player_image = pygame.image.load('character.png')
player_rect = player_image.get_rect()

object_image = pygame.image.load('object.png')
object_rect = object_image.get_rect()

# Initialize player position
player_x = 400
player_y = 500

# Initialize object position and speed
object_x = random.randint(100, 700)
object_y = -50
object_speed = random.uniform(1, 3)

score = 0
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

def display_score():
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def check_collision():
    return player_rect.colliderect(object_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Read Arduino data
    data = ser.readline().decode().strip().split(',')

    if len(data) == 2 and data[0].isdigit() and data[1].isdigit():
        arduino_x = int(data[0])
        arduino_y = int(data[1])
        player_x += arduino_x / 50
        player_y += arduino_y / 50

    # Clamp player position to screen boundaries
    player_x = max(0, min(player_x, 800 - player_rect.width))
    player_y = max(0, min(player_y, 600 - player_rect.height))

    # Update object position
    object_y += object_speed

    # Reset object position if it goes off screen
    if object_y > 600:
        object_x = random.randint(100, 700)
        object_y = -50
        object_speed = random.uniform(1, 3)

    # Check for collision
    if check_collision():
        score += 1
        object_x = random.randint(100, 700)
        object_y = -50
        object_speed = random.uniform(1, 3)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw player and object
    screen.blit(player_image, (player_x, player_y))
    screen.blit(object_image, (object_x, object_y))

    # Display score
    display_score()

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)
