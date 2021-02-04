# encode:utf-8


import socketserver


class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):

        # self.data = self.request.recv(1024).strip()

        self.data = self.request.recv(1024)
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        self.request.sendall(self.data.upper())


if __name__ == "__main__":
    HOST, PORT = "192.168.0.109", 8888
    with socketserver.TCPServer((HOST, PORT), MyTcpHandler) as server:
        server.serve_forever()
