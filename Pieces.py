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
        self.sprite = PieceSprites.BLACK_BISHOP
        self.moveset = {
            'LEFT': None,
            'RIGHT': None,
            'FORWARD': None,
            'BACKWARD': None
        }
        self.specialMoveset = None
    
    def hasSpecialMoveset(self):
        return self.specialMoveset is not None

    def get_moveset(self):
        return []

    def draw(self, x, y):
        screen.blit(self.sprite, (x+PieceSprites.piece_size//2, y+PieceSprites.piece_size//2))

class King(Piece):
    def __init__(self, color):
        super().__init__(color)

        if self.color == PieceColor.BLACK:
            self.sprite = PieceSprites.BLACK_KING
        else :
            self.sprite = PieceSprites.WHITE_KING

        self.moveset['LEFT'] = []
        self.moveset['RIGHT'] = []
        self.moveset['FORWARD'] = []
        self.moveset['BACKWARD'] = []

    def get_moveset(self, i, j):
        for direction in self.moveset:
            self.moveset[direction].clear()

        if j-1 >= 0:
            self.moveset['LEFT'].append((i, j-1))
        if j+1 <= 7:
            self.moveset['RIGHT'].append((i, j+1))
        if i-1 >= 0:
            self.moveset['FORWARD'].append((i-1, j))
        if i+1 <= 7:
            self.moveset['BACKWARD'].append((i+1, j))

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
        movesets = self.moveset.copy()

        maxSpan = 1
        if self.first_time:
            maxSpan = 2
        
        for direction, move in movesets.items():
            if move is None:
                continue
            move.clear()

            if direction == 'BACKWARD':
                for pos_i in range(i+1, i+(maxSpan+1)): 
                    if pos_i > 7:
                        break
                    movesets[direction].append((pos_i, j))
            elif direction == 'FORWARD':
                for pos_i in range(i-maxSpan, i):
                    if pos_i < 0:
                        continue
                    movesets[direction].append((pos_i, j))

        return movesets
     
class Tower(Piece):
    def __init__(self, color):
        super().__init__(color)

        if self.color == PieceColor.BLACK:
            self.sprite = PieceSprites.BLACK_ROOK
        else:
            self.sprite = PieceSprites.WHITE_ROOK

    def get_moveset(self, i, j):
        moveset = self.moveset.copy()

        moveset['LEFT'] = []
        moveset['RIGHT'] = []
        moveset['FORWARD'] = []
        moveset['BACKWARD'] = []

        for pos_i in reversed(range(0, i)):
            moveset['FORWARD'].append((pos_i, j))
        for pos_i in range(i+1, 8):
            moveset['BACKWARD'].append((pos_i, j))
        for pos_j in reversed(range(0, j)):
            moveset['LEFT'].append((i, pos_j))
        for pos_j in range(j+1, 8):
            moveset['RIGHT'].append((i, pos_j))

        return moveset
