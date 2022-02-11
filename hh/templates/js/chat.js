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

    setHandlers() {
        this.socket.onmessage = (e) =>{
            const msgData = JSON.parse(e.data);
            $.ajax({
                url: `receive/${this.chatId}/`,
                data: msgData,
                success: (data) => {
                    if (data.hasOwnProperty('result')) {
                        // let message = `${data.sender}: ${msgData.message.content}`
                        $(`.${this.chatClass}-last`).text(data.message);
                        $(`.chat_date`).replaceWith(data.timestamp);
                        $(`.${this.chatClass}`).append(data.result);
                        $(`.${this.chatClass}`).scrollTop($(`.${this.chatClass}`)[0].scrollHeight);
                    }
                },
                error: (e) => {
                    console.error(eval(e))
                }
            });
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
}

let chats = {};

function findClassInParents(element) {
    if (element.classList.contains('chat_list')) return element;
    return findClassInParents(element.parentElement);
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

window.onload = () => {
    $('.chat_list')
        .click((event) => {
            event.preventDefault();
            $('.active_chat').removeClass('active_chat');
            let container = findClassInParents(event.target);
            container.classList.add('active_chat');
            loadChat(container.parentElement.href);
        })
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
