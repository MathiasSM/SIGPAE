$wintab = $('.wintab');
$(document).ready(function () {
    $wintab.each(function(index) {
        $(this).children('.tab').first().children('.tab-link').addClass('is-active').next().addClass('is-open').show();
    });
    $wintab.on('click', 'div > a.tab-link', function(event) {
        event.preventDefault();
        if (!$(this).hasClass('is-active')) {
            $wintab.find('.is-open').removeClass('is-open').hide();
            $(this).next().toggleClass('is-open').toggle();
            $wintab.find('.is-active').removeClass('is-active');
            $(this).addClass('is-active');
        }
    });
});
$(document).ready(function () {
    var vspace = $wintab.parent().outerHeight() - $('.tab-link').outerHeight();
    $('.pdf-viewer>div').css('height',vspace);
    var timer, $win = $(window);
    $win.on('resize',function(){
        clearTimeout(timer);
        timer = setTimeout(function(){
            vspace = $wintab.parent().outerHeight() - $('.tab-link').outerHeight();
            $('.pdf-viewer>div').css('height',vspace);
        }, 1000);
    });
});