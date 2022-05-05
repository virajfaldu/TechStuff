
$(document).ready(function () {

    $('.fa-bars').click(function () {
        $('.nav-items').toggleClass('active');
    });

    // click to scroll top
    $('.move-up span').click(function () {
        $('html, body').animate({
            scrollTop: 0
        }, 1000);
    })
});