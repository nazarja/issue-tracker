
/*
===========================================
    CART EVENT LISTENERS
===========================================
*/


// add to cart
if (document.querySelector('#ticket-vote-single')) {
    const voteSingle = document.querySelector('#ticket-vote-single');
    const voteDouble = document.querySelector('#ticket-vote-double');

    // create object with appropriate values - single or double vote info
    [voteSingle, voteDouble].forEach(item => item.onclick = (event) => {
        event.preventDefault();

        let data = {
            id: event.target.dataset.id,
            value: 0,
            votes: 0,
        };

        if (event.target.id === 'ticket-vote-single') {
            data.value = 5;
            data.votes = 1;
        }
        else {
            data.value = 8;
            data.votes = 2;
        }

        // call fetch
        postCartTickets('create/', data, 'create')
    });
}


// update cart action to post removed items to backend and trigger page refresh
if (document.querySelector('#update-cart-button')) {
    document.querySelector('#update-cart-button').onclick = () => getCartTickets('update');
    document.querySelector('#go-to-checkout-button').onclick = () => getCartTickets('checkout');
}

/*
===========================================
    GET CART UPDATED ITEMS
===========================================
*/


// figure out which items are due to be removed
// checked checkboxes will be the correct items to be removed
function getCartTickets(action) {
    const checkboxes = document.querySelectorAll('[type="checkbox"]');
    let data = [];

    // create a string of cart item timestamps to send in querystring to backend
    checkboxes.forEach(item => !item.checked ?  data.push(item.value): false);
    data = data.join(',');

    // call fetch
    postCartTickets('update/', data, action);
}


/*
===========================================
    ADD TO CART POST REQUESTS
===========================================
*/

// used for both updating and creating
function postCartTickets(endpoint, data, action) {

    // default body
    let body = `&data=${data}`;
    if (endpoint === 'create/') body = `&id=${data.id}&value=${data.value}&votes=${data.votes}`;

    fetch(`/cart/` + endpoint, {
        headers: new Headers({
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest',
        }),
        credentials: 'same-origin',
        method: 'POST',
        body: body,
    })
    .then(res => {
        if (res.status === 200) return res.json();
    })
    .then(data => {

        // either redirect if an update else increase cart total
        if (action === 'create') afterCreated();
        else if (action === 'update') window.location.href = '/cart/';
        else if (action === 'checkout') window.location.href = '/checkout/';
    })
    .catch(err => console.log(err))
}


/*
===========================================
    AFTER ADD TO CART POST REQUESTS
===========================================
*/


// update nav-bar item count
function afterCreated() {
       document.querySelectorAll('.cart-item-count')
           .forEach(item => item.innerText = parseInt(item.innerText) + 1);
}

