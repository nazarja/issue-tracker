
/*
=========================================================
    DOM ELEMENT LISTENERS
=========================================================
*/


// Search, Filtering, Pagination
let queryString;
if ((document.querySelector('#current-page'))) {
    const nextPage = document.querySelector('#next-page');
    const previousPage = document.querySelector('#previous-page');
    const searchInputButton = document.querySelector('#ticket-search-btn');
    const ticketSearchInput = document.querySelector('#ticket-search-input');
    const ticketFilterButton= document.querySelector('#ticket-order-by');
    const ticketOrderDefault = document.querySelector('#ticket-order-by-default');

    // immediately disable previous button
    previousPage.setAttribute('disabled', 'true');

    // global querystring
    queryString = {
        page: 1,
        query: '',
        issue: 'bug',
        order: '-updated_on'
    };

    // if search or filter performed - get and set values
    [searchInputButton, ticketFilterButton]
        .forEach(item => item.onclick = (event) => {
            event.preventDefault();
            if (event.target.classList.contains('item'))
                ticketOrderDefault.setAttribute('data-order', event.target.dataset.order);
                queryString.page = 1;
                queryString.query = ticketSearchInput.value;
                queryString.issue = event.currentTarget.dataset.issue;
                queryString.order = ticketOrderDefault.dataset.order;
                ticketListAction(queryString);
        });

    // simple next page buttons
    [nextPage, previousPage]
        .forEach(item => item.onclick = (event) => {
            if (event.target.id === 'next-page') queryString.page += 1;
            else queryString.page -= 1;
            ticketListAction(queryString);
        });
}


// delete button event listener - only for edit and detail views
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

    let endpoint = `/tickets/api/list/?issue=${queryString.issue}&order=${queryString.order}&page=${queryString.page}`;
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
        createTicketList(data);
        console.log(data)
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


function createTicketList(data) {
    const container = document.querySelector('#ticket-list-container');
    const emptyContainer = document.querySelector('.ui.placeholder');

    // empty container before rerender
    container.innerHTML = '';

    // if no results show empty placeholder
    !data.results.length ? emptyContainer.style.display = 'block' : emptyContainer.style.display = 'none';

    // map over returned results
    data.results.map(item => {

        // determine status
        let status = item.status === 'need help' ?
                    '<a class="ui tag red label ticket-label">Needs Help</a>' : item.status === 'in progress' ?
                    '<a class="ui yellow tag label ticket-label">In Progress</a>' :  '<a class="ui green tag label ticket-label">Resolved</a>';

        // determine if feature
        let feature = item.issue === 'feature' ? `<span class="pr1"><i class="money bill alternate outline icon"></i> ${item.earned} Earned </span>` : '';


        // create element - map over results and create html
        const div = document.createElement('div');
        div.innerHTML = `<div id="ticket" class="mv1 cards">
            <div class="ui segment top attached">
                <div class="inline">
                    <img class="ui circular image mh2" src="${item.avatar}" height="40" width="40" alt="avatar">
                    <span class="mh1 code">${item.issue.charAt(0).toUpperCase() + item.issue.slice(1)} #${item.id}</span>
                    ${status}
                </div>
            </div>
            <div class="ui segment bottom attached">
                <span class="mv2 mh2"><a class="fw6" href="tickets/${item.id}/${item.slug}/ticket-detail-view/">${item.title}</a></span>
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

        // append results to dom
        container.append(div);
    });

    // set new pagination links
    setPagination(data.next, data.previous)
}


// enable disable pagination buttons
function setPagination(next, previous) {
    const currentPage = document.querySelector('#current-page');
    const nextPage = document.querySelector('#next-page');
    const previousPage = document.querySelector('#previous-page');
    next == null ? nextPage.setAttribute('disabled', 'true') : nextPage.removeAttribute('disabled');
    previous == null ? previousPage.setAttribute('disabled', 'true') :  previousPage.removeAttribute('disabled');
    currentPage.innerHTML = queryString.page;
}


