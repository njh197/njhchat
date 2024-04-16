from Crypto.Cipher import AES
def encrypt(s,key):
    aes_obj=AES.new(key,AES.MODE_CTR)
    cipher=aes_obj.encrypt(s)
    return cipher,aes_obj.nonce

def decrypt(s,key,nonce):
    aes_obj=AES.new(key,AES.MODE_CTR,nonce=nonce)
    plaintext=aes_obj.decrypt(s)
    return plaintext

def send(sock,message):
    head=b'\x02'+len(message).to_bytes(length=7,byteorder="big",signed=False)
    sock.sendall(head)
    sock.sendall(message)

def receive(sock):
    sock.sendall(b'\x01')
    head=sock.recv(8)[1:]
    length=int.from_bytes(head,byteorder="big",signed=False)
    body=sock.recv(length)
    return body
