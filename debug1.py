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
logger = logging.getLogger('NJH Chat Debug')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
consoleHeader = logging.StreamHandler()
consoleHeader.setFormatter(formatter)
consoleHeader.setLevel(logging.DEBUG)
logger.addHandler(consoleHeader)
def connect():
    global need_send,last_received,canv_y
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(addr)
        logger.info(f"Connected to server {addr}")
        data=chatlib.get_all_message(sock)
        print(data)
    finally:
        sock.close()

while True:
    input()
    connect()
