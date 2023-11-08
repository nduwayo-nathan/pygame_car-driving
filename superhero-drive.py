import pygame
import sys
import random
import serial

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 500, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Car Driving Game')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load car image and resize it
car = pygame.image.load('car.png')
car = pygame.transform.scale(car, (90, 150))
car_rect = car.get_rect(center=(WIDTH // 2, HEIGHT - 100))

# Load obstacle image and resize it
obstacle = pygame.image.load('obstacle1.png')
obstacle = pygame.transform.scale(obstacle, (100, 80))

# Load road image
road = pygame.image.load('road.png')
road = pygame.transform.scale(road, (WIDTH, HEIGHT))
road_y = 0

# Load sounds
collision_sound = pygame.mixer.Sound('collision_sound.wav')
collect_sound = pygame.mixer.Sound('collect_sound.wav')

# Initialize obstacle variables
obstacle_speed = 20 # Reduced speed
obstacles = []

score = 0
font = pygame.font.Font(None, 36)

def display_score(score):
    score_text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(score_text, (10, 10))

def spawn_obstacle():
    x = random.randint(50, WIDTH - 50)
    y = -50
    return obstacle.get_rect(topleft=(x, y))

def display_message(text, x, y, color):
    message = font.render(text, True, color)
    screen.blit(message, (x, y))

try:
    # Initialize Serial Communication
    ser = serial.Serial('/dev/ttyACM0', 9600)  # Adjust COM3 to match your Arduino's serial port

    # Game loop
    running = True
    game_over = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        try:
            # Read joystick values from Arduino
            joystick_data = ser.readline().decode().strip().split(',')
            print(joystick_data)
            if len(joystick_data) == 2:
                joyX = int(joystick_data[0])
                joyY = int(joystick_data[1])

                if not game_over:
                    # Update car's position based on joystick values
                    car_rect.move_ip((joyX - 512) / 20, (joyY - 512) / 20)  # Adjust the scaling factor as needed

                    # Ensure car stays within window bounds
                    car_rect.left = max(0, car_rect.left)
                    car_rect.right = min(WIDTH, car_rect.right)
                    car_rect.top = max(0, car_rect.top)
                    car_rect.bottom = min(HEIGHT, car_rect.bottom)
                    
                    

                    # Spawn new obstacles
                    if pygame.time.get_ticks() % 60 == 0:
                        obstacles.append(spawn_obstacle())

                    # Move and remove obstacles
                    for obs in obstacles[:]:
                        obs.move_ip(0, obstacle_speed)
                        if obs.top > HEIGHT:
                            obstacles.remove(obs)
                            score += 1

                    # Check for collisions with obstacles
                    for obs in obstacles[:]:
                        if car_rect.colliderect(obs):
                            game_over = True
                            collision_sound.play()

                # Draw everything
                road_y = (road_y + 5) % HEIGHT  # Scroll the road
                screen.blit(road, (0, road_y))
                screen.blit(road, (0, road_y - HEIGHT))
                screen.blit(car, car_rect)
                
              


                for obs in obstacles:
                    screen.blit(obstacle, obs)

                display_score(score)

                if game_over:
                    display_message("Game Over! Press 'R' to Restart", 90, 100, RED)

                pygame.display.flip()

            # Restart the game if 'R' is pressed
            keys = pygame.key.get_pressed()
            if game_over and keys[pygame.K_r]:
                game_over = False
                car_rect.center = (WIDTH // 2, HEIGHT - 100)
                obstacles.clear()
                score = 0

        except ValueError as e:
            print(f"Error: {e}. Invalid data received from Arduino.")

except serial.SerialException as se:
    print(f"Error: {se}. Unable to establish a connection to the Arduino.")
except Exception as e:
    print(f"Error: {e}. An unexpected error occurred.")

# Clean up
pygame.quit()
sys.exit()
