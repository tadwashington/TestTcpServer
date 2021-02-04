# encode:utf-8

import socket
import socketserver


class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        hsvr, hport = "192.168.0.133", 8888
        # self.data = self.request.recv(1024).strip()

        self.data = self.request.recv(1024)
        print("{} wrote:".format(self.client_address[0]))
        print("DataLength:{}".format(len(self.data)))
        print(self.data)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((hsvr, hport))
        client.send(self.data)
        rev = client.recv(2048)
        #self.request.sendall(self.data.upper())
        self.request.sendall(rev)
        print("CatchLength=:{}".format(len(rev)))
        print("CatchData=:{}".format(rev))
        client.close()


# 自身のIPアドレスを取得する
def getaddr():
    host = socket.gethostname()
    print("Host=: {}".format(host))

    ip = socket.gethostbyname(host)
    print("Ip=: {}".format(ip))
    return ip


# Main
if __name__ == "__main__":
    HOST, PORT = getaddr(), 8888
    with socketserver.TCPServer((HOST, PORT), MyTcpHandler) as server:
        server.serve_forever()
