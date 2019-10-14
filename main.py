import pygame
from Pieces import *
from Constants import *

pygame.init() # now use display and fonts
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

    def get_piece(self):
        return self.piece

    def pop_piece(self):
        old_piece = self.piece
        self.piece = None
        return old_piece

    def draw_selected(self):
        self.draw()
        x, y = self.rect.left, self.rect.top
        sprite_green = self.sprite.copy()
        sprite_green.fill((0, 255, 0, 35))
        screen.blit(sprite_green, self.rect)

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
        self.current_turn = PieceColor.WHITE
        self.piece_list = {
            PieceColor.BLACK: [],
            PieceColor.WHITE: []
        }

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
            self.add_piece(6, i, Pawn(PieceColor.WHITE))
        for i in range(0, 8):
            self.add_piece(1, i, Pawn(PieceColor.BLACK))
        
        self.add_piece(0, 0, Tower(PieceColor.BLACK))
        self.add_piece(0, 1, Knight(PieceColor.BLACK))
        self.add_piece(0, 2, Bishop(PieceColor.BLACK))
        self.add_piece(0, 3, Queen(PieceColor.BLACK))
        self.add_piece(0, 4, King(PieceColor.BLACK))
        self.add_piece(0, 5, Bishop(PieceColor.BLACK))
        self.add_piece(0, 6, Knight(PieceColor.BLACK))
        self.add_piece(0, 7, Tower(PieceColor.BLACK))

        self.add_piece(7, 0, Tower(PieceColor.WHITE))
        self.add_piece(7, 1, Knight(PieceColor.WHITE))
        self.add_piece(7, 2, Bishop(PieceColor.WHITE))
        self.add_piece(7, 3, Queen(PieceColor.WHITE))
        self.add_piece(7, 4, King(PieceColor.WHITE))
        self.add_piece(7, 5, Bishop(PieceColor.WHITE))
        self.add_piece(7, 6, Knight(PieceColor.WHITE))
        self.add_piece(7, 7, Tower(PieceColor.WHITE))
    
    def toggle_turn(self):
        if self.current_turn == PieceColor.WHITE:
            self.current_turn = PieceColor.BLACK
        else:
            self.current_turn = PieceColor.WHITE
    
    def add_piece(self, i, j, piece):
        self.board_places[i][j].setPiece(piece)
        self.piece_list[piece.color].append(piece)
        piece.get_moveset(i, j) # set cache moveset

    def draw(self):
        for line in self.board_places:
            for board_place in line:
                if self.selected == board_place or (board_place.i, board_place.j) in self.possible_moves:
                    board_place.draw_selected()
                else:
                    board_place.draw()
    def clear_selected(self):
        self.selected = None
        self.possible_moves.clear()

    def get_board_place_selected(self, x, y):
        for line in self.board_places:
            for board_place in line:
                if board_place.collidepoint(x, y) == True:
                    return board_place
        return None
    
    def capture_piece(self, piece, board_captured):
        captured_piece = board_captured.pop_piece()
        board_captured.setPiece(piece)
        self.piece_list[captured_piece.color].remove(captured_piece)

    def validate_moves(self, piece, i, j):
        moves = piece.get_moveset(i, j)

        if not isinstance(piece, Knight):
            for direction, moves in moves.items():
                if moves is None:
                    continue
                for move in moves:
                    (pos_i, pos_j) = move
                    board_place = self.board_places[pos_i][pos_j]
                    if not board_place.hasPiece():
                        self.possible_moves.append((pos_i, pos_j))
                    elif (board_place.get_piece().color != piece.color) and not isinstance(piece, Pawn):
                        self.possible_moves.append((pos_i, pos_j))
                        break
                    else:
                        break

            if isinstance(piece, Pawn):
                if piece.color == PieceColor.BLACK:
                    span = 1
                else:
                    span = -1
                
                pos_i = i+span
                if pos_i >= 0 and pos_i <= 7:
                    for pos_inc in [1, -1]:
                        pos_j = j+pos_inc
                        if pos_j >= 0 and pos_j <= 7 and self.board_places[pos_i][pos_j].hasPiece() and self.board_places[pos_i][pos_j].get_piece().color != piece.color:
                            self.possible_moves.append((pos_i, pos_j))
        else:
            for move in moves:
                (i, j) = move
                board_place = self.board_places[i][j]
                if (not board_place.hasPiece()) or (board_place.hasPiece() and board_place.get_piece().color != piece.color):
                    self.possible_moves.append((i, j))
                


    def on_board_place_selection(self, x, y):
        selected = self.get_board_place_selected(x, y)
        
        if selected is not None:
            (i, j) = selected.i, selected.j
            if self.selected is not None:
                if (i, j) in self.possible_moves:
                    piece = self.selected.pop_piece()
                    if not selected.hasPiece():
                        new_place = self.board_places[i][j]
                        if isinstance(piece, Pawn) and piece.first_time:
                            piece.first_time = False
                        new_place.setPiece(piece)
                    elif selected.get_piece().color != piece.color:
                        self.capture_piece(piece, selected)
                    self.toggle_turn()
                self.clear_selected()
            elif selected.hasPiece() and self.current_turn == selected.piece.color:
                self.selected = selected
                if self.selected.hasPiece() == True:
                    piece = self.selected.get_piece()
                    self.validate_moves(piece, i, j)

def main():
    pygame.display.flip()
    board = Board()
    running = True
    clock = pygame.time.Clock()

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
        clock.tick(15)


if __name__ == "__main__":
    main()