# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 02:36:25 2021

@author: Sebastian
"""

from random import*
Fitness = 120
k1 = []
k2 = []
f = []
##Creando listas para pares
Lpares = []
for i in range(0,7,2):
    Lpares.append(i)
p1 = []
p2 = []
p3 = []
p4 = []
##Creando lista para impares 
Limpares = []
for i in range(1,8,2):
    Limpares.append(i)
im1 = []
im2 = []
im3 = []
im4 = []
def generando_genes(y):
    Gen= range(1,25)
    x = []
    for i in range(0,y): 
        s = sample(Gen,k=15)
        x.append(s)
        
    print('                       TABLA DE GENES\n                      ')
    for j in range(y):    
        print(f'{x[j]} |  fitness :  {generando_fitness_mejor(x)[0][j]} | error: {generando_fitness_mejor(x)[4][j]}') 
    
    print(f' El mejor fitness es el individuo: {generando_fitness_mejor(x)[1] + 1}')
    print(f' El peor fitness es el individuo : {generando_fitness_mejor(x)[2] +1}\n')
   
    min_n=generando_fitness_mejor(x)[1]
    max_n=generando_fitness_mejor(x)[2]
    acum = 0
    while(True):
        acum = acum+1
        x[max_n]=x[min_n]
        
        print('CAMBIO DEL PEOR FITNESS POR EL MEJOR DE LOS FITNESS\n')
        for j in range(y):
            print(f'{x[j]} ')
    
        print('\nEMPAREJAMIENTO\n')
        grupos=[]
        grupos = sample(x,len(x))
        for j in range(y):
            print(f'{grupos[j]}')
            
        print("\nREPRODUCCIÓN\n")
        crossover=[]
        for i in range(int(y/2)):
            cross = randint(1, 14)
            for j in range(2):
                crossover.append(cross)
        for j in range(y):
            print(f'{x[j]} | Punto crossover :{crossover[j]}')
                
        for j in Lpares:
            for k in range(crossover[j],15):
                k1.append(grupos[j][k])
        
        for j in Limpares:
            for k in range(crossover[j],15):
                k2.append(grupos[j][k])
                
        for j in range(0,15-crossover[1]):
            p1.append(k2[j])
        for j in range(len(p1),len(p1)+15-crossover[3]):
            p2.append(k2[j])
        for j in range(len(p1)+len(p2),len(p1)+len(p2)+15-crossover[5]):
            p3.append(k2[j])
        for j in range(len(p1)+len(p2)+len(p3),len(p1)+len(p2)+len(p3)+15-crossover[7]):
            p4.append(k2[j])
            
        for j in range(0,15-crossover[1]):
            im1.append(k1[j])
        for j in range(len(im1),len(im1)+15-crossover[3]):
            im2.append(k1[j])
        for j in range(len(im1)+len(im2),len(im1)+len(im2)+15-crossover[5]):
            im3.append(k1[j])
        for j in range(len(im1)+len(im2)+len(im3),len(im1)+len(im2)+len(im3)+15-crossover[7]):
            im4.append(k1[j])
            
         #PAREJA 1    
        for i in range(crossover[1],15): 
                grupos[0][i]= p1[i-crossover[1]]
        for i in range(crossover[1],15): 
                grupos[1][i]= im1[i-crossover[1]]  
        #PAREJA 2
        for i in range(crossover[3],15): 
                grupos[2][i]= p2[i-crossover[3]]
        for i in range(crossover[3],15): 
                grupos[3][i]= im2[i-crossover[3]]  
        #PAREJA 3
        for i in range(crossover[5],15): 
                grupos[4][i]= p3[i-crossover[5]]
        for i in range(crossover[5],15): 
                grupos[5][i]= im3[i-crossover[5]]  
        #PAREJA 4
        for i in range(crossover[7],15): 
                grupos[6][i]= p4[i-crossover[7]]
        for i in range(crossover[7],15): 
                grupos[7][i]= im4[i-crossover[7]] 
        
        print('\nOBTENCIÓN DE LA PRIMERA GENERACIÓN\n')
        for j in range(y):
            print(f'{grupos[j]} | Punto crossover : {crossover[j]}')
        
        #Creando el Factor de mutación 
        op = []
        mut =[]
        listF = []
        for i in range(0,8):
            ñ = randint(0,25)
            mut.append(ñ)
        for i in range(0,15):
            op.append(randint(0, 14))
        
        print('\n FACTOR DE MUTACIÓN\n')
       
        for i in range(0,8):
            grupos[i][op[i]]=mut[i]
            listF.append(op[i])
       
        for j in range(y):
            print(f'{grupos[j]} | se cambio el gen: {listF[j]+1}')
            
        #Generando la nueva genaración
        e1 = []
        z1 = []
        u1 = 0
        
        print('\n GENERACIÓN OBTENIDA MEDIANTE ITERACIONES\n')
        
        for j in range(0,y):
            if u1>0:
                z1.append(u1)
                u1=0
            for k in range(0,15):
                u1+= grupos[j][k]
        z1.append(u1)
        for i in grupos:
            print(i)
        for i in range(0,8):
            
            e1.append(abs(Fitness-z1[i]))
        h = e1.index(min(e1)) 
        o = e1.index(max(e1)) 
        
        if min(e1) == 0:
            break
        else:
            continue
    print(f'\nEl mejor error se encuentra en el individuo : {h+1}  | El numero de iteraciones es: {acum}')
    
    return generando_fitness_mejor(x)

def generando_fitness_mejor(c): 
        e =[]
        z=[]
        u= 0
        for j in range(0,8):
            if u>0:
                z.append(u)
                u=0
            for k in range(0,15):
                u+= c[j][k]  
        #Hallando los Fitness
        z.append(u)
        for i in range(0,8):
            #Lista con los Errores
            e.append(abs(Fitness-z[i]))
        #El menor error con respecto al fitness
        g = min(e)
        #Posición del Mejor Fitness
        h = e.index(min(e)) 
        #Posición del Peor Fitness
        o = e.index(max(e)) 
        return [z,h,o,g,e]

#Llamando a la función 
generando_genes(8)
        