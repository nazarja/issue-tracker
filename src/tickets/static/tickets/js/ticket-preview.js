
document.querySelector('#id_title').onkeyup = (event) => {
    document.querySelector('#title').innerHTML = event.target.value;
};

document.querySelector('#id_description').onkeyup = (event) => {
    document.querySelector('#description').innerHTML = event.target.value;
};

document.querySelector('#id_status').onchange = (event) => {
    const status = event.target.value;
    const ticketLabelContainer = document.querySelector('#ticket-label-container');
    switch(status) {
        case 'need help':
            ticketLabelContainer.innerHTML = `<div class="ui red horizontal label">Need Help</div>`;
            break;
        case 'in progress':
            ticketLabelContainer.innerHTML = `<div class="ui yellow horizontal label">In Progress</div>`;
            break;
        default:
            ticketLabelContainer.innerHTML =`<div class="ui green horizontal label">Resolved</div>`;
    }
};

