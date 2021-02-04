# encode:utf-8

import socket
import socketserver
import threading
import json
import time


# 処理未了テスト用のpythonプードルソースです。。。
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
        print("DspID=404 sending")
        # 処理未了の画面遷移IDを送信する
        senddspid("404")
        print("Waiting now for 1minutes")
        # 0.5分待機
        time.sleep(30)
        senddspid("403")
        print("Waiting now for 1minutes")
        # １分待機
        time.sleep(30)
        #sdata = rdata[:10]
        # 結果コード3バイトとエラーコード3バイトをセット
        resultCD = "T10"
        errorCD = "803"
        sdata = rdata[:10] + resultCD + rdata[12:128] + resultCD + errorCD + rdata[121:]
        '''
        # リターンデータにレシート情報を付加する(xml)
        sdata = sdata[0:172]
        xmtex=""
        #with open('TestMiryo.txt', encoding='utf8') as fl:
        #with open('ResponceData.txt', encoding='utf8') as fl:
        with open('disCompData.txt', encoding='utf8') as fl:
            xmtex = fl.read()
            print(xmtex)
            sdata = sdata.upper() + xmtex
            sdata = xmtex
        '''
        sdata = "3114000030T1000134                    0000000100000000191115164607                                                               114310000600066001366122000189    000000000"
        print("Send Data:[]", sdata)
        senddata = sdata.encode('sjis')
        print("senddata byte:[]", senddata)
        self.request.sendall(senddata)
        time.sleep(1)
        # 処理完了の画面遷移IDを送信する
        senddspid("001")
        '''
        # 別ホスト(この場合VEGA)に受け取った電文をそのまま送信
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
        '''


def senddspid(id):
    hsvr, hport = dist, 9999
    print("Distport:{}".format(dist))
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((hsvr, hport))
    # 画面遷移ID001を送ってやる
    #snddata = "311909000000000003                    001"
    # 画面遷移ID404を送ってやる
    snddata = "311909000000000003                    " + id
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
