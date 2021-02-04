# encode:utf-8

import socket
import socketserver
import threading
import json


class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # クライアント1からTCP電文を受信
        # self.data = self.request.recv(1024).strip()
        self.data = self.request.recv(1024)
        print("{} wrote:".format(self.client_address[0]))
        print("DataLength:{}".format(len(self.data)))
        print(self.data)
        #self.request.sendall(self.data.upper())
        # 別ホスト(この場合VEGA)に受け取った電文をそのまま送信
        #hsvr, hport = "192.168.0.133", 8888
        hsvr, hport = dist, 8888
        print("Distport:{}".format(dist))
        # レシート情報ファイルを読み込む
        rectxt = readxmltxt()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((hsvr, hport))
        #client.send(self.data + rectxt)
        client.send(rectxt)
        # 別ホスト(この場合VEGA)からの電文を受信(取り敢えずバッファ4Kにしておく)
        rev = client.recv(4096)
        # 別ホスト(この場合VEGA)から受信した電文を加工せずにクライアント1に還す
        self.request.sendall(rev)
        print("CatchLength=:{}".format(len(rev)))
        print("CatchData=:{}".format(rev))
        # クライアントを開放する
        client.close()


# 自身のIPアドレスを取得する
def getaddr():
    host = socket.gethostname()
    print("Host=: {}".format(host))

    ip = socket.gethostbyname_ex(host)[2]
    tp = ""
    for t in ip:
        print("Ip=: {}".format(t))
        if len(readjson(t)) > 0:
            tp = t
            break
    return tp


def readjson(vip):
    with open('IPSET.json') as f:
        jsn = json.load(f)
        print(jsn)
        blist = jsn["ipset"]
        print(jsn["ipset"])
        rp2 = ""
        for i in range(len(blist)):
            tpl1 = blist[i]["localip"]
            tpl2 = blist[i]["deviceip"]
            print("localip:{}".format(tpl1))
            print("deviceip:{}".format(tpl2))
            if tpl1 == vip:
                rp2 = tpl2
                break
        return rp2


def readxmltxt():
    with open('TestReceipt.txt', 'rb') as f:
        tx = f.read()
        f.close()
        return tx


# Main
if __name__ == "__main__":
    adrs = getaddr()
    dist = readjson(adrs)
    HOST, PORT = adrs, 8888
    with socketserver.TCPServer((HOST, PORT), MyTcpHandler) as server:
        server.serve_forever()
