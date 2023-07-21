import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from config import settings
from main.forms import MessageForm, MailingForm, ClientForm, BlogForm
from main.models import Message, Mailing, LogiMail, Client, Blog


class IndexView(generic.View):
    # главная страница
    def get(self, request):

        count_mailing = Message.objects.all().count()
        count_mailing_active = Mailing.objects.filter(is_active=True).count()
        count_unique_client = Client.objects.all().distinct('email').count()
        blog_random = []
        count_blog = Blog.objects.all().count()

        while len(blog_random) < 3:
            pk_for_random = random.randint(1, count_blog)
            if Blog.objects.get(pk=pk_for_random) in blog_random and not Blog.is_public:
                continue
            blog_list = Blog.objects.get(pk=pk_for_random)
            if blog_list:
                blog_random.append(blog_list)

        context = {
            'count_mailing': count_mailing,
            'count_mailing_active': count_mailing_active,
            'count_unique_client': count_unique_client,
            'blog_random': blog_random,
            'title': 'Главная'
        }
        return render(request, 'main/index.html', context)


class MessageListView(LoginRequiredMixin, generic.ListView):
    # список сообщений
    model = Message

    def get_object(self, queryset=None):
        # вывод сообщений для создателя и менеджера
        self.object = super().get_object(queryset)
        if self.object.creator != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class MessageDetailView(LoginRequiredMixin, generic.DetailView):
    # отображение сообщения
    model = Message

    def get_object(self, queryset=None):
        # вывод сообщения для создателя и менеджера
        self.object = super().get_object(queryset)
        if self.object.creator != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class MessageCreateView(generic.CreateView):
    # создание сообщения
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:message_list')

    def get_context_data(self, **kwargs):
        # добавление указания условий рассылки
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Message, Mailing, form=MailingForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = SubjectFormset(self.request.POST)
        else:
            context_data['formset'] = SubjectFormset()

        return context_data

    def form_valid(self, form):
        # сохранение формсета с новыми данными
        formset = self.get_context_data()['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    # def get_object(self, queryset=None):
    #     # ограничение прав
    #     self.object = super().get_object(queryset)
    #     if self.object.creator != self.request.user and not self.request.user.is_staff:
    #         raise Http404
    #     return self.object


class MessageUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:message_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Message, Mailing, form=MailingForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = SubjectFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = SubjectFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        with transaction.atomic():
            if form.is_valid():
                self.object = form.save()
                if formset.is_valid():
                    formset.instance = self.object
                    formset.save()

        return super().form_valid(form)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator != self.request.user:
            raise Http404
        return self.object


class MessageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Message
    success_url = reverse_lazy('main:home')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator != self.request.user:
            raise Http404
        return self.object


class MailingListView(generic.ListView):
    model = Mailing


class LogiListView(generic.ListView):
    model = LogiMail


class ClientListView(generic.ListView):
    model = Client


class ClientDetailView(generic.DetailView):
    model = Client

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class ClientCreateView(generic.CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:client_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Message, Mailing, form=MailingForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = SubjectFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = SubjectFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        with transaction.atomic():
            if form.is_valid():
                self.object = form.save()
                if formset.is_valid():
                    formset.instance = self.object
                    formset.save()

        return super().form_valid(form)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator != self.request.user:
            raise Http404
        return self.object


class ClientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Client
    success_url = reverse_lazy('main:client_list')


class ClientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Client
    form_class = MessageForm
    success_url = reverse_lazy('main:client_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Client, Mailing, form=MailingForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = SubjectFormset(self.request.POST)
        else:
            context_data['formset'] = SubjectFormset()

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class BlogListView(generic.ListView):
    model = Blog


class BlogDetailView(generic.DetailView):
    model = Blog

    def get_object(self, queryset=None):
        blog = super().get_object(queryset=queryset)
        blog.num_views += 1
        blog.save()
        return blog


class BlogCreateView(generic.CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('main:blog_list')


class BlogUpdateView(generic.UpdateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('main:blog_list')


class BlogDeleteView(generic.DeleteView):
    model = Blog
    success_url = reverse_lazy('main:blog_list')


