
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
            ticketLabelContainer.innerHTML = `<span class="ui tag red label ticket-label">Needs Help</span>`;
            break;
        case 'in progress':
            ticketLabelContainer.innerHTML = `<span class="ui yellow tag label ticket-label">In Progress</span>`;
            break;
        default:
            ticketLabelContainer.innerHTML =`<span class="ui green tag label ticket-label">Resolved</span>`;
    }
};

