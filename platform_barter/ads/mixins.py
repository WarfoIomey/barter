from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect

from .models import Ad, ExchangeProposal


class OnlyAuthorAdMixin(UserPassesTestMixin):
    """Миксин для проверки авторства объявления."""

    login_url = '/auth/login/'
    redirect_field_name = 'next'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(f'{self.login_url}?next={self.request.path}')
        raise Http404("Страница не найдена")

    def test_func(self):
        object = self.get_object()
        return object.user == self.request.user


class AdEditMixin(OnlyAuthorAdMixin):
    """Миксин для редактирования объявления."""

    model = Ad
    template_name = 'ads/crud_ad.html'
    pk_url_kwarg = 'ad_id'


class ProposalEditMixin(OnlyAuthorAdMixin):
    """Миксин для редактирования предложения."""

    model = ExchangeProposal
    template_name = 'ads/crud_proposal.html'
    pk_url_kwarg = 'proposal_id'
