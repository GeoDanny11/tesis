#Gráfica de la grilla
from mpl_toolkits.mplot3d import Axes3D 
import matplotlib.colors as cm 
import matplotlib.pyplot as plt
import numpy as np 
import matplotlib.mlab as m
from obspy.taup import TauPyModel
import math

#función para cálcular latitud y longitud de la estación
def statlatlon(file,stat):
	lat=file[stat-1,0]
	lon=file[stat-1,1]
	return (lat,lon)

#función para cálcular latitud y longitud del terremoto	
def sourcelatlon (file,source):
	source=int(source)
	lat=file[source-1,1]
	lon=file[source-1,2]
	r=file[source-1,0]
	return(r,lat,lon)

#función para determinar tiempo arrivo de fases
def phases(depth,sourcelat,sourcelon,statlat,statlon):
	dist=dist_degree(sourcelat,sourcelon,statlat,statlon)
	print(dist)
	print(depth)
	arrivals=model.get_travel_times(source_depth_in_km=depth, distance_in_degree=dist, phase_list=["P","pP"])
	arr=arrivals[0]	
	Ptime=arr.time
	arr=arrivals[1]
	Pptime=arr.time 
	return(Ptime,Pptime)

#fucnión para determinar la distancia en grados
def dist_degree(lat1,lon1,lat2,lon2):
	r=6371 #radio de la tierra en km
	c=3.141592654/180
	d = 2*r*math.asin(math.sqrt(math.sin(c*(lat2-lat1)/2)**2 + math.cos(c*lat1)*math.cos(c*lat2)*math.sin(c*(lon2-lon1)/2)**2))
	teta=d/r
	teta=teta*(1/c)
	return(teta)


model=TauPyModel(model="iasp91") #investigar sobre el modelo
#scale=[0,1900,-2,2]
file=input("Ingrese nombre del archivo: ")
data=np.loadtxt(file)
file2="STATIONS" #toca crear un archivo sin las ods primeras columnas de string
#asegurarse de la división decimal del archivo en excel
stations=np.loadtxt(file2)
file3="SOURCE.txt"
sources=np.loadtxt(file3)

f1=int(input("Primera estación a graficar: "))
f2=int(input("Segunda estación a graficar: "))
f3=int(input("Tercera estación a graficar: "))
#Obtiene las latitudes y longitudes de las estaciones
lat1,lon1=statlatlon(stations,f1)
lat2,lon2=statlatlon(stations,f2)
lat3,lon3=statlatlon(stations,f3)

fuente=int(input("Ingrese la fuente a graficar: "))
#Calcula los tiempos de arrivo de las fases, a partir de la fuen elegida, ya se para un evento o para una solo fuente
r1,slat1,slon1=sourcelatlon(sources,fuente)
Ptime1,Pptime1=phases(r1,slat1,slon1,lat1,lon1)
Ptime2,Pptime2=phases(r1,slat1,slon1,lat2,lon2)
Ptime3,Pptime3=phases(r1,slat1,slon1,lat3,lon3)

#Plotea los simogramas
plt.figure(1)
plt.subplot(311)
time=data[:,0]
freq=data[:,f1]
#plt.axis(scale)
plt.plot(time,freq)
plt.axvline(x=Ptime1,label="Arribo onda P",c="red")
plt.axvline(x=Pptime1,label="Arribo onda pP",c="brown")
Ptime=str("%4.1f" % (Ptime1))
Pptime=str("%4.1f" % (Pptime1))
plt.annotate(Ptime,xy=(Ptime1,0))
plt.annotate(Pptime,xy=(Pptime1+150,0))

plt.subplot(312)
freq2=data[:,f2]
#plt.axis(scale)
plt.plot(time,freq2)
plt.axvline(x=Ptime2,label="Arribo onda P",c="red")
plt.axvline(x=Pptime2,label="Arribo onda pP",c="brown")
Ptime=str("%4.1f" % (Ptime2))
Pptime=str("%4.1f" % (Pptime2))
plt.annotate(Ptime,xy=(Ptime2,0))
plt.annotate(Pptime,xy=(Pptime2+150,0))

plt.subplot(313)
freq3=data[:,f3]
#plt.axis(scale)
plt.plot(time,freq3)
plt.axvline(x=Ptime3,label="Arribo onda P",c="red")
plt.axvline(x=Pptime3,label="Arribo onda pP",c="brown")
Ptime=str("%4.1f" % (Ptime3))
Pptime=str("%4.1f" % (Pptime3))
plt.annotate(Ptime,xy=(Ptime3,0))
plt.annotate(Pptime,xy=(Pptime3+150,0))
plt.legend()
plt.show()

