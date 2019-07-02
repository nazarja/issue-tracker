
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
        PUDComments('POST', ticketReplyFormTextArea.value, getURL())
    }
}


// listen for edit or delete actions
function editDeleteCommentListeners() {
    const editComment = document.querySelectorAll('.edit');
    const deleteComment = document.querySelectorAll('.delete');

    editComment.forEach(comment => comment.onclick = (event) => {
        console.log(event.target.dataset.editid);
    });

    deleteComment.forEach(comment => comment.onclick = (event) => {
       getComments('DELETE', event.target.dataset.deleteid);
    });
}


/*
=========================================================
    API CALLS
=========================================================
*/


// get only
function getComments(method, _id=null) {

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
function PUDComments(method, text, url) {

    let endpoint = `/comments/api/${url}/`;
    method === 'POST' ?  endpoint += `create/` :
    method === 'PUT' ?  endpoint += `update/`  : endpoint += 'delete/';

    let body = `text=${text}&ticket=${url}`;


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
        console.log(data);
        switch(method){
            case 'POST':
                prependNewComment(data);
                break;
            case 'PUT':
                insertUpdatedComment(data);
                break;
            default:
                removeComment(data);
        }
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


// update comment text
function insertUpdatedComment(data) {
    console.log(data)
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
            <div class="comment mv1" data-commentid="${item.id}">
                <a class="avatar">
                    <img src="${item.avatar}" alt="avatar image">
                </a>
                <div class="content">
                    <a class="author">${item.username}</a>
                    <div class="metadata">
                        <div class="date">${moment(item.updated_on).fromNow()}</div>
                    </div>
                    <div class="text">
                        <p>${item.text}</p>
                    </div>
                    
                    <div class="actions">
                        ${item.actions}
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
    getComments('GET');
    newPostListener();
    replyCharactersLeftListener();
}
init();
