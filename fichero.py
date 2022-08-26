import foto
import validar
import subirAfirebase as f
nombre=foto.tomar_foto()
prediccion=validar.val(nombre)
print(prediccion)
f.subirValor("/EstadoTomate/"+str(0),'valor',prediccion)
for i in range(11):
 f.subirValor("/Temperatura/"+str(i),'valor',i*13)
 f.subirValor("/Humedad/"+str(i),'valor',i*35)
 f.subirValor("/Luz/"+str(i),'valor',i*67)
print("valoresSubidosConExtito")
