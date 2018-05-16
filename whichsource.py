#whichsource.py
#code that analise which source are to be usen, given a certain direction
import subprocess
import re
import os
import numpy as np 
#ángulo phi deseado para la falla
dirphi=float(input("Ingrese el ángulo en la direccion phi: "))
#ángulo teta deseado para la falla
dirteta=float(input("Ingrese el ángulo en la direccion teta: "))

file= open("GRILLA.txt","r")
lines=list(file)
n=np.size(lines)
file2="GRILLA.TXT"
data=np.loadtxt(file2)
#vector en donde se guardaran las estaciones que se deben utilizar
ws=np.zeros(n)
c=0
for f in range(n):
	if(data[f,1]==dirteta):
		if(data[f,2]==dirphi):
			ws[c]=f+1
			c=c+1
for c in range (n):
	if(data[c,1]==0):
		if(data[c,2]==0):
			if(data[c,0]==0):
				print("La fuente origen es: ",c+1)
for i in range(n):
	if (ws[i]!=0):
		print(ws[i])