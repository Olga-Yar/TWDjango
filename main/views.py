from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from config import settings
from main.forms import MessageForm, MailingForm, ClientForm
from main.models import Message, Mailing, LogiMail, Client


class IndexView(generic.View):
    def get(self, request):

        if settings.CACHES_ENABLE:
            key = 'message_list'
            message_list = cache.get(key)
            if message_list is None:
                message_list = Message.objects.all()
                cache.set(key, message_list)
        else:
            message_list = Message.objects.all()

        context = {
            'message_list': message_list,
            'title': 'Главная'
        }
        return render(request, 'main/index.html', context)


class MessageListView(LoginRequiredMixin, generic.ListView):
    model = Message

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class MessageDetailView(LoginRequiredMixin, generic.DetailView):
    model = Message

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class MessageCreateView(generic.CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:message_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Message, Mailing, form=MailingForm, extra=1)
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

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


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

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


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

