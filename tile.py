import pygame

TILE_SIZE = 40

class Tile:
    hora_texture = None
    trava_texture = None
    voda_texture = None
    cesta_horizontal_texture = None
    cesta_vertical_texture = None
    cesta_cross_texture = None
    cesta_corner_tr_texture = None
    cesta_corner_br_texture = None

    @staticmethod
    def load_textures():
        Tile.hora_texture = pygame.image.load(r'C:\Users\Tom\Pictures\hora.png').convert_alpha()
        Tile.trava_texture = pygame.image.load(r'C:\Users\Tom\Pictures\trava.png').convert_alpha()
        Tile.voda_texture = pygame.image.load(r'C:\Users\Tom\Pictures\voda.png').convert_alpha()
        Tile.cesta_horizontal_texture = pygame.image.load(r'C:\Users\Tom\Pictures\cesta_horizontal.png').convert_alpha()
        Tile.cesta_vertical_texture = pygame.image.load(r'C:\Users\Tom\Pictures\cesta_vertical.png').convert_alpha()
        Tile.cesta_cross_texture = pygame.image.load(r'C:\Users\Tom\Pictures\cesta_cross.png').convert_alpha()
        Tile.cesta_corner_tr_texture = pygame.image.load(r'C:\Users\Tom\Pictures\cesta_corner_tr.png').convert_alpha()
        Tile.cesta_corner_br_texture = pygame.image.load(r'C:\Users\Tom\Pictures\cesta_corner_br.png').convert_alpha()

    def __init__(self, tile_type, position):
        self.tile_type = tile_type
        self.position = (position[0] * TILE_SIZE, position[1] * TILE_SIZE)
        self.texture = getattr(Tile, f'{tile_type}_texture')

    def draw(self, screen):
        if self.texture:
            screen.blit(self.texture, self.position)
