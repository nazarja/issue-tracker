
// add to cart
if (document.querySelector('#ticket-vote-single')) {
    const voteSingle = document.querySelector('#ticket-vote-single');
    const voteDouble = document.querySelector('#ticket-vote-double');


    [voteSingle, voteDouble].forEach(item => item.onclick = (event) => {
        event.preventDefault();

        let data = {
            value: 0,
            id: event.target.dataset.id,
            votes: 0,
        };

        if (event.target.id === 'ticket-vote-single') {
            data.value = 5;
            data.votes = 1;
        }
        else {
            data. value = 8;
            data.votes = 2;
        }

        addToCart(data);
    });
}


// update cart - remove items
if (document.querySelector('#update-cart-button')) {
    const voteSingle = document.querySelector('#update-cart-button');
    const cartItemsCount = document.querySelectorAll('.cart-item-count');
    const checkboxes = document.querySelectorAll('[type="checkbox"]');

    checkboxes.forEach(item => console.log(item.value));
}



function addToCart(data) {
    const cartItemsCount = document.querySelectorAll('.cart-item-count');


    fetch(`/cart/update/`, {
        headers: new Headers({
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest',
        }),
        credentials: 'same-origin',
        method: 'POST',
        body: `&value=${data.value}&votes=${data.votes}&id=${data.id}`,
    })
    .then(res => {
        if (res.status === 200) {
            return res.json()
        }
    })
    .then(data => {
        console.log(data);
        cartItemsCount.forEach(item => item.innerText = parseInt(item.innerText) + 1)
    })
    .catch(err => console.log(err))
}

function removeFromCart() {

}