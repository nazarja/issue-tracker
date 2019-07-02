
/*
=========================================================
   GLOBAL VARIABLES
=========================================================
*/


const postTicketReply = document.querySelector('#comment-reply-form');
const commentCharacterLeft = document.querySelector('#comment-characters-left');
const ticketReplyFormTextArea = document.querySelector('#comment-reply-form textarea');
const commentsContainer = document.querySelector('#comments-container');
const emptyContainer = document.querySelector('#no-comments');
const numberOfComments = document.querySelector('#number-of-comments');


/*
=========================================================
    EVENT LISTENERS
=========================================================
*/


// reply form chars left
function replyCharactersLeftListener() {
    ticketReplyFormTextArea.onkeypress = () =>
        commentCharacterLeft.innerHTML = 500 - ticketReplyFormTextArea.value.length;
}


// listen for new reply
function newPostListener() {
    postTicketReply.onsubmit = () => {
        event.preventDefault();
        PPComments('POST', ticketReplyFormTextArea.value, getURL())
    }
}


// listen for edit or delete actions
function editDeleteCommentListeners() {
    const editComment = document.querySelectorAll('.edit');
    const deleteComment = document.querySelectorAll('.delete');


    // inline editing
    editComment.forEach(comment => comment.onclick = (event) => {
        const _id = event.target.dataset.editid;
        const actions = event.target.parentElement;
        const form = document.querySelector(`[data-formid="${_id}"]`);
        const textarea = form.firstElementChild;
        const text = form.previousElementSibling;

        form.style.display = 'block';
        text.style.display = 'none';
        actions.style.display = 'none';

        form.onsubmit = (event) => {
            event.preventDefault();
            form.style.display = 'none';
            text.innerHTML = textarea.value;
            text.style.display = 'block';
            actions.style.display = 'block';
            PPComments('PUT', textarea.value, _id);
        }
    });

    // delete comment
    deleteComment.forEach(comment => comment.onclick = (event) => {
        const deleteBtn = event.target;
        const deleteButtons = deleteBtn.nextElementSibling;
        deleteButtons.style.display = 'block';
        deleteBtn.style.color = '#2185d0';
        deleteBtn.innerText = 'Are you Sure?';

        deleteButtons.firstElementChild.onclick = () =>
            GDComments('DELETE', event.target.dataset.deleteid);

        deleteButtons.lastElementChild.onclick = () => {
           deleteButtons.style.display = 'none';
           deleteBtn.innerText = 'Delete';
           deleteBtn.style.color = 'rgba(0,0,0,.4)';
        }
    });
}


/*
=========================================================
    API CALLS
=========================================================
*/


// get only
function GDComments(method, _id=null) {

    let endpoint;
    if (method === 'GET') endpoint = `${getURL()}/list/`;
    else endpoint = `${_id}/delete/`;

    fetch('/comments/api/' + endpoint, {
        method: method,
        headers: new Headers({
            'X-CSRFToken': csrftoken,
        }),
        credentials: 'same-origin',
    })
    .then(res => {
        if (method === 'GET') return res.json();
        return res;
    })
    .then(data => {
        if (method === 'GET') createComments(data);
        if (data.status === 204) removeComment(_id);
    })
    .catch(err => console.log(err));
}


// POST, PUT
function PPComments(method, text, _id) {

    let body;
    let endpoint;
    if (method === 'POST') {
        body = `text=${text}&ticket=${_id}`;
        endpoint = `/comments/api/${_id}/create/`;
    }
    else {
        body = `text=${text}&id=${_id}`;
        endpoint = `/comments/api/${_id}/update/`;
    }

    fetch(endpoint, {
        method: method,
        headers: new Headers({
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest',
        }),
        body: body,
        credentials: 'same-origin',
    })
    .then(res => res.json())
    .then(data => {
        if (method === 'POST') prependNewComment(data);
    })
    .catch(err => console.log(err));
}


/*
=========================================================
    COMMENTS DOM ACTIONS
=========================================================
*/


// add new comment
function prependNewComment(item) {
    const div = document.createElement('div');
    div.innerHTML = createCommentHTML(item);
    commentsContainer.prepend(div);
    updateNumberOfComments('increase');
    editDeleteCommentListeners();
}


// remove comments from dom
function removeComment(_id) {
    const comment = document.querySelector(`[data-commentid="${_id}"]`);
    comment.remove();
    updateNumberOfComments('decrease')
}


// create multiple comments
function createComments(data) {
    // if no results show empty placeholder
    if (!data.count) {
        emptyContainer.style.display = 'block';
        return false;
    }
    emptyContainer.style.display = 'none';

    // iterate results, create comment html
    data.results.forEach(item => {
        const div = document.createElement('div');
        div.innerHTML = createCommentHTML(item);
        commentsContainer.append(div);
    });

    // listener for edit / delete actions
    numberOfComments.innerHTML = ` <i class="comment icon"></i> Comments ${data.count}`;
    editDeleteCommentListeners();
}

// update comments count
function updateNumberOfComments(direction) {
    let num = parseInt(numberOfComments.innerHTML.match(/\d+/g)[0]);
    if (direction === 'increase') {
        numberOfComments.innerHTML = ` <i class="comment icon"></i> Comments ${num + 1}`;
    }
    else {
        numberOfComments.innerHTML = ` <i class="comment icon"></i> Comments ${num - 1}`;
    }
}

/*
=========================================================
    COMMENTS HTML CREATION ACTIONS
=========================================================
*/


function createCommentHTML(item) {

    // only allow current user to edit or delete comment
    item.current_user ? item.actions = `
        <a class="reply edit" data-editid="${item.id}">Edit</a>
        <a class="reply delete" data-deleteid="${item.id}">Delete</a>`
        : item.actions = '';

    return `
            <div class="comment mv1 pb1" data-commentid="${item.id}">
                <a class="avatar">
                    <img src="${item.avatar}" alt="avatar image">
                </a>
                <div class="content">
                    <span class="author">${item.username}</span>
                    <div class="metadata">
                        <div class="date">${moment(item.updated_on).fromNow()}</div>
                    </div>
                    <div class="text">
                        <p>${item.text}</p>
                        <form class="inline-form all-forms" data-formid="${item.id}">
                            <textarea class="inline-editing" maxlength="500">${item.text}</textarea>
                            <button class="ui button green tiny">update</button>
                        </form>
                    </div>
                    <div class="actions">
                        ${item.actions}
                        <span class="delete-buttons">
                            <span class="yes">Yes</span>
                            <span class="no">No, Cancel.</span>
                        </span> 
                    </div>
                </div>
            </div>
        `;
}


/*
=========================================================
    MISC FUNCTIONS
=========================================================
*/


function getURL() {
    let url = window.location.href;
    return url.match(/tickets\/\d+/g)[0].match(/\d+/g)[0];
}


function init() {
    GDComments('GET');
    newPostListener();
    replyCharactersLeftListener();
}
init();
