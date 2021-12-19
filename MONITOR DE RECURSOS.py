import tkinter as tk 
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
import psutil 
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

class App:
    def __init__(self,master):
        #Definicion del root master 
            self.master=master
            self.master.resizable(False,False)
            self.master.geometry("500x240")
            self.master.configure(bg='black')
            self.master.title("Monitor de Recursos")
        #Definicion de variables    
            self.var_CPU_usage=tk.DoubleVar()             #Variable del porcentaje de uso del CPU
            self.var_CPU_core=tk.IntVar()                 #Variable del # de núcleos del procesador
            self.var_CPU_usage_current=[0]*10             #Variable de almacenamiento del uso actual del CPU
            self.var_Memory_info=tk.DoubleVar()          #Variable de la cantidad del uso de la memoria 
            self.var_Memory_info_percent=tk.DoubleVar()  #Variable del porcentaje del uso de la memoria 
            self.var_HDD_percent=tk.DoubleVar()  #Variable del porcentaje de uso de la Bateria
            self.var_HDD_info=tk.DoubleVar()  #Variable del porcentaje de uso de la Bateria
            self.var_NET_in=tk.IntVar()       #Variable de datos de entrada
            self.var_NET_out=tk.IntVar()     #Variable de datos de salida 
            self.time= tk.StringVar()        #Variable del tiempo
            #Frames
            #------------Master Frame-----------
            frm=tk.Frame(self.master,bg='black')          
            frm.pack(padx=3,pady=2)
            #------------Frame 1-----------
            frm1=tk.Frame(frm,bg='black')
            frm1.pack(side=tk.LEFT,padx=4,pady=2)
            #------------Frame 2-----------
            frm2=tk.Frame(frm,bg='black')
            frm2.pack(side=tk.LEFT,padx=5,pady=2)
            
            #Instanciacion del grafico de Matplotlib
            self.fig,self.ax=plt.subplots(figsize=(8,3),facecolor="#F0F0F0")
            self.graph=FigureCanvasTkAgg(self.fig,master=frm2)
            self.graph.get_tk_widget().pack(expand=True,fill=tk.BOTH,anchor=tk.CENTER)
            
            #Definicion del estilo de grid y limites del grafico
            self.line,=self.ax.plot([0,1,2,3,4,5,6,7,8,9],self.var_CPU_usage_current,color='#134E76')
            self.ax.grid(linestyle="--")
            self.ax.set_ylim(0,100,20)
            self.ax.set_xlim(0,10)
            
            #Propiedades del Grafico
            self.ax.set_xticklabels([""])
            self.ax.tick_params(left=False)
            self.ax.yaxis.label.set_color("white")
            self.ax.set_facecolor('#000000')
            self.ax.tick_params(axis='y',colors='white')
            self.fig.set_facecolor('black')
            self.ax.set_title('CPU Usage [%]',fontdict={'color':'white'})
            
            #Labels
            #------------Label del CPU-------------------------
            self.CPU_lbl=tk.Label(frm1,text='',fg='#FFFFFF',bg='#000000')
            self.CPU_lbl.grid(row=0,column=0,padx=5,pady=5,sticky=tk.W)
            #------------Label de la Memoria-------------------
            self.MEM_lbl=tk.Label(frm1,text='',fg='#FFFFFF',bg='#000000')
            self.MEM_lbl.grid(row=2,column=0,padx=5,pady=5,sticky=tk.W)
            #------------Label de la Bateria-------------------
            self.HDD_lbl=tk.Label(frm1,text='',fg='#FFFFFF',bg='#000000')
            self.HDD_lbl.grid(row=4,column=0,padx=5,pady=5,sticky=tk.W)
            #------------Progressbar del CPU-------------------
            self.CPU_pbar=ttk.Progressbar(frm1,length=200,maximum=100)
            self.CPU_pbar.grid(row=1,column=0,padx=5,pady=5,sticky=tk.W)
            #------------Progressbar de la Memoria-------------
            self.MEM_pbar=ttk.Progressbar(frm1,length=200,maximum=100)
            self.MEM_pbar.grid(row=3,column=0,padx=5,pady=5,sticky=tk.W)
            #------------Progressbar de la Bateria-------------
            self.HDD_pbar=ttk.Progressbar(frm1,length=200,maximum=100)
            self.HDD_pbar.grid(row=5,column=0,padx=5,pady=1,sticky=tk.W)
            
            self.statusbar=tk.Label(self.master,text='', relief=tk.SUNKEN,fg='#FFFFFF',bg='#000000')
            self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
            

            #Extraccion de la informacion de la PC
            self.read_psutil_data()
            

            
    def read_psutil_data(self): #Funcion de extraccion de informacion
            #Extraccion de la informacion del CPU
            self.var_CPU_usage.set(psutil.cpu_percent())
            self.var_CPU_core.set(psutil.cpu_count(logical=False))
            #Extraccion de la informacion de la Memoria
            self.var_Memory_info.set(psutil.virtual_memory().total/1024/1024/1024)
            self.var_Memory_info_percent.set(psutil.virtual_memory().percent)
            #Extraccion de la informacion del disco duro
            self.var_HDD_info.set(psutil.disk_usage("/").total/1024/1024/1024)
            self.var_HDD_percent.set(psutil.disk_usage("/").percent)
            self.var_NET_in.set(psutil.net_io_counters().bytes_recv)
            self.var_NET_out.set(psutil.net_io_counters().bytes_sent) 
            self.time.set(datetime.datetime.now().strftime("%F %T") )
            #Inscripcion del label del CPU                
            self.CPU_lbl.config(text=f"CPU Usage ({self.var_CPU_core.get()}core): {self.var_CPU_usage.get()} %")
            self.CPU_pbar.config(variable=self.var_CPU_usage)
            #Inscripcion del label de la Memoria
            self.MEM_lbl.config(text=f"RAM Usage:(Total:{self.var_Memory_info.get():.2f}Gb):{self.var_Memory_info_percent.get():.1f} %")
            self.MEM_pbar.config(variable=self.var_Memory_info_percent)
            #Inscripcion del label del HDD
            self.HDD_lbl.config(text=f"HDD Usage:(Total:{self.var_HDD_info.get():.2f}Gb):{self.var_HDD_percent.get():.1f} %")
            self.HDD_pbar.config(variable=self.var_HDD_percent)
            
            #StatusBar
            self.statusbar.config(text=f" Net Info [in: {self.var_NET_in.get():,} | out: {self.var_NET_out.get():,}]                                                {self.time.get()}")
           
            #Dibujo del uso porcentual del procesador en el grafico
            if 10 == len(self.var_CPU_usage_current):
                self.var_CPU_usage_current.insert(0,self.var_CPU_usage.get())
                self.var_CPU_usage_current.pop()
                self.line.set_ydata(self.var_CPU_usage_current)
                self.graph.draw()
                
            else:
                self.var_CPU_usage_current.insert(0,self.var_CPU_usage.get())
                self.line.set_ydata(self.var_CPU_usage_current)
                self.graph.draw()
                
            
            self.master.after(1000, self.read_psutil_data)
            
root=tk.Tk()
app=App(root)
root.mainloop()