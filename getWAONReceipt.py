# encode:utf-8

import socket
import socketserver
import threading
import json
import time
import random

# リターンコードの配列生成
l = ['203', '204', '303', '401', '403', '408', '409', '413', '502', '503', '504']


class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # リターンコードの配列生成
        #l = ['203', '204', '303', '401', '403', '408', '409', '413', '502', '503', '504']
        # クライアント1からTCP電文を受信
        # self.data = self.request.recv(1024).strip()
        self.data = self.request.recv(1024)
        print("{} wrote:".format(self.client_address[0]))
        print("DataLength:{}".format(len(self.data)))
        print(self.data)
        # 受信したデータをShiftJisにしてbyte化
        rdata = self.data.decode('sjis')
        print("after sjis decode:[]", rdata)
        # XMLから取得(UNICODE Byte)
        sdata = readxmltxt()
        print("File Data:[]", sdata)
        #sdata = readxmltxt().decode('sjis')
        #sdata = rdata[:10] + resultCD + rdata[12:128] + resultCD + errorCD + rdata[121:]
        # sdata = "3114000030T1000134                    0000000100000000191115164607                                                               114310000600066001366122000189    000000000"
        #print("Send Data:[]", sdata.encode('utf8'))
        #senddata = sdata.decode('utf8')
        senddata = sdata.encode('sjis')
        print("senddata ", senddata)
        #self.request.sendall(senddata.upper())
        time.sleep(2)
        self.request.sendall(senddata)
        time.sleep(1)
        # 別ホスト(この場合VEGA)に受け取った電文をそのまま送信
        #self.sendDI()
        #hsvr, hport = "192.168.0.133", 8888

        hsvr, hport = dist, 9999
        print("Distport:{}".format(dist))
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((hsvr, hport))
        # 画面遷移ID001を送ってやる
        snddata = ""
        snddata = "311909000000000003                    001"
        print("SEND DISP ID:{}", snddata.encode('sjis'))
        client.send(snddata.encode('sjis'))
        # 別ホスト(この場合VEGA)からの電文を受信(取り敢えずバッファ4Kにしておく)
        rev = client.recv(512)
        # 別ホスト(この場合VEGA)から受信した電文を加工せずにクライアント1に還す
        # self.request.sendall(rev)
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
    # 交通系正常リターン(レシートあり)
    fnm = "ReceiptData01.txt"
    # WAON正常リターン(レシートあり)
    #fnm = "ReceiptData00.txt"
    # WAON正常リターン(レシートあり---文言長)
    # fnm = "ReceiptData02.txt"
    with open(fnm, 'r') as f:
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
