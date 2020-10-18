
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
const endOfComments = document.querySelector('#end-of-comments');


/*
=========================================================
    EVENT LISTENERS
=========================================================
*/


// listen for new reply to a comment
function newPostListener() {
    postTicketReply.onsubmit = () => {
        event.preventDefault();
        PostPutComments('POST', ticketReplyFormTextArea.value, getURL())
    }
}


// listen for edit or delete actions on a single comment
function editDeleteCommentListeners() {
    const editComment = document.querySelectorAll('.edit');
    const deleteComment = document.querySelectorAll('.delete');


    // inline editing - the comment text will be replaced by a text input with
    // its value set to the comment text
    editComment.forEach(comment => comment.onclick = (event) => {
        const _id = event.target.dataset.editid;
        const actions = event.target.parentElement;
        const form = document.querySelector(`[data-formid="${_id}"]`);
        const textarea = form.firstElementChild;
        const text = form.previousElementSibling;

        form.style.display = 'block';
        text.style.display = 'none';
        actions.style.display = 'none';

        // on submit update comment text html and post data
        form.onsubmit = (event) => {
            event.preventDefault();
            form.style.display = 'none';
            text.innerHTML = textarea.value;
            text.style.display = 'block';
            actions.style.display = 'block';
            PostPutComments('PUT', textarea.value, _id);
        }
    });

    // delete comment - on click
    deleteComment.forEach(comment => comment.onclick = (event) => {
        const deleteBtn = event.target;
        const deleteButtons = deleteBtn.nextElementSibling;


        // confirm with user first
        deleteButtons.style.display = 'block';
        deleteBtn.style.color = '#2185d0';
        deleteBtn.innerText = 'Are you Sure?';

        // if ok - post data
        deleteButtons.firstElementChild.onclick = () =>
            GetDeleteComments('DELETE', event.target.dataset.deleteid);

        // if cancelled
        deleteButtons.lastElementChild.onclick = () => {
           deleteButtons.style.display = 'none';
           deleteBtn.innerText = 'Delete';
           deleteBtn.style.color = 'rgba(0,0,0,.4)';
        }
    });
}


// reply form chars left visual indicators
function replyCharactersLeftListener() {
    ticketReplyFormTextArea.onkeypress = () =>
        commentCharacterLeft.innerHTML = (500 - ticketReplyFormTextArea.value.length).toString();
}

/*
=========================================================
    API CALLS
=========================================================
*/


// get and delete requests only
function GetDeleteComments(method, _id=null) {

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
function PostPutComments(method, text, _id) {

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

    editDeleteCommentListeners();
    updateNumberOfComments('increase');
    isEmptyCommentsContainer();
}


// remove comments from dom
function removeComment(_id) {
    const comment = document.querySelector(`[data-commentid="${_id}"]`);
    comment.remove();

    updateNumberOfComments('decrease');
    isEmptyCommentsContainer();
}


// create multiple comments
function createComments(data) {
     updateNumberOfComments();
    if (!data.count) return false;

    // iterate results, create comment html
    data.results.forEach(item => {
        const div = document.createElement('div');
        div.innerHTML = createCommentHTML(item);
        commentsContainer.append(div);
    });

    // listener for edit / delete actions
    numberOfComments.innerHTML = ` <i class="comment icon"></i> Comments ${data.count}`;
    editDeleteCommentListeners();

    // check for empty comments count
    updateNumberOfComments();
}


/*
=========================================================
    COMMENTS HTML CREATION ACTIONS
=========================================================
*/

// return a single comment
function createCommentHTML(item) {

    // only allow current user to edit or delete comment
    item.current_user ? item.actions = `
        <a class="reply edit" data-editid="${item.id}">Edit</a>
        <a class="reply delete" data-deleteid="${item.id}">Delete</a>`
        : item.actions = '';

    // comment html
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

// update comments count
function updateNumberOfComments(direction) {
    let num = parseInt(numberOfComments.innerHTML.match(/\d+/g)[0]);
    if (direction === 'increase') {
        numberOfComments.innerHTML = ` <i class="comment icon"></i> Comments ${num + 1}`;
    }
    else if (direction === 'decrease'){
        numberOfComments.innerHTML = ` <i class="comment icon"></i> Comments ${num - 1}`;
    }

    // check for empty comments count
    isEmptyCommentsContainer();
}

// decide to show empty container
function isEmptyCommentsContainer() {
    const num = parseInt(numberOfComments.innerHTML.match(/\d+/g)[0]);
    if (num === 0) {
        emptyContainer.style.display = 'block';
        endOfComments.style.display = 'none';
    }
    else {
        emptyContainer.style.display = 'none';
        endOfComments.style.display = 'block';
    }
}


/*
=========================================================
    INIT FUNCTIONS
=========================================================
*/


// gets the id of a ticket from the url
function getURL() {
    let url = window.location.href;
    return url.match(/tickets\/\d+/g)[0].match(/\d+/g)[0];
}

// on page load  -startup functions to run
function init() {
    GetDeleteComments('GET');
    newPostListener();
    replyCharactersLeftListener();
}
init();
