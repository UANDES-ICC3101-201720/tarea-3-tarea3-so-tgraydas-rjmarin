import socket 
import os             

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
host = socket.gethostname()
port = 12345 
s.bind(("127.0.0.1", port)) 

file_folder = '/home/raimundo/Desktop/estructura/'
	
def download(name):
	f = open(file_folder+ name, 'rb')
	line = f.read(1024)
	while line:
		c.send(line)
		line = f.read(1024)
	f.close()
	c.send("Sent".encode())
	c.send("File downloaded".encode())


s.listen(5)
search = [] 
name = ""
while True:
    directory =os.listdir(file_folder)
    print()
    c, addr = s.accept()    
    print( 'Got connection from', addr)
    c.send("Connected to server\nfiles to download: ".encode())
    c.send(str(directory).encode())
    while name != "OK":	
    	name = c.recv(1024).decode()
    	for i in directory:
	   		if name ==i:
	   			c.send("OK".encode())
	   			name = "OK"
	   			download(i)

	   			break
	   		if name in i:
	   			search.append(i)
	   			continue
    	c.send(str(search).encode())
    	search = [] 

c.close() 
