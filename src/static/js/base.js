
// init jquery navbar animations
function init() {

    // nav-bar items
    $('.ui.dropdown').dropdown({on: 'hover'});
    $('.cart-popup').popup();
    $('.ui.sidebar').sidebar('attach events', '.toc.item');


	// sticky menu
    $('h1').visibility({
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



