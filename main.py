import os
from pytimedinput import timedInput
import random


class Field:

    def __init__(
            self,
            columns=os.get_terminal_size().columns,
            lines=os.get_terminal_size().lines
    ):
        self.width = (min(columns, lines)) // 3
        self.height = (min(columns, lines)) // 3
        self.values = [[" " for j in range(self.height)] for i in range(self.width)]
        self.generate_an_apple()

    def generate_an_apple(self):
        while True:
            position_of_an_apple = (
                random.randint(0, self.width), random.randint(0, self.width)
            )
            if self.values[
                position_of_an_apple[0] % self.width
            ][
                position_of_an_apple[1] % self.height
            ] == " ":
                self.values[
                    position_of_an_apple[0] % self.width
                ][
                    position_of_an_apple[1] % self.height
                ] = "a"
                break

    def delete_snake_positions(self):
        for index_i in range(len(self.values)):
            for index_j in range(len(self.values[0])):
                if self.values[index_i][index_j] == "*":
                    self.values[index_i][index_j] = " "

    def __str__(self):
        end_string = "|" + "-" * (self.width * 4 - 1) + "|\n"
        separation = "|" + "".join([('-' * 3 + '+') for i in range(self.width)])[:-1] + "|\n"
        field = end_string
        for j in range(self.height):
            for i in range(self.width):
                field += f"| {self.values[j][i]} "
            field += "|\n" + separation
        field = "\n".join(field.split('\n')[0:-2])
        field += "\n" + end_string
        return field


class Snake:

    def __init__(self, width, height, direction: tuple, field: Field):
        self.list_of_positions = [[width // 2, height // 2]]
        self.direction = direction
        self.field = field

    def move(self):
        list_of_positions2 = self.list_of_positions[:]
        prev = self.list_of_positions[0]
        next_position = [
            (self.direction[0] + self.list_of_positions[0][0]) % self.field.width,
            (self.direction[1] + self.list_of_positions[0][1]) % self.field.height
        ]
        if self.field.values[
            next_position[0] % self.field.width
        ][
            next_position[1] % self.field.height
        ] != "*":
            try:
                for index in range(1, len(list_of_positions2)):
                    prev = list_of_positions2[index]
                    self.list_of_positions[index] = list_of_positions2[index-1]
                if self.field.values[next_position[0]][next_position[1]] == "a":
                    self.list_of_positions.append(prev)
                    self.field.generate_an_apple()
            except:
                if self.field.values[next_position[0]][next_position[1]] == "a":
                    self.list_of_positions.append(prev)
                    self.field.generate_an_apple()
            self.list_of_positions[0] = [
                (self.direction[0] + self.list_of_positions[0][0]) % self.field.width,
                (self.direction[1] + self.list_of_positions[0][1]) % self.field.height
            ]
        else:
            print(f"YOU LOSE\nYOUR SCORE:{len(self.list_of_positions)}")
            exit()


class Game:
    width = os.get_terminal_size().columns
    height = os.get_terminal_size().lines
    field = Field(columns=width, lines=height)
    snake = Snake(field.width, field.width, direction=(1, 0), field=field)

    def change_direction(self, cmd: str):
        try:
            if cmd.lower()[0] == 'd':
                self.snake.direction = (0, 1)
            if cmd.lower()[0] == 'a':
                self.snake.direction = (0, -1)
            if cmd.lower()[0] == 'w':
                self.snake.direction = (-1, 0)
            if cmd.lower()[0] == 's':
                self.snake.direction = (1, 0)

        except IndexError:
            pass

    def update_image(self):
        pass

    def run(self):
        while True:
            for elem in self.snake.list_of_positions:
                self.field.values[elem[0] % self.field.width][elem[1] % self.field.height] = "*"
            print(f"Your score: {len(self.snake.list_of_positions)}")
            print(self.field)
            cmd, _ = timedInput(timeout=1, resetOnInput=False)
            self.change_direction(cmd=cmd)
            self.snake.move()
            self.field.delete_snake_positions()
            os.system('cls')


if __name__ == '__main__':
    game = Game()
    game.run()
