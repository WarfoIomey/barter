from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

from .models import Ad, ExchangeProposal


class OnlyAuthorAdMixin(UserPassesTestMixin):
    """Миксин для проверки авторства объявления."""

    def handle_no_permission(self):
        return redirect('ads:ad_detail', ad_id=self.kwargs['ad_id'])

    def test_func(self):
        object = self.get_object()
        return object.user == self.request.user


class OnlyAuthorProposalMixin(UserPassesTestMixin):
    """Миксин для проверки авторства предложения."""

    def handle_no_permission(self):
        return redirect('ads:profile', username=self.request.user.username)


class AdEditMixin(OnlyAuthorAdMixin):
    """Миксин для редактирования объявления."""

    model = Ad
    template_name = 'ads/crud_ad.html'
    pk_url_kwarg = 'ad_id'


class ProposalEditMixin(OnlyAuthorProposalMixin):
    """Миксин для редактирования предложения."""

    model = ExchangeProposal
    template_name = 'ads/crud_proposal.html'
    pk_url_kwarg = 'proposal_id'
