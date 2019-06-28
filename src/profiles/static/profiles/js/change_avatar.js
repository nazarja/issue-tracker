
/*
=======================================================
    Change Avatar Post Request - DOM Actions
=======================================================
*/


// select avatar and add click event listener to each image
const avatars = document.querySelectorAll('.avatar-gallery-item');
avatars.forEach(avatar => avatar.onclick = () => changeAvatar(event));
$('.avatar-gallery-item').popup();


// DOM Actions
function changeAvatar(event) {

    // remove selected class
    avatars.forEach(avatar => avatar.classList.remove('avatar-gallery-item-selected'));

    // add selected class to clicked image and animate
    event.target.classList.add('avatar-gallery-item-selected');
    $(event.target).transition('pulse');

    const url = `/static/img/avatars/${event.target.dataset.url}`;
    // change currently visible profile avatar images
    ['#avatar-1', '#avatar-2', '#side-bar-avatar', '#avatar-modal'].forEach(item => document.querySelector(item).src = url);

    // inform backend of avatar change
    changeAvatarPostRequest(url);
}


// POST Request to DB - Show Modal
function changeAvatarPostRequest(url) {
    fetch('/profiles/change-avatar/', {
        method: 'POST',
        headers: new Headers({
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest',
                }),
        body: `url=${url}`,
        credentials: 'same-origin',
    })
        .then(res => res.text())
        .then(data => {
            $('.ui.tiny.modal')
                .modal({
                    dimmerSettings: {opacity: .3},
                })
                .modal('show')
                .delay(2000)
                .queue(function() {
                    $(this).modal('hide').dequeue();
                });
        })
        .catch(err => console.log('ERROR: ' + err))
}
