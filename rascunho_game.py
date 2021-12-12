import pygame
import os
import random


def main():
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600

    game_speed = 20

    # Imagens que serão utilizadas
    run_animation = []

    jump_animation = []

    background_image = pygame.image.load(os.path.join("Assets/background", "bg.png"))

    projectile_image = pygame.image.load(os.path.join("Assets/projectile", "Aceito.png"))

    obstacle_images = [pygame.image.load(os.path.join("Assets/barrier", "Wrong.png")),
                       pygame.image.load(os.path.join("Assets/barrier", "Runtime_Error.png"))]

    img_coins = [pygame.image.load(os.path.join("Assets/collectables", "zero.png")),
                 pygame.image.load(os.path.join("Assets/collectables", "one.png"))]

    up, down = pygame.image.load(os.path.join("Assets/enemy", "Dikastis_up.png")), pygame.image.load(
        os.path.join("Assets/enemy", "Dikastis_down.png"))
    up, down = pygame.transform.scale(up, (80, 130)), pygame.transform.scale(down, (100, 130))

    dikastis_animation = [up, down]

    destruction_animation = []

    for i in os.listdir("Assets/destroy"):
        destro = pygame.image.load(os.path.join("Assets/destroy", f"{i}"))
        destro_scaled = pygame.transform.scale(destro, (80, 130))
        destruction_animation.append(destro_scaled)

    for i in os.listdir("Assets/player/run"):
        run = pygame.image.load(os.path.join("Assets/player/run", f"{i}"))
        run_scaled = pygame.transform.scale(run, (100, 125))
        run_animation.append(run_scaled)

    for i in os.listdir("Assets/player/jump"):
        jump = pygame.image.load(os.path.join("Assets/player/jump", f"{i}"))
        jump_scaled = pygame.transform.scale(jump, (100, 125))
        jump_animation.append(jump_scaled)

    class BG(object):
        def __init__(self):
            self.x = 0
            self.y = 0

            self.bg_img = background_image
            self.bg_width = self.bg_img.get_width()

        def update(self, game_speed, SCREEN):
            if self.x <= -self.bg_width:
                SCREEN.blit(self.bg_img, (self.bg_width + self.x, self.y))
                self.x = 0
            self.x -= game_speed

        def draw(self, SCREEN):
            SCREEN.blit(self.bg_img, (self.x, self.y))
            SCREEN.blit(self.bg_img, (self.bg_width + self.x, self.y))

    class player(object):
        def __init__(self, y):
            self.x = 50
            self.y = y

            self.run_img = run_animation
            self.jump_img = jump_animation
            self.stepindex = 1
            self.isJump = False
            self.isrun = True
            self.stop = 0

            self.image = self.run_img[0]
            self.boy_rect = self.image.get_rect()
            self.boy_rect.x = self.x
            self.boy_rect.y = self.y

        # Atualiza as informações do player a cada loop
        def update(self, userInput):
            if self.isrun:
                self.run()
            if self.isJump:
                self.jump()
            if self.isJump:
                self.isrun = False

        # Animação de corrida
        def run(self):
            self.image = self.run_img[self.stepindex // 2]
            self.boy_rect.x = self.x
            self.boy_rect.y = self.y
            if self.stepindex < len(run_animation):
                self.stepindex += 1
            else:
                self.stepindex = 0

        # Animação do pulo
        def jump(self):
            self.image = self.jump_img[self.stepindex // 2]
            self.boy_rect.x = self.x
            self.boy_rect.y = self.y
            if self.stepindex < len(jump_animation):
                self.stepindex += 1
            else:
                self.stepindex = 0

        def draw(self, SCREEN):
            SCREEN.blit(self.image, (self.boy_rect.x, self.boy_rect.y))

    class projectile(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.vel = 40

            self.image = projectile_image
            self.proj_rect = self.image.get_rect()
            self.proj_rect.x = self.x
            self.proj_rect.y = self.y

        def draw(self, SCREEN):
            SCREEN.blit(self.image, (self.proj_rect.x, self.proj_rect.y))

    class obstacle:
        def __init__(self, image, type, category):
            self.image = image
            self.type = type
            self.category = category
            self.rect = self.image[self.type].get_rect()
            self.rect.x = 1000

        def update(self):
            self.rect.x -= game_speed
            if self.rect.x < -self.rect.width:
                obstacles.pop()

        def draw(self, SCREEN):
            SCREEN.blit(self.image[self.type], (self.rect.x, self.rect.y))

    class unacceptable(obstacle):
        def __init__(self, image):
            self.type = random.randint(0, 1)
            self.category = "obstacle"
            super().__init__(image, self.type, self.category)
            self.rect.y = 445

    class dikastis(obstacle):
        def __init__(self, image):
            self.type = 0
            self.category = "enemy"
            super().__init__(image, self.type, self.category)
            self.rect.y = random.randint(220, 340)
            self.index = 0

        def draw(self, SCREEN):
            SCREEN.blit(self.image[self.index // 2], self.rect)
            if self.index > 1:
                self.index = 0
            self.index += 1

    class collecty:
        def __init__(self, image, type, category):
            self.image = image
            self.type = type
            self.category = category
            self.rect = self.image[self.type].get_rect()
            self.rect.x = 1000

        def update(self):
            self.rect.x -= game_speed
            if self.rect.x < -self.rect.width:
                try:
                    collectable.pop()
                except:
                    None

        def draw(self, SCREEN):
            SCREEN.blit(self.image[self.type], (self.rect.x, self.rect.y))

    class coin(collecty):
        def __init__(self, image):
            self.type = random.randint(0, 1)
            self.category = "coin"
            super().__init__(image, self.type, self.category)
            self.rect.y = random.randint(230, 350)

    jumpcount = 10

    pygame.init()

    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption("Boy do Bit")

    font = pygame.font.SysFont('comicsans', 20, True)

    # Criando objeto boy --> (player)
    boy = player(400)
    background = BG()

    bullets = []
    obstacles = []
    collectable = []

    wait_animation_player = 0
    wait_animation_enemy = 0

    time = 0
    lifes = 3
    zeros = 0
    ones = 0

    run = True
    while run:
        win.blit(background_image, (0, 0))

        pygame.time.delay(50)

        time += 1

        # Aumenta a dificuldade (velocidade dos objetos) conforme o tempo passa
        if time % 50 == 0:
            game_speed += 0.6

        # Exclui o check quando ele sai da visão
        for bullet in bullets:
            if bullet.x < 1000 and bullet.x > 0:
                bullet.x += bullet.vel
                bullet.proj_rect.x += bullet.vel

            else:
                bullets.pop(bullets.index(bullet))

        # Fecha o jogo quando o player clica no X
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        userInput = pygame.key.get_pressed()

        # Atira um check quando o player aperta ESPAÇO
        if userInput[pygame.K_SPACE]:
            if len(bullets) < 1:
                bullets.append(projectile(165, boy.y + 55))

        # Pula quando o player aperta W
        if not (boy.isJump):
            if userInput[pygame.K_w]:
                boy.isJump = True

        else:
            if jumpcount >= -10:
                neg = 1

                if jumpcount < 0:
                    neg = -1

                boy.y -= 0.40 * jumpcount ** 2 * neg

                jumpcount -= 1

            else:
                boy.isJump = False
                boy.isrun = True
                jumpcount = 10

        win.fill((255, 255, 255))
        background.draw(win)
        background.update(game_speed, win)

        boy.draw(win)
        boy.update(userInput)

        for bullet in bullets:
            bullet.draw(win)

        # Cria um obstáculo aleatório
        if len(obstacles) == 0:
            if random.randint(0, 1) == 0:
                obstacles.append(unacceptable(obstacle_images))

            else:
                obstacles.append(dikastis(dikastis_animation))

        for obstacle in obstacles:
            obstacle.draw(win)
            obstacle.update()

            # O player perde uma vida quando bate em algum obstáculo
            if boy.boy_rect.colliderect(obstacle.rect):
                obstacles.pop(obstacles.index(obstacle))
                lifes -= 1

            # Destrói um Dikastis se o player o atingir com um check
            for bullet in bullets:
                if bullet.proj_rect.colliderect(obstacle.rect) and obstacle.category == "enemy":
                    try:
                        obstacles.pop(obstacles.index(obstacle))
                    except:
                        None

                    bullets.pop(bullets.index(bullet)
                                )
                    bullet.draw(win)
                    obstacle.draw(win)

        if len(collectable) == 0:
            collectable.append(coin(img_coins))

        # Aumenta a pontuação conforme o usuário coleta 0's e 1's
        for collect in collectable:
            collect.draw(win)
            collect.update()

            if boy.boy_rect.colliderect(collect.rect):
                if collect.type == 0:
                    zeros += 1

                if collect.type == 1:
                    ones += 1

                collectable.pop(collectable.index(collect))

        # Mostra na tela os status de vidas e bits coletados
        text0 = font.render('Lifes: ' + str(lifes), True, (0, 0, 0))
        text1 = font.render('0: ' + str(zeros), True, (0, 0, 0))
        text2 = font.render('1: ' + str(ones), True, (0, 0, 0))

        win.blit(text0, (50, 50))
        win.blit(text1, (50, 80))
        win.blit(text2, (50, 100))

        pygame.display.update()

        if lifes == 0:
            Game_Over(zeros, ones)

    pygame.quit()


def Game_Over(zeros=0, ones=0):
    pygame.init()

    win = pygame.display.set_mode((1000, 600))

    pygame.display.set_caption("Boy do Bit")

    font = pygame.font.SysFont('comicsans', 20, True)

    run = True
    while run:
        pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        userInput = pygame.key.get_pressed()

        if userInput[pygame.K_SPACE]:
            main()

        win.fill((255, 255, 255))

        # Mostra o menu de fim de jogo
        text0 = font.render('GAME OVER', True, (0, 0, 0))
        text1 = font.render("press 'space' to restart", True, (0, 0, 0))
        text_zeros = font.render("0's collected:" + str(zeros), True, (0, 0, 0))
        text_ones = font.render("1's collected:" + str(ones), True, (0, 0, 0))

        text0_rect = text0.get_rect(center=(500, 200))
        text1_rect = text1.get_rect(center=(500, 240))
        text_zeros_rect = text_zeros.get_rect(center=(500, 300))
        text_ones_rect = text_ones.get_rect(center=(500, 340))

        win.blit(text0, text0_rect)
        win.blit(text1, text1_rect)
        win.blit(text_zeros, text_zeros_rect)
        win.blit(text_ones, text_ones_rect)

        pygame.display.update()

    pygame.quit()


main()
