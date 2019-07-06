
/*
============================================
    CHARTS
============================================
*/

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

// Get Request
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


// function to create and display the charts
function createCharts(data) {

    [data.highestVotes, data.numOfTickets, data.ticketStatus].forEach((dataset, i) => {

        const ids = ['highestVotes', 'numOfTickets', 'ticketStatus'];
        const backgroundColorsArray = [];
        const borderColorsArray = [];
        for (let x in dataset) {
            backgroundColorsArray.push(colors[x] + '0.2)');
            borderColorsArray.push(colors[x] + '1)');
        }
        let dataLabels = i < 2 ? ['Bugs', 'Features'] : ['Needs Help', 'In Progress', 'Resolved'];

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


     [data.highestBugs, data.highestFeatures, data.highestStatus].forEach((dataset, i) => {

        const ids = ['highestBugs', 'highestFeatures', 'highestStatus'];
        const backgroundColorsArray = [];
        const borderColorsArray = [];
        for (let x in dataset) {
            backgroundColorsArray.push(colors[x] + '0.2)');
            borderColorsArray.push(colors[x] + '1)');
        }
        let dataLabels = [];
        let datasetArray = [];

        dataset.forEach(item => {
            dataLabels.push(`${item.title}`);
            datasetArray.push(item.votes);
        });

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







    // // votes per bugs and features
    // var ctx = document.getElementById('highestVotes').getContext('2d');
    // var highestVotes = new Chart(ctx, {
    //     type: 'bar',
    //     data: {
    //         labels: ['Bugs', 'Features'],
    //         datasets: [{
    //             label: 'No. of Votes',
    //             data: data.highestVotes,
    //             backgroundColor: [
    //                 'rgba(0, 190, 74, 0.2)',
    //                 'rgba(74, 198, 253, 0.2)',
    //             ],
    //             borderColor: [
    //                 'rgba(0, 190, 74, 1)',
    //                 'rgba(74, 198, 253, 1)',
    //             ],
    //             borderWidth: 1
    //         }]
    //     },
    //    options: {
    //          scales: {
    //             yAxes: [{
    //                 ticks: {
    //                     beginAtZero: true
    //                 }
    //             }]
    //         }
    //     }
    // });

    // // number of bugs and features
    // var ctx2 = document.getElementById('numOfTickets').getContext('2d');
    // var numOfTickets = new Chart(ctx2, {
    //     type: 'bar',
    //     data: {
    //         labels: ['Bugs', 'Features'],
    //         datasets: [{
    //             label: 'No. of Tickets',
    //             data: data.numOfTickets,
    //             backgroundColor: [
    //                 'rgba(0, 190, 74, 0.2)',
    //                 'rgba(74, 198, 253, 0.2)',
    //             ],
    //             borderColor: [
    //                  'rgba(0, 190, 74, 1)',
    //                 'rgba(74, 198, 253, 1)',
    //             ],
    //             borderWidth: 1
    //         }]
    //     },
    //     options: {
    //          scales: {
    //             yAxes: [{
    //                 ticks: {
    //                     beginAtZero: true
    //                 }
    //             }]
    //         }
    //     }
    // });


    // // ticket status
    // var ctx3 = document.getElementById('ticketStatus').getContext('2d');
    // var ticketStatus = new Chart(ctx3, {
    //     type: 'polarArea',
    //     data: {
    //         labels: ['Needs Help', 'In Progress', 'Resolved'],
    //         datasets: [{
    //             label: 'Status of Tickets',
    //             data: data.ticketStatus,
    //             backgroundColor: [
    //                 'rgba(255, 104, 94, 0.2)',
    //                 'rgba(74, 198, 253, 0.2)',
    //                 'rgba(0, 190, 74, 0.2)',
    //             ],
    //             borderColor: [
    //                 'rgba(255, 104, 94, 1)',
    //                 'rgba(74, 198, 253, 1)',
    //                 'rgba(0, 190, 74, 1)',
    //             ],
    //             borderWidth: 1
    //         }]
    //     },
    //     options: {
    //          scales: {
    //             yAxes: [{
    //                 ticks: {
    //                     beginAtZero: true
    //                 }
    //             }]
    //         }
    //     }
    // });


    // // ticket status
    // var labels6 = [];
    // var data6 = [];
    //
    // data.highestStatus.forEach(item => {
    //     labels6.push(`Name: ${item.title}`);
    //     data6.push(item.votes);
    // });
    //
    // var ctx6 = document.getElementById('highestStatus').getContext('2d');
    // var highestStatus = new Chart(ctx6, {
    //     type: 'pie',
    //     data: {
    //         labels: labels6,
    //         datasets: [{
    //             label: 'Status of Tickets',
    //             data: data6,
    //             backgroundColor: [
    //                 'rgba(255, 104, 94, 0.2)',
    //                 'rgba(74, 198, 253, 0.2)',
    //                 'rgba(0, 190, 74, 0.2)',
    //                 'rgba(255, 104, 94, 0.2)',
    //                 'rgba(74, 198, 253, 0.2)',
    //                 'rgba(0, 190, 74, 0.2)',
    //                 'rgba(255, 104, 94, 0.2)',
    //                 'rgba(74, 198, 253, 0.2)',
    //                 'rgba(0, 190, 74, 0.2)',
    //                 'rgba(255, 104, 94, 0.2)',
    //                 'rgba(74, 198, 253, 0.2)',
    //                 'rgba(0, 190, 74, 0.2)',
    //             ],
    //             borderColor: [
    //                 'rgba(255, 104, 94, 1)',
    //                 'rgba(74, 198, 253, 1)',
    //                 'rgba(0, 190, 74, 1)',
    //                 'rgba(255, 104, 94, 1)',
    //                 'rgba(74, 198, 253, 1)',
    //                 'rgba(0, 190, 74, 1)',
    //                 'rgba(255, 104, 94, 1)',
    //                 'rgba(74, 198, 253, 1)',
    //                 'rgba(0, 190, 74, 1)',
    //                 'rgba(255, 104, 94, 1)',
    //                 'rgba(74, 198, 253, 1)',
    //                 'rgba(0, 190, 74, 1)',
    //             ],
    //             borderWidth: 1
    //         }]
    //     },
    // });