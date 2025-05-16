import pygame    # Pygame library for game development
import random    # Random library for generating random positions and events
import time      # Time library for delays

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1530, 700   # Screen dimensions
win = pygame.display.set_mode((width, height))   # Create the game window
pygame.display.set_caption("Nebula Strike")   # Set the window title

# Load and resize images
def load_and_resize(image_path, size):
    """Load an image from a file and resize it to the specified size."""
    image = pygame.image.load(image_path)  # Load the image
    return pygame.transform.scale(image, size)  # Resize the image

# Load game assets (images)
background_img = load_and_resize("background.png", (width, height))  # Background image
menu_background_img = load_and_resize("menu_background.png", (width, height))  # Menu background
plane_img = load_and_resize("plane.png", (60, 60))  # Player's plane
enemy_img = load_and_resize("enemy.png", (50, 50))  # Enemy plane
bullet_img = load_and_resize("bullet.png", (10, 30))  # Bullet image
explosion_img = load_and_resize("explosion.png", (60, 60))  # Explosion effect
extra_life_img = load_and_resize("extra_life.png", (30, 30))  # Extra life power-up
multi_bullet_img = load_and_resize("multi_bullet.png", (30, 30))  # Multi-bullet power-up
double_bullet_img = load_and_resize("double_bullet.png", (30, 30))  # Double-bullet power-up
heart_img = load_and_resize("heart.png", (30, 30))  # Heart image for lives display

# Dictionary to map power-up types to their images
powerup_img = {
    'life': extra_life_img,  # Extra life power-up
    'multi': multi_bullet_img,  # Multi-bullet power-up
    'double': double_bullet_img  # Double-bullet power-up
}

# Load sounds
fire_sound = pygame.mixer.Sound("fire_sound.mp3")  # Sound for firing bullets
explosion_sound = pygame.mixer.Sound("explosion_sound.mp3")  # Sound for explosions
enemy_fire_sound = pygame.mixer.Sound("enemy_fire_sound.mp3")  # Sound for enemy firing

# Set up mixer channels
pygame.mixer.set_num_channels(16)  # Allow up to 16 simultaneous sound effects

# Define colors (RGB values)
white = (255, 255, 255)  # White color
black = (0, 0, 0)  # Black color
gray = (128, 128, 128)  # Gray color
red = (255, 0, 0)  # Red color
yellow = (255, 255, 0)  # Yellow color
translucent_black = (0, 0, 0, 180)  # Black with transparency for overlays

# --- Classes ---
# Define the Plane class (player-controlled plane)
class Plane: #done
    def __init__(self):
        """Initialize the player's plane."""
        self.image = plane_img  # Load the plane image
        self.rect = self.image.get_rect()  # Get the rectangle for positioning
        self.rect.center = (width // 2, height - 50)  # Start at the bottom center
        self.speed = 8  # Movement speed 8 pixels per frame
        self.lives = 3  # Number of lives
        self.power_up_type = None  # Current power-up (if any)

    def draw(self):
        """Draw the plane on the screen."""
        win.blit(self.image, self.rect.topleft)

    def move(self, x):
        """Move the plane left or right."""
        self.rect.x += x * self.speed  # Update position  # 500 + (-8) = 492
        # Prevent the plane from moving off-screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > width:
            self.rect.right = width

# Define the Bullet class
class Bullet: #done
    def __init__(self, x, y, speed):
        """Initialize a bullet."""
        self.image = bullet_img  # Load the bullet image
        self.rect = self.image.get_rect()  # Get the rectangle for positioning
        self.rect.center = (x, y)  # Start at the given position
        self.speed = speed  # Movement speed

    def draw(self):
        """Draw the bullet on the screen."""
        win.blit(self.image, self.rect.topleft)

    def move(self):
        """Move the bullet upward."""
        self.rect.y += self.speed  #In each frame, the bullet moves closer to the top of the screen.

# Define the Enemy class
class Enemy: #done
    def __init__(self):
        """Initialize an enemy plane."""
        self.image = enemy_img  # Load the enemy image
        self.rect = self.image.get_rect()  # Get the rectangle for positioning
        self.rect.x = random.randint(0, width - self.rect.width)  # Random x position  ,self.rect.width is the width of the enemy image
        self.rect.y = random.randint(-150, -50)  # Start off-screen
        self.speed = 1  # Movement speed
        self.shoot_cooldown = 2000  # Time between enemy shots (milliseconds)
        self.last_shot_time = pygame.time.get_ticks()  # Track last shot time
        self.alive = True  # Whether the enemy is alive

    def draw(self):
        """Draw the enemy on the screen."""
        if self.alive:
            win.blit(self.image, self.rect.topleft)

    def move(self):
        """Move the enemy downward."""
        if self.alive:
            self.rect.y += self.speed

    def shoot(self):
        """Make the enemy shoot a bullet."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_cooldown and self.alive:
            self.last_shot_time = current_time
            enemy_fire_sound.play()  # Play the shooting sound
            return Bullet(self.rect.centerx, self.rect.bottom, 5)  # Return a new bullet ,speed is 5 pixels per frame
        return None

# Define the Explosion class
class Explosion: #done
    def __init__(self, x, y):
        """Initialize an explosion effect."""
        self.image = explosion_img  # Load the explosion image
        self.rect = self.image.get_rect()  # Get the rectangle for positioning
        self.rect.center = (x, y)  # Start at the given position
        self.timer = 30  # Duration of the explosion (frames)

    def draw(self):
        """Draw the explosion on the screen."""
        win.blit(self.image, self.rect.topleft)

    def update(self):
        """Update the explosion timer."""
        self.timer -= 1
        return self.timer <= 0  # Return True if the explosion is finished

# Define the PowerUp class
class PowerUp: #done
    def __init__(self, x, y, power_type):
        """Initialize a power-up."""
        self.image = powerup_img[power_type]  # Load the corresponding power-up image
        self.rect = self.image.get_rect()  # Get the rectangle for positioning
        self.rect.center = (x, y)  # Start at the given position
        self.speed = 2  # Movement speed
        self.type = power_type  # Type of power-up (life, multi, double)

    def draw(self):
        """Draw the power-up on the screen."""
        win.blit(self.image, self.rect.topleft)

    def move(self):
        """Move the power-up downward."""
        self.rect.y += self.speed

# Functions to save and load high scores
def save_high_score(score): #done
    """Save the high score to a file."""
    with open("high_score.txt", "w") as file:
        file.write(str(score))  # Write the score as a string

def load_high_score(): #done
    """Load the high score from a file."""
    try:
        with open("high_score.txt", "r") as file: #Attempts to open "high_score.txt" in read mode ("r").
            return int(file.read())  # Read and return the score as an integer
    except FileNotFoundError:
        return 0  # If the file does not exist, return a default high score of 0

def draw_translucent_rect(surface, color, rect):
    """Draw a translucent rectangle on the screen."""
    temp_surface = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)  # Create a transparent surface
    temp_surface.fill(color)  # Fill the surface with the specified color
    surface.blit(temp_surface, (rect[0], rect[1]))  # Draw the surface on the screen

def blur_surface(surface): #done n
    """Apply a blur effect to a surface."""
    scale = 0.1  # Adjust the scale for more or less blur effect
    small_surface = pygame.transform.smoothscale(surface, (int(width * scale), int(height * scale)))  # Downscale
    return pygame.transform.smoothscale(small_surface, (width, height))  # Upscale back to original size

def draw_button(rect, text, selected, font): #done
    """Draw a button with text and highlight if selected."""
    pygame.draw.rect(win, black, rect)  # Draw the black background rectangle
    button_text_color = gray if selected else white  # Highlight text if selected
    button_text = font.render(text, True, button_text_color)  # Render the button text
    win.blit(button_text, (rect[0] + (rect[2] - button_text.get_width()) // 2, rect[1] + (rect[3] - button_text.get_height()) // 2))  # Center the text

def show_menu(paused_game_data=None):#done
    """Display the main menu."""
    selected_button = 0  # Index of the currently selected button
    # Define menu buttons based on whether the game is paused
    buttons = ["New Game", "Continue", "High Score", "Quit"] if paused_game_data else ["New Game", "High Score", "Quit"]
    menu = True  # Flag to keep the menu running

    while menu:
        win.blit(menu_background_img, (0, 0))  # Draw the menu background ,(0,0) is the coordinates of the top and left corner 
        font = pygame.font.SysFont(None, 75)  # Font for the title
        title = font.render("Nebula Strike", True, white)  # Render the title text
        win.blit(title, (width // 2 - title.get_width() // 2, height // 4))  # Center the title

        button_font = pygame.font.SysFont(None, 50)  # Font for the buttons
        # Define button positions ,Defines a list of tuples, where each tuple represents a button's position and size.Each tuple is structured as (x, y, width, height)
        button_rects = [
            (width // 2 - 150, height // 2, 300, 50),
            (width // 2 - 150, height // 2 + 60, 300, 50),
            (width // 2 - 150, height // 2 + 120, 300, 50),
            (width // 2 - 150, height // 2 + 180, 300, 50)
        ][:len(buttons)]  # Adjust the number of buttons based on the menu state,the slicing removes excess buttons

        # Draw each button
        for i, rect in enumerate(button_rects):
            draw_button(rect, buttons[i], i == selected_button, button_font)

        pygame.display.update()  # Update the display

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:  # Handle keyboard navigation
                if event.key == pygame.K_DOWN:  # Move selection down
                    selected_button = (selected_button + 1) % len(buttons)
                if event.key == pygame.K_UP:  # Move selection up
                    selected_button = (selected_button - 1) % len(buttons)
                if event.key == pygame.K_RETURN:  # Select the current button
                    if buttons[selected_button] == "New Game":
                        menu = False
                        game_loop()
                    if buttons[selected_button] == "Continue" and paused_game_data:
                        menu = False
                        game_loop(paused_game_data)
                    if buttons[selected_button] == "High Score":
                        show_high_score()
                    if buttons[selected_button] == "Quit":
                        pygame.quit()
                        quit()

def show_high_score(): #done
    """Display the high score screen."""
    selected_button = 0  # Index of the selected button
    high_score = True  # Flag to keep the high score screen running
    high_score_value = load_high_score()  # Load the saved high score

    while high_score:
        win.blit(menu_background_img, (0, 0))  # Draw the menu background
        font = pygame.font.SysFont(None, 75)  # Font for the title
        title = font.render("High Score", True, white)  # Render the title text
        win.blit(title, (width // 2 - title.get_width() // 2, height // 4))  # Center the title

        # Display the high score
        score_font = pygame.font.SysFont(None, 50)
        high_score_rect = (width // 2 - 150, height // 2, 300, 50)
        draw_translucent_rect(win, translucent_black, high_score_rect)  # Draw a translucent background
        score_text = score_font.render(str(high_score_value), True, white)  # Render the score
        win.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2 + (high_score_rect[3] // 2) - (score_text.get_height() // 2)))

        # Back button
        back_button_rect = (width // 2 - 150, height // 2 + 60, 300, 50)
        draw_button(back_button_rect, "Back", selected_button == 0, score_font)

        pygame.display.update()  # Update the display

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:  # Handle keyboard input
                if event.key == pygame.K_RETURN and selected_button == 0:  # Select the back button
                    high_score = False

def pause_menu(paused_game_data): #done
    """Display the pause menu."""
    selected_button = 0  # Index of the selected button
    buttons = ["Resume", "Menu"]  # Pause menu options
    paused = True  # Flag to keep the pause menu running
    blurred_background = blur_surface(win.copy())  # Create a blurred background

    while paused:
        win.blit(blurred_background, (0, 0))  # Draw the blurred background
        font = pygame.font.SysFont(None, 75)  # Font for the title
        pause_text = font.render("Paused", True, white)  # Render the title text
        win.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 4))  # Center the title

        button_font = pygame.font.SysFont(None, 50)  # Font for the buttons
        # Define button positions
        button_rects = [
            (width // 2 - 150, height // 2, 300, 50),
            (width // 2 - 150, height // 2 + 60, 300, 50)
        ]

        # Draw each button
        for i, rect in enumerate(button_rects):
            draw_button(rect, buttons[i], i == selected_button, button_font)

        pygame.display.update()  # Update the display

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:  # Handle keyboard input
                if event.key == pygame.K_ESCAPE:  # Resume the game
                    paused = False
                if event.key == pygame.K_DOWN:  # Move selection down
                    selected_button = (selected_button + 1) % len(buttons)
                if event.key == pygame.K_UP:  # Move selection up
                    selected_button = (selected_button - 1) % len(buttons)
                if event.key == pygame.K_RETURN:  # Select the current button
                    if buttons[selected_button] == "Resume":
                        paused = False
                        return paused_game_data  # Resume the game
                    if buttons[selected_button] == "Menu":
                        show_menu(paused_game_data)  # Return to the main menu
                        return

def game_loop(paused_game_data=None): #done
    """Main game loop that handles gameplay logic."""
    # Initialize or resume game state
    if paused_game_data:
        # Resume from paused state
        plane, bullets, enemy_bullets, enemies, explosions, powerups, score, max_lives, fire_cooldown, last_fire_time = paused_game_data
        firing = False  # Initialize firing variable
        game_over = False  # Initialize game_over variable
    else:
        # Start a new game
        plane = Plane()  # Create the player's plane
        bullets = []  # List to store bullets fired by the player
        enemy_bullets = []  # List to store bullets fired by enemies
        enemies = []  # List to store enemy planes
        explosions = []  # List to store explosion effects
        powerups = []  # List to store power-ups
        game_over = False  # Flag to indicate if the game is over
        firing = False  # Flag to indicate if the player is firing bullets
        fire_cooldown = 250  # Time in milliseconds between bullets
        last_fire_time = 0  # Track the last time the player fired a bullet
        score = 0  # Player's score
        max_lives = 5  # Maximum number of lives the player can have

    high_score_value = load_high_score()  # Load the high score from the file

    clock = pygame.time.Clock()  # Create a clock to control the frame rate
    run = True  # Flag to keep the game running

    while run:
        clock.tick(60)  # Limit the frame rate to 60 FPS #this loop will run at 60 times in a second
        current_time = pygame.time.get_ticks()  # Get the current time ,Retrieves the current time for controlling cooldowns.

        # Handle events (e.g., input)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Start firing bullets
                    firing = True
                if event.key == pygame.K_ESCAPE:  # Open the pause menu
                    paused_game_data = (plane, bullets, enemy_bullets, enemies, explosions, powerups, score, max_lives, fire_cooldown, last_fire_time)
                    paused_game_data = pause_menu(paused_game_data)
                    if paused_game_data is None:  # If the player selects "Menu," exit the game loop
                        return
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:  # Stop firing bullets
                    firing = False

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  # Move left
            plane.move(-1)
        if keys[pygame.K_RIGHT]:  # Move right
            plane.move(1)

        # Handle firing bullets
        if firing and current_time - last_fire_time > fire_cooldown and not game_over:
            if plane.power_up_type == 'multi':  # Multi-bullet power-up
                bullets.append(Bullet(plane.rect.centerx - 15, plane.rect.top, -7))
                bullets.append(Bullet(plane.rect.centerx, plane.rect.top, -7))
                bullets.append(Bullet(plane.rect.centerx + 15, plane.rect.top, -7))
            elif plane.power_up_type == 'double':  # Double-bullet power-up
                bullets.append(Bullet(plane.rect.centerx - 10, plane.rect.top, -7))
                bullets.append(Bullet(plane.rect.centerx + 10, plane.rect.top, -7))
            else:  # Normal single bullet
                bullets.append(Bullet(plane.rect.centerx, plane.rect.top, -7))
            fire_sound.play()  # Play the firing sound
            last_fire_time = current_time  # Update the last fire time

        # Update bullets
        for bullet in bullets[:]:
            bullet.move()  # Move the bullet upward
            if bullet.rect.bottom < 0:  # Remove bullets that go off-screen
                bullets.remove(bullet)

        # Update enemies
        for enemy in enemies[:]:
            enemy.move()  # Move the enemy downward
            enemy_bullet = enemy.shoot()  # Enemy shoots bullets
            if enemy_bullet:
                enemy_bullets.append(enemy_bullet)
            if enemy.rect.top > height and enemy.alive:  # Remove enemies that go off-screen
                enemy.alive = False
            for bullet in bullets:  # Check collision with player bullets
                if enemy.rect.colliderect(bullet.rect) and enemy.alive:
                    enemy.alive = False
                    bullets.remove(bullet)
                    explosions.append(Explosion(enemy.rect.centerx, enemy.rect.centery))  # Add explosion effect
                    pygame.mixer.find_channel(True).play(explosion_sound)  # Play explosion sound
                    score += 10  # Increase score
                    if random.random() < 0.1:  # 10% chance to spawn a power-up
                        powerup_type = random.choice(['life', 'multi', 'double'])
                        powerups.append(PowerUp(enemy.rect.centerx, enemy.rect.centery, powerup_type))
            if enemy.rect.colliderect(plane.rect) and enemy.alive:  # Check collision with the player's plane
                enemy.alive = False
                explosions.append(Explosion(plane.rect.centerx, plane.rect.centery))  # Add explosion effect
                explosions.append(Explosion(enemy.rect.centerx, enemy.rect.centery))
                pygame.mixer.find_channel(True).play(explosion_sound)  # Play explosion sound
                plane.lives -= 1  # Decrease player's lives
                if plane.lives <= 0:  # End the game if lives reach 0
                    game_over = True

        # Update enemy bullets
        for bullet in enemy_bullets[:]:
            bullet.move()  # Move the bullet downward
            if bullet.rect.top > height:  # Remove bullets that go off-screen
                enemy_bullets.remove(bullet)
            if bullet.rect.colliderect(plane.rect):  # Check collision with the player's plane
                enemy_bullets.remove(bullet)
                explosions.append(Explosion(bullet.rect.centerx, bullet.rect.centery))  # Add explosion effect
                pygame.mixer.find_channel(True).play(explosion_sound)  # Play explosion sound
                plane.lives -= 1  # Decrease player's lives
                if plane.lives <= 0:  # End the game if lives reach 0
                    game_over = True

        # Update power-ups
        for powerup in powerups[:]:
            powerup.move()  # Move the power-up downward
            if powerup.rect.top > height:  # Remove power-ups that go off-screen
                powerups.remove(powerup)
            if powerup.rect.colliderect(plane.rect):  # Check collision with the player's plane
                powerups.remove(powerup)
                if powerup.type == 'life' and plane.lives < max_lives:  # Extra life power-up
                    plane.lives += 1
                else:  # Other power-ups (multi or double bullets)
                    plane.power_up_type = powerup.type

        # Update explosions
        for explosion in explosions[:]:
            explosion.draw()  # Draw the explosion
            if explosion.update():  # Remove explosions that are finished
                explosions.remove(explosion)

        # Spawn new enemies
        if random.random() < 0.02 and not game_over:  # 2% chance to spawn an enemy each frame
            enemies.append(Enemy())

        # Draw everything on the screen
        win.blit(background_img, (0, 0))  # Draw the background
        plane.draw()  # Draw the player's plane
        for bullet in bullets:
            bullet.draw()  # Draw player bullets
        for bullet in enemy_bullets:
            bullet.draw()  # Draw enemy bullets
        for enemy in enemies:
            enemy.draw()  # Draw enemies
        for powerup in powerups:
            powerup.draw()  # Draw power-ups
        for explosion in explosions:
            explosion.draw()  # Draw explosions

        # Display score and lives
        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f"Score: {score}", True, black)  # Render the score
        win.blit(score_text, (10, 10))  # Display the score at the top-left corner

        for i in range(plane.lives):  # Display hearts for remaining lives
            win.blit(heart_img, (10 + i * 35, 50))

        # Handle game over
        if game_over:
            if score > high_score_value:  # Save the high score if the current score is higher
                save_high_score(score)
            font = pygame.font.SysFont(None, 75)
            text = font.render("GAME OVER", True, black)  # Render "GAME OVER" text
            win.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(2000)  # Wait for 2 seconds
            show_menu()  # Return to the main menu

        pygame.display.update()  # Update the display

    pygame.quit()  # Quit the game

if __name__ == "__main__": #This checks if the script is being run directly (not imported elsewhere).
    show_menu()  # Show the main menu
    game_loop()  # Start the game loop



