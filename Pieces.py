import pygame
from enum import Enum
from Constants import *

class PieceSprites:
    piece_size = 10
    WHITE_BISHOP = pygame.transform.scale((pygame.image.load(
        'img/white_bishop.png')), (width//piece_size, height//piece_size))
    WHITE_KING = pygame.transform.scale((pygame.image.load(
        'img/white_king.png')), (width//piece_size, height//piece_size))
    WHITE_KNIGHT = pygame.transform.scale((pygame.image.load(
        'img/white_knight.png')), (width//piece_size, height//piece_size))
    WHITE_PAWN = pygame.transform.scale((pygame.image.load(
        'img/white_pawn.png')), (width//piece_size, height//piece_size))
    WHITE_QUEEN = pygame.transform.scale((pygame.image.load(
        'img/white_queen.png')), (width//piece_size, height//piece_size))
    WHITE_ROOK = pygame.transform.scale((pygame.image.load(
        'img/white_rook.png')), (width//piece_size, height//piece_size))

    BLACK_BISHOP = pygame.transform.scale((pygame.image.load(
        'img/black_bishop.png')), (width//piece_size, height//piece_size))
    BLACK_KING = pygame.transform.scale((pygame.image.load(
        'img/black_king.png')), (width//piece_size, height//piece_size))
    BLACK_KNIGHT = pygame.transform.scale((pygame.image.load(
        'img/black_knight.png')), (width//piece_size, height//piece_size))
    BLACK_PAWN = pygame.transform.scale((pygame.image.load(
        'img/black_pawn.png')), (width//piece_size, height//piece_size))
    BLACK_QUEEN = pygame.transform.scale((pygame.image.load(
        'img/black_queen.png')), (width//piece_size, height//piece_size))
    BLACK_ROOK = pygame.transform.scale((pygame.image.load(
        'img/black_rook.png')), (width//piece_size, height//piece_size))

class PieceColor(Enum):
    BLACK = 0
    WHITE = 1

class Piece:
    def __init__(self, color):
        self.color = color
        self.moveset = {
            'LEFT': None,
            'RIGHT': None,
            'FORWARD': None,
            'BACKWARD': None,
            'DIAGONALTL': None,
            'DIAGONALBL': None,
            'DIAGONALTR': None,
            'DIAGONALBR': None
        }

    def get_moveset(self, i, j):
        return []

    def get_cached_moveset(self):
        return self.moveset

    def draw(self, x, y):
        screen.blit(self.sprite, (x+PieceSprites.piece_size//2, y+PieceSprites.piece_size//2))

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        if self.color == PieceColor.BLACK:
            self.sprite = PieceSprites.BLACK_QUEEN
        else :
            self.sprite = PieceSprites.WHITE_QUEEN
        
    def get_moveset(self, i, j):
        tower = Tower(self.color)
        bishop = Bishop(self.color)

        tower_moveset = tower.get_moveset(i, j)
        bishop_moveset = bishop.get_moveset(i, j)

        self.moveset = {
            'LEFT': [],
            'RIGHT': [],
            'FORWARD': [],
            'BACKWARD': [],
            'DIAGONALTL': [],
            'DIAGONALBL': [],
            'DIAGONALTR': [],
            'DIAGONALBR': []
        }

        for direction, moves in tower_moveset.items():
            self.moveset[direction] = moves

        for direction, moves in bishop_moveset.items():
            self.moveset[direction] = moves
        
        return self.moveset


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        if self.color == PieceColor.BLACK:
            self.sprite = PieceSprites.BLACK_BISHOP
        else :
            self.sprite = PieceSprites.WHITE_BISHOP

    def get_moveset(self, i, j):
        self.moveset = {
            'DIAGONALTL': [],
            'DIAGONALBL': [],
            'DIAGONALTR': [],
            'DIAGONALBR': []
        }

        directions_spawn = {
            'DIAGONALTL': (-1, -1),
            'DIAGONALBL': (1, -1),
            'DIAGONALTR': (-1, 1),
            'DIAGONALBR': (1, 1)
        }
        
        for direction_keys, direction in directions_spawn.items():
            pos_i = i
            pos_j = j

            while True:
                pos_i += direction[0]
                pos_j += direction[1]

                if (pos_i >= 0 and pos_i <= 7) and (pos_j >= 0 and pos_j <= 7):
                    self.moveset[direction_keys].append((pos_i, pos_j))
                else:
                    break
        return self.moveset

class King(Piece):
    def __init__(self, color):
        super().__init__(color)

        if self.color == PieceColor.BLACK:
            self.sprite = PieceSprites.BLACK_KING
        else :
            self.sprite = PieceSprites.WHITE_KING

        self.moveset = {
            'LEFT': [],
            'RIGHT': [],
            'FORWARD': [],
            'BACKWARD': [],
            'DIAGONALTL': [],
            'DIAGONALBL': [],
            'DIAGONALTR': [],
            'DIAGONALBR': []   
        }

    def get_moveset(self, i, j):
        self.moveset = {
            'LEFT': [],
            'RIGHT': [],
            'FORWARD': [],
            'BACKWARD': [],
            'DIAGONALTL': [],
            'DIAGONALBL': [],
            'DIAGONALTR': [],
            'DIAGONALBR': []
        }

        top = i - 1
        back = i + 1
        left = j - 1
        right = j + 1

        if left >= 0:
            self.moveset['LEFT'].append((i, left))
            if top >= 0:
                self.moveset['DIAGONALTL'].append((top, left))
            if back <= 7:
                self.moveset['DIAGONALBL'].append((back, left))
        if right <= 7:
            self.moveset['RIGHT'].append((i, right))
            if top >= 0:
                self.moveset['DIAGONALTR'].append((top, right))
            if back <= 7:
                self.moveset['DIAGONALBR'].append((back, right))
        if top >= 0:
            self.moveset['FORWARD'].append((top, j))
        if back <= 7:
            self.moveset['BACKWARD'].append((back, j))

        print(self.moveset)

        return self.moveset

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.first_time = True

        if self.color == PieceColor.BLACK:
            self.sprite = PieceSprites.BLACK_PAWN
            self.moveset['BACKWARD'] = []
        else:
            self.sprite = PieceSprites.WHITE_PAWN
            self.moveset['FORWARD'] = []

    
    def get_moveset(self, i, j):
        if self.color == PieceColor.WHITE:
            self.moveset = {
                'FORWARD': []
            }
            span = -1
        else:
            self.moveset = {
                'BACKWARD': []
            }
            span = 1

        if self.first_time:
            span = span * 2
        
        for direction, move in self.moveset.items():
            if direction == 'FORWARD':
                for pos_i in reversed(range(i+span, i)):
                    if pos_i >= 0 and pos_i <= 7:
                        self.moveset[direction].append((pos_i, j))
            else:
                i = i + 1
                for pos_i in range(i, i+span):
                    if pos_i >= 0 and pos_i <= 7:
                        self.moveset[direction].append((pos_i, j))
        
        return self.moveset
     
class Tower(Piece):
    def __init__(self, color):
        super().__init__(color)

        if self.color == PieceColor.BLACK:
            self.sprite = PieceSprites.BLACK_ROOK
        else:
            self.sprite = PieceSprites.WHITE_ROOK

    def get_moveset(self, i, j):
        self.moveset = {
            'LEFT': [],
            'RIGHT': [],
            'FORWARD': [],
            'BACKWARD': []
        }

        for pos_i in reversed(range(0, i)):
            self.moveset['FORWARD'].append((pos_i, j))
        for pos_i in range(i+1, 8):
            self.moveset['BACKWARD'].append((pos_i, j))
        for pos_j in reversed(range(0, j)):
            self.moveset['LEFT'].append((i, pos_j))
        for pos_j in range(j+1, 8):
            self.moveset['RIGHT'].append((i, pos_j))

        return self.moveset
