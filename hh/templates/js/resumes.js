function showMoreJobs(event) {
    event.preventDefault();
    $('.jobs-ajax li:gt(3)').show();
    $('.show-more-jobs').hide();
}

$(document).ready(function () {
    $('.show-more-jobs').click(showMoreJobs);
});
