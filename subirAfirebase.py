def subirValor(tipo,lectura,valor):
 from firebase import firebase
 firebase = firebase.FirebaseApplication('https://p11sistemasembebidos-default-rtdb.firebaseio.com/', None)
 firebase.put(tipo,lectura,valor)
