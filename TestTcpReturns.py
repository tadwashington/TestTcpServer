# encode:utf-8

import socket
import socketserver
import threading
import json
import time

class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # クライアント1からTCP電文を受信
        # self.data = self.request.recv(1024).strip()
        self.data = self.request.recv(1024)
        print("{} wrote:".format(self.client_address[0]))
        print("DataLength:{}".format(len(self.data)))
        print(self.data)
        # 先頭から10バイトをセット
        rdata = self.data.decode('sjis')
        print("after sjis decode:[]", rdata)
        #sdata = rdata[:10]
        # 結果コード3バイトとエラーコード3バイトをセット
        resultCD = "000"
        errorCD = "000"
        money = "00018952" #金額8桁
        sdata = rdata[:10] + resultCD + rdata[12:37] + money +  rdata[45:128] + resultCD + errorCD + rdata[121:]
        print("Send Data:[]", sdata)
        senddata = sdata.encode('sjis')
        print("senddata byte:[]", senddata)
        self.request.sendall(senddata.upper())
        time.sleep(1)
        # 別ホスト(この場合VEGA)に受け取った電文をそのまま送信
        #self.sendDI()
        #hsvr, hport = "192.168.0.133", 8888

        hsvr, hport = dist, 9999
        print("Distport:{}".format(dist))
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((hsvr, hport))
        # 画面遷移ID001を送ってやる
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


# Main
if __name__ == "__main__":
    adrs = getaddr()
    dist = readjson(adrs)
    HOST, PORT = adrs, 8888
    with socketserver.TCPServer((HOST, PORT), MyTcpHandler) as server:
        server.serve_forever()
