
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

ticketReplyFormTextArea.onkeypress = () => commentCharacterLeft.innerHTML = 500 - ticketReplyFormTextArea.value.length;

postTicketReply.onsubmit = () => {
    event.preventDefault();
    RUDComments('POST', ticketReplyFormTextArea.value, getURL())
};

/*
=========================================================
    API CALLS
=========================================================
*/

// get only
function getComments() {
    fetch(`/comments/api/${getURL()}/list/`, {
        method: 'GET',
        headers: new Headers({
                    'X-CSRFToken': csrftoken,
                }),
        credentials: 'same-origin',
    })
    .then(res => res.json())
    .then(data => createComments(data))
    .catch(err => console.log(err));
}
getComments();



// POST, PUT , DELETE
function RUDComments(method, text, url) {

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


function createComments(data) {
    numberOfComments.innerHTML = ` <i class="comment icon"></i> Comments ${data.count}`;

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
}


function prependNewComment(item) {
    const div = document.createElement('div');
    div.innerHTML = createCommentHTML(item);
    commentsContainer.prepend(div);
}


function insertUpdatedComment(data) {
    console.log(data)
}

function removeComment(data) {
    console.log(data)
}

function createCommentHTML(item) {
        console.log(item.updated_on);
        return `
            <div class="comment mv1" data-commentID="${item.id}">
                <a class="avatar">
                    <img src="${item.avatar}">
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
                        <a class="reply">Edit</a>
                        <a class="reply">Delete</a>
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
