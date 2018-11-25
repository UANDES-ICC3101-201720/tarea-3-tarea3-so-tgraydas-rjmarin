import socket
import os
import threading


file_folder = os.path.dirname(os.path.realpath(__file__))

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def recive(name, s):
    f = open(name, 'w')
    while(True):
        l = s.recv(256)
        if "Sent" in l.decode():
            f.write(l.decode().replace("Sent", ""))
            break
        else:
            f.write(l.decode())
        if l == None:
            break
    f.close()


def download(name, c):
    f = open(file_folder+"/"+name, 'rb')
    line = f.read(256)
    while line:
        c.send(line)
        line = f.read(256)
    f.close()
    c.send("Sent".encode())


def printFiles(l):
    l = l.replace("[", "").replace("]", "").replace("'", "")
    l = l.split(",")
    for i in l:
        print(i.strip())

def Menu(s):
    opt = input("[1] Download\n[2] Upload\n[3] Exit\n")
    if opt == "1":
        s.send(opt.encode())
        print(s.recv(20).decode())
        printFiles(s.recv(1024).decode())
        while True:
            name = input("name of File: ")
            s.send(name.encode())
            files = s.recv(1024).decode()
            n = name
            if files.split(",")[0] == "OK":
                # implente TCP4
                inf = files.split(",")[1]
                print(inf)
                p2p_solitude(inf.split(":")[0], int(inf.split(":")[1]), n)
                print("file found")
                break
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
        exit()


def p2p_solitude(ip, port, file):
    print(ip,port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = ip.strip()
    s.connect((ip, port))
    s.send(file.encode())
    recive(file, s)
    s.close

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
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 12345

        try:
            s.connect(("192.168.0.12", port))

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
