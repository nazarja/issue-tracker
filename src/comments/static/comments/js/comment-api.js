
/*
=========================================================
    EVENT LISTENERS
=========================================================
*/

const postTicketReply = document.querySelector('#comment-reply-form');
const ticketReplyFormTextArea = document.querySelector('#comment-reply-form textarea');

postTicketReply.onsubmit = () => {
    event.preventDefault();
    console.log(ticketReplyFormTextArea.value);
    getComments('POST', ticketReplyFormTextArea.value)
};

// NOTE SEPERATE FETCH FOR GET (Cannot Have Body)
/*
=========================================================
    API CALLS
=========================================================
*/

// // fetch calls to comments api
// function getComments(method=false, data=false, url=false) {
//     let endpoint;
//     if (!url) url = getURL();
//     console.log(method, data, url);
//     switch(method) {
//         case 'GET':
//             endpoint = `/comments/api/${url}/list/`;
//             break;
//         case 'POST':
//             endpoint = `/comments/api/${url}/create/`;
//             break;
//         case 'PUT':
//             endpoint = `/comments/api/${url}/update/`;
//             break;
//         case 'DELETE':
//             endpoint = `/comments/api/${url}/delete/`;
//             break;
//         default:
//             return false;
//     }
//
//     fetch(endpoint, {
//         method: 'POST',
//         headers: new Headers({
//                     'Content-Type': 'application/x-www-form-urlencoded',
//                     'X-CSRFToken': csrftoken,
//                     'X-Requested-With': 'XMLHttpRequest',
//                 }),
//         body: `text=${data}&ticket=${url}`,
//         credentials: 'same-origin',
//     })
//     .then(res => {
//         try {
//             return res.json();
//         }
//         catch (err) {
//             console.log(res.text);
//             console.log(err);
//         }
//     })
//     .then(data => {
//         console.log(data);
//         createComments(data);
//     })
//     .catch(err => console.log(err));
// }
// getComments('GET');



function createComments(data) {
    const commentsContainer = document.querySelector('#comments-container');
    const emptyContainer = document.querySelector('#no-comments');
    const numberOfComments = document.querySelector('#number-of-comments');
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


function createCommentHTML(item) {
    return  `
            <div class="comment mv1">
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
                        <a class="reply">Reply</a>
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