# Ābola klase
class Apple:
    def __init__(self):
        self.image = pygame.image.load("apple.png")
        self.image = pygame.transform.scale(self.image, (50, 70))
        self.x = random.randint(0, 600 - 50)
        self.y = -70
        self.speed = 5

    def update(self):
        self.y += self.speed
        if self.y > 800:
            self.reset()
            return True
        return False

    # āboļa pozicijas atjaunošana
    def reset(self):
        self.x = random.randint(0, 600 - 40)
        self.y = -70

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    # āboļa pozicijas noteikšana
    def get_rect(self):
        return pygame.Rect(self.x, self.y, 50, 70)

    # āboļa paātrinājums
    def accelerate(self):
        self.speed += 1

    # paātrinājuma izņemšana
    def remove_accel(self):
        self.speed = 5

class Bomb:
    def __init__(self):
        self.image = pygame.image.load("bomb.png")
        self.image = pygame.transform.scale(self.image, (50,70))
        self.x = random.randint(0, 600 - 50)
        self.y = -70
        self.speed = 6

    def update(self):
        self.y += self.speed
        if self.y > 800:
            self.reset()

    # bumbas pozicijas atjaunošana
    def reset(self):
        self.x = random.randint(0,600 - 50)
        self.y = -70

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    # bumbas pozicijas noteikšana
    def get_rect(self):
        return pygame.Rect(self.x, self.y, 50, 70)

    # bumbas paātrinājums
    def accelerate(self):
        self.speed += 1

    # paātrinājuma izņēmšana
    def remove_accel(self):
        self.speed = 6

import pygame
import random


# Instrukcijas klase
class Tip:
    def __init__(self):
        # Starta poga
        self.button_font = pygame.font.SysFont("Arial", 30)
        self.button_text = self.button_font.render("Start Game", True, (0, 0, 0))

        self.button_width = 200
        self.button_height = 60
        self.button_color = (255, 255, 255)
        self.button_hover_color = (200, 200, 200)

        self.button_x = (600 - self.button_width) // 2
        self.button_y = (1400 - self.button_height) // 2 + 50
        # paša instrukcija
        self.image = pygame.image.load("tip.png")
        self.image = pygame.transform.scale(self.image, (600, 700))
        self.x = 0
        self.y = 0


    def draw(self, window, mouse_pos):
        # instrukcijas izvade
        window.fill((50, 90, 50))
        window.blit(self.image, (self.x, self.y))

        # pogas izskata maiņa
        if self.is_hovered(mouse_pos):
            color = self.button_hover_color
        else:
            color = self.button_color

        button_rect = pygame.Rect(self.button_x, self.button_y, self.button_width, self.button_height)
        pygame.draw.rect(window, color, button_rect, border_radius=10)

        text_rect = self.button_text.get_rect(center=button_rect.center)
        window.blit(self.button_text, text_rect)

        pygame.display.update()

    # parbaude, vai pele ir uz pogas
    def is_hovered(self, mouse_pos):
        x, y = mouse_pos
        return (self.button_x <= x <= self.button_x + self.button_width) and (self.button_y <= y <= self.button_y + self.button_height)


# Rezultata klase
class Score:
    def __init__(self):
        # pats rezultāts
        self.score = 0
        # pogas izskats
        self.button_font = pygame.font.SysFont("Arial", 30)
        self.button_text = self.button_font.render("Retry", True, (0, 0, 0))

        self.button_width = 200
        self.button_height = 60
        self.button_color = (255, 255, 255)
        self.button_hover_color = (200, 200, 200)

        self.button_x = (600 - self.button_width) // 2
        self.button_y = (1000 - self.button_height) // 2

    def draw(self, window, mouse_pos):
        # pogas izskata maiņa
        if self.is_hovered(mouse_pos):
            color = self.button_hover_color
        else:
            color = self.button_color
        # pogas un rezultāta izvadīšana
        button_rect = pygame.Rect(self.button_x, self.button_y, self.button_width, self.button_height)
        pygame.draw.rect(window, color, button_rect, border_radius=10)
        text_rect = self.button_text.get_rect(center=button_rect.center)
        window.blit(self.button_text, text_rect)

        pygame.display.update()

    # parbaude, vai pele ir uz pogas
    def is_hovered(self, mouse_pos):
        x, y = mouse_pos
        return (self.button_x <= x <= self.button_x + self.button_width) and (self.button_y <= y <= self.button_y + self.button_height)

# pašas spēles klase
class Game:
    def __init__(self):
        # speles logs
        pygame.init()
        self.window = pygame.display.set_mode((600, 800))
        pygame.display.set_caption("Catch Apples")
        self.clock = pygame.time.Clock()
        self.run = True

        # spēlētāja (groza) izskāts
        self.player_image = pygame.image.load(" basket.png")
        self.player_image = pygame.transform.scale(self.player_image, (120, 70))
        self.player_x = 300
        self.player_y = 700
        self.player_speed = 7

        # spēles laikā rezultāts
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 32)

        # dzīves
        self.max_lives = 3
        self.lives = self.max_lives

        self.heart_image = pygame.image.load("life.png")
        self.heart_image = pygame.transform.scale(self.heart_image, (50, 50))

        self.heart_black_image = pygame.image.load("wasted.png")
        self.heart_black_image = pygame.transform.scale(self.heart_black_image, (50, 50))

        # ābols un bumba
        self.apple = Apple()
        self.bomb = Bomb()

        # spēles pirmais stavoklis
        self.state = "instruction"

        # instrukcijas un nobeiguma ekrani
        self.tip = Tip()
        self.scoreScreen = Score()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            # ievada loģika, ja spēle instrukcijas stāvokļā
            if self.state == "instruction":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.tip.is_hovered(mouse_pos):
                        self.state = "ingame"

            # ievada loģika, ja spēle nobeiguma stāvokļā
            if self.state == "game over":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.scoreScreen.is_hovered(mouse_pos):
                        self.state = "instruction"
                        self.score = 0
                        self.lives = self.max_lives
                        self.apple.remove_accel()
                        self.bomb.remove_accel()
                        self.apple.reset()
                        self.bomb.reset()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.run = False
        # ievada loģika, ja spēle aktivas spēles stāvokļā
        if self.state == "ingame":
            if keys[pygame.K_RIGHT]:
                self.player_x += self.player_speed
            if keys[pygame.K_LEFT]:
                self.player_x -= self.player_speed

    def update(self):
        if self.state == "ingame":
            # groza noteikšana
            self.player_x = max(-20, min(self.player_x, 600 - 100))
            self.bomb.update()
            missed = self.apple.update()
            if missed:
                self.lives -= 1

            # rezultāta palielināšana
            if self.get_player_rect().colliderect(self.apple.get_rect()):
                self.score += 100
                self.apple.reset()
                # āboļa un bumbas paātrināšana
                if self.score / 1000 == self.score // 1000:
                    self.apple.accelerate()
                    self.bomb.accelerate()

            # bumbas uzķēršana
            if self.get_player_rect().colliderect(self.bomb.get_rect()):
                self.lives -= 1
                self.bomb.reset()

            # spēles zaudējums
            if self.lives < 1:
                self.state = "game over"

        elif self.state == "instruction":
            pass

        elif self.state == "game over":
            pass

    # groza lokacijas noteikšana
    def get_player_rect(self):
        return pygame.Rect(self.player_x, self.player_y, 120, 70)

    def draw(self):
        if self.state == "ingame":
            # groza (spēlētāja), bumbas un āboļa attēlu izvade
            self.window.fill((50, 90, 50))
            self.window.blit(self.player_image, (self.player_x, self.player_y))
            self.apple.draw(self.window)
            self.bomb.draw(self.window)

            # dzivību izvade
            for i in range(self.max_lives):
                x = 600 - (i + 1) * (50 + 10)
                y = 10
                if i < self.lives:
                    self.window.blit(self.heart_image, (x, y))
                else:
                    self.window.blit(self.heart_black_image, (x, y))

            # spēles laikā rezultāta izvade
            pygame.draw.rect(self.window, (0, 0, 0), (5, 5, 200, 50), border_radius=8)
            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.window.blit(score_text, (15, 10))

            pygame.display.update()

        elif self.state == "instruction":
            # instrukcijas loga izvade
            mouse_pos = pygame.mouse.get_pos()
            self.tip.draw(self.window, mouse_pos)

        elif self.state == "game over":
            # teksta "Game Over" izvade
            self.window.fill((50, 0, 0))
            font = pygame.font.SysFont("Arial", 64)
            text = font.render("Game Over", True, (255, 255, 255))
            rect = text.get_rect(center=(600 // 2, 800 // 2))
            self.window.blit(text, rect)

            # rezultāta izvade
            font_score = pygame.font.SysFont("Arial", 40)
            score_text = font_score.render(f"Your Score: {self.score}", True, (255,255,255) )
            score_rect = score_text.get_rect(center=(600//2,800//2 -40))
            self.window.blit(score_text, score_rect)

            # jauna maģiņājuma pogas izvade
            mouse_pos = pygame.mouse.get_pos()
            self.scoreScreen.draw(self.window, mouse_pos)

            pygame.display.update()

    def run_game(self):
        while self.run:
            self.input()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run_game()
