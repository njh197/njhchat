import tkinter as tk
import socket,threading,time,chatlib

username=None
addr=None
key=None
need_send=False
need_close=False
last_received=""
message=b""

def connect():
    global need_send,last_received
    SERVER_IP=addr
    SERVER_PORT=15432
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_IP, SERVER_PORT))
        print(f"Connected to server {SERVER_IP}:{SERVER_PORT}")
        while True:
            if need_send:
                chatlib.send(sock,message)
                text2.delete('0.0','end')
                need_send=False
            data=chatlib.receive(sock)
            data=data.decode(encoding='utf8')+'\n'
            if last_received!=data:
                text1['state']='normal'
                text1.insert('end',data)
                text1['state']='disabled'
                last_received=data
            if need_close:
                break
            time.sleep(0.2)
    finally:
        sock.close()

def send_message():
    global message,need_send
    message=text2.get('0.0','end').strip()
    if message:
        message=bytes(username+": "+message,encoding='utf8')
        need_send=True

def finish_login():
    global username,key,addr
    username=entry1.get()
    key=entry2.get()
    addr=entry3.get()
    login.destroy()
    #print(username,pwd,addr)

def on_closing():
    global need_close
    need_close=True
    root.destroy()
    time.sleep(0.3)

#登录界面
login=tk.Tk()
login.geometry("460x170")
login.title("NJH Chat Login")
label1=tk.Label(login,text="请输入用户名:")
entry1=tk.Entry(login,font=("宋体",25))
label2=tk.Label(login,text="请输入密钥:")
entry2=tk.Entry(login,font=("宋体",25))
label3=tk.Label(login,text="请输入服务器IP:")
entry3=tk.Entry(login,font=("宋体",25))
login_button=tk.Button(login,text="确定",font=("宋体",25),command=finish_login)
label1.grid(row=0,column=0)
entry1.grid(row=0,column=1)
label2.grid(row=1,column=0)
entry2.grid(row=1,column=1)
label3.grid(row=2,column=0)
entry3.grid(row=2,column=1)
login_button.grid(row=3,column=1)
login.mainloop()
if username is None:
    exit(0)

#主界面
root=tk.Tk()
root.geometry("400x600")
root.title("NJH Chat")
root.protocol("WM_DELETE_WINDOW", on_closing)
text1=tk.Text(root,font=("宋体",20),width=28,height=15,state=tk.DISABLED)
text2=tk.Text(root,font=("宋体",20),width=28,height=3)
space1=tk.Label(root,text="",font=("宋体",10))
space2=tk.Label(root,text="",font=("宋体",10))
button=tk.Button(root,text="发送",font=("宋体",20),command=send_message)
text1.grid(row=0,column=0)
space1.grid(row=1,column=0)
text2.grid(row=2,column=0)
space2.grid(row=3,column=0)
button.grid(row=4,column=0)

thr=threading.Thread(target=connect)
thr.daemon=True
thr.start()

root.mainloop()
