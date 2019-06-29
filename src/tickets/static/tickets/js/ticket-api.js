// href="{% url 'tickets:ticket-delete-api' slug=object.slug %}"


// check if delete button is on the page
if ( document.querySelector('#ticket-delete-btn')) {
    document.querySelector('#ticket-delete-btn').onclick = (event) => {
        event.preventDefault();

        deleteTicketAction();
        $('.ui.basic.modal').modal('show');
    }
}

function deleteTicketAction() {
    const deleteTicketConfirmBtn = document.querySelector('#ticket-delete-confirm-btn');
    const _id = deleteTicketConfirmBtn.dataset.id;
    const issue = deleteTicketConfirmBtn.dataset.issue;

     // POST to delete the object
    deleteTicketConfirmBtn.onclick = () => {
        fetch(`/tickets/api/${_id}/delete/`, {
        method: 'DELETE',
        headers: new Headers({
            'X-CSRFToken': csrftoken,
        }),
        credentials: 'same-origin',
        })
        .then(res => {
            console.log(res);
            if (res.status === 204) window.location.href = `/tickets/${issue}s/`;
            else  $('.ui.basic.modal.error').modal('show');
        })
        .catch(err => console.log(err));
    };
}
