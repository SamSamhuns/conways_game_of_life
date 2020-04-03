# Conway's game of life simulation on the terminal
# Samridha 25 Oct, Friday
import argparse
from time import sleep as time_sleep
from subprocess import call as subprocess_call


class Space:
    ''' A col * row 2D array object'''
    __slots__ = ['space', 'col', 'row',
                 'alive', 'dead', 'directions']

    def __init__(self, dimension):
        self.row = dimension[0]
        self.col = dimension[1]
        self.alive = '0'
        self.dead = ' '
        # Eight directions  r,l,u,d,ur,ul,lr,ll
        self.directions = [(0, 1), (0, -1), (-1, 0), (1, 0),
                           (-1, 1), (-1, -1), (1, 1), (1, -1)]

        self.space = [[' '] * self.col for i in range(self.row)]

    def check_if_coord_valid(self, xy_coord):
        x, y = xy_coord[0], xy_coord[1]
        if x >= 0 and x < self.row and y >= 0 and y < self.col:
            return True
        return False

    def is_vicinity_live(self, xy_coord):
        ''' Check if any cells in the vicinity are alive, including the cell itself '''
        x, y = xy_coord[0], xy_coord[1]
        if self.space[x][y] == self.alive:
            return True

        for direc in self.directions:
            # move to each neighbouring cell
            pos = (x + direc[0], y + direc[1])
            if self.check_if_coord_valid(pos):
                if self.space[pos[0]][pos[1]] == self.alive:
                    return True

        return False

    def count_number_of_live_neighbour_cells(self, xy_coord):
        x, y = xy_coord[0], xy_coord[1]
        live_neighbour_cells = 0

        for direc in self.directions:
            # move to each neighbouring cell
            pos = (x + direc[0], y + direc[1])
            if self.check_if_coord_valid(pos):
                if self.space[pos[0]][pos[1]] == self.alive:
                    live_neighbour_cells += 1

        return live_neighbour_cells

    def get_updated_cell(self, xy_coord):
        ''' Updates one cell based on its 8 neighbouring cells according to the
            rules of game of life:
            1) Any live cell with fewer than two live neighbours dies, as if by underpopulation.
            2) Any live cell with two or three live neighbours lives on to the next generation.
            3) Any live cell with more than three live neighbours dies, as if by overpopulation.
            4) Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction. '''

        x, y = xy_coord[0], xy_coord[1]
        live_neighbour_cells = self.count_number_of_live_neighbour_cells(
            (x, y))

        if self.space[x][y] == self.alive:
            # death by underpopulation
            if live_neighbour_cells < 2:
                return self.dead
            # Stasis or survival to next generation
            if live_neighbour_cells in (2, 3):
                return self.alive
            # death by overpopulation
            if live_neighbour_cells > 3:
                return self.dead
        elif self.space[x][y] == self.dead:
            # birth by reproduction
            if live_neighbour_cells == 3:
                return self.alive
        # all other conditions cell is dead
        return self.dead

    def set_cell_status(self, xy_coord, status):
        ''' status can be True [self.alive] or False [self.dead]'''
        if not(self.check_if_coord_valid(xy_coord)):
            raise IndexError("Coordinate indexes out of range")
        if status:
            status = self.alive
        else:
            starts = self.dead

        x, y = xy_coord[0], xy_coord[1]
        self.space[x][y] = status

    def draw_with_grids(self):
        ''' Coord counting starts from top left [0, 0] and increases towards bottom right '''
        subprocess_call('clear', shell=False)

        print('----'*self.col + '-')
        for i in range(self.row):
            print('| ', end='')
            for j in range(self.col):
                print(f'{self.space[i][j]} | ', end='')
            print('')
            print('----'*self.col + '-')

    def draw_without_grids(self):
        ''' Coord counting starts from top left [0, 0] and increases towards bottom right '''
        subprocess_call('clear', shell=False)

        print(f"{'    '*self.col} ")
        for i in range(self.row):
            print('  ', end='')
            for j in range(self.col):
                print(f'{self.space[i][j]}   ', end='')
            print('')
            print(f"{'    '*self.col} ")

    def update(self):
        ''' Simultaneously updates all cells '''
        update_dict = {}  # Saves updates for each step
        for i in range(self.row):
            for j in range(self.col):
                if self.is_vicinity_live((i, j)):
                    update_dict[(i, j)] = self.get_updated_cell((i, j))

        # Simultaneous update loop
        for update_cell in update_dict:
            x, y = update_cell[0], update_cell[1]
            self.space[x][y] = update_dict[update_cell]


def check_arg_positive(val):
    if int(val) <= 0:
        raise argparse.ArgumentTypeError(
            f"{val} is not a valid positive integer")
    return int(val)


def get_validated_args():
    parser = argparse.ArgumentParser(
        description="Simulate the game of life in a terminal with Python")

    parser.add_argument("no_of_rows",
                        type=check_arg_positive,
                        action='store',
                        default=8,
                        help="Number of rows in the game of life space")
    parser.add_argument("no_of_cols",
                        type=check_arg_positive,
                        action='store',
                        default=16,
                        help="Number of cols in the game of life space")
    parser.add_argument("init_live_cell_file",
                        type=str,
                        action='store',
                        default='init_patterns/block.csv',
                        help="CSV file storing the coords of starting live cells as csv")

    return parser.parse_args()


def get_live_cells_from_csv(coord_csv):
    ''' Gets coords of all live cells as a list of coords (x,y) '''
    with open(coord_csv, 'r') as csv:
        live_cell_list = []

        for line in csv:
            sep_line = line.strip().split(',')
            sep_line = [int(coord) for coord in sep_line]
            live_cell_list.append(sep_line)

        return live_cell_list


def get_live_cells_from_txt(coord_txt):
    ''' Gets coords of all live cells as a list of coords (x,y)
        from the format found online, i.e.
        .O.
        ..O
        OOO
    '''

    with open(coord_txt, 'r') as file:
        live_cell_list = []

        row = 0
        for line in file:
            sep_line = list(line.strip())
            sep_line = [live_cell_list.append([row, i]) for i in range(
                len(sep_line)) if sep_line[i] == 'O']
            row += 1

        return live_cell_list


def get_live_cells(coord_file):
    ''' Checks if the file is a txt or csv file and calls the right function '''
    live_cell_list = []
    extension = coord_file.rpartition('.')[-1]
    if extension == 'csv':
        live_cell_list = get_live_cells_from_csv(coord_file)
    elif extension == 'txt':
        live_cell_list = get_live_cells_from_txt(coord_file)
    else:
        raise OSError(
            "Incorrect file type. Only .txt or .csv files are allowed")

    return live_cell_list


def initialize_live_cells(life_board, live_cell_list):

    if live_cell_list is None or live_cell_list == []:
        raise ValueError("Live cell lists coordinates are empty")

    for cell in live_cell_list:
        x, y = cell[0], cell[1]
        life_board.set_cell_status((x, y), True)


def simulate_game_of_life(life_board, delay=1.5, grids=False):
    while True:
        if grids:
            life_board.draw_with_grids()
        else:
            life_board.draw_without_grids()
        life_board.update()
        time_sleep(delay)


def main():
    parsed_args = get_validated_args()
    life_board = Space((parsed_args.no_of_rows, parsed_args.no_of_cols))
    live_cell_list = get_live_cells(parsed_args.init_live_cell_file)
    initialize_live_cells(life_board, live_cell_list)
    simulate_game_of_life(life_board, delay=0.05, grids=False)


if __name__ == "__main__":
    main()
