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

        if not self.place_water(grid):
            return None
        if not self.place_mountain(grid):
            return None

        self.add_trees(grid)
        self.add_houses(grid)

        return grid

    def place_water(self, grid):
        for _ in range(10):  # Počet pokusů o umístění vody
            x, y = random.randint(0, self.grid_size_x - 1), random.randint(0, self.grid_size_y - 1)
            if self.can_place_terrain(grid, x, y, 1, 'cesta'):
                self.expand_terrain(grid, x, y, 'voda', random.randint(3, 6))  # Náhodná velikost
                return True
        return False

    def place_mountain(self, grid):
        for _ in range(10):  # Počet pokusů o umístění hory
            x, y = random.randint(0, self.grid_size_x - 1), random.randint(0, self.grid_size_y - 1)
            if self.can_place_terrain(grid, x, y, 1, 'cesta') and 'voda' not in grid[y][x]:
                self.expand_terrain(grid, x, y, 'hora', random.randint(2, 4))  # Náhodná velikost
                return True
        return False

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

    def expand_terrain(self, grid, x, y, terrain_type, max_size):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        terrain_cells = [(x, y)]
        grid[y][x] = terrain_type

        while terrain_cells and len(terrain_cells) < max_size:
            x, y = random.choice(terrain_cells)
            if random.random() > len(terrain_cells) / max_size: 
                continue

            random.shuffle(directions)
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < self.grid_size_x and 0 <= new_y < self.grid_size_y and
                        self.can_place_terrain(grid, new_x, new_y, 1, exclude_terrain='cesta') and
                        grid[new_y][new_x] != terrain_type):
                    grid[new_y][new_x] = terrain_type
                    terrain_cells.append((new_x, new_y))
                    break  

            if random.random() < 0.1:  
                terrain_cells.remove((x, y))

        return grid

    def place_terrain(self, grid, x, y, block_size, terrain_type):
        for i in range(block_size):
            for j in range(block_size):
                if x + i < self.grid_size_x and y + j < self.grid_size_y:
                    grid[y + j][x + i] = terrain_type

    def add_trees(self, grid, chance_to_add_tree=0.2):
        for y in range(self.grid_size_y):
            for x in range(self.grid_size_x):
                if grid[y][x] == 'trava' and random.random() < chance_to_add_tree:
                    grid[y][x] = 'strom'

    def add_houses(self, grid, chance_to_add_house=0.04):
        for y in range(self.grid_size_y):
            for x in range(self.grid_size_x):
                if grid[y][x] == 'trava' and random.random() < chance_to_add_house:
                    grid[y][x] = 'dum'

if __name__ == '__main__':
    Main()
