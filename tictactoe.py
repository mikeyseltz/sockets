from IPython.display import clear_output
import socket
import pickle
from numpy import transpose

def main():
	p = Player()
	p.join_game()

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
		self.await_move()

	def select_action(self):
		self.board.show_board()
		row = int(input('pick row: 1=top, 2=mid, 3=bottom > '))
		space = int(input('pick space: 1=left, 2=mid, 3=right > '))
		if self.board.state[row-1][space-1] == "-":
			self.board.state[row-1][space-1] = self.choice
			self.board.show_board()
			data = pickle.dumps(self.board.state)
			self.board.check_for_win()
			self.send_state(data)
		else:
			print('!!! space occupied (try again) !!!')
			self.select_action()

	def await_move(self):
		while True:
			try:
				move = self.s.recv(1024)
				print('vvv received vvv')
				self.board.state = pickle.loads(move)
				self.board.check_for_win()
				clear_output()
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

	def show_board(self):
		for row in self.state:
			for space in row:
				print(space, end=" ")
			print("")

	def check_for_win(self):
		for row in self.state:
			if row[0] == row[1] == row[2]:
				if row[0] != "-":
					print(f"{row[0]} WINS!")
		for row in transpose(self.state):
			if row[0] == row[1] == row[2]:
				if row[0] != "-":
					print(f"{row[0]} WINS!")
		if self.state[1][1] != "-":
			if self.state[0][0] == self.state[1][1] == self.state[2][2] or self.state[0][2] == self.state[1][1] == self.state[2][0]:
				print(f"{self.state[1][1]} WINS!")

	def test_win(self, board):
		b1 = [
			  ["-","x","x"],
			  ["o","o","o"],
			  ["x","-","-"]
				]
		b2 = [
			  ["x","x","o"],
			  ["-","x","o"],
			  ["-","-","o"]
				]

		b3 = [
			  ["x","x","o"],
			  ["-","x","o"],
			  ["o","-","x"]
				]

		if board == "b1":
			self.state = b1
			self.check_for_win()
		if board == "b2":
			self.state = b2
			self.check_for_win()
		if board == 'b3':
			self.state = b3
			self.check_for_win()

if __name__ == "__main__":
    main()