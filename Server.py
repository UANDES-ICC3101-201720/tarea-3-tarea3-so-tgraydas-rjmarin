import socket
import os
import threading
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 12345
s.bind(("127.0.0.1", port))


file_folder = os.path.dirname(os.path.realpath(__file__))

# Nombre Archivo, clienteIP, port, ruta
data_file = open("datafile.txt", "r")

data = []

for linea in data_file:
	data.append(linea.split(","))


def download(name):
	f = open(file_folder + name, 'rb')
	line = f.read(1024)
	while line:
		c.send(line)
		line = f.read(1024)
	f.close()
	c.send("Sent".encode())
	c.send("File downloaded".encode())


def connection(c, addr, directory):
	print('Got connection from ' + addr)
	c.send("Connected to server\nfiles to download: ".encode())
	c.send(str(directory).encode())
	while name != "OK":
		name=c.recv(1024).decode()
		for i in data:
			if name == i[0]:
				c.send("OK".encode())
				name="OK"
				c.send(str(i.encode()))
			if name in i[0]:
				search.append(i[0])
				continue
		c.send(str(search).encode())
		search=[]





s.listen(5)
search=[]
name=""
while True:
	directory=os.listdir(file_folder)
	c, addr=s.accept()
	connection(c, addr)
	one = threading.Thread(target=connection)
	one.start()

c.close()
