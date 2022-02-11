from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView

from .models import Chat, Contact, Message
from accounts.models import UserStatus, JobSeeker, Employer
from resumes.models import Resume
from recruiting.models import Response

User = get_user_model()


class ChatListView(ListView, LoginRequiredMixin):
    model = Chat
    extra_context = {'title': 'Чат'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ChatListView, self).get_context_data(object_list=object_list, **kwargs)
        employers, jobseekers = [], []
        resumes, responses = [], []
        last_messages, last_timestamps = [], []

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
            if chat.resume:
                responses.append(None)
                resumes.append(chat.resume)
            elif chat.response:
                responses.append(chat.response)
                resumes.append(chat.response.resume)
        context['chat_contacts'] = list(zip(
            context['chat_list'],
            jobseekers if jobseekers else employers,
            resumes,
            responses,
            last_messages,
            last_timestamps
        ))
        return context

    def get_queryset(self):
        queryset = Chat.objects.all()
        if Contact.objects.filter(user=self.request.user).exists():
            contact = Contact.objects.get(user=self.request.user)
            queryset = contact.chats.all()
        return queryset


class ChatCreateView(TemplateView, LoginRequiredMixin):
    extra_context = {'title': 'Сообщение кандидату'}
    template_name = 'chat/chat_create.html'

    def get_context_data(self, **kwargs):
        context = super(ChatCreateView, self).get_context_data(**kwargs)
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


def create_chat(request, user_id):
    if response_id := request.POST.get('response_id', None):
        response = Response.objects.get(id=response_id)
        chat = Chat(response=response)
    elif resume_id := request.POST.get('resume_id', None):
        resume = Resume.objects.get(id=resume_id)
        chat = Chat(resume=resume)
    else:
        raise Exception('Neither resume, nor response ID was provided')
    chat.save()
    contact_employer = Contact.objects.get(user=request.user)
    contact_jobseeker = Contact.objects.get(user__id=user_id)
    chat.participants.add(contact_employer)
    chat.participants.add(contact_jobseeker)
    message = Message(contact=contact_employer, content=request.POST.get('start_message', ''))
    message.save()
    chat.messages.add(message)
    chat.save()
    return redirect('chat:list')


def open_chat(request, chat_id):
    if request.is_ajax():
        chat = Chat.objects.get(id=chat_id)
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


def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-timestamp').all()[:10]


def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Contact, user=user)


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)
