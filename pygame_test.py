import pygame
import random

pygame.init()   

#Screen Settings
WIDTH, HEIGHT = 640, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SLAM 'EM!")

#Game State
game_state = "main_menu"

#Enemy Settings
enemy_img = pygame.image.load("enemy.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (50,50))
enemies = []
def spawn_enemies():
    for _ in range(5):
        enemies.append([random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)])
spawn_enemies()

#Skins
goggles_img = pygame.image.load("Goggles.png").convert_alpha()
goggles_img = pygame.transform.scale(goggles_img, (75,75))
python_img = pygame.image.load("Python.png").convert_alpha()
python_img = pygame.transform.scale(python_img, (75,75))

skins = [
    {"image": goggles_img, "rect": goggles_img.get_rect(topleft = (100, 160))},
    {"image": python_img, "rect": python_img.get_rect(topleft = (200, 160))}
]

current_skin = "Goggles"


#Player Settings
x = 100
y = 100
score = 0
speed = 5
velocity_x = 0
velocity_y = 0
friction = 0.88
acceleration = 1.2

#Jumping
can_jump = True
is_jumping = False
boyut = 50
current_boyut = 50


#Fonts
font = pygame.font.SysFont('Arial', 24)
title_font = pygame.font.Font("PressStart2P-Regular.ttf", 50)
skinScreen_title_font = pygame.font.Font("PressStart2P-Regular.ttf", 30)
button_font = pygame.font.Font("PressStart2P-Regular.ttf", 20)

#Buttons
start_button = pygame.Rect(WIDTH / 2 - 100, 200, 200, 50)
skins_button = pygame.Rect(WIDTH / 2 - 100, 270, 200, 50)
exit_button = pygame.Rect(WIDTH / 2 - 100, 340, 200, 50)

back_button_skinScreen = pygame.Rect(WIDTH /2 -100, 500, 200 ,50)
back_button_game = pygame.Rect(WIDTH /2 +120, 0, 200 ,50)




#Screen Shake
shake_duration = 0
shake_intensity = 5
rect_size = 50


#particles
particles = []


#Main Loop
clock = pygame.time.Clock()
running = True
while running:
    #Drawing the Screen
    screen.fill((100,200,150))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if game_state == "main_menu":
                if start_button.collidepoint(mouse_pos):
                    game_state = "game"
                elif skins_button.collidepoint(mouse_pos):
                    game_state = "skin_screen"
                elif exit_button.collidepoint(mouse_pos):
                    running = False
            if game_state == "skin_screen":
                if back_button_skinScreen.collidepoint(mouse_pos):
                    game_state = "main_menu"
                for skin in skins:
                    if skin["rect"].collidepoint(mouse_pos):

                        relative_x = max(0, min(mouse_pos[0] - skin["rect"].x, skin["image"].get_width() - 1))
                        relative_y = max(0, min(mouse_pos[1] - skin["rect"].y, skin["image"].get_height() - 1))

                        pixel_color = skin["image"].get_at((relative_x, relative_y))

                        if pixel_color.a > 0:
                            if skin == skins[0]:
                                current_skin = "Goggles"
                            elif skin == skins[1]:
                                current_skin = "Python"
                            print(current_skin)
            if game_state == "game":
                if back_button_game.collidepoint(mouse_pos):
                    game_state = "main_menu"

    keys = pygame.key.get_pressed()
    if game_state == "game":
        if current_skin == "Goggles":
            player_img = pygame.transform.scale(goggles_img, (50,50))
        elif current_skin == "Python":
            player_img = pygame.transform.scale(python_img, (50,50))
        else:
            player_img = pygame.transform.scale(goggles_img, (50,50))
        #Movement Mechanics
        if keys[pygame.K_w]:
            velocity_y -= acceleration
        if keys[pygame.K_s]:
            velocity_y += acceleration
        if keys[pygame.K_a]:
            velocity_x -= acceleration
        if keys[pygame.K_d]:
            velocity_x += acceleration

        velocity_x *= friction
        velocity_y *= friction

        x += velocity_x
        y += velocity_y

        x = max(0, min(x, WIDTH - 50))  # 50 is player size
        y = max(0, min(y, HEIGHT - 50))

        #Jumping Mechanics
        if keys[pygame.K_SPACE] and not is_jumping and can_jump:
            is_jumping = True
            jump_timer = 15
            can_jump = False
        if is_jumping:
            current_boyut = 55
            jump_timer -= 1
            if jump_timer <= 0:
                is_jumping = False
                #Particles
                for _ in range(20):
                    particles.append([
                        x + boyut // 2,  # Particle x position
                        y + boyut,      # Particle y position
                        random.uniform(-4, 4), # X velocity
                        random.uniform(-4, 4),  # Y velocity                        
                        random.uniform(8, 15)   # Particle lifetime
                    ])
                #Shake when jump
                shake_duration = 10
                #Killing Enemies
                for enemy in enemies:
                    if x < enemy[0] + 40 and x + current_boyut > enemy[0]:
                        if y < enemy[1] + 40 and y + current_boyut > enemy[1]:
                            enemies.remove(enemy)
                            score += 1
        else:
            current_boyut = boyut

            if not keys[pygame.K_SPACE]:
                can_jump = True

        #Spawn enemies when there're none
        if len(enemies) == 0:
            spawn_enemies()

        #For Particles
        for particle in particles:
            particle[0] += particle[2]  # Move x
            particle[1] += particle[3]  # Move y
            particle[4] -= 1  # Decrease lifetime
    
        # Remove dead particles
        particles = [p for p in particles if p[4] > 0]

        #Screen Shake mechanic
        if shake_duration > 0:
            shake_offset_x = random.randint(-shake_intensity, shake_intensity)
            shake_offset_y = random.randint(-shake_intensity, shake_intensity)
            shake_duration -= 1
        else:
            shake_offset_x, shake_offset_y = 0, 0



        #Drawing Enemies
        for enemy in enemies:
            screen.blit(enemy_img, (enemy[0] + shake_offset_x, enemy[1] + shake_offset_y))

        # Draw particles
        for particle in particles:
            pygame.draw.circle(screen, (143, 111, 62), (particle[0] + shake_offset_x, particle[1] + shake_offset_y), 3)

        offset = (current_boyut - rect_size) // 2

    
        current_scale = max(1, offset, 1.2)  # Prevents going invisible

    
        player_size = int(55 * current_scale)

        draw_x = x - (player_size - 55) / 2
        draw_y = y - (player_size - 55) / 2

        screen.blit(pygame.transform.scale(player_img, (player_size, player_size)), (draw_x + shake_offset_x, draw_y + shake_offset_y))
        #Back Button
        pygame.draw.rect(screen, (255,255,255), back_button_game)
        text_surface = button_font.render("Go Back", True, (0,0,0))
        text_rect = text_surface.get_rect(center=back_button_game.center)
        screen.blit(text_surface, text_rect)
    if game_state == "main_menu":
        #Title
        title_text = title_font.render('SLAM \'EM', True, (255,255,255))
        screen.blit(title_text,(WIDTH / 2 - title_text.get_width() / 2, 100))
        
        #Buttons
        pygame.draw.rect(screen, (255,255,255), start_button)
        pygame.draw.rect(screen, (255,255,255), skins_button)
        pygame.draw.rect(screen, (255,255,255), exit_button)

        # Button text
        def draw_button_text(text, button_rect):
            text_surface = button_font.render(text, True, (0,0,0))
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)

        draw_button_text("Start", start_button)
        draw_button_text("Skins", skins_button)
        draw_button_text("Exit", exit_button)

    if game_state == "skin_screen":
        #Title
        skinScreenTitle = skinScreen_title_font.render('Choose Ur Skin', True, (255,255,255))
        screen.blit(skinScreenTitle,(WIDTH / 2 - skinScreenTitle.get_width() / 2, 100))

        #Back Button
        pygame.draw.rect(screen, (255,255,255), back_button_skinScreen)
        text_surface = button_font.render("Go Back", True, (0,0,0))
        text_rect = text_surface.get_rect(center=back_button_skinScreen.center)
        screen.blit(text_surface, text_rect)


        for skin in skins:
            screen.blit(skin["image"], skin["rect"])
    
    pygame.display.flip()
#    print(score)
    clock.tick(60)
    
pygame.quit()