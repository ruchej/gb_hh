function showMoreJobs(event) {
    event.preventDefault();
    $('.jobs-ajax li:gt(3)').show();
    $('.show-more-jobs').hide();
}

window.onload = () => {
    $('.show-more-jobs').click(showMoreJobs);
}
