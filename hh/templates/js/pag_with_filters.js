function onPaginationFinished() {
    reloadSelect();
    activateFavorites();
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
                activateFavorites();
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

function showMoreCities(event) {
    event.preventDefault();
    $('.search-cities-ajax li:gt(3)').show();
    $('.show-more-cities').hide();
}

function vacanciesAjax(event) {
    let link = event.target.href ?? event.target.parentNode.href;
    let vacId = link.split('vac_id=')[1];
    $('.search-vacancies-ajax .search-selected').removeClass('search-selected');
    $(this).closest('li').addClass('search-selected');
    $('#vac-id-input-ajax').val(vacId);
    searchSubmit(event);
}

function showMoreVacancies(event) {
    event.preventDefault();
    $('.search-vacancies-ajax li:gt(3)').show();
    $('.show-more-vacancies').hide();
}

function searchClear(event) {
    let link = event.target.href ?? event.target.parentNode.href;
    event.preventDefault();
    $('.search-input-ajax').val('')
    searchAjax(link);
}

function searchHashtag(event) {
    event.preventDefault();
    const regex = /\/\?search=([^\/]+)/;
    let link = $(this).attr('href');
    let text = regex.exec(link)[1];
    $('.search-input-ajax').val(text);
    searchAjax(link);
}

window.onload = () => {
    $('.search-cities-ajax').on('click', 'a', cityAjax);
    $('.search-vacancies-ajax').on('click', 'a', vacanciesAjax);
    $('.ajax-search').submit(searchSubmit);
    $('.show-more-cities').click(showMoreCities);
    $('.show-more-vacancies').click(showMoreVacancies);
    $('.hashtag').click(searchHashtag);
    // Too laggy
    // $('.search-input-ajax').on('input', searchSubmit);
    $('.clear-link').on('click', searchClear);
    initEndlessPagination();
}
