
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
    const resetAllButton = document.querySelector('#reset-all-values');
    const toTopClick = document.querySelector('#to-top-btn');
    const ticketIssueType = document.querySelector('h1');

    // set pagination button on first load
    if (parseInt(nextPage.dataset.count) <= 8)
        nextPage.setAttribute('disabled', 'true');
        previousPage.setAttribute('disabled', 'true');

    // global querystring
    queryString = {
        page: 1,
        query: '',
        issue: ticketIssueType.dataset.issue,
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
                queryString.order = ticketOrderDefault.dataset.order;
                ticketListAction(queryString);
        });

    // simple next page buttons
    [nextPage, previousPage]
        .forEach(item => item.onclick = (event) => {
            if (event.currentTarget.id === 'next-page') queryString.page += 1;
            else queryString.page -= 1;
            toTopClick.click();
            busyLoader(1000);
            setTimeout(() => ticketListAction(queryString), 1000);
        });

    resetAllButton.onclick = () => {
        queryString.page = 1;
        queryString.query = '';
        queryString.order = '-updated_on';
        ticketSearchInput.value = '';
        ticketOrderDefault.dataset.order = '-updated_on';
        ticketOrderDefault.innerHTML = 'Filter';
        ticketListAction(queryString);
    };
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
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest',
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
                    '<div class="ui red horizontal label">Need Help</div>' : item.status === 'in progress' ?
                    '<div class="ui yellow horizontal label">In Progress</div>' :  '<div class="ui green horizontal label">Resolved</div>';

        // determine if feature
        let feature = item.issue === 'feature' ? `<span class="pr1"><i class="money bill alternate outline icon green"></i> &euro;${item.earned} earned</span>` : '';


        // create element - map over results and create html
        const div = document.createElement('div');
        div.innerHTML = `
             <div id="ticket" class="ui card">
                <div class="content">
                    <div class="left floated">
                        ${status}
                        <span class="ticket-category category pl1 tcg70">${item.issue.charAt(0).toUpperCase() + item.issue.slice(1)} </span>
                    </div>
                    <div id="author-container" class="author right floated">
                        <span id="author-username">${item.username.charAt(0).toUpperCase() + item.username.slice(1)}</span>
                        <img class="ui avatar image" src="${item.avatar}" height="40" width="40" alt="avatar">
                    </div>
                    <div class="meta">
            
                    </div>
                    <div class="description pt1">
                        <a class="header" href="/tickets/${item.id}/${item.slug}/details/">${item.title}</a>
                        <a class="ticket-view-details-button category pl1 pr1 right floated ui button mini" href="/tickets/${item.id}/${item.slug}/details/">Vote : View Details</a>
                    </div>
                </div>
                <div class="extra content">
                    <div id="extra-content-left" class="left floated">
                        <div class="meta">
                            <span class="code tcb"> #${item.id}</span>
                            <span class="pl1">last updated: </span>
                            <span class="time time-since">${moment(item.updated_on).fromNow()}</span>
                        </div>
                    </div>
                    <div id="extra-content-right" class="right floated">
                        <span class="pr1"><i class="thumbs up outline icon blue"></i> ${item.votes} votes</span>
                        ${feature}
                    </div>
                </div>
            </div>
        `;

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


function timeSince() {
    const time = document.querySelectorAll('.time-since');
    time.forEach(item =>
        item.innerHTML =  moment(new Date(item.innerHTML)).fromNow()
    );
}
timeSince();


