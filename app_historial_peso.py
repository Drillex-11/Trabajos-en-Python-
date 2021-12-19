# -*- coding: utf-8 -*-
#%%
import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from random import randint, uniform, choice

#%%
def genera_pacientes():
    # Retorna una lista de tuplas [(nombre, apellido, altura), ...]
    N_PAC = 25
    
    dataset = set()
    nombres = ["Enzo", "Rosa", "Ruben", "Marcelo", "Ernesto", "Carlos",
               "Marcial", "Diana", "Carolina", "Eduardo", "Ricardo", "Ana"]
    apellidos = ["Ramirez", "Quispe", "Jimenez", "Perez", "Samame", 
                 "Vicente", "Rojas", "Quiroz", "Quevedo", "Martinez", 
                 "Vengas", "Ramos"]
    
    while len(dataset) < N_PAC:
        dataset.add(choice(nombres) + ' ' + choice(apellidos))
    else:
        dataset = list(dataset)
    
    return [(item, round(uniform(1.50, 1.90), 2)) for item in dataset]


def genera_data(pk_id):
    # Datos aleatorios de un programa de perdida de peso de 25 semanas
    # Fecha de inicio: 2020/07/06
    start_date = datetime(2020, 7, 6)
    delta_time = timedelta(days=7)
    
    # Se generan datos para las proximas 25 semanas
    data = [[start_date, randint(50, 120), pk_id]]
    idx = 0    
    
    while len(data) < 25:
        tendencia = randint(-1, 1)
        new_date = data[idx][0] + delta_time
        
        if tendencia == 0:
            data.append([new_date, data[idx][1], pk_id])
        elif tendencia > 0:
            data.append([new_date, data[idx][1] + 3, pk_id])
        else:
            data.append([new_date, data[idx][1] - 2, pk_id])
            
        idx += 1
        
    # La informacion de fecha de convertirse a str (datetime.strfime(datetime))
    for idx in range(len(data)):
        data[idx][0] = datetime.strftime(data[idx][0], "%Y-%m-%d")
        data[idx] = tuple(data[idx])
    
    return data
        
#%%
conn = sqlite3.connect("database.db")

with conn:
    cur = conn.cursor()
    
    # Eliminamos las tablas previas en caso existan: pacientes, registros
    try:
        cur.execute("DROP TABLE pacientes")
        cur.execute("DROP TABLE registros")
    except:
        pass
    
    # Se crean las tablas pacientes y registros
    cur.execute("""CREATE TABLE IF NOT EXISTS pacientes 
                         (id_pac INTEGER PRIMARY KEY, 
                          nombre TEXT NOT NULL, 
                          altura REAL NOT NULL)""")
                          
    cur.execute("""CREATE TABLE IF NOT EXISTS registros 
                         (id_reg INTEGER PRIMARY KEY, 
                          fecha TEXT NOT NULL, 
                          peso REAL NOT NULL, 
                          id_pac INTEGER NOT NULL, 
                          FOREIGN KEY (id_pac) REFERENCES pacientes(id_pac))""")

    # Se cargan los datos por pacientes
    for paciente in genera_pacientes():
        # Se inserta un paciente y se obtiene el PK de este registro
        cur.execute("INSERT INTO pacientes (nombre, altura) VALUES (?, ?)", 
                        paciente)
        pk = cur.lastrowid
        
        # Por cada paciente, se cargan los datos de sus registros de peso
        cur.executemany("INSERT INTO registros (fecha, peso, id_pac) VALUES (?, ?, ?)", 
                        genera_data(pk))
        
conn.close()
        
#%%
class Database:
    datafile = "database.db"
    def __init__(self):
        self.conn = sqlite3.connect(Database.datafile)
        self.cur = self.conn.cursor()
        
        
    def __del__(self):
        self.conn.close()
        
        
    def lista_pac(self):
        # Retorna una lista con los nombres de los pacientes
        sql = """SELECT nombre FROM pacientes ORDER BY nombre"""
        data_cur = self.cur.execute(sql)
        return [item[0] for item in data_cur] 
    
    
    def data_time(self, nombre):
        # Retiornar una lista de tuplas de la forma [(fecha1, peso1), (fecha2, peso2), ...]
        sql = """SELECT fecha, peso 
                 FROM registros JOIN pacientes 
                 ON registros.id_pac = pacientes.id_pac 
                 WHERE pacientes.nombre = ?"""
        return self.cur.execute(sql, (nombre,)).fetchall()
        
    
#%%
class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Historial Pacientes")
        self.master.resizable(0, 0)
        
        self.db = Database()
        
        frm = tk.Frame(self.master)
        frm1 = tk.Frame(frm)
        frm2 = tk.Frame(frm)
        
        frm.pack(padx=10, pady=10)
        frm1.pack(side=tk.LEFT, padx=10, pady=10)
        frm2.pack(side=tk.LEFT, padx=10, pady=10)
        
        # ------------------------ frm1 --------------------------------
        self.scrY = tk.Scrollbar(frm1, orient='vertical')
        self.lstPac = tk.Listbox(frm1, height=18, yscrollcommand=self.scrY.set)
        self.scrY.config(command=self.lstPac.yview)
        
        self.lstPac.pack(side=tk.LEFT)
        self.scrY.pack(side=tk.LEFT, expand=True, fill=tk.Y)
        self.lstPac.bind("<<ListboxSelect>>", self.graph_records)
        
        for item in self.db.lista_pac():
            self.lstPac.insert(tk.END, item)
            
        # ------------------------- frm2 ------------------------------
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.fig.set_facecolor("#F0F0F0")
        self.graph = FigureCanvasTkAgg(self.fig, master=frm2)
        self.graph.get_tk_widget().pack(expand=True, fill=tk.BOTH)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        
    def graph_records(self, event):
        name = self.lstPac.get(self.lstPac.curselection())
        data = self.db.data_time(name)
        
        pesos = [item[1] for item in data]
        fechas = [item[0] for item in data]
        fechas = [datetime.strptime(fecha, "%Y-%m-%d") for fecha in fechas]
        
        self.ax.cla()     # Limpiar el axis
        self.ax.set_title("Historial del peso del paciente")
        self.ax.plot(fechas, pesos, '-o')
        self.ax.set_ylabel("Pesos [kg]")
        self.ax.grid()
        plt.xticks(rotation=45)
        plt.tight_layout()
        self.graph.draw()   # Refresca la figura
        
        
root = tk.Tk()
app = App(root)
root.mainloop()