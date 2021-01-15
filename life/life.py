import pathlib
import random
import typing as tp
import copy

Cell = tp.Tuple[int, int]
CellsArray = tp.List[int]
Grid = tp.List[CellsArray]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.number_of_rows, self.number_of_columns = size

        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()

        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)

        # Максимальное число поколений
        self.max_generations = max_generations

        # Текущее число поколений
        self.generations = 1

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

                is_alive = self.curr_generation[row][column]
                neighbours.append(is_alive)

        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = copy.deepcopy(self.curr_generation)

        for row in range(self.number_of_rows):
            for column in range(self.number_of_columns):
                neighbours = self.get_neighbours((row, column))
                is_alive = self.curr_generation[row][column]
                sum_for_neighbours = sum(neighbours)

                if sum_for_neighbours in [2, 3] and is_alive == 1:
                    pass

                elif sum_for_neighbours == 3:
                    new_grid[row][column] = 1

                else:
                    new_grid[row][column] = 0

        return new_grid

    def step(self) -> None:
        if self.is_max_generations_exceeded:
            return

        self.prev_generation = copy.deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()

        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        if self.generations >= self.max_generations:
            return True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        is_changed = False

        for row in range(self.number_of_rows):
            for column in range(self.number_of_columns):
                if self.prev_generation[row][column] != self.curr_generation[row][column]:
                    is_changed = True
                    break

        return is_changed

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        file_with_grid = filename.read_text().split('\n')
        file_with_grid.remove('')

        main_grid = []
        for line in file_with_grid:
            main_grid.append(list(map(int, line)))

        field_size = (len(main_grid), len(main_grid[0]))
        game = GameOfLife(field_size, False)
        game.curr_generation = main_grid

        return game
