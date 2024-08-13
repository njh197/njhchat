from socketserver import ThreadingTCPServer, BaseRequestHandler
import chatlib,logging,queue,json
new_message=[b'']
logger = logging.getLogger('NJH Chat Server')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
consoleHeader = logging.StreamHandler()
consoleHeader.setFormatter(formatter)
consoleHeader.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler("njhchat_server.log")
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.addHandler(consoleHeader)
class ChatServer(BaseRequestHandler):
    def handle(self):
        global new_message
        logger.info(f"started a connection with {self.client_address}")
        # 获取客户端发送的数据
        while True:
            head=self.request.recv(8)
            length=int.from_bytes(head[1:],byteorder="big",signed=False)
            if not head:
                break
            if head[0]==1:
                chatlib.send(self.request,new_message[-1])
            elif head[0]==2:
                data = self.request.recv(length)
                if not data:
                    break
                logger.info(f"Received from client: {data}")
                if new_message[-1]!=data:
                    new_message.append(data)
                if len(new_message)>100:
                    del new_message[0]
                    logger.info("reached the limit,deleted a message before")
            elif head[0]==3:
                logger.info(f"{self.client_address} get all messages")
                logger.debug(repr(new_message))
                b_ls=b''
                for i in new_message:
                    if i!=b'':
                        b_ls+=b'\x02'+len(i).to_bytes(length=7,byteorder="big",signed=False)+i
                logger.debug(repr(b_ls))
                chatlib.send(self.request,b_ls)
        logger.info(f"stopped a connection with {self.client_address}")

HOST, PORT = '127.0.0.1', 15432
server = ThreadingTCPServer((HOST, PORT), ChatServer)
logger.info("server started")
server.serve_forever()
