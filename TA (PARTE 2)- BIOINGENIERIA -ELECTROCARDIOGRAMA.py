
# Alumno: Sebastián Jorge Solís Dianderas
# TIU = 201714474

import matplotlib.pyplot as plt
import numpy as np

#Parámetros
fs=500
vrefh=3.3
vrefl=0
ganancia=200
n_bits=10
ciclo = 0
T50ms = int(500*0.05)
posicion = []
picos = []
tiempo = []
FrecIns = []
T2 = []
restas = []
s =[]
vp = []
pos_s=[]
pos_q = []
punto_l =[]
punto_h = []
q =[]
t =[]

data = np.loadtxt("Grupo02_a.txt")
tam = data.size
maxim = max(data)
minim = min(data)
umbral = (maxim-minim)*0.8 + minim

for i in range (tam-2):
    if(data[i]>data[i+1] and data[i]>data[i+2] and data[i]>=data[i-1] and data[i]>data[i-2] and data[i]>umbral):
        posicion.append(i)
        picos.append(int(data[i]))
        ciclo+= 1

Ttotal = (posicion[ciclo-1]-posicion[0])/fs
PromFrec = ((ciclo-1)*60)/Ttotal
for i in range(len(posicion)-1):
    T1 = (posicion[i+1]-posicion[i])/fs 
    T2.append(abs((posicion[i+1]-posicion[i])/fs))
    FrecIns.append(round(60/T1))

for i in range (len(T2)-1):
    tiempo.append(abs(T2[i+1]-T2[i]))

print("a) Frecuencias cardiaca de la señal")
print(f"La frecuencia cardiaca promedio es: {round(PromFrec)} bpm/n\n")

print("b) Frecuencias cardiacas instantaneas")
for i in range (len(FrecIns)):
    print(f"La {i+1} frecuencia cardiaca instantanea: {FrecIns[i]} bpm")
print("\n")

print("c) Ritmo Cardiaco ")
for i in range (len(tiempo)):
      if (tiempo[i]<0.04 and (60<=round(PromFrec) and round(PromFrec)<=100)):
          print(f"La diferencias entre el ciclo {i+1} y {i+2} es menor a 40 milisegundos,no presenta Arritmia. Ademas su frecuencia cardiaca  esta dentro del rango de 60 y 100 bpm tiene un ritmo cardiaco normal")
      elif (tiempo[i]>0.04 and (60<=round(PromFrec) and round(PromFrec)<=100)):
           print(f"La diferencias entre el ciclo {i+1} y {i+2} es mayor a 40 milisegundos,presenta Arritmia. Ademas su frecuencia cardiaca instantanea esta dentro del rango de 60 y 100 bpm tiene un ritmo cardiaco normal")
      elif (tiempo[i]>0.04 and (60>round(PromFrec) and round(PromFrec)<=100)):
           print(f"La diferencias entre el ciclo {i+1} y {i+2} es mayor a 40 milisegundos,presenta Arritmia. Ademas su frecuencia cardiaca instantanea no esta dentro del rango de 60 y 100 bpm tiene un ritmo cardiaco que presenta Bradicardia")
      elif (tiempo[i]<0.04 and (60>round(PromFrec) and round(PromFrec)<=100)):
           print(f"La diferencias entre el ciclo {i+1} y {i+2} es menor a 40 milisegundos,no presenta Arritmia. Ademas su frecuencia cardiaca no esta dentro del rango de 60 y 100 bpm tiene un ritmo cardiaco que presenta Bradicardia")
      elif (tiempo[i]<0.04 and (60<=round(PromFrec) and round(PromFrec)>100)):    
           print(f"La diferencias entre el ciclo {i+1} y {i+2} es menor a 40 milisegundos,no presenta Arritmia. Ademas su frecuencia cardiaca no esta dentro del rango de 60 y 100 bpm tiene un ritmo cardiaco que presenta Taquicardia")
      elif (tiempo[i]>0.04 and (60<=round(PromFrec) and round(PromFrec)>100)): 
           print(f"La diferencias entre el ciclo {i+1} y {i+2} es mayor a 40 milisegundos,presenta Arritmia. Ademas su frecuencia cardiaca no esta dentro del rango de 60 y 100 bpm tiene un ritmo cardiaco que presenta Taquicardia")

for i in range(len(posicion)):
    picos1 = posicion[i]-T50ms
    q_r =[]
    pos_q1 = []
    for j in range(T50ms):
        q_r.append(data[picos1+j])
    for h in range(0,len(q_r)):
        if data[picos1+h]<=data[picos1+h-1] and data[picos1+h]<=data[picos1+h-3] and data[picos1+h]<=data[picos1+h+1] and data[picos1+h]<=data[picos1+h+3] and data[picos1+h]<umbral:
            pos_q1.append(picos1+h)
    pos_q.append(pos_q1[-1])
for i in range(len(pos_q)):
    q.append(int(data[pos_q[i]]))

for i in range(0,len(posicion)):
    pl = posicion[i]-T50ms
    ph = posicion[i]+T50ms
    punto_l.append(int(pl))
    punto_h.append(int(ph))
    s.append(min(data[pl:ph]))
minimoqs=min(q,s)
for i in range(0,len(posicion)):
    aux=[]
    aux2=[]
    for j in range(punto_l[i], punto_h[i]):
        aux.append(int(data[j]))
        aux2.append(j)
    pos_s.append(aux2[aux.index(s[i])])
    aux.clear()
for i in range(len(picos)):
    vp.append((((picos[i]-minimoqs[i])*(vrefh-vrefl))/(pow(2,10)))*(1/ganancia)*1000)
print("\n")
print('d) Amplitudes de los complejos QRS')
for i in range(len(vp)):
    print(f"La Amplitud QRS {i+1} es {vp[i]:.2f} mV")
for i in range(len(posicion)):
    t.append(((pos_s[i]-pos_q[i])/fs)*1000)
print("\n")
print('e) Duración de los complejos QRS')
for i in range(len(t)):
    print(f"La Duracion QRS {i+1} es {t[i]} ms")

plt.plot(data)
plt.plot(posicion,picos,'o',color = 'r')
plt.title('Senal de Electrocargiograma')
plt.ylabel('Amplitud [mV]')
plt.xlabel('Duración [mseg]')
plt.axhline(umbral,color = 'y',lineStyle= '--')
plt.grid()
plt.show()




