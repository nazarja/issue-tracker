

/*
===================================================
    UPDATE PREVIEW INLINE WITH CURRENT EDITING
===================================================
*/

// GLOBAL SELECTORS
const titleCharsLeft = document.querySelector('.title-chars-left span');
const descriptionCharsLeft = document.querySelector('.description-chars-left span');
const titleInput = document.querySelector('#id_title');
const titlePreview = document.querySelector('#title');
const descriptionInput = document.querySelector('#id_description');
const descriptionPreview = document.querySelector('#description');
titleInput.onkeyup = () => titleInputAction();
descriptionInput.onkeyup = () => descriptionInputAction();



// get initial values for update page
if (location.href.includes('update')) {
    descriptionInputAction();
    titleInputAction();
}

// counts characters of the title and calculates how many characters the user has left
function titleInputAction() {
    titlePreview.innerHTML = titleInput.value;
    titleCharsLeft.innerHTML = (100 - titleInput.value.length).toString();
}

// counts characters of the description and calculates how many characters the user has left
function descriptionInputAction() {
    descriptionPreview.innerHTML = descriptionInput.value;
    descriptionCharsLeft.innerHTML = (2000 - descriptionInput.value.length).toString();
}

// changes the status icon on the preview, entire element needs to be replaced in the DOM
document.querySelector('#id_status').onchange = (event) => {
    const status = event.target.value;
    const ticketLabelContainer = document.querySelector('#ticket-label-container');

    switch(status) {
        case 'need help':
            ticketLabelContainer.innerHTML = `<div class="ui red horizontal label">Need Help</div>`;
            break;
        case 'in progress':
            ticketLabelContainer.innerHTML = `<div class="ui yellow horizontal label">In Progress</div>`;
            break;
        default:
            ticketLabelContainer.innerHTML =`<div class="ui green horizontal label">Resolved</div>`;
    }
};

