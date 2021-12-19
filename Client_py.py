# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 03:30:21 2021

@author: Sebastian
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
import socket
from time import sleep
import threading
import tkinter.messagebox
HOST = "127.0.0.1"   
PORT = 5000
HEADER_SIZE = 10


class Client:
    def __init__(self, master, ):
        self.address = "Desconocido"
        self.master = master
        self.PORT = 5000
        self.master.title(f"Chat")
        self.master.geometry("+50+50")
        self.master.resizable(0, 0)
        
        self.address = tk.StringVar()
        self.username = tk.StringVar()
        self.envio = tk.StringVar()
        # ------------------------ FRAMES -----------------------------
        frm1 = tk.LabelFrame(self.master, text="Server")
        frm2 = tk.Frame(self.master)
        frm3 = tk.LabelFrame(self.master, text="Enviar mensaje")
        frm1.pack(padx=5, pady=5, anchor=tk.W)
        frm2.pack(padx=5, pady=5, fill='y', expand=True)
        frm3.pack(padx=5, pady=5)
        
        # ------------------------ FRAME 1 ----------------------------
        self.lblip = tk.Label(frm1, text="Dirección: ") 
        self.entip = tk.Entry(frm1, textvariable = self.address) 
        self.lblSpace = tk.Label(frm1, text="")
        self.btnConnect = ttk.Button(frm1, text="Conectar", width=16,
                                     command = self.cone)
        self.btnBorra = ttk.Button(frm1, text="Borrar", width=16,
                                     command = self.borrar)
        self.lblus = tk.Label(frm1, text="Usuario: ") 
        self.entus = tk.Entry(frm1, textvariable = self.username)

        self.lblip.grid(row=0, column=0, padx=5, pady=5)
        self.entip.grid(row=0, column=1, padx=5, pady=5)
        self.lblSpace.grid(row=0,column=2, padx=30, pady=5)
        self.btnConnect.grid(row=0, column=3, padx=5, pady=5)
        self.btnBorra.grid(row=1,column=3,padx=20,pady=5)
        self.lblus.grid(row=1, column=0, padx=5, pady=5)
        self.entus.grid(row=1, column=1, padx=5, pady=5)
        
        # ------------------------ FRAME 2 ---------------------------
        self.txtChat = ScrolledText(frm2, height=25, width=50, wrap=tk.WORD,
                                    state='disable')
        self.txtChat.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
    
        # ------------------------ FRAME 3 --------------------------
        self.lblText = tk.Label(frm3, text="Texto:")
        self.inText = tk.Entry(frm3, width=45, state='disable',
                               textvariable = self.envio)
        self.btnSend = ttk.Button(frm3, text="Enviar", width=12, state='disable',
                                  command = self.sendMsg)
        self.lblText.grid(row=0, column=0, padx=5, pady=5)
        self.inText.grid(row=0, column=1, padx=5, pady=5)
        self.btnSend.grid(row=0, column=2, padx=5, pady=5)
               
        # --------------------------- StatusBar -----------------------
        self.statusBar = tk.Label(self.master, bd=1, relief=tk.SUNKEN,
                                  anchor=tk.W)
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X)
        self.inText.bind("<Enter>", lambda x: self.statusBar.config(text="Escriba aqui el mensaje"))
        self.inText.bind("<Leave>", lambda x: self.statusBar.config(text=""))
        
        #------------------------------------------------------------
        
        self.colores = ['morado', 'verde', 'azul', 'rojo']
        self.colorin = ['purple', 'green', 'blue', 'red']
        self.name = []
        self.thread()
        self.ports = []
    def thread(self):
        thcon = threading.Thread(target=self.coneNormal, daemon=True)
        thcon.start()
        
    def coneNormal(self):
        try:
            while True:
                if len(self.address.get())==0:
                    self.btnConnect.config(state = 'disable')
                elif len(self.username.get())==0:
                    self.btnConnect.config(state = 'disable')
                elif len(self.username.get())>=1 and len(self.address.get())>=1:
                    self.btnConnect.config(state = 'normal')
                    break
        except:
            pass
        
        
        
    def cone(self):
        if self.address.get() == HOST:
            self.entip.config(state = 'disable')
            self.entus.config(state = 'disable')
            self.txtChat.config(state = 'disable')
            self.inText.config(state = 'normal')
            self.btnSend.config(state = 'normal')
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.address.get(), PORT))#intenta conectar al server
            
           
            self.statusBar.config(text = f"Conectado como {self.username.get()}")
            
            th = threading.Thread(target=self.recive, daemon=True)
            th.start()
            
        elif self.address.get() != HOST:
            self.entip.config(state = 'normal')
            self.entus.config(state = 'normal')
            self.txtChat.config(state = 'disable')
            self.statusBar.config(text = "Error al conectar con el servidor")
        
    def borrar(self):
        self.entus.delete(0,'end')
        self.statusBar.config(text='')    
    def Desconectar(self):
       
        self.entip.config(state = 'normal')
        self.entus.config(state = 'normal')
        self.txtChat.config(state = 'normal')
        self.txtChat.delete(1.0,tk.END)
        self.inText.config(state = 'disable')
        self.btnSend.config(state = 'disable')
        self.btnConnect.config(text = "Conectar",
                               command = self.cone)
        self.statusBar.config(text = "Desconectado")
        self.txtChat.config(state = 'normal')
        self.entus.delete(0, 'end')
        self.entus.focus()
        self.thread()
        self.sock.close()
        
    def recive(self):
        try:

           while True:
                self.txtChat.config(state = 'normal')
                self.btnConnect.config(text = "Desconectar",
                                       command = self.Desconectar)
                data_len = self.sock.recv(HEADER_SIZE)
                
                if not data_len:
                    break
                dataR = self.sock.recv(int(data_len))
                i = 1
                self.txtChat.insert(tk.INSERT,
                                f"{dataR.decode('utf-8')}" + '\n', self.colores[i])
                self.txtChat.tag_config(self.colores[i], foreground = self.colorin[i])
                
        except:
            pass
            
    def sendMsg(self):
        env = threading.Thread(target=self.envioMsg, daemon=True)
        env.start()
        
    def envioMsg(self):
        try:
            self.txtChat.config(state = 'normal')
            strData = (self.envio.get()) 
            if len(strData) >= 1:
                data_len = len(strData + self.username.get() + "> ")
                z = 2
                self.txtChat.insert(tk.INSERT,
                                f"{self.username.get()}> {strData}" + '\n', self.colores[z])
                self.txtChat.tag_config(self.colores[z], foreground = self.colorin[z])
        
                data = f"{data_len:<{HEADER_SIZE}}{self.username.get()}> {strData}".encode('utf-8')
                #######
                self.inText.delete(0, 'end')
                self.inText.focus()
                self.statusBar.config(text = "Enviando mensaje")
                sleep(0.25)
                self.statusBar.config(text = "Enviando mensaje .")
                sleep(0.25)
                self.statusBar.config(text = "Enviando mensaje . .")
                sleep(0.25)
                self.statusBar.config(text = "Enviando mensaje . . .")
                sleep(0.25)
                self.statusBar.config(text = "Enviando mensaje")
                sleep(0.25)
                self.statusBar.config(text = "Enviando mensaje .")
                sleep(0.25)
                self.statusBar.config(text = "Enviando mensaje . .")
                sleep(0.25)
                self.statusBar.config(text = "Enviando mensaje . . .")
                sleep(0.25)
                self.statusBar.config(text = f"Conectado como {self.username.get()}")
                self.sock.send(data)
            else:
                self.espera()
        except:
            pass
    def espera(self):
        esp = threading.Thread(target=self.time, args = (1,), daemon=True)
        esp.start()
        
    def time(self, t):
        try:
            self.statusBar.config(text = "Error: Mensaje vacio")
            sleep(t)
            self.statusBar.config(text = f"Conectado como {self.username.get()}")
        except:
            pass
    
root = tk.Tk()
app = Client(root)
root.mainloop()