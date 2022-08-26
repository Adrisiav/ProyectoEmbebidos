from serial import *
from time import *
import sys
from threading import *
import validar as validar
import foto as ft
from firebase import firebase
actuador=False


def subirValor(tipo,lectura,valor):
 firebase.put(tipo,lectura,valor)


def cargar_datos(dato):
 datos_recibidos = ""
 atmega.write(dato.encode())
 atmega.write('\r'.encode())
 atmega.flushInput()
 print("enviado")
 sleep(2)
 try:
  print("recibiendo datos: ")
  while not (atmega.in_waiting > 0):
   print("datos recibidos")
   sleep(1.5)
   pass
  mens = atmega.readline().strip()
  print(mens.decode())
  datos_recibidos = mens.decode()
 except:
  print("no data recive")
 return datos_recibidos

def pedir_datos():
 global numLeida
 datos_pedir=["a","b","c","d"]#cada letra corresponde a humedad1,humedad2,temperatura y luz respectivamente
 valores=[]
 for sensor in datos_pedir:
  valor=cargar_datos(sensor)
  valores.append(valor)
 print(valores)
 analizar_datos(valores)
 if(actuador):
  Timer(3,pedir_datos).start()
  return
 nombre=ft.tomar_foto()
 prediccion=validar.val(nombre)
 subirValor("/EstadoTomate/"+str(0),'valor',prediccion)
 subirValor("/Temperatura/"+str(numLeida),'valor',int(valores[2]))
 subirValor("/Humedad/"+str(numLeida),'valor',(int(valores[0])+int(valores[1]))/2)
 subirValor("/Luz/"+str(numLeida),'valor',int(valores[3]))
 numLeida+=1
 Timer(30,pedir_datos).start()

def enviar_pedido(pedido):
 atmega.write(pedido.encode())
 atmega.write('\r'.encode())
 atmega.flushInput()

def analizar_datos(datos):
 global actuador
 if(actuador):
  if(int(datos[0])<607 and int(datos[1])<607):
   enviar_pedido("desactivar")
   actuador=False
 else:
  if(int(datos[0])>637 and int(datos[1])>580):
   if(int(datos[3])>600 and int(datos[3])<820):
    if(int(datos[2])>47 and int(datos[2])<65):
     enviar_pedido("activar")
     actuador=True
    else:
     enviar_pedido("desactivar")
   elif(int(datos[3])>870):
    if(int(datos[2])>30 and int(datos[2])<70):
     enviar_pedido("activar")
     actuador=True
    else:
     enviar_pedido("desactivar")
   else:
    enviar_pedido("desactivar")
  else:
   enviar_pedido("desactivar")
atmega = Serial('/dev/ttyUSB0', 9600)
firebase = firebase.FirebaseApplication('https://p11sistemasembebidos-default-rtdb.firebaseio.com/', None)
valores = firebase.get('/Temperatura', None)
numLeida=len(valores)
sleep(2)
try:
   while not (atmega.in_waiting > 0):
    print("datos recibidos")
    sleep(1.5)
    pass
   print()
   mens = atmega.readline().strip()
   print(mens.decode())
except:
   print("no data recive")
Timer(30,pedir_datos).start()
try:
 while 1:
  sleep(2)
except(KeyboardInterrupt,SystemExit):
 print("Bye")
 Timer(30,pedir_datos)._stop() #_stop() #delete() #cancel()
 Timer(30,pedir_datos).cancel() #_stop() #delete() #cancel()
 Timer(30,pedir_datos)._delete() #_stop() #delete() #cancel()
 Timer(3,pedir_datos)._stop() #_stop() #delete() #cancel()
 Timer(3,pedir_datos).cancel() #_stop() #delete() #cancel()
 Timer(3,pedir_datos)._delete() #_stop() #delete() #cancel()
 sys.exit()
atmega.close()
