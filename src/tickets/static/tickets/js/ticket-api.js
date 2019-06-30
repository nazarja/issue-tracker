
/*
=========================================================
    DOM ELEMENT LISTENERS
=========================================================
*/


// check if tickets segment on page
if (document.querySelector('#ticket-segment')) {
    const searchInputButton = document.querySelector('#ticket-search-btn');
    const ticketSearchInput = document.querySelector('#ticket-search-input');
    const ticketFilterButton= document.querySelector('#ticket-order-by');
    const ticketOrderDefault = document.querySelector('#ticket-order-by-default');

    let queryString = {
            query: '',
            issue: 'bug',
            order: '-updated_on'
        };

    [searchInputButton, ticketFilterButton].forEach(item =>  item.onclick = (event) => {
        event.preventDefault();

        if (event.target.classList.contains('item'))
            ticketOrderDefault.setAttribute('data-order', event.target.dataset.order);

        queryString.query = ticketSearchInput.value;
        queryString.issue = event.currentTarget.dataset.issue;
        queryString.order = ticketOrderDefault.dataset.order;

        ticketListAction(queryString);
    });

}

// check if delete button is on the page
if (document.querySelector('#ticket-delete-btn')) {
    document.querySelector('#ticket-delete-btn').onclick = (event) => {
        event.preventDefault();
        ticketDeleteAction();
        $('.ui.basic.modal').modal('show');
    }
}


/*
=========================================================
    API REQUEST ACTIONS
=========================================================
*/

function ticketListAction(queryString) {

        let endpoint = `/tickets/api/list/?issue=${queryString.issue}&order=${queryString.order}`;
        endpoint = queryString.query === false ? endpoint : endpoint + `&q=${queryString.query}`;

        fetch(endpoint, {
            method: 'GET',
            headers: new Headers({
                'X-CSRFToken': csrftoken,
            }),
            credentials: 'same-origin',
        })
        .then(res => res.json())
        .then(data => {
            console.log(data);
            createTicketList(data);
        })
        .catch(err => console.log(err));
}



function ticketDeleteAction() {
    const ticketDeleteConfirmBtn = document.querySelector('#ticket-delete-confirm-btn');
    const _id = ticketDeleteConfirmBtn.dataset.id;
    const issue = ticketDeleteConfirmBtn.dataset.issue;

     // POST to delete the object
    ticketDeleteConfirmBtn.onclick = () => {
        fetch(`/tickets/api/${_id}/delete/`, {
            method: 'DELETE',
            headers: new Headers({
                'X-CSRFToken': csrftoken,
            }),
            credentials: 'same-origin',
        })
        .then(res => {
            if (res.status === 204) window.location.href = `/tickets/${issue}s/`;
            else  $('.ui.basic.modal.error').modal('show');
        })
        .catch(err => console.log(err));
    };
}


/*
=========================================================
    CREATE HTML
=========================================================
*/


function timeSince() {
    const time = document.querySelectorAll('.time-since');
    time.forEach(item =>
        item.innerHTML =  moment(new Date(item.innerHTML)).fromNow()
    );
}
timeSince();


function createTicketList(data) {
    const container = document.querySelector('#ticket-list-container');
    const emptyContainer = document.querySelector('.ui.placeholder');

    container.innerHTML = '';

    !data.length ? emptyContainer.style.display = 'block' : emptyContainer.style.display = 'none';

    data.map(item => {
        let status = item.status === 'need help' ?
                    '<a class="ui tag red label ticket-label">Needs Help</a>' : item.status === 'in progress' ?
                    '<a class="ui yellow tag label ticket-label">In Progress</a>' :  '<a class="ui green tag label ticket-label">Resolved</a>';

        let feature = item.issue === 'feature' ? `<span class="pr1"><i class="money bill alternate outline icon"></i> ${item.earned} Earned </span>` : '';



        const div = document.createElement('div');
        div.innerHTML = `<div id="ticket" class="mv1 cards">
            <div class="ui segment top attached">
                <div class="inline">gi
                    <img class="ui circular image mh2" src="${item.avatar}" height="40" width="40" alt="avatar">
                    <span class="mh1 code">${item.issue} #${item.id}</span>
                    <span class="mh1"><a class="fw6" href="tickets/${item.id}/${item.slug}/ticket-detail-view/">${item.title}</a></span>
                    ${status}
                </div>
            </div>
            <div class="ui segment bottom attached">
                <p id="ticket-list-description" class="mh2">${item.description}</p>
                <div class="inline">
                    <span class="mh2 font-light">
                        <span>Submitted by:</span> <span>${item.username}</span></span>
                        <span class="font-light">Last updated: <span class="time-since">${moment(item.updated_on).fromNow()}</span>
                    </span>
                </div>
                <div class="fr float-right">
                    <span class="pr1"><i class="thumbs up outline icon"></i> ${item.votes} votes </span>
                    ${feature} 
                </div>
            </div>
        </div>`;
        container.append(div);
    });
}
