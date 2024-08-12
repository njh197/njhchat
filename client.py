import tkinter as tk
from tkinter import messagebox
import socket,threading,time,sys,json,os,logging,queue,platform
import chatlib

username=None
addr=None
key=None
need_send=False
need_close=False
last_received=""
message=b""
canv_y=0
os_name=platform.system()
logger = logging.getLogger('NJH Chat Client')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
consoleHeader = logging.StreamHandler()
consoleHeader.setFormatter(formatter)
consoleHeader.setLevel(logging.INFO)
fileHandler = logging.FileHandler(f"njhchat_client.log")
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.addHandler(consoleHeader)
def connect():
    global need_send,last_received,canv_y
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(addr)
        logger.info(f"Connected to server {addr}")
        old_message=chatlib.get_all_message(sock)
        if old_message:
            logger.debug(repr(old_message))
            text1.append(canvas.create_text(1,canv_y,text="\n".join(old_message),anchor=tk.NW,font=("宋体",20)))
            canv_y=canvas.bbox(text1[-1])[3]
            canvas.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
            canvas.yview_moveto(1.0)
            last_received=old_message[-1]
        while True:
            if need_send:
                chatlib.send(sock,message)
                text2.delete('0.0','end')
                need_send=False
            data=chatlib.receive(sock)
            data=data.decode(encoding='utf8')
            if last_received!=data and data!='\n':
                text1.append(canvas.create_text(1,canv_y,text=data,anchor=tk.NW,font=("宋体",20)))
                canv_y=canvas.bbox(text1[-1])[3]
                canvas.update_idletasks()
                canvas.config(scrollregion=canvas.bbox("all"))
                canvas.yview_moveto(1.0)
                last_received=data
            if need_close:
                break
            time.sleep(0.2)
    except Exception as err:
        logger.error(str(err))
        messagebox.showerror(title="子线程发生错误!",message="请将以下报错信息发给njh197\n"+str(err))
        on_closing()
    finally:
        sock.close()

def send_message():
    global message,need_send
    message=text2.get('0.0','end').strip()
    if message:
        message=bytes(f"<{username}> {message}",encoding='utf8')
        need_send=True

def finish_login():
    global username,key,addr
    username=entry1.get()
    key=entry2.get()
    login.destroy()
    #print(username,pwd,addr)

def on_closing():
    global need_close
    need_close=True
    root.destroy()
    time.sleep(0.3)
def scroll(event):
    if os_name=="Windows":
        canvas.yview_scroll(-1 * int(event.delta/120),"units")
    elif os_name=="Linux":
        canvas.yview_scroll((-1)*event.delta)

try:
    if not os.path.exists("config.json"):
        with open("config.json",mode='w') as f:
            f.write("{}")
        logger.info("Generated config.json")
    with open("config.json") as f:
        conf=json.load(f)
    with open("config.json",mode='w') as f:
        conf["server_address"]=conf.get("server_address","47.97.49.128")
        conf["port"]=conf.get("port",15432)
        json.dump(conf,f)
    addr=(conf["server_address"],conf["port"])

    #登录界面
    login=tk.Tk()
    login.geometry("430x140")
    login.title("NJH Chat Login")
    label1=tk.Label(login,text="请输入用户名:")
    entry1=tk.Entry(login,font=("宋体",25))
    label2=tk.Label(login,text="请输入密钥:")
    entry2=tk.Entry(login,font=("宋体",25))
    login_button=tk.Button(login,text="确定",font=("宋体",25),command=finish_login)
    label1.grid(row=0,column=0)
    entry1.grid(row=0,column=1)
    label2.grid(row=1,column=0)
    entry2.grid(row=1,column=1)
    login_button.grid(row=3,column=0,columnspan=2)
    login.mainloop()
    if username is None:
        sys.exit(0)

    #主界面
    root=tk.Tk()
    root.geometry("400x600")
    root.title("NJH Chat")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    frame1=tk.Frame(root)
    text1=[]
    text2=tk.Text(root,font=("宋体",20),width=28,height=3)
    space1=tk.Label(root,text="",font=("宋体",10))
    space2=tk.Label(root,text="",font=("宋体",10))
    button=tk.Button(root,text="发送",font=("宋体",20),command=send_message)
    scrbar1=tk.Scrollbar(frame1,orient="vertical")
    scrbar2=tk.Scrollbar(frame1,orient="horizontal")
    canvas=tk.Canvas(frame1,yscrollcommand=scrbar1.set,xscrollcommand=scrbar2.set)
    canvas.bind_all('<MouseWheel>', scroll)
    frame1.pack(fill=tk.BOTH,expand=True)
    space1.pack()
    text2.pack(fill=tk.X)
    space2.pack()
    button.pack()
    scrbar1.pack(side=tk.RIGHT,fill=tk.Y)
    scrbar2.pack(side=tk.BOTTOM,fill=tk.X)
    canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
    scrbar1.config(command=canvas.yview)
    scrbar2.config(command=canvas.xview)

    thr=threading.Thread(target=connect)
    thr.daemon=True
    thr.start()
    root.mainloop()
except Exception as err:
    logger.error(str(err))
    messagebox.showerror(title="主线程发生错误!",message="请将以下报错信息发给njh197\n"+str(err))
    on_closing()
