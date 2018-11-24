import socket
import os
import threading

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


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


def download(name):
    f = open(file_folder + name, 'rb')
    line = f.read(1024)
    while line:
        c.send(line)
        line = f.read(1024)
    f.close()
    c.send("Sent".encode())
    c.send("File downloaded".encode())


def Menu(s):
    print(s.recv(4096))
    while True:
        name = input("name of File: ")
        s.send(name.encode())
        files = s.recv(1024).decode()
        if files == "OK":
            # implente TCP4
            name = s.recv(1024).decode()
            print(name)
            print("file found")
        else:
            print(files)


def p2p():
    s_p2p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_p2p = socket.gethostname()
    port_p2p = 1234
    s_p2p.bind(("127.0.0.1", port_p2p))
    s_p2p.listen(5)
    while True:
        c, addr = s_p2p.accept()
        name = c.recv(1024).decode()
        download(name)
        c.close()


def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 12345

    try:
        s.connect(("127.0.0.1", port))

    except Exception as e:
        print("Error!")
        exit(1)
    print(s.recv(1024).decode())
    Menu(s)
    s.close



client_t = threading.Thread(target=client)

p2p_t = threading.Thread(target=p2p)
p2p_t.start()
client_t.start()
