from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from dal import autocomplete

from .models import Ad
from .forms import AdForm
from .utils import get_ads
from .mixins import AdEditMixin


POSTS_PER_PAGE = 5

User = get_user_model()


class AdListView(ListView):
    """Получение всех объявлений."""

    model = Ad
    template_name = 'ads/index.html'
    paginate_by = POSTS_PER_PAGE

    def get_queryset(self):
        return get_ads()


class AdDetailView(DetailView):
    """Просмотр объявления"""

    model = Ad
    template_name = 'ads/detail.html'
    pk_url_kwarg = 'ad_id'


class AdUpdateView(AdEditMixin, UpdateView):
    """Редактирование объявления."""
    form_class = AdForm

    def get_success_url(self):
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


class UserAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = User.objects.all()
        if self.q:
            qs = qs.filter(username__icontains=self.q)
        return qs
 

class ProfileDetailView(ListView):
    """Обзор профиля"""

    # model = Post
    # paginate_by = POSTS_PER_PAGE
    # template_name = 'blog/profile.html'
    # user = None

    # def get_queryset(self):
    #     self.user = get_object_or_404(User, username=self.kwargs['username'])
    #     return Post.objects.select_related(
    #         'location', 'author', 'category'
    #     ).filter(author=self.user)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['profile'] = self.user
    #     return context
