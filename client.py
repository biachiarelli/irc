import socket
import re
import sys
from threading import Thread
import multiprocessing as mp
from time import sleep

port = 65000
host = '192.168.0.16'
#host = '172.29.37.38'

class Client:
    numClients = 0

    def __init__(self, ipv4, sock, nickname="USR"+str(numClients), hostname="", channel=""):
        self.ipv4     = ipv4
        self.sock     = sock
        self.nickname = nickname
        self.hostname = hostname
        self.channel  = channel

        Client.numClients += 1

    def sendMsg(self, msg):
        msg = self.nickname + ' : ' + msg   
        self.sock.send(bytes(msg, "utf-8"))

    def __repr__(self):
        return "<IPV4: %s\nSOCK: %s\nNICKNAME: %s\nHOSTNAME: %s\nCHANEEL: %s\n>" % (self.ipv4, self.sock, self.nickname, self.hostname, self.channel)

    def __str__(self):
        return "<From str method of Channel:\nIPV4: %s\nSOCK: %s\nNICKNAME: %s\nHOSTNAME: %s\nCHANEEL: %s\n>" % (self.ipv4, self.sock, self.nickname, self.hostname, self.channel)


# Conecta o socket
sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sck.connect((host, 65000))
processes = []

# Le mensagem do usuario
def outbound():
    open = True

    while open:
        if(sck.fileno() != -1):
            try:
                outbound = input('>> ')
                sck.send(bytes(outbound, 'utf-8'))
                sleep(0.2)
            except:
                open = False
        else:
            open = False
    return

# Imprime mensagens para o usuario
def inbound():  
    open = True

    while open:
        try:
            inbound = sck.recv(512)
            if(inbound.decode() == '/SAIR'):
                print('Conexão fechada')
                sck.close();
            else:
                if(len(inbound) > 0):
                    print('<<', inbound.decode())
        except:
            open = False
    return

def main():

    # Cria os processos
    processes.append(Thread(target=outbound))
    processes.append(Thread(target=inbound))

    #Inicia os processos
    for process in processes:
        process.start()

    for process in processes:
        process.join()

    return


if __name__ == '__main__':
    main()

