
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


