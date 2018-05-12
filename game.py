import pygame
import random
from datetime import datetime
from math import atan, tanh, exp
import numpy as np

colours = {"Red": (255, 0, 0), "Green": (0, 255, 0),
           "White": (255, 255, 255), "Blue": (0, 0, 255),
           "Black": (0, 0, 0)}


class nn:
    def __init__(self, numInput=4, numHidden=3, numOutput=9, initialize_weight_bias=True):
        self.input_neurons = numInput
        self.hidden_neurons = numHidden
        self.output_neurons = numOutput
        self.input_node = np.zeros(shape=[self.input_neurons], dtype=np.float32)
        self.hidden_node = np.zeros(shape=[self.hidden_neurons], dtype=np.float32)
        self.output_node = np.zeros(shape=[self.output_neurons], dtype=np.float32)
        self.rnd = random.uniform(-5, 5)
        if initialize_weight_bias:
            self.input_hidden_weights = np.zeros(shape=[self.input_neurons, self.hidden_neurons], dtype=np.float32)
            self.hidden_output_weights = np.zeros(shape=[self.hidden_neurons, self.output_neurons], dtype=np.float32)
            self.hBiases = np.zeros(shape=[self.hidden_neurons], dtype=np.float32)
            self.oBiases = np.zeros(shape=[self.output_neurons], dtype=np.float32)
            self.initializeWeights()

    @staticmethod
    def softmax(oSums):
        result = np.zeros(shape=[len(oSums)], dtype=np.float32)
        m = max(oSums)
        divisor = 0.0
        for k in range(len(oSums)):
            divisor += exp(oSums[k] - m)
        for k in range(len(result)):
            result[k] = exp(oSums[k] - m) / divisor
        return result

    def setWeights(self, weights):
        if len(weights) != self.totalWeights(self.input_neurons, self.hidden_neurons, self.output_neurons):
            print("Warning: len(weights) error in setWeights()")

        idx = 0
        for i in range(self.input_neurons):
            for j in range(self.hidden_neurons):
                self.input_hidden_weights[i][j] = weights[idx]
                idx += 1

        for j in range(self.hidden_neurons):
            self.hBiases[j] = weights[idx]
            idx += 1

        for i in range(self.hidden_neurons):
            for j in range(self.output_neurons):
                self.hidden_output_weights[i][j] = weights[idx]
                idx += 1

        for k in range(self.output_neurons):
            self.oBiases[k] = weights[idx]
            idx += 1

    def getWeights(self):
        tw = self.totalWeights(self.input_neurons, self.hidden_neurons, self.output_neurons)
        result = np.zeros(shape=[tw], dtype=np.float32)
        idx = 0  # points into result

        for i in range(self.input_neurons):
            for j in range(self.hidden_neurons):
                result[idx] = self.input_hidden_weights[i][j]
                idx += 1

        for j in range(self.hidden_neurons):
            result[idx] = self.hBiases[j]
            idx += 1

        for i in range(self.hidden_neurons):
            for j in range(self.output_neurons):
                result[idx] = self.hidden_output_weights[i][j]
                idx += 1

        for k in range(self.output_neurons):
            result[idx] = self.oBiases[k]
            idx += 1

        return result

    def initializeWeights(self):
        numWts = self.totalWeights(self.input_neurons, self.hidden_neurons, self.output_neurons)
        wts = np.zeros(shape=[numWts], dtype=np.float32)
        lo = -0.01
        hi = 0.01
        for idx in range(len(wts)):
            wts[idx] = (hi - lo) * self.rnd + lo
        self.setWeights(wts)

    def computeOutputs(self, xValues):
        hSums = np.zeros(shape=[self.hidden_neurons], dtype=np.float32)
        oSums = np.zeros(shape=[self.output_neurons], dtype=np.float32)

        for i in range(self.input_neurons):
            self.input_node[i] = xValues[i]

        for j in range(self.hidden_neurons):
            for i in range(self.input_neurons):
                hSums[j] += self.input_node[i] * self.input_hidden_weights[i][j]

        for j in range(self.hidden_neurons):
            hSums[j] += self.hBiases[j]

        for j in range(self.hidden_neurons):
            self.hidden_node[j] = self.hypertan(hSums[j])

        for k in range(self.output_neurons):
            for j in range(self.hidden_neurons):
                oSums[k] += self.hidden_node[j] * self.hidden_output_weights[j][k]

        for k in range(self.output_neurons):
            oSums[k] += self.oBiases[k]

        softOut = self.softmax(oSums)
        for k in range(self.output_neurons):
            self.output_node[k] = softOut[k]

        result = np.zeros(shape=self.output_neurons, dtype=np.float32)
        for k in range(self.output_neurons):
            result[k] = self.output_node[k]

        return result

    @staticmethod
    def hypertan(x):
        if x < -20.0:
            return -1.0
        elif x > 20.0:
            return 1.0
        else:
            return tanh(x)

    @staticmethod
    def totalWeights(nInput, nHidden, nOutput):
        tw = (nInput * nHidden) + (nHidden * nOutput) + nHidden + nOutput
        return tw


class Player(pygame.sprite.Sprite, nn):
    def __init__(self, width=10, height=30, x=80, y=350, velocity=6, acceleration=-1, color=colours["Blue"]):
        pygame.sprite.Sprite.__init__(self)
        nn.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pressed = False
        self.counter = 2
        self.init_velocity = velocity
        self.init = y
        self.acceleration = acceleration
        self.velocity = velocity
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.fitness = -1

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global run
                run = False

        if self.pressed:
            self.velocity += self.acceleration
            self.rect.y -= self.velocity

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and (self.counter < 10) and self.rect.y == self.init:
            self.counter += 1
        else:
            if self.rect.y >= self.init and self.pressed:
                self.velocity = self.init_velocity
                self.rect.y = self.init
                self.pressed = False
            elif self.counter > 2 and not self.pressed:
                self.velocity *= round(self.counter / (1.5 ** 2.8))
                self.pressed = True
                self.counter = 2


class Barrier(pygame.sprite.Sprite):

    def __init__(self, width=10, height=0, x_velocity=-3, color=colours["Green"], screen_width=500,
                 player_y_position=350):
        super(Barrier, self).__init__()
        self.x_velocity = x_velocity
        self.height_randomizer()

        self.image = pygame.Surface([width, self.height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = player_y_position - self.height + 30

    def height_randomizer(self):
        self.height = random.randint(15, 45)

    def update(self):
        self.rect.x += self.x_velocity


class Top_Barrier(pygame.sprite.Sprite):
    def __init__(self, width=10, height=0, x_velocity=-3, color=colours["Green"], screen_width=500,
                 player_y_position=350):
        super(Top_Barrier, self).__init__()
        self.height = 350 - random.randint(50, 100) - height
        self.x_velocity = x_velocity
        self.image = pygame.Surface([width, self.height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = 0

    def height_randomizer(self, bottom_barrier):
        self.height = 350 - random.randint(50, 70) - bottom_barrier - 10

    def update(self):
        self.rect.x += self.x_velocity


def outside_frame(barriers):
    for s in barriers.sprites():
        if s.rect.x < 0 - s.rect.width:
            barriers.remove(s)
    barriers.update()
    return barriers


def barrier_generator(barriers, speed_change, counter):
    new_barrier = Barrier(x_velocity=-3 + speed_change)
    top_barrier = Top_Barrier(x_velocity=-3 + speed_change, height=new_barrier.rect.height)
    barriers.add(new_barrier)
    barriers.add(top_barrier)
    return barriers


def player_generator():
    players = pygame.sprite.Group()
    for i in range(100):
        player = Player(velocity=random.randrange(1, 6),
                        color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        players.add(player)
    return players


def fitness(player, barriers):
    if pygame.sprite.spritecollideany(player, barriers) is None:
        player.fitness += 1


def selection(selected, player):
    selected.add(player)


def get_last_barrier_x(barriers, player):
    for i, barrier in enumerate(barriers.sprites()):
        if barrier.rect.x < player.rect.x and barriers.sprites()[-1] != barrier:
            return barriers.sprites()[i + 1].rect.x
        else:
            return barrier.rect.x


def neuron_inputs(player, barriers, speed_change):
    input = np.array([player.velocity, player.rect.x, speed_change, get_last_barrier_x(barriers, player)])
    return np.argmax(player.computeOutputs(input), 0)


def mutate(selected):
    highest = selected.sprites()[-1]
    players = pygame.sprite.Group()
    for i in range(100):
        new_player = Player()
        weights = []
        rnd = random.randrange(0, 8)
        randomly_selected = selected.sprites()[rnd]
        for weight in range(51):
            rnd_2 = random.randrange(1, 3)
            if rnd_2 == 1:
                weights.append(highest.getWeights()[weight])
            elif rnd_2 == 2:
                weights.append(randomly_selected.getWeights()[weight])
            else:
                weights.append(random.uniform(-5, 5))
        new_player.setWeights(weights)
        players.add(new_player)
    return (players)


def reset(speed_change, barriers, counter, players, select_players):
    mutate(select_players)
    speed_change = 0
    barriers = pygame.sprite.Group()
    speed_change = 0
    counter = 1
    players = mutate(select_players)
    select_players = pygame.sprite.Group()
    return (speed_change, barriers, counter, players, select_players)


pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("TRex")
barriers = pygame.sprite.Group()
speed_change = 0
counter = 1
players = player_generator()
select_players = pygame.sprite.Group()
run = True
timer = datetime.now()
clock = pygame.time.Clock()
parents_found = False
run = True
timer = datetime.now()
clock = pygame.time.Clock()
generation = 0
pygame.font.init()
gen = 0


def generation_counter(generation, players):
    pygame.font.init()
    myfont = pygame.font.SysFont('Arial', 15)
    textsurface = myfont.render('Gen: ' + str(generation) + ' Number of players: ' + str(len(players.sprites())), False,
                                (0, 0, 0))
    return textsurface


while run:
    gen_text = generation_counter(gen, players)
    secondary_timer = datetime.now()
    diff = secondary_timer - timer
    diff = diff.total_seconds()
    if diff >= 1.3 - 0.5 * atan(counter / 10):
        timer = datetime.now()
        barriers = barrier_generator(barriers, speed_change, counter)
        counter += 1
    if counter % 5 == 0:
        speed_change -= 0.01
    for s in players.sprites():
        if pygame.sprite.spritecollideany(s, barriers) is not None:
            if len(players.sprites()) <= 10:
                selection(select_players, s)
            players.remove(s)
        fitness(s, barriers)

        s.counter = neuron_inputs(s, barriers, speed_change)
        if pygame.sprite.spritecollideany(s, barriers) is not None:
            players.remove(s)
    if not players:
        gen += 1
        speed_change, barriers, counter, players, select_players = reset(speed_change, barriers, counter, players,
                                                                         select_players)
    clock.tick(100)
    win.fill(colours["White"])
    players.update()
    players.draw(win)
    barriers.update()
    barriers = outside_frame(barriers)
    barriers.draw(win)
    win.blit(gen_text, (0, 0))
    pygame.display.update()

pygame.quit()
