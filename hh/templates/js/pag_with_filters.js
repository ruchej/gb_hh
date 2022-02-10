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

function searchAjax(link) {
    $.ajax({
        url: link,
        data: $('#search-form').serialize(),
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
    let $form = $('#search-form');
    let link = $form.attr('action');
    event.preventDefault();
    searchAjax(link);
}

function cityAjax(event) {
    let link = event.target.href ?? event.target.parentNode.href;
    let cityId = link.split('city_id=')[1];
    $('.search-cities-ajax .search-selected').removeClass('search-selected');
    $(this).closest('li').addClass('search-selected');
    $('#city-id-input-ajax').val(cityId);
    searchSubmit(event);
}

function vacanciesAjax(event) {
    let link = event.target.href ?? event.target.parentNode.href;
    let vacId = link.split('vac_id=')[1];
    $('.search-vacancies-ajax .search-selected').removeClass('search-selected');
    $(this).closest('li').addClass('search-selected');
    $('#vac-id-input-ajax').val(vacId);
    searchSubmit(event);
}

function searchClear(event) {
    let link = event.target.href ?? event.target.parentNode.href;
    event.preventDefault();
    $('.search-input-ajax').val('')
    searchAjax(link);
}

window.onload = () => {
    $('.search-cities-ajax').on('click', 'a', cityAjax);
    $('.search-vacancies-ajax').on('click', 'a', vacanciesAjax);
    $('.ajax-search').submit(searchSubmit);
    // Too laggy
    // $('.search-input-ajax').on('input', searchSubmit);
    $('.clear-link').on('click', searchClear);
    initEndlessPagination();
}
