const ctx = document.getElementById('grafico').getContext('2d');

let grafico = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Temperatura (°C)',
                borderColor: 'red',
                data: [],
                fill: false
            },
            {
                label: 'Umidade (%)',
                borderColor: 'blue',
                data: [],
                fill: false
            },
            {
                label: 'Gás (ppm)',
                borderColor: 'green',
                data: [],
                fill: false
            }
        ]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

function atualizarGrafico() {
    fetch('/api/dados')
        .then(resp => resp.json())
        .then(data => {
            grafico.data.labels = data.labels;
            grafico.data.datasets[0].data = data.temperatura;
            grafico.data.datasets[1].data = data.umidade;
            grafico.data.datasets[2].data = data.gas;
            grafico.update();
        });
}

atualizarGrafico();
setInterval(atualizarGrafico, 5000);