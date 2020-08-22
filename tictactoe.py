from IPython.display import clear_output
import socket


class Player:

	def __init__(self):
		HOST = "127.0.0.1"
		PORT = 50500
		ADDRESS = (HOST, PORT)
		self.s = socket.socket()
		self.s.connect(ADDRESS)
		self.s.setblocking(False)

	def join_game(self):
		self.name = input('your name > ')
		self.name = self.name.encode('utf-8')
		self.choice = input('your letter > ')	
		self.choice = self.choice.encode('utf-8')
		self.s.send(self.name + b"/" + self.choice)

	def select_action(self, board, choice):
		self.board.show_board()
		row = int(input('pick row: 1=top, 2=mid, 3=bottom > '))
		space = int(input('pick space: 1=left, 2=mid, 3=right > '))
		self.board.state[row][space] = self.choice
		self.send_state(self.board.state.encode('utf-8'))


	def await_move(self):
		while True:
			try:
				move = self.s.recv(1024)
			except:
				pass

	def send_state(self, board):
		self.s.send(board)
		await_move()

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

board = Board()
player = Player()
player.join_game()