import tkinter as tk
from tkinter import messagebox
import socket,threading,time,sys,json,os,logging,queue,platform
import chatlib

username=None
addr=("127.0.0.1",15432)
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
        data=chatlib.get_all_message(sock)
        print(data)
    except Exception as err:
        logger.error(str(err))
        messagebox.showerror(title="子线程发生错误!",message="请将以下报错信息发给njh197\n"+str(err))
        on_closing()
    finally:
        sock.close()

while True:
    input()
    connect()
