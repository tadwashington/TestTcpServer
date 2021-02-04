# encode:utf-8


import socketserver


class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):

        # self.data = self.request.recv(1024).strip()

        self.data = self.request.recv(1024)
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # CLIENTに送り返す文字列
        # 電子マネー(Suica正常)
        sendata='311400617200001963                    0000033000000000201128111805                                                               000000000500055223002586002274    000001829'\
                '<?xml version="1.0"?><receiptInfo><header><date>2020/11/28</date><time>11:18:05</time><brand>交通系</brand>'\
                '<amount>￥330</amount><proc>支払</proc></header><body><receiptNum>1</receiptNum><receiptList><receipt><type>1</type>'\
                '<itemNum>16</itemNum><itemList><item><newline>1</newline><left></left><center>電子マネー売上票</center><right></right></item>'\
                '<item><newline>1</newline><left></left><center></center><right></right></item><item><newline>0</newline><left>ｺﾅﾐｽﾎﾟｰﾂｸﾗﾌﾞ ｲｲﾀﾞﾊﾞｼ</left><center></center><right></right></item>'\
                '<item><newline>0</newline><left>東京都新宿区揚場町２－１軽子坂ＭＮビルＢ１Ｆ</left><center></center><right></right></item>'\
                '<item><newline>0</newline><left>電話： 03-3266-9301</left><center></center><right></right></item>'\
                '<item><newline>0</newline><left>2020年11月28日 11時18分</left><center></center><right></right></item>'\
                '<item><newline>1</newline><left></left><center>交通系支払</center><right></right></item>'\
                '<item><newline>1</newline><left>交通系支払</left><center></center><right>￥330</right></item><item><newline>0</newline><left>交通系残高</left><center></center><right>￥11,330</right></item>'\
                '<item><newline>1</newline><left></left><center></center><right></right></item><item><newline>0</newline><left>カード番号</left><center></center><right>JE*** **** **** 3520</right></item>'\
                '<item><newline>0</newline><left>SPRWID</left><center></center><right>JE10740517216</right></item><item><newline>1</newline><left></left><center></center><right></right></item>'\
                '<item><newline>0</newline><left>端末# 01851</left><center></center><right>レシート# 02274</right></item><item><newline>0</newline><left>問い合わせ番号</left><center></center><right>0005-5223002586</right></item>'\
                '<item><newline>12</newline><left></left><center></center><right></right></item></itemList></receipt></receiptList></body></receiptInfo>'
        # クレジット決済正常
        # sendata = "311100617800000391                    0001154000000000201128140934497116245000605025XXXXXXXXXXXX8905    NAMIZOU/OONAMI           10 1022JCB GROUP XXXX    0000000990 ｺﾅﾐｽﾎﾟｰﾂｸﾗﾌﾞ ｲｲﾀﾞﾊﾞｼ   03-3266-9301           ご利用ありがとうございました\nまたのご来店をお待ちしております                                                                           A0000000651010                   0019 J/Smart   JCB Credit                      00"
        # クレジット決済エラー(D90)
        # sendata =   "3111006179D9000391                    0000330000000000201128142226497116245000605026XXXXXXXXXXXX8001   UENO/YUKARI               10 1041ﾋﾞｻﾞ/ﾏｽﾀｰ XXXX    0000000990 ｺﾅﾐｽﾎﾟｰﾂｸﾗﾌﾞ ｲｲﾀﾞﾊﾞｼ   03-3266-9301           不明なエラー\n" \
# "ヘルプデスクにお問合せ下さい\n" \
# "TEL : 0120-044-877\n" \
# "\n" \
# "<D90>                                                                                                                                                      "
        # CLIENTに送り返す文字列をShift-jisでByte化
        # Shift-JISエンコードでエラーを起こしたのでリプレース('\uff0d')
        sendata = sendata.replace('\uff0d', '-')
        sendbyte = sendata.encode('shift-jis')
        # sendbyte = sendata.encode('utf-8')
        # 送り返す。いわゆる返信な
        self.request.sendall(sendbyte)
        #self.request.sendall(self.data.upper())


if __name__ == "__main__":
    HOST, PORT = "192.168.0.102", 8888
    with socketserver.TCPServer((HOST, PORT), MyTcpHandler) as server:
        server.serve_forever()
