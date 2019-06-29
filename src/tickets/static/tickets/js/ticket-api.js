
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
        console.log(endpoint);
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
    container.innerHTML = '';

    data.map(item => {
        let status = item.status === 'need help' ?
                    '<a class="ui tag red label">Needs Help</a>' : item.status === 'in progress' ?
                    '<a class="ui yellow tag label">In Progress</a>' :  '<a class="ui green tag label">Resolved</a>';

        const div = document.createElement('div');
        div.innerHTML = `
        <div class="mv1">
            <img src="${item.avatar}" height="40" width="40" alt="avatar">
            <a href="${item.id}/${item.slug}/ticket-detail-view">${item.title}</a><br/>
            <span>${item.title}</span><br/>
            C: <span>${moment(item.updated_on).fromNow()}</span><br/>
            U: <span>${moment(item.created_on).fromNow()}</span><br/>
            ${status}
        </div>
        `;
        container.append(div);
    });
}

