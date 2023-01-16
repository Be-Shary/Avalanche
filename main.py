import random
import time
import pgzrun


game_mode = 0 # 0 title screen; 1 game; 2 game over
WIDTH = 640
HEIGHT = 480
paddle_size = 80
rocks_speed = 2
level = 1
misses = 0
score = 0
high_score = 0
delay = 0
rocks_drop = 0
paddles = []
rocks = [[],[],[],[],[],[]]
falling_rocks = []


class Paddle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def draw(self):
        screen.draw.filled_rect(Rect((self.x, self.y), (self.size, 15)), color=(80, 220, 255))


class Rock:
    def __init__(self, x, y, size, speed, color):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.is_move = False
        self.color = color

    def move(self):
        if self.is_move:
            self.y += self.speed
            if self.y >= HEIGHT:
                return True
            return False

    def draw(self):
        screen.draw.filled_circle((self.x, self.y), self.size, color=self.color)

    def collide(self, list):
        for paddle in list:
            if self.x - self.size < paddle.x + paddle.size and self.x + self.size > paddle.x and self.y < paddle.y + 15 and self.size + self. y > paddle.y:
                return True
        return False


def reset_game():
    global delay, rocks_drop, misses, score, level, falling_rocks, rocks_speed
    level = 1
    misses = 0
    score = 0
    delay = 0
    rocks_drop = 0
    rocks_speed = 2
    make_level(rocks_speed)
    make_paddles(len(rocks), paddle_size, HEIGHT - 40)
    falling_rocks.clear()


def make_level(speed):
    global rocks
    y = 40
    size = 5
    c = 0
    color = [(220, 220, 0), (200, 100, 40), (80, 220, 255)]
    rocks = [[],[],[],[],[],[]]
    for row in range(len(rocks)):
        x = 10
        for _ in range(round(WIDTH / 20)):
            rock = Rock(x, y, size, speed, color[c])
            rocks[row].append(rock)
            x += 20
        y += 15
        if row % 2:
            size += 1
            c += 1


def make_paddles(quantity, size , y):
    global paddles
    paddles = []
    for _ in range(quantity):
        paddle = Paddle(WIDTH / 2, y, size)
        paddles.append(paddle)
        y -= 45


def on_mouse_move(pos):
    global game_mode
    if game_mode == 1:
        if not pos[0] < 0 and not pos[0] > WIDTH - paddles[0].size:
            for paddle in paddles:
                paddle.x = pos[0]


def on_mouse_down():
    global game_mode
    if game_mode == 0:
        game_mode = 1
    elif game_mode == 2:
        game_mode = 0

def update():
    global delay, rocks_drop, game_mode, misses, score, level, high_score

    if game_mode == 1:
        delay += 1

        if not len(rocks):
            if level < 4:
                level += 1
            make_level(rocks_speed + level)
            make_paddles(len(rocks) - (1 + level), paddle_size, HEIGHT - 40)

        if len(falling_rocks):
            for rock in falling_rocks:
                if rock.move():
                    falling_rocks.remove(rock)
                    misses += 1
                    if misses > 2:
                        game_mode = 2
                    else:
                        falling_rocks.clear()
                        rocks_drop = 0
                        time.sleep(1)
                        if len(rocks[-1]) == 0:
                            rocks.remove(rocks[-1])
                            if len(paddles) > 1 and len(paddles) >= len(rocks):
                                paddles.remove(paddles[-1])
                        return
                if rock.collide(paddles):
                    score += 7 - len(rocks)
                    if high_score < score:
                        high_score = score
                    rocks_drop -= 1
                    falling_rocks.remove(rock)
            if len(falling_rocks) == 0:
                if len(rocks):
                    rocks.remove(rocks[-1])
                if len(paddles) > 1 and len(paddles) >= len(rocks):
                    paddles.remove(paddles[-1])
                for paddle in paddles:
                    if paddle.size > 40:
                        paddle.size -= 20
                    else:
                        paddle.size = 35


        if delay > 30:
            delay = 0
            if rocks_drop < 4:
                if len(rocks):
                    if len(rocks[-1]):
                        rocks_drop += 1
                        rock = random.choice(rocks[-1])
                        rock.is_move = True
                        falling_rocks.append(rock)
                        rocks[-1].remove(rock)


def draw():
    global game_mode, score, misses, high_score
    if game_mode in (0,1):
        screen.clear()
        screen.draw.text("Misses: " + str(misses), (5, 5), color=(80, 220, 255), fontname="arcade", fontsize=12)
        screen.draw.text("Player score: " + str(score), (5, 20), color=(0, 0, 200), fontname="arcade", fontsize=12)
        screen.draw.text("High score: " + str(high_score), (WIDTH - 200, 20), color=(80, 220, 255), fontname="arcade", fontsize=12)
        for row in range(len(rocks)):
            for rock in rocks[row]:
                rock.draw()
        for rock in falling_rocks:
            rock.draw()
        if game_mode == 1:
            for paddle in paddles:
                paddle.draw()

    if game_mode == 0:
        reset_game()
        text = "Avalanche"
        screen.draw.text(text, (WIDTH / 2 - len(text) * 12, HEIGHT / 2), color=(255, 255, 255), fontname="arcade")
        text = "Press mouse to start"
        screen.draw.text(text, (WIDTH / 2 - len(text) * 12, HEIGHT / 2 + 50), color=(255, 255, 255), fontname="arcade")

    if game_mode == 2:
        text = "game over"
        screen.draw.text(text, (WIDTH / 2 - len(text) * 12, HEIGHT / 2), color=(255, 255, 255), fontname="arcade")


pgzrun.go()
