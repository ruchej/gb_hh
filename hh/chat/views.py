from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView
from django.db.models import Q
from notifications.signals import notify

from .models import Chat, Contact, Message
from accounts.models import UserStatus, JobSeeker, Employer
from resumes.models import Resume
from recruiting.models import Response
from recruiting.views import response_accept, response_reject

User = get_user_model()

NEW_MESSAGE = 'New message'


class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    extra_context = {'title': 'Чат'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ChatListView, self).get_context_data(object_list=object_list, **kwargs)
        update_context_from_chats(self.request, context, context['chat_list'])
        return context

    def get_queryset(self):
        queryset = Chat.objects.all()
        if Contact.objects.filter(user=self.request.user).exists():
            contact = Contact.objects.get(user=self.request.user)
            queryset = contact.chats.all()
        return queryset


class ChatAcceptView(LoginRequiredMixin, TemplateView):
    extra_context = {'title': 'Сообщение кандидату'}
    template_name = 'chat/chat_accept.html'

    def get_context_data(self, **kwargs):
        context = super(ChatAcceptView, self).get_context_data(**kwargs)
        response_id = kwargs.get('response_id', None)
        resume_id = kwargs.get('resume_id', None)
        if response_id:
            context['response'] = Response.objects.get(id=response_id)
            resume = context['response'].resume
        elif resume_id:
            resume = Resume.objects.get(id=resume_id)
            context['resume'] = resume
        else:
            raise Exception('Neither resume, nor response ID was provided')
        context['jobseeker'] = JobSeeker.objects.get(user=resume.user)
        context['responding'] = True
        return context


class ChatRejectView(LoginRequiredMixin, TemplateView):
    extra_context = {'title': 'Сообщение кандидату об отказе'}
    template_name = 'chat/chat_reject.html'

    def get_context_data(self, **kwargs):
        context = super(ChatRejectView, self).get_context_data(**kwargs)
        response_id = kwargs.get('response_id', None)
        if response_id:
            context['response'] = Response.objects.get(id=response_id)
            resume = context['response'].resume
        else:
            raise Exception('Neither resume, nor response ID was provided')
        context['jobseeker'] = JobSeeker.objects.get(user=resume.user)
        context['responding'] = True
        return context


def create_chat_with_msg(request, chat, user_id):
    contact_employer = Contact.objects.get(user=request.user)
    contact_jobseeker = Contact.objects.get(user__id=user_id)
    chat.participants.add(contact_employer)
    chat.participants.add(contact_jobseeker)
    message = Message(contact=contact_employer, content=request.POST.get('start_message', ''))
    message.save()
    chat.messages.add(message)
    chat.save()
    notify.send(contact_employer.user, recipient=contact_jobseeker.user,
                verb=NEW_MESSAGE, target=chat)
    return redirect('chat:list')


def accept_chat(request, user_id):
    if response_id := request.POST.get('response_id', None):
        response = Response.objects.get(id=response_id)
        response_accept(request, response_id)
        resume = response.resume
        chat = Chat(response=response)
    elif resume_id := request.POST.get('resume_id', None):
        resume = Resume.objects.get(id=resume_id)
        chat = Chat(resume=resume)
    else:
        raise Exception('Neither resume, nor response ID was provided')
    resume.accepted_by.add(request.user)
    resume.save()
    chat.save()
    return create_chat_with_msg(request, chat, user_id)


def create_reject_chat(request, user_id):
    if response_id := request.POST.get('response_id', None):
        response = Response.objects.get(id=response_id)
        response_reject(request, response_id)
        chat = Chat(response=response)
        resume = response.resume
    else:
        raise Exception('Neither resume, nor response ID was provided')
    resume.accepted_by.add(request.user)
    resume.save()
    chat.save()
    return create_chat_with_msg(request, chat, user_id)


def get_notifications(request):
    from conf.context_processor import new_messages
    if request.is_ajax():
        return JsonResponse(new_messages(request))


def read_notifications(request, chat_id=None, chat=None):
    if chat_id and not chat:
        chat = Chat.objects.get(id=chat_id)
    for notif in request.user.notifications.unread():
        if notif.verb == NEW_MESSAGE and notif.target == chat:
            notif.mark_as_read()
            notif.save()


def open_chat(request, chat_id):
    if request.is_ajax():
        chat = Chat.objects.get(id=chat_id)

        read_notifications(request, chat=chat)

        if chat.resume:
            jobseeker = JobSeeker.objects.get(user=chat.resume.user)
        elif chat.response:
            jobseeker = JobSeeker.objects.get(user=chat.response.resume.user)
        else:
            raise Exception('Chat without resume or response??')
        context = {}
        context['chat'] = chat
        context['jobseeker'] = jobseeker
        result = render_to_string('chat/snippets/chat.html',
                                  context=context,
                                  request=request)
        return JsonResponse({'result': result, 'chatId': chat.id})
    return redirect('blog:news')


def get_last_message_text(request, user, text):
    if request.user == user:
        sender = 'Вы'
    elif user.status == UserStatus.JOBSEEKER:
        sender = JobSeeker.objects.get(user=user)
        sender = f'{sender.first_name} {sender.last_name}'
    elif user.status == UserStatus.EMPLOYER:
        sender = Employer.objects.get(user=user)
        sender = sender.name
    else:
        sender = 'Неизвестный'
    string = f'{sender}: {text}'
    return f'{string[:40] + "..." if len(string) > 40 else string}'


def receive_message(request, chat_id):
    if request.is_ajax():
        chat = Chat.objects.get(id=chat_id)
        context = {}
        context['message'] = chat.messages.all().last()
        user = User.objects.get(username=request.GET.get('message[author]'))
        content = request.GET.get('message[content]')
        message = get_last_message_text(request, user, content)
        result = render_to_string('chat/snippets/message.html',
                                  context=context,
                                  request=request)
        timestamp = render_to_string('chat/snippets/msg_time.html',
                                     context={'timestamp': context['message'].timestamp},
                                     request=request)
        return JsonResponse({'result': result, 'message': message, 'timestamp': timestamp})


def update_context_from_chats(request, context, chats):
    employers, jobseekers = [], []
    resumes, responses = [], []
    last_messages, last_timestamps = [], []
    notify_present = []

    notifs = [notif for notif in request.user.notifications.unread()
              if notif.verb == NEW_MESSAGE]
    notif_chats = [notif.target for notif in notifs]
    for chat in chats:
        if request.user.status == UserStatus.EMPLOYER:
            contact = chat.participants.all()[1]
            jobseekers.append(JobSeeker.objects.get(user=contact.user))
        elif request.user.status == UserStatus.JOBSEEKER:
            contact = chat.participants.all()[0]
            employers.append(Employer.objects.get(user=contact.user))
        last_message = chat.messages.all().last()
        last_message_text = get_last_message_text(request, last_message.contact.user, last_message.content)
        last_messages.append(last_message_text)
        last_timestamps.append(last_message.timestamp)
        if chat.resume:
            responses.append(None)
            resumes.append(chat.resume)
        elif chat.response:
            responses.append(chat.response)
            resumes.append(chat.response.resume)
        if chat in notif_chats:
            num = notif_chats.index(chat)
            notify_present.append(notifs[num].id)
        else:
            notify_present.append(None)
    pack = list(zip(
        chats,
        jobseekers if jobseekers else employers,
        resumes,
        responses,
        last_messages,
        last_timestamps,
        notify_present
    ))
    context['chat_contacts'] = sorted(pack, key=lambda x: x[5], reverse=True)


def search_contact(request):
    if request.is_ajax():
        name = request.GET.get('contact')
        if name:
            if request.user.status == UserStatus.JOBSEEKER:
                contacts = Employer.objects.filter(name__contains=name)
            elif request.user.status == UserStatus.EMPLOYER:
                contacts = JobSeeker.objects.filter(Q(first_name__contains=name) | Q(last_name__contains=name))
            else:
                raise Exception('Unsupported user')
            usernames = []
            usernames.extend([cont.user.username for cont in contacts])
        else:
            usernames = [request.user.username]
        chats = Chat.objects.filter(participants__user__username__in=usernames)
        user_contact = Contact.objects.get(user=request.user)
        chats = [chat for chat in chats if user_contact in chat.participants.all()]
        context = {}
        update_context_from_chats(request, context, chats)
        result = render_to_string('chat/snippets/contacts.html',
                                  context=context,
                                  request=request)
        return JsonResponse({'result': result})


def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-timestamp').all()[:10]


def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Contact, user=user)


def notify_participants(chat, sender_contact):
    chat_participants = [cont for cont in chat.participants.all()]
    chat_participants.remove(sender_contact)
    for contact in chat_participants:
        notify.send(sender_contact.user, recipient=contact.user,
                    verb=NEW_MESSAGE, target=chat)


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)
