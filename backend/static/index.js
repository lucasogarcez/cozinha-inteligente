const ctx = document.getElementById('grafico').getContext('2d');

const grafico = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Temperatura (°C)',
                data: [],
                borderColor: 'red',
                fill: false
            },
            {
                label: 'Umidade (%)',
                data: [],
                borderColor: 'blue',
                fill: false
            }
        ]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: false
            }
        }
    }
});

function atualizarGrafico() {
    fetch('/api/dados')
        .then(res => res.json())
        .then(dados => {
            grafico.data.labels.push(...dados.labels);
            grafico.data.datasets[0].data.push(...dados.temperatura);
            grafico.data.datasets[1].data.push(...dados.umidade);
            grafico.update();
        });
}

// Atualiza a cada 5 segundos
setInterval(atualizarGrafico, 5000);
