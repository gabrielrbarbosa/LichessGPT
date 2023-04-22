import threading
import datetime
import time
import chess
import openai
import re
import os
from pathlib import Path

chess_board = chess.Board()
runOnce = True

class Game(threading.Thread):

    def __init__(self, board, game_id, player_id, isWhite, color, time, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.board = board
        self.stream = board.stream_game_state(game_id)
        self.player_id = player_id
        self.isWhite = isWhite
        self.color = color
        self.clock = {'white': datetime.datetime(1970, 1, 1, 0, time, 0), 'black': datetime.datetime(1970, 1, 1, 0, time, 0)}
        self.first_move = 2 # returns false after 2 moves have been made
        self.canMove = True

        openai_file = Path(__file__).parent.absolute() / "openai.key"
        openai.api_key = openai_file.read_text()
        if self.isWhite:
            self.white_first_move()


    def run(self):
        for event in self.stream:
            if event['type'] == 'gameState':
                self.handle_state_change(event)

    def handle_state_change(self, game_state):
        global chess_board

        self.canMove = True

        if game_state.get(self.color[0].lower() + "draw") is True:
            print('DRAW!')
            self.canMove = False
            os._exit(0)
        elif game_state["status"] == "resign":
            print("The opponent resigned. Congrats!")
            self.canMove = False
            os._exit(0)
        else:
            # update time
            self.clock['white'] = game_state['wtime']
            self.clock['black'] = game_state['btime']

            # there's no "amount of turns" variable in the JSON, so we have to construct one manually
            turn = len(game_state["moves"].split())-1
            if turn % 2 == self.isWhite:

                last_move = game_state["moves"].split()[-1]
                print(self.color + " moved: " + last_move)
                print()

                chess_board.push_uci(last_move)
                self.display_board()
                print()

                # decrement first move counter
                if self.first_move:
                    self.first_move -= 1

                self.check_mate(chess_board)

                # user move start time
                move_start = datetime.datetime.now()
            
                while(self.canMove):
                    try:
                        #move = input("Make your move: ")
                        playerColor = 'white' if self.isWhite else 'black'
                        prompt = 'Given the current chess game: ' + game_state["moves"] + \
                                    ' output in one word the best next move for ' + playerColor + ' in SAN notation'
                        
                        completion = openai.Completion.create(engine='text-davinci-002', prompt=prompt, temperature=0.5)
                        move = re.sub(r'\W+', '', completion.choices[0].text.strip())
                        print('ChatGPT move: %s' % move)
                        time.sleep(3)

                        self.board.make_move(self.game_id, chess_board.parse_san(move))
                        chess_board.push_san(move)
                        if self.first_move:
                            self.first_move -= 1
                        elif self.color[0] == 'b':
                            self.clock['white'] -= datetime.datetime.now() - move_start
                        else:
                            self.clock['black'] -= datetime.datetime.now() - move_start
                        break    
                    except Exception as e:
                        print(f"Error: {e}")
                        continue

                self.display_board()
                self.check_mate(chess_board)
                print()
                print(self.color + "'s turn...")

    def white_first_move(self):
        global chess_board

        self.display_board()
        while(True):
            try:
                #move = input("Make your move: ")
                move = "d4"
                if move.lower() == "resign":
                    self.board.resign_game(self.game_id)
                    os._exit(0)
                else:
                    self.board.make_move(self.game_id, chess_board.parse_san(move))
                    chess_board.push_san(move)
            except Exception as e:
                print("You can't make that move. Try again!")
                print(f'Reason: {e}')
                continue
            break

        self.display_board()
        self.first_move -= 1
        print(self.color + "'s turn...")

    def check_mate(self, chess_board):
        if str(chess_board.result()) != "*":
            if chess_board.result() == "1-0":
                if self.isWhite:
                    print("Congrats! You won by checkmating your opponent!")
                else:
                    print("You lose! Your opponent has checkmated you!")
            elif chess_board.result() == "0-1":
                if self.isWhite:
                    print("You lose! Your opponent has checkmated you!")
                else:
                    print("Congrats! You won by checkmating your opponent!")
            elif chess_board.result() == "1/2-1/2":
                print("The game ended in a stalemate (draw)!")

            print("Thanks for playing!")
            os._exit(0)

    def display_board(self):
        global chess_board

        m = {'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
             'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚',
             '.': '·', ' ': ' '}

        # Replace each piece in the board representation with its Unicode equivalent

        # Display the chess board, if the the player's color is black then flip the board 
        if not self.isWhite:
            chess_board = chess_board.transform(chess.flip_vertical).transform(chess.flip_horizontal)

        board_str = str(chess_board)
        for piece, char in m.items():
            board_str = board_str.replace(piece, char)

        print(board_str)
        print("[%02d:%02d : %02d:%02d]" % (self.clock['white'].minute, self.clock['white'].second, 
                                           self.clock['black'].minute, self.clock['black'].second))
        print()