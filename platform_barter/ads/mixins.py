from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse

from .models import Ad
from .forms import AdForm


class OnlyAuthorMixin(UserPassesTestMixin):

    def handle_no_permission(self):
        return redirect('ads:ad_detail', post_id=self.kwargs['ad_id'])

    def test_func(self):
        object = self.get_object()
        return object.user == self.request.user


class AdEditMixin(OnlyAuthorMixin):
    model = Ad
    template_name = 'ads/create.html'
    pk_url_kwarg = 'ad_id'
