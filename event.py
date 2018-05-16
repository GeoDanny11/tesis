#whichsource.py
#code that analise which source are to be usen, given a certain direction
import subprocess
import re
import os
import numpy as np 

#funcion para calcular el timestep, cuantos datos de muestreo debe correrse el siguiente archivo para hacer la suma
def timestep (X,vel,deltar):
	time=X[:,0]
	step=np.zeros(np.size(time))
	suma=0
	c=0
	for i in range(1,np.size(time)):
		step[c]=time[i]-time[i-1]
		suma=suma+step[c]
		c=c+1
	deltat=suma/c #intervalo de tiempo en el archivo
	timestep=deltar/vel
	return (int(timestep/deltat),deltat)

#función para contar el número de fuentes a sumar 
def howmanysources (ws,lenght,deltar,rmax):
	sources=0
	for i in range(np.size(ws)):
		if(ws[i]!=0):
			sources=sources+1		
	if (length >= rmax):
		return (sources,sources)
	else:
		return (sources,length//deltar)

#funcion para sumar los archivos
def suma(X,Y,consecutivo,xy):
	newxy=xy*consecutivo	
	nf=np.size(X[:,0])+newxy
	nc=np.size(X[0,:])
	suma=np.zeros((nf,nc))	
	#print (np.size(X[:,0]))
	#print(nf)
	print ("-------------------",consecutivo,newxy,"-------------------")
	for k in range (1,129): #k controla las columnas
		for i in range(nf): #i controla las filas
			if(i < newxy):
				suma[i,k]=X[i,k]								
			elif (i<np.size(X[:,0])and i<np.size(Y[:,0])):
				suma[i,k]=X[i,k]+Y[i-newxy-1,k]
			elif (i>np.size(Y[:,0])):
				suma[i,k]=0
			elif(i>np.size(X[:,0])):
				suma[i,k]=Y[i-newxy-1,k]
	#print (suma)
	return(suma)

#ángulo phi deseado para la falla
dirphi=float(input("Ingrese la dirección phi: "))
#ángulo teta deseado para la falla
dirteta=float(input("Ingrese la dirección teta: "))


#velocidad de ruptura en km/h
vel=float(input("Ingrese la velocidad de ruptura en km/h: "))

#intervalo del radio en la grilla
deltar=10

#valor máximo del radio de la grilla
rmax= 30

#longitud desada para la ruptura
length=30

f1="S212.txt"
f2="S187.txt"
f3="S247.txt"
f4="S307.txt"#fuente origen
#f5="S222.txt"
#f6="S282.txt"
#f7="S342.txt"
A=np.loadtxt(f1)
B=np.loadtxt(f2)
C=np.loadtxt(f3)
D=np.loadtxt(f4)
#E=np.loadtxt(f5)
#F=np.loadtxt(f6)
#G=np.loadtxt(f7)

num,deltat=timestep(A,vel,deltar) #el primer archivo será el de referencia

sources4use=int(input("Cuantas fuentes desea usar: "))
#numero de datos de más en el archivo final del evento
xy=num*sources4use

#suma cuando se usa la longitud maxima posible
if (sources4use==allsources):
	S=suma(A,B,1,xy)
	S=suma(S,C,2,xy)
	S=suma(S,D,3,xy)
	#S=suma(S,E,4,xy)
	#S=suma(S,F,5,xy)
	#S=suma(S,G,6,xy)

#print(np.shape(S))	
#print(S)
#np.savetxt("EVENT_less_time.TXT",suma, delimiter="   ")
name=input("Ingrese el nombre del evento: ")

#rellena la columna del tiempo 
num,op=np.shape(S)
time=np.zeros(num)
for i in range (num):
	if (i<np.size(A[:,0])):
		time[i]=A[i,0]
	else:
		time[i]=time[i-1]+deltat

for i in range (num):
	S[i,0]=time[i]

np.savetxt(name,S, delimiter="   ")
