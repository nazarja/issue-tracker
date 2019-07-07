
/*
============================================
    CHARTS
============================================
*/

// set default colors
const colors = [
    'rgba(255, 104, 94, ',
    'rgba(74, 198, 253, ',
    'rgba(0, 190, 74, ',
    'rgba(246, 219, 62, ',
    'rgba(207, 218, 217, ',
    'rgba(241, 132, 175, ',
    'rgba(108, 136, 130, ',
    'rgba(246, 153, 36, ',
    'rgba(235, 235, 237, ',
    'rgba(246, 153, 36, ',
];


// get request to charts api view for charts data
function getChartsData() {
    fetch('/charts/api/data/', {
        method: 'GET',
        headers: new Headers({
            'X-CSRFToken': csrftoken,
        }),
        credentials: 'same-origin',
    })
        .then(res => res.json())
        .then(data => {
            createCharts(data);
        })
        .catch(err => console.log(err));
}

getChartsData();


/*
============================================
    CREATE CHARTS

    function is split into two sub loops,
    each loop creates a separate row of charts
============================================
*/

function createCharts(data) {

    // first row of charts
    [data.highestVotes, data.numOfTickets, data.ticketStatus].forEach((dataset, i) => {

        // selectors for charts canvas divs
        const ids = ['highestVotes', 'numOfTickets', 'ticketStatus'];

        // colors arrays
        const backgroundColorsArray = [];
        const borderColorsArray = [];

        // assign colors based on length of dataset
        for (let x in dataset) {
            backgroundColorsArray.push(colors[x] + '0.2)');
            borderColorsArray.push(colors[x] + '1)');
        }

        // set labels - either first choice or second
        let dataLabels = i < 2 ? ['Bugs', 'Features'] : ['Needs Help', 'In Progress', 'Resolved'];

        // 3 bar charts
        var ctx = document.getElementById(ids[i]).getContext('2d');
        var newChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: dataLabels,
                datasets: [{
                    label: 'No. of Tickets: ',
                    data: dataset,
                    backgroundColor: backgroundColorsArray,
                    borderColor: borderColorsArray,
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    });

    // second row of charts
    [data.highestBugs, data.highestFeatures, data.highestStatus].forEach((dataset, i) => {

        // selectors for charts canvas divs
        const ids = ['highestBugs', 'highestFeatures', 'highestStatus'];

        // colors arrays
        const backgroundColorsArray = [];
        const borderColorsArray = [];

        // assign colors based on length of dataset
        for (let x in dataset) {
            backgroundColorsArray.push(colors[x] + '0.2)');
            borderColorsArray.push(colors[x] + '1)');
        }

        // label and datasets
        let dataLabels = [];
        let datasetArray = [];

        // each dataset needs to be split into two
        // separate arrays of labels and values
        dataset.forEach(item => {
            dataLabels.push(`${item.title}`);
            datasetArray.push(item.votes);
        });

        // polar area charts
        var ctx = document.getElementById(ids[i]).getContext('2d');
        var newChart = new Chart(ctx, {
            type: 'polarArea',
            data: {
                labels: dataLabels,
                datasets: [{
                    label: 'Status of Tickets',
                    data: datasetArray,
                    backgroundColor: backgroundColorsArray,
                    borderColor: borderColorsArray,
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    });
}
