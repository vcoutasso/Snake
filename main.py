#!/usr/bin/python3

import tkinter as tk
from random import seed, randint, randrange

WIDTH = 640
HEIGHT = 480
DELAY = 100

SQUARE_SIDE_LENGTH = 20

LEFT = 1
DOWN = 2
UP = 3
RIGHT = 4

class Game(object):
    def __init__(self, snake, apple):
        self.window = tk.Tk()
        self.window.configure(background='black')
        self.window.attributes('-type', 'dialog')
        self.canvas = tk.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.window.bind('<KeyPress>', snake.keyDown)
        apple.newPosition(snake)
        self.timer()
        self.window.mainloop()

    def timer(self):
        self.canvas.delete("all")
        self.printGrid()
        apple.print(self.canvas)
        snake.move(apple, self.canvas)
        self.printScore(snake)
        if snake.fimDeJogo == False:
            self.window.after(100, self.timer)
        else:
            snake.gameOver(self.canvas)

    def printScore(self, snake):
        self.canvas.create_text(550, 10, fill="darkblue", font="Times 12 bold", text="Score: %d" % snake.score)

    def printGrid(self):
        # Imprime linhas verticais
        self.canvas.create_line(SQUARE_SIDE_LENGTH, SQUARE_SIDE_LENGTH, SQUARE_SIDE_LENGTH, HEIGHT - SQUARE_SIDE_LENGTH, width=1)
        self.canvas.create_line(WIDTH - SQUARE_SIDE_LENGTH, SQUARE_SIDE_LENGTH, WIDTH - SQUARE_SIDE_LENGTH, HEIGHT - SQUARE_SIDE_LENGTH, width=1)
        # Imprime linhas horizontais
        self.canvas.create_line(SQUARE_SIDE_LENGTH, SQUARE_SIDE_LENGTH, WIDTH - SQUARE_SIDE_LENGTH, SQUARE_SIDE_LENGTH, width=1)
        self.canvas.create_line(SQUARE_SIDE_LENGTH, HEIGHT - SQUARE_SIDE_LENGTH, WIDTH - SQUARE_SIDE_LENGTH, HEIGHT - SQUARE_SIDE_LENGTH, width=1)

class Apple(object):
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.radius = 16

    def newPosition(self, Snake):
        while True:
            self.pos_x = randrange(1, int((WIDTH - SQUARE_SIDE_LENGTH) / SQUARE_SIDE_LENGTH)) * SQUARE_SIDE_LENGTH
            self.pos_y = randrange(1, int((HEIGHT - SQUARE_SIDE_LENGTH) / SQUARE_SIDE_LENGTH)) * SQUARE_SIDE_LENGTH

            if(self.pos_y in Snake.posicoes_y and self.pos_x in Snake.posicoes_x):
                continue

            break

    def print(self, canvas):
        canvas.create_oval(self.pos_x + 4, self.pos_y + 4, self.pos_x + self.radius, self.pos_y + self.radius, fill='red')


class Snake(object):

    def __init__(self):
        self.fimDeJogo = False
        self.pos_x = WIDTH / 2
        self.pos_y = HEIGHT / 2
        self.size = SQUARE_SIDE_LENGTH
        self.speed = SQUARE_SIDE_LENGTH
        self.thickness = SQUARE_SIDE_LENGTH
        self.direction = randint(LEFT, RIGHT)
        self.quadradinhos = 1
        self.score = 0
        self.posicoes_x = []
        self.posicoes_y = []

    def comeu(self):
        self.quadradinhos += 1
        self.score += 1

        if self.quadradinhos == 2:
            self.posicoes_x.append(self.pos_x)
            self.posicoes_y.append(self.pos_y)
        else:
            self.posicoes_x.append(self.posicoes_x[len(self.posicoes_x) - 2])
            self.posicoes_y.append(self.posicoes_y[len(self.posicoes_y) - 2])

    def move(self, apple, canvas):
        if self.fimDeJogo == False:

            if self.quadradinhos > 1:


                for i in range(len(self.posicoes_y) - 1, 0, -1):
                        self.posicoes_x[i] = self.posicoes_x[i-1]
                        self.posicoes_y[i] = self.posicoes_y[i-1]

                self.posicoes_x[0] = self.pos_x
                self.posicoes_y[0] = self.pos_y


            if self.direction == LEFT:
                self.pos_x = self.pos_x - self.speed
            elif self.direction == DOWN:
                self.pos_y = self.pos_y + self.speed
            elif self.direction == UP:
                self.pos_y = self.pos_y - self.speed
            elif self.direction == RIGHT:
                self.pos_x = self.pos_x + self.speed

            # If out of bounds
            if (self.pos_x < SQUARE_SIDE_LENGTH or self.pos_x >= WIDTH - SQUARE_SIDE_LENGTH or self.pos_y < SQUARE_SIDE_LENGTH or self.pos_y >= HEIGHT - SQUARE_SIDE_LENGTH):
                self.fimDeJogo = True

            for i in range(0, len(self.posicoes_y) - 1):
                if self.pos_x == self.posicoes_x[i] and self.pos_y == self.posicoes_y[i]:
                    self.fimDeJogo = True

            canvas.create_rectangle(self.pos_x, self.pos_y, self.pos_x + self.size, self.pos_y + self.size, fill='green')

            for i in range(0, len(self.posicoes_x)):
                canvas.create_rectangle(self.posicoes_x[i], self.posicoes_y[i], self.posicoes_x[i] + self.size, self.posicoes_y[i] + self.size, fill='green')


            if (apple.pos_x == self.pos_x and apple.pos_y == self.pos_y):
                self.comeu()
                apple.newPosition(self)

    def keyDown(self, e):
        if e.keysym == "Left":
            if self.direction == RIGHT:
                self.fimDeJogo = True
            else:
                self.direction = LEFT

        elif e.keysym == "Down":
            if self.direction == UP:
                self.fimDeJogo = True
            else:
                self.direction = DOWN
        elif e.keysym == "Up":
            if self.direction == DOWN:
                self.fimDeJogo = True
            else:
                self.direction = UP
        elif e.keysym == "Right":
            if self.direction == LEFT:
                self.fimDeJogo = True
            else:
                self.direction = RIGHT
        elif e.keysym == "Escape":
            exit(1)


    def gameOver(self, canvas):
        canvas.create_text(WIDTH / 2, HEIGHT / 2, font="Times 20 bold", text="GAME OVER")



if __name__ == "__main__":

    # Inicializa o gerador de números aleatórios com uma semente (por padrão baseada no tempo atual)
    seed()

    apple = Apple()
    snake = Snake()
    main = Game(snake, apple)
