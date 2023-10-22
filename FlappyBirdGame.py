import pygame, sys, random

pygame.init()


class Background:
    def __init__(self):
        self.sky_surf = pygame.image.load("background-day.png").convert()
        self.sky_surf = pygame.transform.scale(self.sky_surf, (403.2, 716.8))

        self.ground_surf = pygame.image.load("ground.png").convert()
        self.ground_surf = pygame.transform.scale(self.ground_surf, (470.4, 156.8))

        self.ground_x = 0

    def draw_sky(self):
        screen.blit(self.sky_surf, (0, 0))

    def draw_ground(self):
        self.ground_x += -screen_speed
        screen.blit(self.ground_surf, (self.ground_x, screen_height - 156.8))
        screen.blit(self.ground_surf, (self.ground_x + 336 * 1.4, screen_height - 156.8))
        if self.ground_x <= -470.4:
            self.ground_x = 0


class Bird:
    def __init__(self):
        self.bird1_surf = pygame.image.load("bird-upflap.png").convert()
        self.bird1_surf = pygame.transform.scale(self.bird1_surf, (47.6, 33.6))
        self.bird2_surf = pygame.image.load("bird-midflap.png").convert()
        self.bird2_surf = pygame.transform.scale(self.bird2_surf, (47.6, 33.6))
        self.bird3_surf = pygame.image.load("bird-downflap.png").convert()
        self.bird3_surf = pygame.transform.scale(self.bird3_surf, (47.6, 33.6))
        self.bird_list = [self.bird1_surf, self.bird2_surf, self.bird3_surf]
        self.bird_rect = self.bird1_surf.get_rect(center=(100, screen_height // 3))
        self.gravity = 0

    def draw_bird(self):
        self.bird_surf = self.animate_bird()
        self.bird_surf = pygame.transform.rotate(self.bird_surf, -(self.gravity * 4))
        screen.blit(self.bird_surf, self.bird_rect)

    def move_bird(self):
        self.gravity += gravity_fall
        self.bird_rect.y += self.gravity

        if self.bird_rect.bottom >= screen_height - 156.8:
            self.bird_rect.bottom = screen_height - 156.8

    def animate_bird(self):
        global bird_index
        new_bird_surf = self.bird_list[int(bird_index)]
        bird_index += 0.1
        if bird_index >= len(self.bird_list):
            bird_index = 0

        return new_bird_surf


class Pipes:
    def __init__(self):
        self.pipe_surf = pygame.image.load("pipe-green.png").convert()
        self.pipe_surf_1 = pygame.transform.scale(self.pipe_surf, (72.8, 448))
        self.pipe_surf_2 = pygame.transform.flip(self.pipe_surf_1, False, True)

        self.pipe_rect_1_list = []
        self.pipe_rect_2_list = []

        self.pipe_vertical_distance = 130

    def make_pipe(self):
        global del_list

        pipe_height = random.choice([200, 300, 400, 500])

        self.pipe_rect_1 = self.pipe_surf_1.get_rect(midtop=(600, pipe_height))
        self.pipe_rect_2 = self.pipe_surf_2.get_rect(midbottom=(600, pipe_height - self.pipe_vertical_distance))
        self.pipe_rect_1_list.append(self.pipe_rect_1)
        self.pipe_rect_2_list.append(self.pipe_rect_2)


        if self.pipe_rect_1_list[0].x <= -600:  # the total no. of rects is never > 4
            self.pipe_rect_1_list.pop(0)
            self.pipe_rect_2_list.pop(0)

    def draw_pipe(self):
        for i in range(len(self.pipe_rect_1_list)):
            screen.blit(self.pipe_surf_1, self.pipe_rect_1_list[i])
            screen.blit(self.pipe_surf_2, self.pipe_rect_2_list[i])

    def move_pipe(self):
        for i in range(len(self.pipe_rect_1_list)):
            self.pipe_rect_1_list[i].x += -screen_speed
            self.pipe_rect_2_list[i].x += -screen_speed


class Main:
    def __init__(self):
        self.bg = Background()
        self.bird = Bird()
        self.pipes = Pipes()

    def update(self):
        self.bg.draw_sky()

        self.bird.draw_bird()
        self.bird.move_bird()

        self.pipes.draw_pipe()
        self.pipes.move_pipe()

        self.bg.draw_ground()

        self.collision()
        self.score2()

    def collision(self):
        global screen_window
        for i in range(len(self.pipes.pipe_rect_1_list)):
            if self.bird.bird_rect.colliderect(self.pipes.pipe_rect_1_list[i]) or self.bird.bird_rect.colliderect(self.pipes.pipe_rect_2_list[i]) or self.bird.bird_rect.bottom >= screen_height - 156.8 or self.bird.bird_rect.top <= -100:
                sound_die.play()
                screen_window = "end"

    def score(self):
        global score_value
        for i in self.pipes.pipe_rect_1_list:
            if self.bird.bird_rect.center[0] >= i.midleft[0]:
                score_value = self.pipes.pipe_rect_1_list.index(i) + 1

        score_font = font_medium.render(str(score_value), True, (0, 0, 0))
        score_font_rect = score_font.get_rect(midtop=(screen_width / 2, 20))
        screen.blit(score_font, score_font_rect)

    def score2(self):
        global score_value, score_start
        if len(self.pipes.pipe_rect_1_list) > 0:
            if self.bird.bird_rect.center[0] >= self.pipes.pipe_rect_1_list[0].midleft[0]:
                if score_start:
                    score_value = 1
                    score_start = False
                score_value += 0.0057

        score_font = font_medium.render(str(int(score_value)), True, (0, 0, 0))
        score_font_rect = score_font.get_rect(midtop=(screen_width / 2, 20))
        screen.blit(score_font, score_font_rect)


screen_width = 403.2
screen_height = 716.8
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font_medium = pygame.font.Font("freesansbold.ttf", 50)

main_game = Main()

gravity_jump = -3.5
gravity_fall = 0.12
screen_speed = 2
bird_index = 0
del_list = 0

pipe_spawn = pygame.USEREVENT
pygame.time.set_timer(pipe_spawn, 1300)
score_start = True

screen_window = "start"

img_start = pygame.image.load("gamestart.png")
img_start = pygame.transform.scale(img_start, (screen_width, screen_height))
img_end = pygame.image.load("gameover.png")
img_end_rect = img_end.get_rect(center=(screen_width / 2, screen_height / 2))

sound_die = pygame.mixer.Sound("sound_sfx_die.wav")
sound_point = pygame.mixer.Sound("sound_sfx_point.wav")
sound_wing = pygame.mixer.Sound("sound_sfx_wing.wav")

score_value = 0
current_time = 0

while True:
    if screen_window == "start":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    screen_window = "game"
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen_window = "game"

        screen.fill((0, 0, 0))
        screen.blit(img_start, (0, 0))


    if screen_window == "game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_game.bird.gravity = gravity_jump
                    sound_wing.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                main_game.bird.gravity = gravity_jump
                sound_wing.play()

            if event.type == pipe_spawn:
                main_game.pipes.make_pipe()

        main_game.update()


    if screen_window == "end":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    screen_window = "start"
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen_window = "start"

        screen.fill((0, 0, 0))
        screen.blit(img_end, img_end_rect)

        main_game.pipes.pipe_rect_1_list = []
        main_game.pipes.pipe_rect_2_list = []
        main_game.bird.bird_rect.center = (100, screen_height//3)
        main_game.bird.gravity = gravity_fall
        score_value = 0

    pygame.display.update()
    clock.tick(130)
