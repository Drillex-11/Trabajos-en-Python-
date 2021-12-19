# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 03:30:29 2021

@author: Sebastian
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
import socket
from time import sleep
import threading

HOST = "127.0.0.1"  #Se mantiene un host fijo 
PORT = 5000
HEADER_SIZE = 10


class Server:
    def __init__(self, master):
        self.master = master
        self.PORT = 5000
        
        self.master.title(f"SERVIDOR")
        self.master.geometry("+50+50")
        self.master.resizable(0, 0)
        # ------------------------ FRAMES -----------------------------
        frm1 = tk.LabelFrame(self.master, text="Server")
        frm2 = tk.Frame(self.master)
        frm1.pack(padx=5, pady=5, anchor=tk.W)
        frm2.pack(padx=5, pady=5, fill='y', expand=True)
        
        # ------------------------ FRAME 1 ----------------------------
        self.lblip = tk.Label(frm1, text=" ") 
        self.space1 = tk.Label(frm1, text="    ") 
        self.space2 = tk.Label(frm1, text="    ") 
        
        self.space1.grid(row=0, column=0, padx=5, pady=5)
        self.lblip.grid(row=0, column=1, padx=5, pady=5)
        self.space2.grid(row=0, column=2, padx=5, pady=5)

        # ------------------------ FRAME 2 ---------------------------
        self.txtChat = ScrolledText(frm2, height=15, width=38, wrap=tk.WORD,
                                    state='disable')
        self.txtChat.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
               
        # --------------------------- StatusBar -----------------------
        self.statusBar = tk.Label(self.master, bd=1, relief=tk.SUNKEN,
                                  anchor=tk.W, text = "Esperando conexiones...")
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X)
        
        
        #--------------------------------------------------------------
        
        
        # Lista con los sockets de los clientes
        self.connections = []
        self.colores = ['morado', 'verde', 'azul', 'rojo']
        self.colorin = ['purple', 'green', 'blue', 'red']
        # Socket del servidor
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST, PORT))
        self.sock.listen()
        
        th = threading.Thread(target=(self.run), daemon=True)
        th.start()
        
    def run(self):
        try:    
           
            self.lblip.config(text = "  Servidor iniciado  ",
                              font = 'Arial 12 bold', width = 25)
            ###################################################
            i = 0
            while True:
                self.txtChat.config(state = 'normal')
                conn, addr = self.sock.accept()
                
                th = threading.Thread(target=self.Conn2, 
                                      args=(conn, addr), 
                                      daemon=True)
                th.start()
                
                #print(f"{addr[0]}:{addr[1]} conectado")
                
                if len(self.connections) >= 0:
                    self.txtChat.insert(tk.INSERT,
                                    f"{addr[0]}:{addr[1]} Conectado     " + '\n', self.colores[i])
                    self.txtChat.tag_config(self.colores[i], foreground = self.colorin[i])
                    i = i +1
               
                
                if i == 4:
                    i = 0
                self.connections.append(conn)
                self.txtChat.config(state = 'disable')
        except:
            self.txtChat.config(state = 'disable')
            pass
            
            
    def Conn2(self, conn, addr):
    
        
        while True:
            # Si es que no hay un problema con la conexion del cliente...
            try:
                self.txtChat.config(state = 'normal')
                # Lee el encabezado para el buffer y el payload
                data_header = conn.recv(HEADER_SIZE)
                data = conn.recv(int(data_header))
                
                # Hace un broadcast del dato entrante a los demas sockets
                for connection in self.connections:
                    if connection != conn:
                        connection.send(data_header + data)
                self.txtChat.config(state = 'disable')
            # Si hay problemas con la conexion del cliente...
            except:
                self.txtChat.config(state = 'normal')
                # el clente se ha desconectado. Informar y eliminar de la lista
               
                self.txtChat.insert(tk.INSERT,
                    f"{addr[0]}:{addr[1]} Desconectado  " + '\n', 'negro')
                self.txtChat.tag_config('negro', foreground = 'black')

                self.txtChat.config(state = 'disable')
                self.connections.remove(conn)
                conn.close()
                break
        
    
    
root = tk.Tk()
app = Server(root)
root.mainloop()