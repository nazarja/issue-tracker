
/*
=======================================================
    JavaScript Functions common to all pages
=======================================================
*/


// init jquery nav-bar animations
function init() {

    // nav-bar items
    $('.ui.dropdown').dropdown({on: 'hover'});
    $('.cart-popup').popup();
    $('.ui.sidebar').sidebar('attach events', '.toc.item');


    // sticky menu
    $('.masthead').visibility({
        once: false,
        onBottomPassed: function () {
            $('.fixed.menu').transition('fade in');
        },
        onBottomPassedReverse: function () {
            $('.fixed.menu').transition('fade out');
        }
    });
}
init();



// smooth scroll function for anchor links
function smoothScroll() {
    $('a[href*="#"]').on('click', function (e) {
        e.preventDefault();

        $('html, body').animate(
            {
                scrollTop: $($(this).attr('href')).offset().top - 100,
            },
            800,
            'linear'
        );
    });
}
smoothScroll();



// scroll back to top button
function scrollToTop() {
    window.addEventListener('scroll', () => {
        const toTopBtn = document.querySelector('#to-top-btn');
        if (window.innerWidth > 800) {
            if (window.scrollY > 500 ? toTopBtn.style.right = "30px" : toTopBtn.style.right = "-50px") ;
        } else {
            toTopBtn.style.right = "-50px";
        }
    });
}
scrollToTop();



// change page / busy loader
function busyLoader(delay=0) {
    $("#busy-loader").fadeIn("fast");
    const animation = () => $("#busy-loader").fadeOut("slow");
    setTimeout(animation, delay)
}



// Go back to last page in history
function goBackInHistory() {
    $('.go-back-history-btn').on('click', () => window.history.back())
}
goBackInHistory();








