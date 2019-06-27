
// selectors
const form = document.querySelector('#contact-form');
const name = document.querySelector('#id_name');
const email = document.querySelector('#id_email');
const subject = document.querySelector('#id_subject');
const message = document.querySelector('#id_message');
form.onsubmit = (event) => postContactForm(event);

// dont allow editing username/email if user is not anon
if (name.value.length) {
    name.setAttribute('readonly', 'true');
    email.setAttribute('readonly', 'true');
}

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

// fetch callback
function onSuccessFormSubmit(data) {

    // clear fields
    if (!data.isAuth) {
        name.value = '';
        email.value = '';
    }
    subject.value = '';
    message.value = '';

    // show modal
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