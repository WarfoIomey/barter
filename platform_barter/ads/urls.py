from django.urls import path
from .views import (
    AdListView,
    AdDetailView,
    AdUpdateView,
    AdDeleteView,
    UserAutocomplete,
    ProfileDetailView
)


app_name = 'ads'

urlpatterns = [
    path(
        '',
        AdListView.as_view(),
        name='index'
    ),
    path(
        'ads/<int:ad_id>',
        AdDetailView.as_view(),
        name='ad_detail'
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
]
