import pygame
from Pieces import *
from Constants import *

pygame.mixer.quit()

class BoardPlace:
    def __init__(self, sprite, i, j):
        self.sprite = sprite
        self.rect = sprite.get_rect()
        self.piece = None
        self.i = i
        self.j = j

        x, y = width//8*j, height//8*i
        self.rect.move_ip(x, y)

    def draw_selected(self):
        self.draw()
        x, y = self.rect.left, self.rect.top
        sprite_green = self.sprite.copy()
        sprite_green.fill((0, 255, 0, 35))
        screen.blit(sprite_green, (x, y))

    def get_piece_moves(self):
        if self.piece is not None:
            return self.piece.get_moveset(self.i, self.j)
        return []

    def pop_piece(self):
        old_piece = self.piece
        self.piece = None
        return old_piece

    def draw(self):
        x, y = self.rect.left, self.rect.top
        screen.blit(self.sprite, self.rect)

        if self.hasPiece():
            self.piece.draw(x, y)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def hasPiece(self):
        return self.piece is not None

    def setPiece(self, piece):
        self.piece = piece

class Board:
    def __init__(self):
        self.board_places = []
        self.selected = None
        self.possible_moves = []

        for i in range(0, 8):
            line = []
            for j in range(0, 8):
                # conditions to be black
                cond1 = i % 2 == 0 and j % 2 != 0
                cond2 = i % 2 != 0 and j % 2 == 0

                if cond1 or cond2: sprite = black_square
                else: sprite = white_square

                line.append(BoardPlace(sprite, i, j))
            self.board_places.append(line)
        for i in range(0, 8):
            self.board_places[7][i].setPiece(Pawn(PieceColor.BLACK))
        for i in range(0, 8):
            self.board_places[0][i].setPiece(Tower(PieceColor.WHITE))

    def draw(self):
        for line in self.board_places:
            for board_place in line:
                if self.selected == board_place or ((board_place.i, board_place.j) in self.possible_moves and not board_place.hasPiece()):
                    board_place.draw_selected()
                else:
                    board_place.draw()
    def clear_selected(self):
        self.selected = None
        self.possible_moves.clear()

    def on_board_place_selection(self, x, y):
        selected = None

        for line in self.board_places:
            for board_place in line:
                if board_place.collidepoint(x, y) == True:
                    selected = board_place
                    break
        
        if selected is not None:
            (i, j) = selected.i, selected.j
            if self.selected is not None:
                if (i, j) in self.possible_moves and not selected.hasPiece():
                    new_place = self.board_places[i][j]
                    piece = self.selected.pop_piece()
                    if isinstance(piece, Pawn) and piece.first_time:
                        piece.first_time = False
                    new_place.setPiece(piece)
                self.clear_selected()
            elif selected.hasPiece():
                self.selected = selected
                if self.selected.hasPiece() == True:
                    possible_moves = self.selected.get_piece_moves()
                    for moviment, max_value in possible_moves.items():
                        value = 1
                        while value <= max_value:
                            acc = 0
                            if moviment == 'LEFT' or moviment == 'FORWARD':
                                acc = -value
                            else:
                                acc = value
                            
                            if moviment == 'FORWARD' or moviment == 'BACKWARD':
                                if i+acc > 7 or i+acc < 0 or self.board_places[i+acc][j].hasPiece():
                                    break
                                self.possible_moves.append((i+acc, j))
                            else:
                                if j+acc > 7 or j+acc < 0 or self.board_places[i][j+acc].hasPiece():
                                    break
                                self.possible_moves.append((i, j+acc))
                            value = value + 1

def main():
    pygame.display.flip()
    board = Board()
    running = True
    while running:
        pygame.display.update()
        board.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (x,y) = pygame.mouse.get_pos()
                board.on_board_place_selection(x, y)
        pygame.display.flip()
        pygame.time.wait(0)


if __name__ == "__main__":
    main()