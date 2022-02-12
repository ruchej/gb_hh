class Chat {
    constructor(chatId) {
        this.chatId = chatId;
        this.chatClass = `chat-${chatId}`
        this.socket = this.establishConnection(chatId);
        this.setHandlers();
    }

    establishConnection(chatId) {
        return new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + chatId
            + '/'
        );
    }

    loadChatAjax(msgData, e) {
        $.ajax({
            url: `receive/${this.chatId}/`,
            data: msgData,
            success: (data) => {
                if (data.hasOwnProperty('result')) {
                    // let message = `${data.sender}: ${msgData.message.content}`

                    // $('#search-form').submit();

                    // if (!$(`.${this.chatClass}-contact`).hasClass('active_chat')) {
                    //     $(`.${this.chatClass}-alert`).addClass('alert-danger');
                    // }

                    $(`.${this.chatClass}-last`).text(data.message);
                    $(`.${this.chatClass}-date`).replaceWith(data.timestamp);

                    $(`.${this.chatClass}-alert`).prependTo($('.contacts-ajax'));

                    $(`.${this.chatClass}`).append(data.result);
                    $(`.${this.chatClass}`).scrollTop($(`.${this.chatClass}`)[0].scrollHeight);

                    // let container = findClassInParents('chat_list', event.target);
                    // let alertContainer = findClassInParents('alert', container);
                    // alertContainer.classList.remove('alert-danger');
                    // container.classList.add('active_chat');
                }
            },
            error: (e) => {
                console.error(eval(e))
            }
        });
    }

    setHandlers() {
        this.socket.onmessage = (e) => {
            const msgData = JSON.parse(e.data);
            if ($(`.${this.chatClass}-contact`).hasClass('active_chat')) {
                this.readNotification();
            } else {
                $(`.${this.chatClass}-alert`).addClass('alert-danger');
            }
            this.loadChatAjax(msgData, e);
        };
        this.socket.onclose = function (e) {
            console.error('Chat socket closed unexpectedly');
        };
    }

    sendMessage() {
        const messageInputDom = document.querySelector('.write_msg');
        const message = messageInputDom.value;
        this.socket.send(JSON.stringify({
            'command': 'new_message',
            'chatId': this.chatId,
            'from': JSON.parse(document.getElementById('sender').textContent),
            'message': message
        }));
        messageInputDom.value = '';
    }

    readNotification() {
        $.ajax({
            url: `notif/read/${this.chatId}/`
        })
    }
}

let chats = {};

function updateActive() {
    let activeChat = document.getElementById('chat-id');
    if (activeChat) {
        let activeChatId = JSON.parse(activeChat.textContent);
        $(`.chat-${activeChatId}-contact`).addClass('active_chat');
    }
}

function findClassInParents(cls, element) {
    if (element.classList.contains(cls)) return element;
    return findClassInParents(cls, element.parentElement);
}

function loadChat(link) {
    $.ajax({
        url: link,
        success: (data) => {
            if (data.hasOwnProperty('result')) {
                $('.chat-ajax').html(data.result);
                let chatId = data.chatId;
                $('.msg_history').scrollTop($('.msg_history')[0].scrollHeight);
                $('.msg_send_btn').click((event) => {
                    event.preventDefault();
                    chats[chatId].sendMessage()
                })
                $(`chat-${chatId}-submit`).submit((event) => {
                    event.preventDefault();
                    chats[chatId].sendMessage()
                })
            }
        },
        error: (e) => {
            console.error(eval(e))
        }
    });
}

function searchContact(event) {
    let $form = $('#search-form');
    let link = $form.attr('action');
    event.preventDefault();
    $.ajax({
        url: link,
        data: $('#search-form').serialize(),
        success: (data) => {
            if (data.hasOwnProperty('result')) {
                $('.contacts-ajax').html(data.result);
                ajaxReloadHandlers();
                updateActive();
            }
        },
        error: (e) => {
            console.error(eval(e))
        }
    });
}

function ajaxReloadHandlers() {
    $('.chat_list')
        .click((event) => {
            event.preventDefault();
            $('.active_chat').removeClass('active_chat');
            let container = findClassInParents('chat_list', event.target);
            let alertContainer = findClassInParents('alert', container);
            alertContainer.classList.remove('alert-danger');
            container.classList.add('active_chat');
            loadChat(container.parentElement.href);
        })
}

window.onload = () => {
    ajaxReloadHandlers();
    $('#search-form').submit((event) => {
        searchContact(event);
        $('.search-clear').show();
    });
    $('.search-clear').click((event) => {
        $('.search-bar').val('');
        searchContact(event);
        $('.search-clear').hide();
    });
    let chatIds = $('.chat-link').map(function () {
        const regex = /\/open\/(\d+)\//;
        return regex.exec(this.href)[1]
    }).get();
    for (const chatId of chatIds) {
        chats[chatId] = new Chat(chatId);
    }
    // .mouseenter((event) => {
    //     findChat(event.target).classList.add('active_chat');
    // })
    // .mouseleave((event) => {
    //     findChat(event.target).classList.remove('active_chat');
    // })
}
