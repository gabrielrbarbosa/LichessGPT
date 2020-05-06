import threading
import chess

chess_board = chess.Board()
move_count = 0
isWhite = True
color = "Black"


class Game(threading.Thread):

    def __init__(self, board, game_id, player_id, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.board = board
        self.stream = board.stream_game_state(game_id)
        self.current_state = next(self.stream)
        self.player_id = player_id

    def run(self):
        for event in self.stream:
            if event['type'] == 'gameState':
                self.handle_state_change(event)
            elif event['type'] == 'chatLine':
                self.handle_chat_line(event)

    def handle_state_change(self, game_state):
        
        # big spaghetti code alert, horrible code below needs improvement
        # TODO: What if you're white?

        global move_count
        global chess_board
        global isWhite
        global color

        if move_count == 0:
            if game_state["white"]["id"] != self.player_id:
                isWhite = False
                color = "White"

        if move_count%2==0:
            print(color + " moved.")
            print()
            
            chess_board.push_uci(game_state["moves"].split()[-1])
            print(chess_board)
            print()

            move = input("Make your move: ")
            self.board.make_move(self.game_id, move)
            chess_board.push_uci(move)
            print(chess_board)
            print()
            print(color + "'s turn...")
        
        move_count+=1
        
        # Another example is moving knight from g8 to f6
        # self.board.make_move(self.game_id, "g8f6")

    def handle_chat_line(self, chat_line):
        pass