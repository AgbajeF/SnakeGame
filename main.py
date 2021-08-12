

#libraries
import pygame
import time
import random
from pygame.locals import *

size_of_block = 40

#Create Class Apple
class Apple:
    def __init__(self, parent_screen):
        self.apple_image = pygame.image.load("resources/apple.jpeg")
        self.parent_screen = parent_screen
        self.x = size_of_block*3
        self.y = size_of_block*3

    def draw(self):
        self.parent_screen.blit(self.apple_image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0,24)*size_of_block
        self.y = random.randint(0,19)*size_of_block

#Create Class Snake
class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpeg").convert()
        # snake start location on screen
        self.x = [size_of_block]*length
        self.y = [size_of_block]*length
        self.direction = 'RIGHT'

    def draw(self):
        #clears screen before creating block/Eliminates the block trails
        #self.parent_screen.fill(background_color)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_up(self):
        self.direction = 'UP'

    def move_down(self):
        self.direction = 'DOWN'

    def move_left(self):
        self.direction = 'LEFT'

    def move_right(self):
        self.direction = 'RIGHT'

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

#Function to keep snake moving in the intended direction
    def slither(self):

        for i in range(self.length-1, 0, -1):
            self.y[i] = self.y[i-1]
            self.x[i] = self.x[i-1]

        if self.direction == 'UP':
            self.y[0] -= size_of_block
        if self.direction == 'DOWN':
            self.y[0] += size_of_block
        if self.direction == 'LEFT':
            self.x[0] -= size_of_block
        if self.direction == 'RIGHT':
            self.x[0] += size_of_block

        self.draw()

#Create Game Class
class Game:
    def __init__(self):
        # initialize pygame class/package
        pygame.init()
        pygame.mixer.init()
        self.play_background_music()
        #Creates and displays window
        self.game_background = pygame.display.set_mode((1000, 800))
        self.render_background()
        #create snake and apple objects in game
        self.snake = Snake(self.game_background, 1)
        self.snake.draw()
        self.apple = Apple(self.game_background)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + size_of_block:
            if y2 <= y1 < y2 + size_of_block:
                return True

        return False

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        background = pygame.image.load("resources/background.jpeg")
        self.game_background.blit(background, (0,0))
        pass

    #Animate function
    def anim(self):
        self.render_background()
        self.snake.slither()
        self.apple.draw()
        self.score_display()
        pygame.display.flip()

        #snake picks up apple/collides with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        #snake collides with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game Over"

    def score_display(self):
        font = pygame.font.SysFont('times new roman',30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.game_background.blit(score, (800,10))

    def game_over(self):
        self.render_background()
        font = pygame.font.SysFont('times new roman', 30)
        line1 = font.render(f"Game Over! Final Score: {self.snake.length}", True, (255, 255, 255))
        self.game_background.blit(line1, (200, 300))
        line2 = font.render("Press ENTER to play again. To EXIT press ESC.", True, (255, 255, 255))
        self.game_background.blit(line2, (200, 350))
        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.game_background, 1)
        self.apple = Apple(self.game_background)

    def run_game(self):
        game_running = True
        pause = False
        while game_running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        game_running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    game_running = False

            try:
                if not pause:
                    self.anim()
            except Exception as e:
                self.game_over()
                pause = True
                self.reset()

            time.sleep(0.2)


if __name__ == '__main__':
    game = Game()
    game.run_game()

