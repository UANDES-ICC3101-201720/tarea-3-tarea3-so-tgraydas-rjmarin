import socket  
import os 



def clear(): 
	os.system('cls' if os.name == 'nt' else 'clear')     

def Menu(s):
	print(s.recv(4096))

	while True:
		name=input("name of File: ")  
		s.send(name.encode())
		files = s.recv(1024).decode() 
		if files == "OK":
			#implente TCP
			print("file found")
			recive(name)


		else:
			print(files)


def recive(name):
	f = open(name, 'wb')
	while(True):
		l = s.recv(1024)
		if "Sent" in l.decode():
			l = s.recv(1024).decode()
			print(l)
			break
		f.write(l)
		if l == None:
			break


		

	


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
host = socket.gethostname() 
port = 12345 
try:
    s.connect(("127.0.0.1", port))

except Exception as e:
    print("Error!")
    exit(1)
  
print( s.recv(1024).decode())
Menu(s)
s.close                 
