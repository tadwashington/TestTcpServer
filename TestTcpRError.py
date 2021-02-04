# coding: utf-8

import socket
import socketserver
import threading
import json
import time
import random

# リターンコードの配列生成
l = ['203', '204', '303', '401', '403', '408', '409', '413', '502', '503', '504']
# この受信は何回目？のカウント
ix = 0

class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global ix
        # リターンコードの配列生成
        l = ['203', '204', '303', '401', '403', '408', '409', '413', '502', '503', '504']
        # クライアント1からTCP電文を受信
        # self.data = self.request.recv(1024).strip()
        self.data = self.request.recv(1024)
        print("{} wrote:".format(self.client_address[0]))
        print("DataLength:{}".format(len(self.data)))
        print(self.data)
        # 先頭から10バイトをセット
        rdata = self.data.decode('sjis')
        print("after sjis decode:[]", rdata)
        sdata = ""
        #sdata = rdata[:10]

        ic = [0, 1, 2]
        # ix = 2

        if ix == 0:
            # エラー結果コード3バイトとエラーコード3バイトをセット
            resultCD = "T10"
            errorCD = "801"
            # errorCD = random.choice(l)
            print("ErrorCode:[]", errorCD)
            #
            #sdata = readxmltxt()
            #sdata = readxmltxt().decode('sjis')
            sdata = rdata[:10] + resultCD + rdata[12:128] + resultCD + errorCD + rdata[121:]
            sdata = sdata.replace('\uff0d', '-')
            senddata = sdata.encode('sjis')
            # ix = random.choice(ic)
            '''
            0:最初のエラー,1:決済成功,2:処理未了→決済成功,3:決済エラー
            '''
            ix = 2

        elif ix == 1:
            '''
            # 2回目のリターンを作る
            # エラー結果コード3バイトとエラーコード3バイトをセット
            resultCD = "000"
            errorCD = "000"
            print("ErrorCode:[]", errorCD)
            #
            # sdata = '311400161500001964                    0000200000000000201213114725                                                               000000000500055230549651000498    000001830<?xml version="1.0"?><receiptInfo><header><date>2020/12/13</date><time>11:47:25</time><brand>交通系</brand><amount>￥2,000</amount><proc>支払</proc></header><body><receiptNum>1</receiptNum><receiptList><receipt><type>1</type><itemNum>16</itemNum><itemList><item><newline>1</newline><left></left><center>電子マネー売上票</center><right></right></item><item><newline>1</newline><left></left><center></center><right></right></item><item><newline>0</newline><left>ｺﾅﾐｽﾎﾟｰﾂｸﾗﾌﾞ ｶﾏﾀ</left><center></center><right></right></item><item><newline>0</newline><left>東京都大田区蒲田５－４７－７マルエツ蒲田店５Ｆ</left><center></center><right></right></item><item><newline>0</newline><left>電話： 03-3737-1601</left><center></center><right></right></item><item><newline>0</newline><left>2020年12月13日 11時47分</left><center></center><right></right></item><item><newline>1</newline><left></left><center>交通系支払</center><right></right></item><item><newline>1</newline><left>交通系支払</left><center></center><right>￥2,000</right></item><item><newline>0</newline><left>交通系残高</left><center></center><right>￥2,141</right></item><item><newline>1</newline><left></left><center></center><right></right></item><item><newline>0</newline><left>カード番号</left><center></center><right>JE*** **** **** 5884</right></item><item><newline>0</newline><left>SPRWID</left><center></center><right>JE10740517211</right></item><item><newline>1</newline><left></left><center></center><right></right></item><item><newline>0</newline><left>端末# 01846</left><center></center><right>レシート# 00498</right></item><item><newline>0</newline><left>問い合わせ番号</left><center></center><right>0005-5230549651</right></item><item><newline>12</newline><left></left><center></center><right></right></item></itemList></receipt></receiptList></body></receiptInfo>'
            '''
            sdata = '311400161500001964                    ' \
                    '0000200000000000201213114725                                                               ' \
                    '000000000500055230549651000498    000001830' \
                    '<?xml version="1.0"?><receiptInfo><header><date>2020/12/13</date><time>11:47:25</time>' \
                    '<brand>交通系</brand><amount>￥2,000</amount><proc>支払</proc></header><body><receiptNum>1</receiptNum>' \
                    '<receiptList><receipt><type>1</type><itemNum>16</itemNum><itemList>' \
                    '<item><newline>1</newline><left></left><center>電子マネー売上票</center><right></right></item>' \
                    '<item><newline>1</newline><left></left><center></center><right></right></item>' \
                    '<item><newline>0</newline><left>ｺﾅﾐｽﾎﾟｰﾂｸﾗﾌﾞ ｶﾏﾀ</left><center></center><right></right></item>' \
                    '<item><newline>0</newline><left>東京都大田区蒲田５－４７－７マルエツ蒲田店５Ｆ</left><center></center><right></right>' \
                    '</item><item><newline>0</newline><left>電話： 03-3737-1601</left><center></center><right></right></item>' \
                    '<item><newline>0</newline><left>2020年12月13日 11時47分</left><center></center><right></right></item>' \
                    '<item><newline>1</newline><left></left><center>交通系支払</center><right></right></item>' \
                    '<item><newline>1</newline><left>交通系支払</left><center></center><right>￥2,000</right></item>' \
                    '<item><newline>0</newline><left>交通系残高</left><center></center><right>￥2,141</right></item>' \
                    '<item><newline>1</newline><left></left><center></center><right></right></item>' \
                    '<item><newline>0</newline><left>カード番号</left><center></center><right>JE*** **** **** 5884</right></item>' \
                    '<item><newline>0</newline><left>SPRWID</left><center></center><right>JE10740517211</right></item>' \
                    '<item><newline>1</newline><left></left><center></center><right></right></item>' \
                    '<item><newline>0</newline><left>端末# 01846</left><center></center><right>レシート# 00498</right></item>' \
                    '<item><newline>0</newline><left>問い合わせ番号</left><center></center><right>0005-5230549651</right></item>' \
                    '<item><newline>12</newline><left></left><center></center><right></right></item>' \
                    '</itemList></receipt></receiptList></body></receiptInfo>'
            ix = 0
        elif ix == 2:
            miryou(self)
            ix = 0
            return
        elif ix == 3:
            resultCD = "T10"
            errorCD = "310"
            # errorCD = random.choice(l)
            print("ErrorCode:[]", errorCD)
            #
            #sdata = readxmltxt()
            #sdata = readxmltxt().decode('sjis')
            sdata = rdata[:10] + resultCD + rdata[12:128] + resultCD + errorCD + rdata[121:]
            sdata = sdata.replace('\uff0d', '-')
            senddata = sdata.encode('sjis')

        sdata = sdata.replace('\uff0d', '-')
        senddata = sdata.encode('sjis')
        # senddata = sdata.encode('utf8')
        time.sleep(11)

        # sdata = "3114000030T1000134                    0000000100000000191115164607                                                               114310000600066001366122000189    000000000"
        # print("Send Data:[]", sdata.encode('sjis'))
        # senddata = sdata.encode('sjis')

        # sdata = sdata.replace('\uff0d', '-')
        # senddata = sdata.encode('sjis')
        print("senddata byte:[]", senddata)
        # self.request.sendall(senddata.upper())
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

# 処理未了パターン
def miryou(self):
    hsvr, hport = dist, 9999
    print("Distport:{}".format(dist))
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((hsvr, hport))
    # 画面遷移ID404(処理未了)を送ってやる
    snddata = "311909000000000003                    404"
    print("SEND DISP ID:{}", snddata.encode('sjis'))
    client.send(snddata.encode('sjis'))
    # クライアントを開放する
    client.close()
    # 1分待機(VEGAで操作してる風にする)
    time.sleep(60)
    '''
    1分待ったら正常データを送ってあげる。
    但し、本当の処理未了後の正常データはレシート2枚付くけど今回はテストなのでそこは勘弁してもらう
    '''
    sdata = '311400161500001964                    ' \
            '0000200000000000201213114725                                                               ' \
            '000000000500055230549651000498    000001830' \
            '<?xml version="1.0"?><receiptInfo><header><date>2020/12/13</date><time>11:47:25</time>' \
            '<brand>交通系</brand><amount>￥2,000</amount><proc>支払</proc></header><body><receiptNum>1</receiptNum>' \
            '<receiptList><receipt><type>1</type><itemNum>16</itemNum><itemList>' \
            '<item><newline>1</newline><left></left><center>電子マネー売上票</center><right></right></item>' \
            '<item><newline>1</newline><left></left><center></center><right></right></item>' \
            '<item><newline>0</newline><left>ｺﾅﾐｽﾎﾟｰﾂｸﾗﾌﾞ ｶﾏﾀ</left><center></center><right></right></item>' \
            '<item><newline>0</newline><left>東京都大田区蒲田５－４７－７マルエツ蒲田店５Ｆ</left><center></center><right></right>' \
            '</item><item><newline>0</newline><left>電話： 03-3737-1601</left><center></center><right></right></item>' \
            '<item><newline>0</newline><left>2020年12月13日 11時47分</left><center></center><right></right></item>' \
            '<item><newline>1</newline><left></left><center>交通系支払</center><right></right></item>' \
            '<item><newline>1</newline><left>交通系支払</left><center></center><right>￥2,000</right></item>' \
            '<item><newline>0</newline><left>交通系残高</left><center></center><right>￥2,141</right></item>' \
            '<item><newline>1</newline><left></left><center></center><right></right></item>' \
            '<item><newline>0</newline><left>カード番号</left><center></center><right>JE*** **** **** 5884</right></item>' \
            '<item><newline>0</newline><left>SPRWID</left><center></center><right>JE10740517211</right></item>' \
            '<item><newline>1</newline><left></left><center></center><right></right></item>' \
            '<item><newline>0</newline><left>端末# 01846</left><center></center><right>レシート# 00498</right></item>' \
            '<item><newline>0</newline><left>問い合わせ番号</left><center></center><right>0005-5230549651</right></item>' \
            '<item><newline>12</newline><left></left><center></center><right></right></item>' \
            '</itemList></receipt></receiptList></body></receiptInfo>'
    sdata = sdata.replace('\uff0d', '-')
    senddata = sdata.encode('sjis')
    print("senddata byte:[]", senddata)
    # self.request.sendall(senddata.upper())
    self.request.sendall(senddata)
    time.sleep(1)
    '''
    DSP_ID:001を送るよ
    '''
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


def readxmltxt():
    with open('ReceiptData01.txt', 'rb') as f:
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
