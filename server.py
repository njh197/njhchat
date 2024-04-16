from socketserver import ThreadingTCPServer, BaseRequestHandler
import chatlib
new_message=b""
class ChatServer(BaseRequestHandler):
    def handle(self):
        global new_message
        print(f"started a connection with {self.client_address}")
        # 获取客户端发送的数据
        while True:
            head=self.request.recv(8)
            length=int.from_bytes(head[1:],byteorder="big",signed=False)
            if not head:
                break
            if head[0]==1:
                chatlib.send(self.request,new_message)
            elif head[0]==2:
                data = self.request.recv(length)
                if not data:
                    break
                print(f"Received from client: {data}")
                new_message=data
        print(f"stopped a connection with {self.client_address}")

HOST, PORT = '127.0.0.1', 15432
server = ThreadingTCPServer((HOST, PORT), ChatServer)
server.serve_forever()
