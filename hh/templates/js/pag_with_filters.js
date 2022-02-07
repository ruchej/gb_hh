function reloadSelect() {
    if (document.getElementById('default-select')) {
        $('select').niceSelect();
    }
}

function onPaginationFinished() {
    reloadSelect();
}

function initEndlessPagination() {
    $.endlessPaginate({
        paginateOnScroll: true,
        onCompleted: onPaginationFinished
    });
}

function cityAjax(event) {
    let link = event.target.href ?? event.target.parentNode.href;
    let data = $('.search-input-ajax').serialize() ?? {};

    $.ajax({
        url: link,
        data,
        success: (data) => {
            if (data.hasOwnProperty('result')) {
                $('.data-ajax').html(data.result);
                reloadSelect();
                initEndlessPagination();
            }
        },
        error: (e) => {
            console.error(eval(e))
        }
    });

    event.preventDefault();
}

function searchAjax(link) {
    $.ajax({
        url: link,
        data: $('.search-input-ajax').serialize(),
        success: (data) => {
            if (data.hasOwnProperty('result')) {
                $('.data-ajax').html(data.result);
                reloadSelect();
                initEndlessPagination();
            }
        },
        error: (e) => {
            console.error(eval(e))
        }
    });
}

function searchSubmit(event) {
    let $form = $(this)
    let link = $form.attr('action');
    event.preventDefault();
    searchAjax(link);
}

function searchClear(event) {
    let link = event.target.href ?? event.target.parentNode.href;
    event.preventDefault();
    $('.search-input-ajax').val('')
    searchAjax(link);
}

window.onload = () => {
    $('.search-cities-ajax').on('click', 'a', cityAjax);
    $('.ajax-search').submit(searchSubmit);
    // Too laggy
    // $('.search-input-ajax').on('input', searchSubmit);
    $('.clear-link').on('click', searchClear);
    initEndlessPagination();
}
