import socket
import urllib.request
from channel import Channel

port = 65000
host = '192.168.0.16'
#host = '172.29.37.38'

class Server:

    def __init__(self):
        # Estruturas de clientes e canais
        self.clients = {}
        self.canais   = {}

        self.canais["Canal 1"] = Channel("Canal 1")
        self.canais["Canal 2"] = Channel("Canal 2")
        self.canais["Canal 3"] = Channel("Canal 3")
        # Handlers para comandos
        self.handlers = {"NICK"   : self.nickClientHandler,
                         "USUARIO": self.userClientHandler,
                         "SAIR"   : self.quitClientHandler,
                         "ENTRAR" : self.subscribeChannelHandler,
                         "SAIRC"  : self.quitChannelHandler,
                         "LISTAR" : self.listChannelHandler,
                        }
        
        # requisita API do SO uma conexão AF_INET (IPV4) com protocolo de transporte SOCK_STREAM (TCP)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # requisita ao SO a posse de uma porta associada a um IP
        self.sock.bind((host, port))

        # requisita ao SO que a porta indicada de um dado IP seja reservado para escuta
        self.sock.listen(5)

        print("Conexão aberta porta: ", port)

        self.run()

    def run(self):
        open = True

        while open:
            # aceita requisição de conexão
            (clientsock, address) = self.sock.accept()
            welcome = 'Bem vindo, utilize os comandos: '
            welcome += '\n/NICK -nickName'
            welcome += '\n/USUARIO -hostName'
            welcome += '\n/SAIR'
            welcome += '\n/ENTRAR -nomeCanal'
            welcome += '\n/SAIRC'
            welcome += '\n/LISTAR'            

            self.sendMessage(welcome, clientsock)

            while open:
                # recebe do socket do cliente e uma mensagem de 512 bytes
                message = clientsock.recv(512)

                print("Mensagem: ", message.decode())
                print("Endereco: ", address)

                if(message.decode() == '/SAIR'):
                    self.sendMessage('/SAIR', clientsock)
                    open = False
                    pass

                # processa mensagem
                answer, client, isCommand = self.parseCommands(clientsock, address, message)
                if len(answer) > 0:
                    if(isCommand):
                        self.sendMessage(answer, client.sock)
                    else:
                        self.sendMsgChannel(answer, client.channel)
        self.sock.close()
        pass

    def sendMessage(self, msg, clientsock):
        clientsock.send(bytes(msg, 'utf-8'))

    def parseCommands(self, clientsock, clientAddr, message):
        from client import Client

        message = message.decode()
        answer = ''

        if clientAddr not in self.clients.keys():
            self.clients[clientAddr] = Client(clientAddr, clientsock)
            #self.canais[""].clients[clientAddr] = self.clients[clientAddr]
            
        client = self.clients[clientAddr]

        print('Canal: ', self.clients[clientAddr].channel)

        if(message[0] == '/'):
            message = message [1:] 
            answer = self.commands(clientAddr, message)
            return answer, client, True
        else:
            if(self.clients[clientAddr].channel == ""):
                answer = 'Entre em um canal para começar uma conversa'
                return answer, client, True
            else:
                answer = message
                return answer, client, False

    def commands(self, clientAddr, message):
        answer = ''
        command = message.partition(' ')[0]
        args = message.partition(' -')[2]

        if (command in self.handlers.keys()):
           answer = self.handlers[command](clientAddr, args)
        else:
            answer += 'Comando inválido, tente:'
            answer += '\n/NICK -nickName'
            answer += '\n/USUARIO -hostName'
            answer += '\n/SAIR'
            answer += '\n/ENTRAR -nomeCanal'
            answer += '\n/SAIRC'
            answer += '\n/LISTAR'

        return answer

    # Enviar mensagem para o canal
    def sendMsgChannel(self, msg, channel):
        for client in self.canais[channel].clients:
            self.clients[client].sendMsg(msg)

    # Criar apelido ou mudar anterior
    def nickClientHandler(self, clientAddr, args):
        if(args != ""):
            self.clients[clientAddr].nickname = args
            return 'Nickname alterado para: ' + args
        else:
            return '/NICK -nickName'

   # Especificar nome do usuario
    def userClientHandler(self, clientAddr, args):
        if(args != ""):
            self.clients[clientAddr].hostname = args
            return 'HostName alterado para: ' + args
        else:
            return '/USUARIO -hostName'

    # Sair do canal
    def quitClientHandler(self, clientAddr, args):
        return self.clients[clientAddr].nickname + 'saiu'

    # Entrar no canal
    def subscribeChannelHandler(self, clientAddr, args):
        if args in self.canais:
            self.canais[args].clients[clientAddr] = self.clients[clientAddr]
            self.clients[clientAddr].channel = args
            return 'Entrou no canal: ' + args
        else:
            if(args != ""):
                return 'Canal "%s" Inválido\n' % args + self.listChannelHandler(clientAddr, args)
            else:
                return '/ENTRAR -nomeCanal'

    # Sair do canal
    def quitChannelHandler(self, clientAddr, args):
        channel = self.clients[clientAddr].channel
        #print('ClientAddr', clientAddr)
        #print('Channel', channel)
        #print('Canais[channel]', self.canais[channel])
        print('Clients: \n', self.canais[channel].clients[clientAddr])
        #self.canais[channel].remove(clients[clientAddr]);
        self.clients[clientAddr].channel == ""
        return 'Saiu do canal' + channel

    # Listar canais
    def listChannelHandler(self, clientAddr, args):
        list = 'Lista de canais\n'
        for canal in self.canais:
            print('Nome do canal: ', canal)
            list += '-' +canal + '\n'

        return list

def main():
    Sever()
    pass

if __name__ == '__main__':
    Server()