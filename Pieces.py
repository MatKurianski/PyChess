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
            'LEFT': 0,
            'RIGHT': 0,
            'FORWARD': 0,
            'BACKWARD': 0
        }

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

        self.moveset['LEFT'] = 1
        self.moveset['RIGHT'] = 1
        self.moveset['FORWARD'] = 1
        self.moveset['BACKWARD'] = 1

    def get_moveset(self, i, j):
        return self.moveset

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.first_time = True

        if self.color == PieceColor.BLACK:
            self.sprite = PieceSprites.BLACK_PAWN
        else:
            self.sprite = PieceSprites.WHITE_PAWN

        self.moveset['FORWARD'] = 1
    
    def get_moveset(self, i, j):
        if self.first_time:
            moveset = self.moveset.copy()
            moveset['FORWARD'] = 2
            return moveset
        return self.moveset
     
class Tower(Piece):
    def __init__(self, color):
        super().__init__(color)

        if self.color == PieceColor.BLACK:
            self.sprite = PieceSprites.BLACK_ROOK
        else:
            self.sprite = PieceSprites.WHITE_ROOK

    def get_moveset(self, i, j):
        moveset = self.moveset.copy()

        moveset['LEFT'] = 7
        moveset['RIGHT'] = 7
        moveset['FORWARD'] = 7
        moveset['BACKWARD'] = 7

        return moveset
