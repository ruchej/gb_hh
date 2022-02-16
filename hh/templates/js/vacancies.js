function selectStatus(vacancyId) {
    $(`.select-ajax-${vacancyId} .vacancy-status li`).click(function(e) {
        let link = $(this).attr('data-value');
        event.preventDefault();
        if (link === '#') return;
        $.ajax({
            url: $(this).attr('data-value'),
            success: (data) => {
                if (data.hasOwnProperty('result')) {
                    $(`.edit-ajax-${vacancyId}`).html(data.result);
                    reloadSelect();
                    selectStatus(vacancyId);
                }
            },
        })
    });
}

function setStatusHandler() {
    $('.vacancy-status li').click(function(event) {
        const regex = /status\/(\d+)\//;
        let link = $(this).attr('data-value');
        let vacancyId = regex.exec(link)[1];
        event.preventDefault();
        if (link === '#') return;
        $.ajax({
            url: $(this).attr('data-value'),
            success: (data) => {
                if (data.hasOwnProperty('result')) {
                    $(`.edit-ajax-${vacancyId}`).html(data.result);
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
