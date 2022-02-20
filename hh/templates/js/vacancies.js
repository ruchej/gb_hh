function selectStatus(vacancyId) {
    $(`.select-ajax-${vacancyId} .vacancy-status li`).click(function(event) {
        const statusRegex = /status\/\d+\/(\w+)\//;
        let link = $(this).attr('data-value');
        let newStatus = statusRegex.exec(link)[1];
        event.preventDefault();
        if (link === '#') return;
        $.ajax({
            url: link,
            success: (data) => {
                if (data.hasOwnProperty('result')) {
                    $(`.edit-ajax-${vacancyId}`).html(data.result);
                    $(`.vacancy-${vacancyId}-card`).prependTo($(`#${newStatus} .card-body`));
                    reloadSelect();
                    selectStatus(vacancyId);
                }
            },
        })
    });
}

function setStatusHandler() {
    $('.vacancy-status li').click(function(event) {
        const vacRegex = /status\/(\d+)\//;
        const statusRegex = /status\/\d+\/(\w+)\//;
        let link = $(this).attr('data-value');
        let vacancyId = vacRegex.exec(link)[1];
        let newStatus = statusRegex.exec(link)[1];
        event.preventDefault();
        if (link === '#') return;
        $.ajax({
            url: link,
            success: (data) => {
                if (data.hasOwnProperty('result')) {
                    $(`.edit-ajax-${vacancyId}`).html(data.result);
                    $(`.vacancy-${vacancyId}-card`).prependTo($(`#${newStatus} .card-body`));
                    reloadSelect();
                    selectStatus(vacancyId);
                }
            },
        })
    });
}

$(document).ready(function () {
    setStatusHandler();
});
