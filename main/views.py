from django.core.cache import cache
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from config import settings
from main.forms import MessageForm, MailingForm
from main.models import Message, Mailing, LogiMail


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


class MessageDetailView(generic.DetailView):
    model = Message


class MessageCreateView(generic.CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:home')

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


class MessageUpdateView(generic.UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:message_item')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Message, Mailing, form=MailingForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = SubjectFormset(self.request.POST)
        else:
            context_data['formset'] = SubjectFormset()

        return context_data

    # def form_valid(self, form):
    #     formset = self.get_context_data()['formset']
    #     self.object = form.save()
    #
    #     if formset.is_valid():
    #         formset.instance = self.object
    #         formset.save()
    #
    #     return super().form_valid(form)


class MailingListView(generic.ListView):
    model = Mailing


class LogiListView(generic.ListView):
    model = LogiMail
