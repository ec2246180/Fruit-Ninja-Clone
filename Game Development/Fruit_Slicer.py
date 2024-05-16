import pygame
import random
import sys

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

background = pygame.image.load("images/Fruit_Slicer_Background.png")  
background = pygame.transform.scale(background, (screen_width, screen_height))
bomb_image = pygame.image.load("images/Bomb.png")  
bomb_image = pygame.transform.scale(bomb_image, (50, 50))

apple_image = pygame.image.load("images/Apple.png")  
apple_image = pygame.transform.scale(apple_image, (50, 50))
orange_image = pygame.image.load("images/Orange.png")  
orange_image = pygame.transform.scale(orange_image, (50, 50))
banana_image = pygame.image.load("images/Banana.png")  
banana_image = pygame.transform.scale(banana_image, (50, 50))
watermelon_image = pygame.image.load("images/Watermelon.png")
watermelon_image = pygame.transform.scale(watermelon_image, (50, 50))
kiwi_image = pygame.image.load("images/Kiwi.png")
kiwi_image = pygame.transform.scale(kiwi_image, (50, 50))

clock = pygame.time.Clock()
font = pygame.font.Font("go3v2.ttf", 36)
score = 0
game_running = False
lives = 3  
bombs_clicked = 0 

fruits = []
bombs = []
spawn_rate = 25  
fruit_speed = 5  
bomb_spawn_rate = 150  
gravity = .5 

menu_sfx = pygame.mixer.Sound("sound_effects/menu_music.mp3")

def spawn_fruit():
    x_pos = random.randint(50, screen_width - 50)
    fruit_type = random.choice(["apple", "orange", "banana", "watermelon", "kiwi"])
    fruit_image = eval(f"{fruit_type}_image")
    
    # More noticeable initial upward speed
    speed_y = random.randint(-15, -10)
    speed_x = random.randint(-5, 5)

    fruit = {'x': x_pos, 'y': screen_height, 'image': fruit_image, 'speed_x': speed_x, 'speed_y': speed_y}
    fruits.append(fruit)

def spawn_bomb():
    x_pos = random.randint(50, screen_width - 50)
    speed_y = random.randint(-15, -10)  
    speed_x = random.randint(-3, 3)

    bomb = {'x': x_pos, 'y': screen_height, 'image': bomb_image, 'speed_x': speed_x, 'speed_y': speed_y}
    bombs.append(bomb)

def move_objects():
    for obj in fruits + bombs:
        obj['x'] += obj['speed_x']
        obj['speed_y'] += gravity  
        obj['y'] += obj['speed_y']

       
        if obj['y'] > screen_height:
            fruits.remove(obj) if obj in fruits else bombs.remove(obj)
            
def slice_objects():
    global score, lives, bombs_clicked
    mouse_pos = pygame.mouse.get_pos()
    for fruit in fruits[:]: 
        fruit_center_x = fruit['x'] + fruit['image'].get_width() // 2
        fruit_center_y = fruit['y'] + fruit['image'].get_height() // 2
        if abs(mouse_pos[0] - fruit_center_x) < fruit['image'].get_width() // 2 and \
           abs(mouse_pos[1] - fruit_center_y) < fruit['image'].get_height() // 2:
            fruits.remove(fruit)
            score += 1  # Increment score for each fruit sliced

    for bomb in bombs[:]:
        bomb_center_x = bomb['x'] + bomb['image'].get_width() // 2
        bomb_center_y = bomb['y'] + bomb['image'].get_height() // 2
        if abs(mouse_pos[0] - bomb_center_x) < bomb['image'].get_width() // 2 and \
           abs(mouse_pos[1] - bomb_center_y) < bomb['image'].get_height() // 2:
            bombs.remove(bomb)
            bombs_clicked += 1
            lives -= 1  # Decrement lives for slicing bombs
            if bombs_clicked == 3 or lives <= 0:
                game_over()
                return


def draw_objects():
    for fruit in fruits:
        screen.blit(fruit['image'], (fruit['x'] - fruit['image'].get_width() // 2, fruit['y'] - fruit['image'].get_height() // 2))
    for bomb in bombs:
        screen.blit(bomb['image'], (bomb['x'] - bomb['image'].get_width() // 2, bomb['y'] - bomb['image'].get_height() // 2))

def draw_menu():
    play_text = font.render("Press X To Play", True, WHITE)
    screen.blit(play_text, (screen_width // 2 - play_text.get_width() // 2, 300))
    menu_sfx.play()

def game_over():
    game_over_text = font.render("Game Over!", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, 200))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 300))
    pygame.display.flip()  
    pygame.time.wait(3000)  
    pygame.quit()
    sys.exit()

def game_loop():
    global score, game_running, lives, bombs_clicked, fruits, bombs
    slicing = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                slicing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                slicing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    game_running = True
                    score = 0
                    lives = 3
                    bombs_clicked = 0
                    fruits = []
                    bombs = []

        screen.blit(background, (0, 0))
        if game_running:
            if slicing:
                slice_objects()
            if random.randint(1, spawn_rate) == 1:
                spawn_fruit()
            if random.randint(1, bomb_spawn_rate) == 1:
                spawn_bomb()
            move_objects()
            draw_objects()
            score_text = font.render(f"Score: {score}", True, WHITE)
            lives_text = font.render(f"Lives: {lives}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (10, 50))
            if lives == 0:
                game_over()
        else:
            draw_menu()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    game_loop()



