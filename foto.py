import cv2
import os
from datetime import datetime
def current_date_format(date):
    months = ("Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre","Octubre","Noviembre","Diciembre")
    day = date.day
    month = months[date.month - 1]
    year = date.year
    hora = date.hour
    minuto = date.minute
    segundo = date.second
    messsage = "{}-{}-{}-{}-{}-{}".format(day, month, year, hora, minuto, segundo)

    return messsage

def tomar_foto():
 #valores globales
 ruta='/home/pi/cultivos/imagenes'
 extension='.jpg'
 #abrimos la camara
 cap = cv2.VideoCapture(0)

 #Definimos caracteristicas de la imagen
 cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280) #ancho
 cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720) #alto

 date=datetime.now()
 formato=current_date_format(date)
 nombre_img='/'+formato+extension
 ruta_final=ruta+nombre_img
 #Tomamos la imagen
 ret, frame = cap.read()
 cv2.imwrite(ruta_final,frame) 

 #liberamos la imagen
 cap.release()
 
 return ruta_final

