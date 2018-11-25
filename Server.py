import socket
import os
import threading
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
host_ip = socket.gethostbyname(host) 
print (host)
port = 12345
s.bind(("0.0.0.0", port))


file_folder = os.path.dirname(os.path.realpath(__file__))

# Nombre Archivo, clienteIP, port, ruta
data_file = open("datafile.txt", "r")

data = []
files = []

for linea in data_file:
	data.append(linea.split(","))
	files.append(linea.split(",")[0])

def getClient(file_name):
	for i in data:
		if i[0] == file_name:
			return i[1], i[2]


def download(name):
	f = open(file_folder + name, 'rb')
	line = f.read(1024)
	while line:
		c.send(line)
		line = f.read(1024)
	f.close()
	c.send("Sent".encode())
	c.send("File downloaded".encode())


def connection(cl):
	print(cl[2])
	c = cl[0]
	addr = cl[1]
	directory = cl[2]
	print('Got connection from ' + str(addr[0])+ ":" + str(addr[1]))
	c.send("Connected to server\nfiles to download: ".encode())
	c.send(str(directory).encode())
	name = ""
	search = []
	while name != "OK":
		name=c.recv(1024).decode()
		for i in directory:
			if name == i:
				c.send("OK".encode())
				client, port = getClient(name)
				c.send((str(client)+":"+str(port)).encode())
			if name in i:
				search.append(i)
				continue
		c.send(str(search).encode())
		search=[]





s.listen(5)
search=[]
name=""
while True:
	c, addr=s.accept()
	x = (c, addr, files)
	one = threading.Thread(target=connection, args = (x, ))
	one.start()

c.close()
