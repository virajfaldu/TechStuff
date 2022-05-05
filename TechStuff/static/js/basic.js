
$(document).ready(function () {

    $('.fa-bars').click(function () {
        $('.nav-items').toggleClass('active');
    });

    $('.move-up span').click(function () {
        $('html').animate({
            scrollTop: 0
        }, 1000);
    })
});