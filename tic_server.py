import socket
import select
from tictactoe import Board

HOST = "127.0.0.1"
PORT = 50500
ADDRESS = (HOST, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(ADDRESS)
server.listen()
sockets = [server]
players = {}


print(f'Ready for game on {HOST}:{PORT}')

while True:
	read_sockets, _, _ = select.select(sockets, [], [])
	for socket in read_sockets:
		if socket == server:
			socket, addr = server.accept()
			sockets.append(socket)
			data = socket.recv(1024).decode('utf-8')
			name = data.split('/')[0]
			symbol = data.split('/')[1]
			players[name] = symbol
		else:
			board = server.recv(1024)
			rec_board = Board(board.decode('utf-8'))
			rec_board.show_board()
server.close()
