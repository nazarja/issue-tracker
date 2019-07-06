
/*
============================================
    CHARTS
============================================
*/


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
    console.log(data)
}