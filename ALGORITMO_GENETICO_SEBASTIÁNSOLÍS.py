# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 02:45:03 2021

@author: Sebastian
"""

from random import*
Fitness = 120



def generando_genes(y):
    Gen= range(1,25)
    x = []
    for i in range(0,y): 
        s = sample(Gen,k=15)
        x.append(s)
        
    print('                       TABLA DE GENES\n                      ')
    for j in range(y):    
        print(f'{x[j]} |  fitness :  {generando_fitness_mejor(x)[0][j]}') 
    
    print(f' El mejor fitness es el individuo: {generando_fitness_mejor(x)[1] + 1}')
    print(f' El peor fitness es el individuo : {generando_fitness_mejor(x)[2] +1}')
    
    
    return x,generando_fitness_mejor(x)

def generando_fitness_mejor(c): 
        e =[]
        z=[]
        u= 0
        for j in range(0,y):
            if u>0:
                z.append(u)
                u=0
            for k in range(0,15):
                u+= c[j][k]    
        z.append(u)
        for i in range(0,y):
            e.append(abs(120-z[i]))
            for j in e:
                h = e.index(min(e)) 
                o = e.index(max(e)) 
    
        return [z,h,o]


        
    
        

#def hallando_fitness(o):
        
z=int(input("Ingrese la cantidad de individuos: "))


generando_genes(z)