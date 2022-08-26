// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.9.3/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.9.3/firebase-analytics.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyAFMLdQVpoXzRWS6s3yzT2ePV9OZPqSLLo",
    authDomain: "p11sistemasembebidos.firebaseapp.com",
    databaseURL: "https://p11sistemasembebidos-default-rtdb.firebaseio.com",
    projectId: "p11sistemasembebidos",
    storageBucket: "p11sistemasembebidos.appspot.com",
    messagingSenderId: "151283961793",
    appId: "1:151283961793:web:d9b8a1858b1f295065e940",
    measurementId: "G-SF6NP969K3"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
import { getDatabase, ref, set } from "https://www.gstatic.com/firebasejs/9.9.3/firebase-database.js"

var Temperatura = document.getElementById('Temperatura');
var Humedad = document.getElementById('Humedad');
var Luz = document.getElementById('Luz');
var Estado = document.getElementById('Estado');
import { onValue } from "https://www.gstatic.com/firebasejs/9.9.3/firebase-database.js"
const db = getDatabase();
grafico('Temperatura', 'curve_chart1');
grafico('Humedad', 'curve_chart2');
grafico('Luz', 'curve_chart3');

const estadoTomate = ref(db, 'EstadoTomate');
onValue(estadoTomate, (snapshot) => {
    const data = snapshot.val();
    console.log(data[0].valor);
    const est = data[0].valor;
    Estado.innerHTML = "<h2>Estado del tomate</h2> <p>" + est + "</p>";
})

console.log('agregado');

function grafico(Tipo, id) {
    const starCountRef = ref(db, Tipo);
    const valoresFirebase = [['Valor', 'Lectura']];
    onValue(starCountRef, (snapshot) => {
        /* tabla.innerHTML=''; */
        const data = snapshot.val();
        var i = 0;
        data.forEach(element => {
            i++;
            var datos = ['' + i, element.valor];
            valoresFirebase.push(datos);
            /* console.log(valoresFirebase); */
        });
        var ultimoValor = document.getElementById(Tipo);
        console.log(data[data.length - 1])
        var valorPresntar = 0
        var unidades = ''
        if (Tipo == 'Temperatura') {
            valorPresntar = (((data[data.length - 1].valor) * 5 / 1023) * 100).toFixed(2)
            unidades = "°C"
        } else if (Tipo == 'Humedad') {
            valorPresntar = ((1050 - (data[data.length - 1].valor)) * 100 / 625).toFixed(2)
            unidades = "%"
        } else if (Tipo == "Luz") {
            if((data[data.length - 1].valor)>870){
                valorPresntar='Noche'
            }else{
                valorPresntar="Dia"
            }
        }
        ultimoValor.innerHTML = "<h2> Estado de " + Tipo + "</h2> <p>" + valorPresntar +unidades+ "</p>";
        google.charts.load('current', { 'packages': ['corechart'] });
        google.charts.setOnLoadCallback(drawChart);
        function drawChart() {
            var data = google.visualization.arrayToDataTable(
                valoresFirebase
            );

            var options = {
                title: Tipo,
                curveType: 'function',
                legend: { position: 'bottom' }
            };

            var chart = new google.visualization.LineChart(document.getElementById(id));

            chart.draw(data, options);
        }
        /* console.log(data) */
    });
}