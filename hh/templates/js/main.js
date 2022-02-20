let getUrl = window.location;

function activateFavorites() {
    $('.favorite-icon').on('click', (event) => {
        let iconSpan = event.target.localName === 'span' ? event.target : event.target.querySelector('span');
        let url = iconSpan.closest('a').href;
        event.preventDefault();
        if (iconSpan.className.includes('lnr-star')) {
            iconSpan.classList.remove('lnr-star');
            iconSpan.classList.add('lnr-trash');
        } else {
            iconSpan.classList.remove('lnr-trash');
            iconSpan.classList.add('lnr-star');
        }
        $.ajax({url});
    });
}

function updateChatNav() {
    $.ajax({
        url: `/chat/notif/get/`,
        success: (data) => {
            let notifications = data['new_messages'];
            if (notifications && notifications !== '0') {
                $('.chat-nav-notif').html(notifications);
            } else {
                $('.chat-nav-notif').html('');
            }
        }
    })
}

function updateRespNav() {
    $.ajax({
        url: `/recruiting/responses/notif/get/`,
        success: (data) => {
            let notifications = data['new_responses'];
            if (notifications && notifications !== '0') {
                $('.resp-nav-notif').html(notifications);
            } else {
                $('.resp-nav-notif').html('');
            }
        }
    })
}

$(document).ready(function () {
    "use strict";

    let window_width = $(window).width(),
        window_height = window.innerHeight,
        header_height = $(".default-header").height(),
        header_height_static = $(".site-header.static").outerHeight(),
        fitscreen = window_height - header_height;

    $(".fullscreen").css("height", window_height)
    $(".fitscreen").css("height", fitscreen);

    if (document.getElementById("default-select")) {
        $('select').niceSelect();
    }

    if (document.getElementById("default-selects")) {
        $('select').niceSelect();
    }

    if (document.getElementById("default-selects2")) {
        $('select').niceSelect();
    }


    // Initiate superfish on nav menu
    $('.nav-menu').superfish({
        animation: {
            opacity: 'show'
        },
        speed: 400
    });

    if ($('#nav-menu-container').length) {
        let $mobile_nav = $('#nav-menu-container').clone().prop({
            id: 'mobile-nav'
        });
        $mobile_nav.find('> ul').attr({
            'class': '',
            'id': ''
        });
        $('body').append($mobile_nav);
        $('body').prepend('<button type="button" id="mobile-nav-toggle"><i class="lnr lnr-menu"></i></button>');
        $('body').append('<div id="mobile-body-overly"></div>');
        $('#mobile-nav').find('.menu-has-children').prepend('<i class="lnr lnr-chevron-down"></i>');

        $(document).on('click', '.menu-has-children i', function (e) {
            $(this).next().toggleClass('menu-item-active');
            $(this).nextAll('ul').eq(0).slideToggle();
            $(this).toggleClass("lnr-chevron-up lnr-chevron-down");
        });

        $(document).on('click', '#mobile-nav-toggle', function (e) {
            $('body').toggleClass('mobile-nav-active');
            $('#mobile-nav-toggle i').toggleClass('lnr-cross lnr-menu');
            $('#mobile-body-overly').toggle();
        });

        $(document).click(function (e) {
            let container = $("#mobile-nav, #mobile-nav-toggle");
            if (!container.is(e.target) && container.has(e.target).length === 0) {
                if ($('body').hasClass('mobile-nav-active')) {
                    $('body').removeClass('mobile-nav-active');
                    $('#mobile-nav-toggle i').toggleClass('lnr-cross lnr-menu');
                    $('#mobile-body-overly').fadeOut();
                }
            }
        });
    } else if ($("#mobile-nav, #mobile-nav-toggle").length) {
        $("#mobile-nav, #mobile-nav-toggle").hide();
    }

    $('.nav-menu a, #mobile-nav a, .scrollto').on('click', function () {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            let target = $(this.hash);
            if (target.length) {
                let top_space = 0;
                if ($('#header').length) {
                    top_space = $('#header').outerHeight();

                    if (!$('#header').hasClass('header-fixed')) {
                        top_space = top_space;
                    }
                }

                $('html, body').animate({
                    scrollTop: target.offset().top - top_space
                }, 1500, 'easeInOutExpo');

                if ($(this).parents('.nav-menu').length) {
                    $('.nav-menu .menu-active').removeClass('menu-active');
                    $(this).closest('li').addClass('menu-active');
                }

                if ($('body').hasClass('mobile-nav-active')) {
                    $('body').removeClass('mobile-nav-active');
                    $('#mobile-nav-toggle i').toggleClass('lnr-times lnr-bars');
                    $('#mobile-body-overly').fadeOut();
                }
                return false;
            }
        }
    });

    $(document).ready(function () {
        $('html, body').hide();
        if (window.location.hash) {
            setTimeout(function () {
                $('html, body').scrollTop(0).show();
                $('html, body').animate({
                    scrollTop: $(window.location.hash).offset().top
                }, 1000)
            }, 0);
        } else {
            $('html, body').show();
        }
    });

    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('#header').addClass('header-scrolled');
        } else {
            $('#header').removeClass('header-scrolled');
        }
    })
    activateFavorites();
    if ($('.chat-nav-notif')[0]) {
        setInterval(updateChatNav, 1000);
    }
    if ($('.resp-nav-notif')[0]) {
        setInterval(updateRespNav, 5000);
    }
});
