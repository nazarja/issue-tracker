
/*
=========================================================
   VOTING ON BUGS ONLY
=========================================================
*/


if (document.querySelector('#ticket-vote-free')) {
    const votesCount = document.querySelector('#votes-count');
    const voteFree = document.querySelector('#ticket-vote-free');

    // on click get the tickets id and post to backend
    voteFree.onclick = (event) => {
        event.preventDefault();
        const _id = event.target.dataset.id;

        fetch(`/tickets/api/${_id}/vote/`, {
            headers: new Headers({
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest',
            }),
            credentials: 'same-origin',
            method: 'PUT',
            body: `votes=1&id=${_id}`
        })
        .then(res => {
            if (res.status === 200) {
                return res.json()
            }
        })
        .then(data => {

            // if response if ok, make sure user cannot vote again
            // increase the vote number of the ticket
            if (data.text === 'ok') {
                voteFree.setAttribute('disabled', 'true');
                voteFree.classList.add('gey');
                voteFree.classList.remove('primary');
                voteFree.innerText = 'You have already voted for this';
                votesCount.innerText = data.votes.toString()
            }
        })
        .catch(err => console.log(err))
    }
}