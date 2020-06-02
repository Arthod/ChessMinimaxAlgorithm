import chess
import chess.engine
import pygame as pg
import time
import sys
import math

class Main:
    def __init__(self):
        #Chess
        self.board = chess.Board()
        self.status = ""
        self.move_list = []
        self.move_number = 1

        self.whose_move = True #hvis tur det er. Hvis den er initialiseret som False, er hvid AI. Ellers er sort AI.

        #Misc
        self.from_move = ""
        self.from_move_coordinates = (0, 0)
        self.to_move = "white"
        self.columns = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.rows = ["8", "7", "6", "5", "4", "3", "2", "1"]

        #Minimax
        self.depth = 2
        self.position_count = 0
        self.color = True
        self.eval = 0

        #pg
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        self.unicode = pg.font.Font("segoe-ui-symbol.ttf", 60)
        self.font = pg.font.SysFont("monospace", 15)
        clock = pg.time.Clock()
        pg.font.init()

        done = False
        while not done:
            self.position_count = 0
            if self.color == True:
                start = time.time()
                move = self.board.parse_san(self.minimax_root(self.depth, self.board, True))
                self.board.push(move)
                self.color = False

                print (time.time() - start)
            else:
                move = self.board.parse_san(self.minimax_root(self.depth, self.board, False))
                self.board.push(move)
                self.color = True

            '''
            else:
                x = int(pg.mouse.get_pos()[0] / 70)
                y = int(pg.mouse.get_pos()[1] / 70)
                if x < 8 and y < 8:
                    move = self.columns[x] + self.rows[y]
                    if pg.mouse.get_pressed()[0]:
                        self.from_move = move
                        self.from_move_coordinates = (x, y)
                    if pg.mouse.get_pressed()[2] and len(self.from_move) == 2:
                        self.to_move = move
                        move = chess.Move.from_uci(self.from_move + self.to_move)
                        if (self.board.is_legal(move)):
                            self.board.push(move)
                            self.color = False
                            self.from_move = ""
                            self.from_move_coordinates = ""
                            self.to_move = ""
            '''
                        
            
            self.draw_board(pg, self.board)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True

            pg.display.flip()
            clock.tick(60)
        pg.quit()

    def char_to_int(self, char):
        for i in range(len(self.columns)):
            if self.columns[i] == char:
                return i+1

    def move_to_coordinates(self, move):
        from_coordinate = (self.char_to_int(move[0]), int(move[1]))
        to_coordinate = (self.char_to_int(move[2]), int(move[3]))
        return (from_coordinate, to_coordinate)

    def minimax_root(self, depth, board, is_maximising_player):
        new_board_moves = [board.san(move) for move in board.legal_moves]
        best_move = -9999
        best_move_found = False

        for i in range(len(new_board_moves)):
            new_board_move = new_board_moves[i]
            move = board.parse_san(new_board_move)
            board.push(move)
            value = self.minimax(depth - 1, board, float("-inf"), float("inf"), is_maximising_player)

            pos = self.move_to_coordinates(str(move))

            self.draw_board(pg, self.board)
            pg.draw.rect(self.screen, (240, 230, 140), pg.Rect(pos[0][0]*70-70, 70*8-pos[0][1]*70, 70, 70))
            pg.draw.rect(self.screen, (240, 230, 140), pg.Rect(pos[1][0]*70-70, 70*8-pos[1][1]*70, 70, 70))

            text = self.unicode.render(self.to_array(self.board.unicode())[(pos[1][0]-1+(8-pos[1][1])*8) * 2], False, (0, 0, 0))
            self.screen.blit(text, (pos[1][0]*70-70, 70*8-pos[1][1]*70))
            text = self.font.render(str(value), False, (0, 0, 0))
            self.screen.blit(text, (pos[1][0]*70-70, 70*8-pos[1][1]*70))

            pg.display.flip()

            board.pop()
            if (value > best_move):
                best_move = value
                best_move_found = new_board_move
        self.eval = best_move
        return best_move_found
        
    def minimax(self, depth, board, alpha, beta, is_maximising_player):
        self.position_count += 1

        if type(depth) == type(0) and depth == 0:
            return -self.evaluate_board(board, self.eval)

        new_board_moves = [board.san(move) for move in board.legal_moves]
        if (is_maximising_player):
            best_move = float("-inf")
            for board_move in new_board_moves:
                board.push(board.parse_san(board_move))
                value = self.minimax(depth - 1, board, alpha, beta, False)
                best_move = max(best_move, value)
                alpha = max(alpha, best_move)
                board.pop()
                if beta <= alpha:
                    return best_move
            return best_move
        else:
            best_move = float("inf")
            for board_move in new_board_moves:
                board.push(board.parse_san(board_move))
                value = self.minimax(depth - 1, board, alpha, beta, True)
                best_move = min(best_move, value)
                beta = min(beta, best_move)
                board.pop()
                if beta <= alpha:
                    return best_move
            return best_move

    def evaluate_board(self, board, old_eval):
        eval = old_eval

        dupe_board = board.copy()
        for i in range(self.depth):
            move = dupe_board.pop()
            coordinates = self.move_to_coordinates(str(move))[1]
            taken_piece = self.to_array(dupe_board.unicode())[(coordinates[0]-1+(8-coordinates[1])*8) * 2]

            if not(taken_piece in ['·', '\n', ' ']):
                if taken_piece == "♔":
                    eval -= 100
                if taken_piece == "♕":
                    eval -= 9
                if taken_piece == "♖":
                    eval -= 5
                if taken_piece == "♗":
                    eval -= 3
                if taken_piece == "♘":
                    eval -= 3
                if taken_piece == "♙":
                    eval -= 1
                if taken_piece == "♚":
                    eval += 100
                if taken_piece == "♛":
                    eval += 9
                if taken_piece == "♜":
                    eval += 5
                if taken_piece == "♝":
                    eval += 3
                if taken_piece == "♞":
                    eval += 3
                if taken_piece == "♟":
                    eval += 1
        return eval


    def draw_board(self, pg, board):
        def rect(x, y, w, h, color_rgb):
            pg.draw.rect(self.screen, color_rgb, pg.Rect(x, y, w, h))
        def text(x, y, font, txt, color_rgb=(0, 0, 0)):
            text = font.render(txt, False, color_rgb)
            self.screen.blit(text, (x, y))
        rect(0, 0, 800, 600, (255, 255, 255))

        #Draw board
        tile = True
        for ix in range(8):
            tile = not tile
            for iy in range(8):
                if (ix, iy) == self.from_move_coordinates:
                    rect(ix * 70, iy * 70, 70, 70, (160, 0, 0))
                else:
                    if tile:
                        rect(ix * 70, iy * 70, 70, 70, (160, 160, 160))
                    else:
                        rect(ix * 70, iy * 70, 70, 70, (255, 255, 255))
                tile = not tile
                if self.to_array(board.unicode())[(ix+iy*8) * 2] != "·":
                    text(ix * 70+5, iy * 70-5, self.unicode, self.to_array(self.board.unicode())[(ix+iy*8) * 2])

    def to_array(self, n):
        return list(n)

Main()