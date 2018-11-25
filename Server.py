import socket
import os
import threading
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()

print (host)
port = 12345
s.bind(("0.0.0.0", port))


file_folder = os.path.dirname(os.path.realpath(__file__))

# Nombre Archivo, clienteIP, port, ruta





def getClient(file_name, data):
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
	c = cl[0]
	addr = cl[1]
	directory = []
	data_file = open("datafile.txt", "r")
	data = []
	for linea in data_file:
		data.append(linea.split(","))
		directory.append(linea.split(",")[0])
	data_file.close()
	print('Got connection from ' + str(addr[0])+ ":" + str(addr[1]))
	c.send("Connected to server".encode())
	opt = c.recv(1024).decode()
	if opt == "1":
		c.send("Files to download: ".encode())
		c.send(str(directory).encode())
		name = ""
		search = []
		while name != "OK":
			name=c.recv(1024).decode()
			for i in directory:
				if name == i:
					client, port = getClient(name, data)
					var = "OK,"+str(client)+":"+str(port)+","
					c.send(var.encode())
					search = []
				if name in i:
					search.append(i)
					continue
			c.send(str(search).encode())
			search=[]
	elif opt == "2":
		file_name = c.recv(4096).decode()
		data_file = open("datafile.txt", "a")
		data_file.write(file_name+","+str(addr[0])+",1234\n")
		directory.append(file_name)
		data.append([file_name, addr[0], 1234])
		c.send("File Uploaded".encode())




s.listen(5)
search=[]
name=""
while True:
	c, addr=s.accept()
	print(addr)
	x = (c, addr)
	one = threading.Thread(target=connection, args = (x, ))
	one.start()

c.close()
