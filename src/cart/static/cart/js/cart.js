
/*
===========================================
    CART EVENT LISTENERS
===========================================
*/

// add to cart
if (document.querySelector('#ticket-vote-single')) {
    const voteSingle = document.querySelector('#ticket-vote-single');
    const voteDouble = document.querySelector('#ticket-vote-double');


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
        postCartTickets('create/', data, 'create')
    });
}


// update cart - remove items
if (document.querySelector('#update-cart-button')) {
    document.querySelector('#update-cart-button').onclick = () => getCartTickets('update');
    document.querySelector('#go-to-checkout-button').onclick = () => getCartTickets('checkout');
}

/*
===========================================
    GET CART UPDATED ITEMS
===========================================
*/

function getCartTickets(action) {
    const checkboxes = document.querySelectorAll('[type="checkbox"]');
    let data = [];

    checkboxes.forEach(item => !item.checked ?  data.push(item.value): false);
    console.log(data);
    data = data.join(',');
    postCartTickets('update/', data, action);
}



/*
===========================================
    CART POST REQUESTS
===========================================
*/

function postCartTickets(endpoint, data, action) {

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
        if (action === 'create') afterCreated();
        else if (action === 'update') window.location.href = '/cart/';
        else if (action === 'checkout') window.location.href = '/checkout/';
    })
    .catch(err => console.log(err))
}

/*
===========================================
    AFTER CART POST REQUESTS
===========================================
*/

function afterCreated() {
       document.querySelectorAll('.cart-item-count')
           .forEach(item => item.innerText = parseInt(item.innerText) + 1);
}

