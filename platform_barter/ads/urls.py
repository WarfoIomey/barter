from django.urls import path, reverse_lazy

from .views import (
    AdListView,
    AdCreateView,
    AdDetailView,
    AdUpdateView,
    AdDeleteView,
    change_proposal_status,
    ProfileDetailView,
    ProfileUpdateView,
    ProposalCreateView,
    ProposalUpdateView,
    ProposalDeleteView,
    UserAutocomplete,
)


app_name = 'ads'

urlpatterns = [
    path(
        '',
        AdListView.as_view(),
        name='index'
    ),
    path(
        'proposal/create/',
        ProposalCreateView.as_view(),
        name='create_proposal'
    ),
    path(
        'proposal/<int:proposal_id>/edit/',
        ProposalUpdateView.as_view(),
        name='edit_proposal'
    ),
    path(
        'proposal/<int:proposal_id>/delete/',
        ProposalDeleteView.as_view(),
        name='delete_proposal'
    ),
    path(
        'proposal/<int:proposal_id>/<str:action>/',
        change_proposal_status,
        name='change_proposal'
    ),
    path(
        'ads/<int:ad_id>',
        AdDetailView.as_view(),
        name='ad_detail'
    ),
    path(
        'ads/create/',
        AdCreateView.as_view(),
        name='create_ad'
    ),
    path(
        'ads/<int:ad_id>/edit/',
        AdUpdateView.as_view(),
        name='edit_ad'
    ),
    path(
        'ads/<int:ad_id>/delete/',
        AdDeleteView.as_view(),
        name='delete_ad'
    ),
    path(
        'user-autocomplete/',
        UserAutocomplete.as_view(),
        name='user-autocomplete'
    ),
    path(
        'profile/<str:username>/',
        ProfileDetailView.as_view(),
        name='profile'
    ),
    path(
        '<int:pk>/edit/',
        ProfileUpdateView.as_view(
            success_url=reverse_lazy('ads:index'),
        ),
        name='edit_profile',
    ),
]
