
// init jquery nav-bar animations
function init() {

    // nav-bar items
    $('.ui.dropdown').dropdown({on: 'hover'});
    $('.cart-popup').popup();
    $('.ui.sidebar').sidebar('attach events', '.toc.item');


	// sticky menu
    $('.masthead').visibility({
        once: false,
        onBottomPassed: function() {
            $('.fixed.menu').transition('fade in');
        },
            onBottomPassedReverse: function() {
            $('.fixed.menu').transition('fade out');
        }
    });
}
init();


// smooth scroll function for anchor links
function smoothScroll() {
    $('a[href*="#"]').on('click', function(e) {
        e.preventDefault();

        $('html, body').animate(
            {
                scrollTop: $($(this).attr('href')).offset().top - 100,
            },
            500,
            'linear'
        );
    });
}
smoothScroll();


// Scroll back to Top Btn logic
const toTopBtn = document.querySelector('#to-top-btn');
window.addEventListener('scroll', () => {
    if (window.innerWidth > 800) {
        if (window.scrollY > window.innerHeight ? toTopBtn.style.right = "30px" : toTopBtn.style.right = "-50px");
    }
    else {
        toTopBtn.style.right = "-50px";
    }
});



