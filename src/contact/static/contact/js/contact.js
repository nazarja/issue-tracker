
/*
=======================================================
    GLOBAL VARIABLES
=======================================================
*/

const form = document.querySelector('#contact-form');
const name = document.querySelector('#id_name');
const email = document.querySelector('#id_email');
const subject = document.querySelector('#id_subject');
const message = document.querySelector('#id_message');


// form submit event listener
form.onsubmit = (event) => postContactForm(event);

// dont allow editing username / email if user is a logged in user
if (name.value.length) {
    name.setAttribute('readonly', 'true');
    email.setAttribute('readonly', 'true');
}


/*
=======================================================
    POST FORM ACTIONS
=======================================================
*/


// post form
function postContactForm(event) {
    event.preventDefault();

    fetch('/contact/', {
        method: 'POST',
        headers: new Headers({
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest',
                }),
        body: `name=${name.value}&email=${email.value}&subject=${subject.value}&message=${message.value}`,
        credentials: 'same-origin',
    })
    .then(res => res.json())
    .then(data => onSuccessFormSubmit(data))
    .catch(err => console.log(err))
}

// successful form posted
function onSuccessFormSubmit(data) {

    // clear form fields is anonymous user
    if (!data.isAuth) {
        name.value = '';
        email.value = '';
    }
    subject.value = '';
    message.value = '';

    // show modal to confirm successful form posted to backend
    document.querySelector('#form-response-text').innerHTML = data.text;
    if (document.querySelector('.ui.tiny.modal')) {
        $('.ui.tiny.modal')
            .modal({
                dimmerSettings: {opacity: .3},
            })
            .modal('show')
            .delay(2000)
            .queue(function () {
                $(this).modal('hide').dequeue();
            });
    }
}