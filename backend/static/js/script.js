const tempCtx = document.getElementById('graficoTemp').getContext('2d');
const umidCtx = document.getElementById('graficoUmidade').getContext('2d');
const gasCtx = document.getElementById('graficoGas').getContext('2d');

const chartOptions = {
    responsive: true
};

const graficoTemp = new Chart(tempCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Temperatura (ºC)',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderWidth: 1
        }]
    },
    options: chartOptions
})

const graficoUmidade = new Chart(umidCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Umidade (%)',
            data: [],
            borderColor: 'rgba(54, 162, 235, 1)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderWidth: 1
        }]
    },
    options: chartOptions
})

const graficoGas = new Chart(gasCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Gás (ppm)',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderWidth: 1
        }]
    },
    options: chartOptions
})

function atualizarGrafico() {
    fetch('/api/dados')
        .then(resp => resp.json())
        .then(data => {
            graficoTemp.data.labels = data.labels;
            graficoTemp.data.datasets[0].data = data.temperatura;
            graficoTemp.update();

            graficoUmidade.data.labels = data.labels;
            graficoUmidade.data.datasets[0].data = data.umidade;
            graficoUmidade.update();

            graficoGas.data.labels = data.labels;
            graficoGas.data.datasets[0].data = data.gas;
            graficoGas.update();

            const tempAtual = data.temperatura[data.temperatura.length - 1]; // Último valor
            const gasAtual = data.gas[data.gas.length - 1]; // Último valor

            const sirene = document.getElementById('sirene');
            const cooler = document.getElementById('cooler');

            if (gasAtual >= 3500) {
                sirene.src = URL_SIRENE_ATIVA;
            } else {
                sirene.src = URL_SIRENE_INATIVA;
            }
            
            if (tempAtual >= 30) {
                cooler.src = URL_COOLER_ATIVO;
            } else {
                cooler.src = URL_COOLER_INATIVO;
            }
        });
}

atualizarGrafico();
setInterval(atualizarGrafico, 5000);