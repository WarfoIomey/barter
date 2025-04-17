from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.core.paginator import Paginator
from dal import autocomplete

import ads.constants as constants
from .models import Ad, Category, Condition, ExchangeProposal
from .forms import (
    AdForm,
    ChangeStatusProposalForm,
    ExchangeProposalForm,
    UserForm,
)
from .utils import get_ads, get_sent_proposals, get_received_proposals
from .mixins import AdEditMixin, ProposalEditMixin


User = get_user_model()


class AdListView(ListView):
    """Получение всех объявлений."""

    model = Ad
    template_name = 'ads/index.html'
    paginate_by = constants.PAGINATION_PER_PAGE

    def get_queryset(self):
        """Получение всех объявлений."""
        return get_ads()


class AdCreateView(CreateView):
    """Создание объявления."""

    model = Ad
    template_name = 'ads/crud_ad.html'
    form_class = AdForm

    def form_valid(self, form):
        """Автоподстановка пользователя."""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Перенаправление на основную страницу."""
        return reverse(
            'ads:index',
        )


class AdDetailView(DetailView):
    """Просмотр объявления."""

    model = Ad
    template_name = 'ads/detail.html'
    pk_url_kwarg = 'ad_id'


class AdUpdateView(AdEditMixin, UpdateView):
    """Редактирование объявления."""

    form_class = AdForm

    def get_success_url(self):
        """Перенаправление на страницу просмотра объявления."""
        return reverse(
            'ads:ad_detail',
            kwargs={'ad_id': self.kwargs['ad_id']}
        )


class AdDeleteView(AdEditMixin, DeleteView):
    """Удаление объявления."""

    success_url = reverse_lazy('ads:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad = get_object_or_404(Ad, pk=self.kwargs['ad_id'])
        context['form'] = AdForm(instance=ad)
        return context


class ProposalCreateView(CreateView):
    """Создание предложения."""

    model = ExchangeProposal
    template_name = 'ads/crud_proposal.html'
    form_class = ExchangeProposalForm

    def get_form_kwargs(self):
        """Передача текущего пользователя в форму."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Автоподстановка пользователя."""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Перенаправление на страницу профиля."""
        return reverse(
            'ads:profile',
            kwargs={'username': self.request.user.username}
        )


class ProposalDeleteView(ProposalEditMixin, DeleteView):
    """Удаление предложения."""

    def get_success_url(self):
        """Перенаправление на страницу профиля."""
        return reverse(
            'ads:profile',
            kwargs={'username': self.request.user.username}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proposal = get_object_or_404(
            ExchangeProposal,
            pk=self.kwargs['proposal_id']
        )
        context['form'] = ExchangeProposalForm(instance=proposal)
        return context

    def test_func(self):
        """Проверка на авторство."""
        object = self.get_object()
        return object.ad_sender.user.id == self.request.user.id


class ProposalUpdateView(ProposalEditMixin, UpdateView):
    """Редактирование предложения."""

    form_class = ChangeStatusProposalForm

    def get_success_url(self):
        """Перенаправление на страницу профиля."""
        return reverse(
            'ads:profile',
            kwargs={'username': self.request.user.username}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proposal = get_object_or_404(
            ExchangeProposal,
            pk=self.kwargs['proposal_id']
        )
        context['form'] = ChangeStatusProposalForm(instance=proposal)
        return context

    def test_func(self):
        """Проверка на авторство."""
        object = self.get_object()
        return object.ad_sender.user.id == self.request.user.id


class UserAutocomplete(autocomplete.Select2QuerySetView):
    """Получение пользователей с поиском в Select."""

    def get_queryset(self):
        qs = User.objects.exclude(id=self.request.user.id)
        if self.q:
            qs = qs.filter(username__icontains=self.q)
        return qs


class ProfileDetailView(ListView):
    """Обзор профиля."""

    model = Ad
    paginate_by = constants.PAGINATION_PER_PAGE
    template_name = 'ads/profile.html'
    user = None

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        return Ad.objects.select_related(
            'user', 'category', 'condition'
        ).filter(user=self.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.user
        if self.request.user == self.user:
            search_query = self.request.GET.get('q', '')
            category_id = self.request.GET.get('category')
            condition = self.request.GET.get('condition')
            receiver = self.request.GET.get('receiver')
            sender = self.request.GET.get('sender')
            status_proposal = self.request.GET.get(
                'status_proposal'
            )
            ads = Ad.objects.filter(user=self.user.id)
            proposal_receiver = get_sent_proposals(self.user)
            proposal_sender = get_received_proposals(self.user)
            if search_query:
                ads = ads.filter(
                    Q(title__icontains=search_query) | 
                    Q(descriptions__icontains=search_query)
                )
            if category_id:
                ads = ads.filter(category_id=category_id)
        
            if condition:
                ads = ads.filter(condition=condition)
            if status_proposal:
                proposal_sender = proposal_sender.filter(
                    status=status_proposal
                ).order_by('-created_at', '-status')
                proposal_receiver = proposal_receiver.filter(
                    status=status_proposal
                ).order_by('-created_at', '-status')
            if receiver:
                proposal_receiver = proposal_receiver.filter(
                    ad_receiver=receiver
                ).order_by('-created_at', '-status')
            if sender:
                proposal_sender = proposal_sender.filter(
                    ad_sender__user=sender
                ).order_by('-created_at', '-status')

            paginator_ads = Paginator(ads, constants.PAGINATION_PER_PAGE)
            page_number = self.request.GET.get('page')
            context['page_obj'] = paginator_ads.get_page(page_number)
            paginator_sent = Paginator(
                proposal_receiver,
                constants.PAGINATION_PER_PAGE - 2
            )
            sent_page_number = self.request.GET.get('sent_page')
            context['sent_proposals'] = paginator_sent.get_page(
                sent_page_number
            )
            paginator_received = Paginator(
                proposal_sender,
                constants.PAGINATION_PER_PAGE - 2
            )
            received_page_number = self.request.GET.get('received_page')
            context['received_proposals'] = paginator_received.get_page(
                received_page_number
            )
            context['categories'] = Category.objects.all()
            context['conditions'] = Condition.objects.all()
            context['users'] = User.objects.all()
            context['statuses'] = ['awaiting', 'accepted', 'cancelled']
        else:
            context['check'] = True
        return context


class ProfileUpdateView(UserPassesTestMixin, UpdateView):
    """Изменение профиля."""

    model = User
    template_name = 'ads/user.html'
    form_class = UserForm

    def test_func(self):
        """Проверка на авторство."""
        object = self.get_object()
        return object == self.request.user


def change_proposal_status(request, proposal_id, action):
    """Принятие или отказ от предложения."""
    proposal = get_object_or_404(ExchangeProposal, pk=proposal_id)
    if action == ExchangeProposal.StatusChoices.ACCEPTED:
        proposal.status = ExchangeProposal.StatusChoices.ACCEPTED
    elif action == ExchangeProposal.StatusChoices.CANCELLED:
        proposal.status = ExchangeProposal.StatusChoices.ACCEPTED
    proposal.save()
    return HttpResponseRedirect(
        reverse(
            'ads:profile',
            kwargs={'username': request.user.username}
        )
    )
