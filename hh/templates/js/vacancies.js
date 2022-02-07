function reloadSelect() {
    if (document.getElementById("default-select")) {
        $('select').niceSelect();
    }
}

function cityAjax(event) {
    let link = event.target.href ?? event.target.parentNode.href;
    let data = $('.vacancy-search-input').serialize() ?? {};

    $.ajax({
        url: link,
        data,
        success: (data) => {
            if (data.hasOwnProperty('result')) {
                $('.vacancies-ajax').html(data.result);
                reloadSelect();
                $.endlessPaginate({paginateOnScroll: true})
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
        data: $('.vacancy-search-input').serialize(),
        success: (data) => {
            if (data.hasOwnProperty('result')) {
                $('.vacancies-ajax').html(data.result);
                reloadSelect();
                $.endlessPaginate({paginateOnScroll: true})
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
    $('.vacancy-search-input').val('')
    searchAjax(link);
}

function onPaginationFinished() {
    reloadSelect();
}

window.onload = () => {
    $('.city-list').on('click', 'a', cityAjax);
    $('.vacancy-search').submit(searchSubmit);
    // Too laggy
    // $('.vacancy-search-input').on('input', searchSubmit);
    $('.clear-link').on('click', searchClear);
    $.endlessPaginate({paginateOnScroll: true});
}
