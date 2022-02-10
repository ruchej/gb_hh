from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView

from .models import Chat, Contact
from accounts.models import UserStatus, JobSeeker, Employer

User = get_user_model()


class ChatListView(ListView, LoginRequiredMixin):
    model = Chat
    extra_context = {'title': 'Чат'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ChatListView, self).get_context_data(object_list=object_list, **kwargs)
        last_messages, employers, jobseekers, last_timestamps = [], [], [], []
        for chat in context['chat_list']:
            if self.request.user.status == UserStatus.EMPLOYER:
                contact = chat.participants.all()[1]
                jobseekers.append(JobSeeker.objects.get(user=contact.user))
            elif self.request.user.status == UserStatus.JOBSEEKER:
                contact = chat.participants.all()[0]
                employers.append(Employer.objects.get(user=contact.user))
            last_message = chat.messages.all().last()
            last_message_text = get_last_message_text(self.request, last_message.contact.user, last_message.content)
            last_messages.append(last_message_text)
            last_timestamps.append(last_message.timestamp)
            # last_contact.append(last_message.contact.user)
        context['chat_contacts'] = list(zip(
            context['chat_list'],
            jobseekers if jobseekers else employers,
            last_messages,
            last_timestamps
        ))
        # if self.request.user.status == UserStatus.EMPLOYER:
        #     jobseekers = []
        #     for chat in context['chat_list']:
        #         contact = chat.participants.all()[1]
        #         jobseekers.append(JobSeeker.objects.get(user=contact.user))
        #         last_messages.append(chat.messages.all().last())
        #     context['chat_jobseekers'] = list(zip(context['chat_list'], jobseekers, last_messages))
        # elif self.request.user.status == UserStatus.JOBSEEKER:
        #     employers = []
        #     for chat in context['chat_list']:
        #         contact = chat.participants.all()[0]
        #         employers.append(Employer.objects.get(user=contact.user))
        #         last_messages.append(chat.messages.all().last())
        #     context['chat_employers'] = list(zip(context['chat_list'], employers, last_messages))
        return context

    def get_queryset(self):
        queryset = Chat.objects.all()
        if Contact.objects.filter(user=self.request.user).exists():
            contact = Contact.objects.get(user=self.request.user)
            queryset = contact.chats.all()
        return queryset


class ChatCreateView(TemplateView, LoginRequiredMixin):
    extra_context = {'title': 'Начните Чат'}
    template_name = 'chat/chat_create.html'


def create_chat(request, user_id):
    chat = Chat()
    chat.save()
    contact_employer = Contact.objects.get(user=request.user)
    contact_jobseeker = Contact.objects.get(user__id=user_id)
    chat.participants.add(contact_employer)
    chat.participants.add(contact_jobseeker)
    chat.save()
    return redirect('chat:list')


def open_chat(request, chat_id):
    if request.is_ajax():
        chat = Chat.objects.get(id=chat_id)
        context = {}
        context['chat'] = chat
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
    return f'{sender}: {text[:40] + "..." if len(text) > 40 else text}'


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


def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-timestamp').all()[:10]


def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Contact, user=user)


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)
