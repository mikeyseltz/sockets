from IPython.display import clear_output
import socket
import pickle

class Player:

	def __init__(self):
		HOST = "127.0.0.1"
		PORT = 5050
		ADDRESS = (HOST, PORT)
		self.s = socket.socket()
		self.s.connect(ADDRESS)
		self.s.setblocking(False)
		self.board = Board()
		self.choice = "n"

	def join_game(self):
		self.name = input('your name > ')
		self.name = self.name.encode('utf-8')
		self.choice = input('your letter > ')	
		self.choice_coded = self.choice.encode('utf-8')
		self.s.send(self.name + b"/" + self.choice_coded)

	def select_action(self):
		self.board.show_board()
		row = int(input('pick row: 1=top, 2=mid, 3=bottom > '))
		space = int(input('pick space: 1=left, 2=mid, 3=right > '))
		self.board.state[row-1][space-1] = self.choice
		data = pickle.dumps(self.board.state)
		self.send_state(data)


	def await_move(self):
		while True:
			try:
				move = self.s.recv(1024)
				print('received')
				self.board.state = pickle.loads(move)
				self.select_action()
			except:
				continue

	def send_state(self, board):
		self.s.send(board)
		self.await_move()


class Board:
	def __init__(self):
		self.state = [
					  ["-","-","-"],
					  ["-","-","-"],
					  ["-","-","-"]
						]

	def move(self, row, space, choice):
		self.state[row][space] = choice

	def show_board(self):
		for row in self.state:
			for space in row:
				print(space, end=" ")
			print("")

