import sys
import random
import pygame


class Collision:
    def __init__(self, screen, x, y, ):
        self.screen = screen
        self.x = x
        self.y = y


class Heart:
    def __init__(self, screen, x, y, image):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.hearts = []

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))


class Image:
    def __init__(self, screen, x, y, image):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))


class Coin:
    def __init__(self, screen, x, y, coin_image):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load(coin_image)
        self.coins = []

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def hit_by(self, player):
        coin_hit_box = pygame.Rect(self.x - 16, self.y - 16, (self.image.get_width() + 32), (self.image.get_height() + 32))
        # pygame.draw.rect(self.screen, (0, 0, 0), (self.x - 16, self.y - 16, (self.image.get_width() + 32), (self.image.get_height() + 32)))
        return coin_hit_box.collidepoint((player.x, player.y))


class Enemy:
    def __init__(self, screen, x, y, x_motion, y_motion, enemy_image, enemy_image2):
        self.screen = screen
        self.x = x
        self.y = y
        self.enemy_image = pygame.image.load(enemy_image)
        self.enemy_image2 = pygame.image.load(enemy_image2)
        self.x_motion = x_motion
        self.y_motion = y_motion
        self.speed = -11
        self.direction = 1

    def draw(self):
        current_image = self.enemy_image
        self.screen.blit(current_image, (self.x, self.y))

    def restart(self):
        self.x = 500
        self.y = 300
        self.direction = 1

    def hit_by(self, player):
        enemy_hit_box = pygame.Rect(self.x, self.y, self.enemy_image.get_width(), self.enemy_image.get_height())
        return enemy_hit_box.collidepoint((player.x, player.y))

    def sight(self, player):
        sight_up = pygame.Rect(self.x, self.y - 128, self.enemy_image.get_width(), 128)
        sight_down = pygame.Rect(self.x, self.y, self.enemy_image.get_width(), 128)
        sight_left = pygame.Rect(self.x - 512, self.y, 512, self.enemy_image.get_height())
        sight_right = pygame.Rect(self.x, self.y, 512, self.enemy_image.get_height())
        if sight_up.collidepoint((player.x, player.y)):
            # print(player.y)
            # print(self.check_wall_up(1))
            if player.y > self.check_wall_up(1):
                # print(self.check_wall_up(1))
                self.direction = 1
                return sight_up.collidepoint((player.x, player.y))
        if sight_down.collidepoint((player.x, player.y)):
            # print(self.check_wall_up(2))
            # print(player.y)
            if player.y < self.check_wall_up(2):
                self.direction = 2
                return sight_down.collidepoint((player.x, player.y))
        if sight_left.collidepoint((player.x, player.y)):
            if player.x > self.check_wall_up(3):
                self.direction = 3
                return sight_left.collidepoint((player.x, player.y))
        if sight_right.collidepoint((player.x, player.y)):
            if player.x < self.check_wall_up(4):
                self.direction = 4
                return sight_right.collidepoint((player.x, player.y))

    # returns the y cord of the wall
    def check_wall_up(self, loc):
        if loc == 1:
            s_y = self.y
            while (1024 > self.x > 0 and 0 < (s_y - 1) < 1024) and \
                    (not self.check_wall_enemy(self.x, s_y)):
                s_y -= 1
            return s_y
        if loc == 2:
            s_y2 = self.y
            # print("self.y: ", self.y)
            while ( # 1024 > self.x > 0
                   #and
                   #0 < (s_y2 + self.enemy_image.get_height() + 1) < 1024) \
                    #and
                    not self.check_wall_enemy(self.x, s_y2 + 1)):
                s_y2 += 1
            #     print(" in while. s_y2:", s_y2)
            #
            # print("right before return. s_y2: ", s_y2)
            return s_y2
        if loc == 3:
            s_x = self.x
            while not self.check_wall_enemy(s_x - 1, self.y):
                s_x -= 1
            return s_x
        if loc == 4:
            s_x2 = self.x
            while not self.check_wall_enemy(s_x2 + 1, self.y):
                s_x2 += 1
            return s_x2

    def check_wall_enemy(self, x, y):
        # print("[check_wall] x, y, color: ", x, y, self.screen.get_at((x, y)))
        if self.screen.get_at((x, y)) == pygame.Color("black"):
            return True
        else:
            return False

    def get_next_wall_loc_enemy(self, direction):
        if direction == 1:  # 1 means going up
            temp_y = self.y
            while (1024 > self.x > 0 and 0 < (temp_y - 1) < 1024) and \
                    (not self.check_wall_enemy(self.x, temp_y - 1)):
                temp_y -= 1
            return temp_y
        elif direction == 2:  # 2 down
            temp_y2 = self.y
            while (1024 > self.x > 0 and 0 < (temp_y2 + self.enemy_image.get_height() + 1) < 1024) and \
                    (not self.check_wall_enemy(self.x, temp_y2 + self.enemy_image.get_height() + 1)):
                temp_y2 += 1
            return temp_y2
        elif direction == 3:
            temp_x = self.x
            while (1024 > (temp_x - 1) > 0 and 0 < self.y < 1024) and \
                    (not self.check_wall_enemy(temp_x - 1, self.y)):
                temp_x -= 1
            return temp_x
        elif direction == 4:  # 4: right
            temp_x2 = self.x
            while ((temp_x2 + self.enemy_image.get_width() + 1) < 1024 and (
                    temp_x2 + self.enemy_image.get_width() + 1) > 0 and 0 < self.y < 1024) and \
                    (not self.check_wall_enemy(temp_x2 + self.enemy_image.get_width() + 1, self.y)):
                temp_x2 += 1
            return temp_x2

    def turn(self, rand):
        if rand == (-1):
            # while not self.check_wall_enemy(self.x, self.y):
            # print("right")
            self.x = self.x - self.speed

        if rand == 1:
            # print("left")
            self.x = self.x + self.speed

        if rand == 2:
            # print("up")
            self.y = self.y + self.speed

        if rand == 3:
            # print("down")
            self.y = self.y - self.speed

    def move(self):
        if self.direction == 1:
            if self.y + self.speed < self.get_next_wall_loc_enemy(1):
                self.y = self.get_next_wall_loc_enemy(1) + 1
                if self.y == self.get_next_wall_loc_enemy(1) + 1:
                    # print("ok")
                    randomizer = random.randrange(-1, 2)
                    if randomizer == -1:
                        self.direction = 4
                        self.turn(randomizer)
                    elif randomizer == 1:
                        self.direction = 3
                        self.turn(randomizer)
            else:
                self.y = self.y + self.speed

        elif self.direction == 2:
            randomizer = 3
            if self.y - self.speed > self.get_next_wall_loc_enemy(2):
                self.y = self.get_next_wall_loc_enemy(2) - 1
                if self.y == self.get_next_wall_loc_enemy(2) - 1:
                    # print("ok")
                    randomizer = random.randrange(-1, 2)
                    if randomizer == -1:
                        self.direction = 4
                        self.turn(randomizer)
                    elif randomizer == 1:
                        self.direction = 3
                        self.turn(randomizer)
            else:
                self.turn(randomizer)

        elif self.direction == 4:
            randomizer = -1
            if self.x - self.speed > self.get_next_wall_loc_enemy(4):
                self.x = self.get_next_wall_loc_enemy(4) - 1
                if self.x == self.get_next_wall_loc_enemy(4) - 1:
                    # print("ok")
                    randomizer = random.randrange(2, 4)
                    if randomizer == 2:
                        self.direction = 1
                        self.turn(randomizer)
                    elif randomizer == 3:
                        self.direction = 2
                        self.turn(randomizer)
            else:
                self.turn(randomizer)

        elif self.direction == 3:
            randomizer = 1
            if self.x + self.speed < self.get_next_wall_loc_enemy(3):
                self.x = self.get_next_wall_loc_enemy(3) + 1
                if self.x == self.get_next_wall_loc_enemy(3) + 1:
                    # print("ok")
                    randomizer = random.randrange(2, 4)
                    if randomizer == 2:
                        self.direction = 1
                        self.turn(randomizer)
                    elif randomizer == 3:
                        self.direction = 2
                        self.turn(randomizer)
            else:
                self.turn(randomizer)

        # if self.direction == 2:
        # try making radius of no black around hit box
        # if self.y + self.enemy_image.get_height() < 1024:
        #     self.y -= self.y_motion
        #     self.y_motion = 0
        #     self.x_motion = 5 * randomizer
        # elif self.x + self.enemy_image.get_width() > 1024:
        #     self.x -= self.x_motion
        #     self.y_motion = 5 * randomizer
        #     self.x_motion = 0
        # elif self.x < 0:
        #     self.x -= self.x_motion
        #     self.y_motion = 5 * randomizer
        #     self.x_motion = 0
        # elif self.y < 0:
        #     self.y -= self.y_motion
        #     self.y_motion = 0
        #     self.x_motion = 5 * randomizer
        # self.y = self.y + self.y_motion
        # self.x += self.x_motion


class Player:
    def __init__(self, screen, x, y, player_image, player_image2):
        self.screen = screen
        self.x = x
        self.y = y
        self.speed = 12
        self.player_image = pygame.image.load(player_image)
        self.player_image2 = pygame.image.load(player_image2)

    def check_wall(self, x, y):

        # debug
        # print("check_wall (x, y)", x, y)

        if self.screen.get_at((x, y)) == pygame.Color("black"):
            return True
        else:
            return False

            # if x < 1024 and x > 0 and y > 0 and y < 1024:
            # or self.screen.get_at((x + self.player_image.get_width(), y)) == pygame.Color("black")

    def get_next_wall_loc(self, direction):
        if direction == 1:  # 1 means going up
            temp_y = self.y

            while (1024 > self.x > 0 and 0 < (temp_y - 1) < 1024) and (not self.check_wall(self.x, temp_y - 1))\
                    and (not self.check_wall(self.x + self.player_image.get_width() - 5, temp_y - 1)):
                temp_y -= 1
            return temp_y
        elif direction == 2:  # 2 down
            temp_y2 = self.y
            while (1024 > self.x > 0 and 0 < (temp_y2 + self.player_image.get_height() + 1) < 1024) and \
                    (not self.check_wall(self.x, temp_y2 + self.player_image.get_height() + 1)) and \
                    (not self.check_wall(self.x + self.player_image.get_width() - 5,
                                         temp_y2 + self.player_image.get_height() + 1)):
                temp_y2 += 1
            return temp_y2
        elif direction == 3:
            temp_x = self.x
            while (1024 > (temp_x - 1) > 0 and 0 < self.y < 1024) and \
                    (not self.check_wall(temp_x - 1, self.y)) and \
                    (not self.check_wall(temp_x - 1, self.y + self.player_image.get_height() - 3)):
                temp_x -= 1
            return temp_x
        elif direction == 4:  # 4: right
            temp_x2 = self.x
            while (1024 > (temp_x2 + self.player_image.get_width() + 1) > 0 and 0 < self.y < 1024) and \
                    (not self.check_wall(temp_x2 + self.player_image.get_width() + 1, self.y)) and \
                    (not self.check_wall(temp_x2 + self.player_image.get_width() + 1,
                                         self.y + self.player_image.get_height() - 3)):
                temp_x2 += 1
            return temp_x2

    def move(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP]:
            if self.y - self.speed < self.get_next_wall_loc(1):
                self.y = self.get_next_wall_loc(1) + 1
            else:
                self.y = self.y - self.speed

            # if self.check_wall(self.x, self.y - 1):
            #     self.y += 1
            # if self.y - (self.player_image.get_height() / 8) < 0:
            #     self.y += self.speed
            # else:

        elif key_pressed[pygame.K_DOWN]:
            if self.y + self.speed > self.get_next_wall_loc(2):
                self.y = self.get_next_wall_loc(2) - 1
            else:
                self.y = self.y + self.speed

            # self.y += self.speed
            # if self.check_wall(self.x, self.y + self.player_image.get_height() + 1):
            #     self.y = self.y - 1
            # if self.y + (self.player_image.get_height()) > 1024:
            #     self.y -= self.speed
            # elif:

        elif key_pressed[pygame.K_LEFT]:
            if self.x - self.speed < self.get_next_wall_loc(3):
                self.x = self.get_next_wall_loc(3) + 1
            else:
                self.x = self.x - self.speed

            # self.x -= 12
            # if self.check_wall(self.x - 1, self.y):
            #     self.x = self.x + 12
            # if self.x < 0:
            #     self.x += self.speed
            # else:

        elif key_pressed[pygame.K_RIGHT]:
            if self.x + self.speed > self.get_next_wall_loc(4):
                self.x = self.get_next_wall_loc(4) - 1
            else:
                self.x = self.x + self.speed

            # self.x += self.speed
            # if self.check_wall(self.x + 1, self.y):
            #     self.x = self.x - 12
            # if self.x + (self.player_image.get_width()) > 1024:
            #     self.x -= self.speed
            # else:

    def draw(self, time):
        if time >= 15:
            current_image = self.player_image2
        else:
            current_image = self.player_image
        self.screen.blit(current_image, (self.x, self.y))

    def restart(self):
        self.x = 500
        self.y = 600


class Wall:
    def __init__(self, screen, x, y, wall_image):
        self.screen = screen
        self.x = x
        self.y = y
        self.wall_image = pygame.image.load(wall_image)

    def draw(self):
        current_image = self.wall_image
        self.screen.blit(current_image, (self.x, self.y))


def main():
    pygame.init()
    pygame.display.set_caption("Hotel 76")
    screen = pygame.display.set_mode((1024, 1024))
    clock = pygame.time.Clock()
    font1 = pygame.font.Font(None, 30)
    font2 = pygame.font.Font(None, 20)

    enemy1 = Enemy(screen, 500, 300, 0, 5, "enemy_car.png", "enemy_car.png")
    player1 = Player(screen, 500, 600, "pixil-frame-0.png", "pixil-frame-0 (1).png")
    q1 = Wall(screen, 0, 0, "2house1u.png")
    q2 = Wall(screen, 512, 0, "2house2u.png")
    q3 = Wall(screen, 0, 512, "2house3.png")
    q4 = Wall(screen, 512, 512, "2house4u.png")
    enemy2 = Enemy(screen, 500, 300, 0, 5, "enemy_car.png", "enemy_car.png")
    enemy3 = Enemy(screen, 500, 300, 0, 5, "enemy_car.png", "enemy_car.png")
    coin2 = Image(screen,  380, 457, "coin1.png")
    coin3 = Image(screen, 410, 473, "coin1.png")
    coin_pos = [(505, 170), (505, 504), (505, 285), (440, 665), (408, 665), (376, 665), (570, 665), (602, 665),
                (634, 665), (762, 224), (248, 224), (25, 248), (25, 88), (986, 248), (986, 88)]
                # (600, 665), (630, 665), (345, 570), (345, 605), (345, 635), (345, 667), (345, 698), (345, 730),
                # (665, 667), (665, 698), (665, 730), (665, 635), (665, 605), (665, 570)]
                # (377, 730), (409, 730),
                # (441, 730), (473, 730), (505, 730), (537, 730), (569, 730), (601, 730), (633, 730),
                # (121, 760),
                # (153, 760),
                # (185, 760), (217, 760),
                # (249, 760), (281, 760), (313, 760), (345, 760),
                # (377, 760), (409, 760), (441, 760), (473, 760), (505, 760), (537, 760), (569, 760), (601, 760),
                # (633, 760), (665, 760), (697, 760), (729, 760), (761, 760), (793, 760)
    coin_list = []
    coin_left = 0
    coin_got = 0
    hit_count = 0
    coinsound = pygame.mixer.Sound("Coin sound.wav")
    car_sound = pygame.mixer.Sound("Dababy Let's Go Sound Effect.wav")
    for coin in coin_pos:
        coin1 = Coin(screen, coin[0], coin[1], "coin1.png")
        coin_left += 1
        coin_list.append(coin1)

    heart_pos = [(548, 457), (580, 457), (612, 457)]
    heart_list = []
    for heart in heart_pos:
        heart1 = Heart(screen, heart[0], heart[1], "heart2.png")
        heart_list.append(heart1)

    time = 0
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_pos = event.pos
            x = event.pos[0]
            y = event.pos[1]
            print(click_pos[0], click_pos[1])
            print(event.pos[0], event.pos[1])


        time += 1
        if time >= 30:
            time = 0

        if enemy1.hit_by(player1) or enemy2.hit_by(player1) or enemy3.hit_by(player1):
            # print("hit")
            hit_count += 1
            del heart_list[-1]
            car_sound.play()
            # print(hit_count)
            player1.restart()
            enemy1.restart()
            enemy2.restart()
            enemy3.restart()

        screen.fill((255, 255, 255))

        q1.draw()
        q2.draw()
        q3.draw()
        q4.draw()

        if coin_left > 0 and hit_count < 3:
            player1.move()
            player1.draw(time)
            enemy1.move()
            enemy1.draw()
            enemy2.move()
            enemy2.draw()
            enemy3.move()
            enemy3.draw()
            coin2.draw()
            for heart in heart_list:
                heart.draw()
            caption1 = font1.render("coins left:", True, (255, 255, 255))
            screen.blit(caption1, (400, 455))
            caption2 = font1.render(str(coin_left), True, (255, 255, 255))
            screen.blit(caption2, (510, 456))
        if hit_count > 2:
            caption3 = font1.render("GAME OVER: YOU LOSE", True, (255, 255, 255))
            screen.blit(caption3, (390, 450))
            caption5 = font2.render("COINS COLLECTED:", True, (255, 255, 255))
            caption6 = font2.render(str(coin_got), True, (255, 255, 255))
            screen.blit(caption5, (430, 475))
            screen.blit(caption6, (570, 475))
            coin3.draw()
        if coin_left == 0:
            caption4 = font1.render("GAME OVER: YOU WIN", True, (255, 255, 255))
            screen.blit(caption4, (395, 450))
            caption5 = font2.render("COINS COLLECTED:", True, (255, 255, 255))
            caption6 = font2.render(str(coin_got), True, (255, 255, 255))
            screen.blit(caption5, (430, 475))
            screen.blit(caption6, (570, 475))
            coin3.draw()
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 16, 1024))
        pygame.draw.rect(screen, (0, 0, 0), (1008, 0, 16, 1024))
        for coin in coin_list:
            coin.draw()
            if coin.hit_by(player1):
                # print("hit coin")
                coin_left -= 1
                coin_got += 1
                # print(coin_left)
                coinsound.play()
                coin_list.remove(coin)



        if enemy1.sight(player1) or enemy2.sight(player1) or enemy3.sight(player1):
            print("lesgoooooo")

        # if coin_left == 0:
        #     pygame.draw.rect(screen, (0, 0, 0), (100, 100, 824, 824))
        #
        # if hit_count > 2:
        #     pygame.draw.rect(screen, (0, 0, 0), (100, 100, 824, 824))

        # pygame.draw.rect(screen, (255, 255, 255), (360, 500, 128, 10))

        pygame.display.update()


main()
