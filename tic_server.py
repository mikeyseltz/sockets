import socket
import select
import pickle

from tictactoe import Board

HOST = "100.115.92.206"
PORT = 5050
ADDRESS = (HOST, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(ADDRESS)
server.listen()
sockets = [server]
players = {}

print(f'Ready for game on {HOST}:{PORT}')

board = Board()
start = pickle.dumps(board.state)

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
			print(f"New Player: {name}")
			if len(sockets) == 3:
				socket.send(start)
				continue
		else:
			board = socket.recv(1024)
			for sock in sockets:
				if sock != server:
					if sock != socket:
						sock.send(board)