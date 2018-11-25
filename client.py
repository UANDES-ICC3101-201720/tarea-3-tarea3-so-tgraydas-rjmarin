import socket
import os
import threading

file_folder = os.path.dirname(os.path.realpath(__file__))
print(file_folder)
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def recive(name, s):
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


def download(name, c):
    f = open(file_folder+'/'+name, 'rb')
    line = f.read(1024)
    while line:
        c.send(line)
        line = f.read(1024)
    f.close()
    c.send("Sent".encode())
    c.send("File downloaded".encode())


def printFiles(l):
    l = l.replace("[", "").replace("]", "").replace("'", "")
    l = l.split(",")
    for i in l:
        print(i.strip())

def Menu(s):
    while True:
        opt = input("[1] Download\n[2] Upload\n[3] Exit\n")
        if opt == "1":
            s.send(opt.encode())
            printFiles(s.recv(4096).decode())
            while True:
                name = input("name of File: ")
                s.send(name.encode())
                files = s.recv(1024).decode()
                n = name
                if files == "OK":
                    # implente TCP4
                    name = s.recv(1024).decode()
                    inf = name.split(":")
                    p2p_solitude(inf[0], int(inf[1].split("\n")[0]), n)
                    print("file found")
                else:
                    printFiles(files)
        elif opt == "2":
            s.send(opt.encode())
            name = input("Enter file address:\n")
            try:
                file = open(name, "r")
                file.close()
                s.send(name.encode())
                print(s.recv(1024).decode())
            except Exception as e:
                print("File not found")
        elif opt == "3":
            break


def p2p_solitude(ip, port, file):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = ip.strip()
    s.connect((ip, port))
    s.send(file.encode())
    recive(file, s)

def p2p():
    s_p2p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_p2p = socket.gethostname()
    port_p2p = 1234
    s_p2p.bind(("0.0.0.0", port_p2p))
    s_p2p.listen(5)
    while True:
        c, addr = s_p2p.accept()
        name = c.recv(1024).decode()
        download(name, c)
        c.close()


def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 12345

    try:
        s.connect(("192.168.0.17", port))

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
