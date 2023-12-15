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
        grid = [['trava' for _ in range(self.grid_size_y)] for _ in range(self.grid_size_x)]
        # Rozhodnout, zda cesta začne vertikálně nebo horizontálně
        start_edge = random.choice(['left', 'top'])
        direction = 'horizontal' if start_edge == 'left' else 'vertical'
        if start_edge == 'left':
            x, y = 0, random.randint(0, self.grid_size_y - 1)
        else:
            x, y = random.randint(0, self.grid_size_x - 1), 0

        # Vytvořit cestu, která vede z jedné strany na druhou
        while 0 <= x < self.grid_size_x and 0 <= y < self.grid_size_y:
            if direction == 'horizontal':
                grid[y][x] = 'cesta_horizontal'
                next_tile = 'cesta_corner_tr' if random.random() < 0.5 else 'cesta_horizontal'
            else:
                grid[y][x] = 'cesta_vertical'
                next_tile = 'cesta_corner_br' if random.random() < 0.5 else 'cesta_vertical'

            # Pokud nastane změna směru, použijeme rohovou dlaždici
            if next_tile.startswith('cesta_corner'):
                grid[y][x] = next_tile
                direction = 'vertical' if direction == 'horizontal' else 'horizontal'

            # Posunutí podle směru
            x += 1 if direction == 'horizontal' else 0
            y += 1 if direction == 'vertical' else 0

        # Přidání jedné oblasti vody a jedné oblasti hor
        water_added = False
        mountain_added = False
        while not water_added or not mountain_added:
            x, y = random.randint(0, self.grid_size_x - 1), random.randint(0, self.grid_size_y - 1)

            # Nastavit velikost bloku pro vodu a hory
            water_block_size = 4  # Například 3x3 blok pro vodu
            mountain_block_size = 3  # Například 2x2 blok pro hory

            if 'cesta' not in grid[y][x]:
                if not water_added:
                    if self.can_place_terrain(grid, x, y, water_block_size):
                        self.place_terrain(grid, x, y, water_block_size, 'voda')
                        water_added = True
                elif not mountain_added:
                    if self.can_place_terrain(grid, x, y, mountain_block_size):
                        self.place_terrain(grid, x, y, mountain_block_size, 'hora')
                        mountain_added = True

        return grid

    def can_place_terrain(self, grid, x, y, block_size):
        for i in range(block_size):
            for j in range(block_size):
                if x + i >= self.grid_size_x or y + j >= self.grid_size_y or 'cesta' in grid[y + j][x + i]:
                    return False
        return True

    def place_terrain(self, grid, x, y, block_size, terrain_type):
        for i in range(block_size):
            for j in range(block_size):
                if x + i < self.grid_size_x and y + j < self.grid_size_y:
                    grid[y + j][x + i] = terrain_type


if __name__ == '__main__':
    Main()
