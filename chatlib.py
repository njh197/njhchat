from Crypto.Cipher import AES
def encrypt(s, key):
    aes_obj = AES.new(key, AES.MODE_EAX)
    cipher, tag = aes_obj.encrypt_and_digest(s)
    return cipher, aes_obj.nonce, tag

def decrypt(s, key, nonce, tag):
    aes_obj = AES.new(key, AES.MODE_EAX, nonce = nonce)
    plaintext = aes_obj.decrypt(s)
    aes_obj.verify(tag)
    return plaintext

def send(sock, message):
    head = b'\x02' + len(message).to_bytes(length = 7, byteorder = "big", signed = False)
    sock.sendall(head)
    sock.sendall(message)

def receive(sock,code=b'\x01'):
    sock.sendall(code)
    head = sock.recv(8)[1:]
    length = int.from_bytes(head, byteorder="big", signed=False)
    body = sock.recv(length)
    return body

def get_all_message(sock,debug=False):
    if not debug:
        aa=receive(sock,b'\x03')
    else:
        aa=b'\x02\x00\x00\x00\x00\x00\x00\x10abcdefghijabcdef\x02\x00\x00\x00\x00\x00\x00\x0A1234567890'
    ls=[]
    i=0
    while i<len(aa):
        head=aa[i+1:i+8]
        i+=8
        length = int.from_bytes(head, byteorder="big", signed=False)
        body=aa[i:i+length]
        i+=length
        ls.append(body.decode(encoding="utf8"))
    return ls
    
if __name__ == '__main__':
    print(get_all_message(None,True))
