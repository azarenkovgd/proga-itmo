import random
import typing as tp
import copy
import pygame

Cell = tp.Tuple[int, int]
CellsArray = tp.List[int]
Grid = tp.List[CellsArray]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height

        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.number_of_rows = self.height // self.cell_size
        self.number_of_columns = self.width // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        self.grid = None

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))

        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for row in range(self.number_of_rows):
            for col in range(self.number_of_columns):
                rect = (col * self.cell_size+1, row * self.cell_size+1, self.cell_size-1, self.cell_size-1)

                if self.grid[row][col] == 1:
                    color = pygame.Color('green')
                else:
                    color = pygame.Color('white')

                pygame.draw.rect(surface=self.screen, rect=rect, color=color)

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_lines()
            self.draw_grid()
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize=False):
        grid = []

        for row in range(self.number_of_rows):
            grid.append([])
            for column in range(self.number_of_columns):
                if randomize:
                    is_alive = random.choice([0, 1])
                else:
                    is_alive = 0

                grid[row].append(is_alive)

        return grid

    def get_neighbours(self, cell: Cell) -> CellsArray:
        cell_row, cell_column = cell
        neighbours = []

        for row in range(cell_row - 1, cell_row + 2):
            for column in range(cell_column - 1, cell_column + 2):
                if row < 0 or row >= self.number_of_rows or column < 0 or column >= self.number_of_columns:
                    continue

                if row == cell_row and column == cell_column:
                    continue

                is_alive = self.grid[row][column]
                neighbours.append(is_alive)

        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = copy.deepcopy(self.grid)

        for row in range(self.number_of_rows):
            for column in range(self.number_of_columns):
                neighbours = self.get_neighbours((row, column))
                is_alive = self.grid[row][column]
                sum_for_neighbours = sum(neighbours)

                if sum_for_neighbours in [2, 3] and is_alive == 1:
                    pass

                elif sum_for_neighbours == 3:
                    new_grid[row][column] = 1

                else:
                    new_grid[row][column] = 0

        return new_grid

