$wintab = $('.wintab');
$(document).ready(function () {
    $wintab.find('a.tab-link.is-active').next().toggle();
    $wintab.on('click', 'div > a.tab-link', function(event) {
        event.preventDefault();
        if ($(this).hasClass('is-blocked')) {}
        else if (!$(this).hasClass('is-active')) {
            $wintab.find('.is-open').removeClass('is-open').hide();
            $(this).next().toggleClass('is-open').toggle();
            $wintab.find('.is-active').removeClass('is-active');
            $(this).addClass('is-active');
        }
    });
});