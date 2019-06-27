
const form = document.querySelector('#contact-form');
form.addEventListener('submit', (event) => {
    event.preventDefault();

    let obj = {
        name: document.querySelector('#id_name').value,
        email: document.querySelector('#id_email').value,
        subject: document.querySelector('#id_subject').value,
        message: document.querySelector('#id_message').value,
    };

    fetch('/contact/', {
        method: 'POST',
        headers: new Headers({
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest',
                }),
        body: `name=${obj.name}&email=${obj.email}&subject=${obj.subject}&message=${obj.subject}`,
        credentials: 'same-origin',
    })
    .then(res => res.json())
    .then(data => {
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
    })
    .catch(err => console.log(err))
});