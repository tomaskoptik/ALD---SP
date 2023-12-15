import pygame
import sys
import random
from tile import Tile, TILE_SIZE

class Main:
    def __init__(self):
        self.screen_width = 400
        self.screen_height = 400
        self.grid_size_x, self.grid_size_y = 10, 10

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game World Generator with Tiles")

        self.white = (255, 255, 255)

        Tile.load_textures()

        self.grid = self.generate_grid_with_logic()
        self.game_loop()

    def draw_grid(self):
        for x in range(self.grid_size_x):
            for y in range(self.grid_size_y):
                tile_type = self.grid[y][x]
                tile = Tile(tile_type, (x, y))
                tile.draw(self.screen)

    def game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(self.white)
            self.draw_grid()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def generate_grid_with_logic(self):
        while True:
            grid = [['trava' for _ in range(self.grid_size_y)] for _ in range(self.grid_size_x)]
            path_length = 0
            start_edge = random.choice(['left', 'top'])
            direction = 'horizontal' if start_edge == 'left' else 'vertical'
            x, y = (0, random.randint(0, self.grid_size_y - 1)) if direction == 'horizontal' else (
            random.randint(0, self.grid_size_x - 1), 0)

            while 0 <= x < self.grid_size_x and 0 <= y < self.grid_size_y:
                grid[y][x] = 'cesta_horizontal' if direction == 'horizontal' else 'cesta_vertical'
                path_length += 1

                next_direction = 'vertical' if direction == 'horizontal' else 'horizontal'
                next_tile = 'cesta_corner_tr' if next_direction == 'vertical' and random.random() < 0.5 else 'cesta_corner_br' if next_direction == 'horizontal' and random.random() < 0.5 else \
                grid[y][x]

                if next_tile.startswith('cesta_corner'):
                    grid[y][x] = next_tile
                    direction = next_direction

                x += 1 if direction == 'horizontal' else 0
                y += 1 if direction == 'vertical' else 0

            if path_length >= 15:
                break

        water_added = False
        mountain_added = False
        while not water_added or not mountain_added:
            x, y = random.randint(0, self.grid_size_x - 1), random.randint(0, self.grid_size_y - 1)

            water_block_size = 3
            mountain_block_size = 2

            if 'cesta' not in grid[y][x]:
                if not water_added:
                    # 'self' je předán automaticky, nemusíte jej uvádět
                    if self.can_place_terrain(grid, x, y, water_block_size, 'hora'):
                        self.place_terrain(grid, x, y, water_block_size, 'voda')
                        water_added = True
                if not mountain_added:
                    if self.can_place_terrain(grid, x, y, mountain_block_size, 'voda'):
                        self.place_terrain(grid, x, y, mountain_block_size, 'hora')
                        mountain_added = True

            self.add_trees(grid)
            self.add_houses(grid)

        return grid

    def can_place_terrain(self, grid, x, y, block_size, exclude_terrain=None):
        for i in range(block_size):
            for j in range(block_size):
                if x + i >= self.grid_size_x or y + j >= self.grid_size_y:
                    return False
                if 'cesta' in grid[y + j][x + i]:
                    return False
                if exclude_terrain and exclude_terrain in grid[y + j][x + i]:
                    return False
        return True

    def place_terrain(self, grid, x, y, block_size, terrain_type):
        for i in range(block_size):
            for j in range(block_size):
                if x + i < self.grid_size_x and y + j < self.grid_size_y:
                    grid[y + j][x + i] = terrain_type

    def add_trees(self, grid, chance_to_add_tree=0.1):
        for y in range(self.grid_size_y):
            for x in range(self.grid_size_x):
                if grid[y][x] == 'trava' and random.random() < chance_to_add_tree:
                    grid[y][x] = 'strom'

    def add_houses(self, grid, chance_to_add_house=0.02):
        for y in range(self.grid_size_y):
            for x in range(self.grid_size_x):
                if grid[y][x] == 'trava' and random.random() < chance_to_add_house:
                    grid[y][x] = 'dum'

if __name__ == '__main__':
    Main()
