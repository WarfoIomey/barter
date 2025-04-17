from django.contrib.auth import get_user_model

from .models import Ad, ExchangeProposal


User = get_user_model()


def get_ads():
    """Получение постов."""
    return Ad.objects.select_related(
        'user', 'category', 'condition'
    ).order_by('-created_at')


def get_sent_proposals(user):
    """Получение отправленых предложений обмена."""
    return ExchangeProposal.objects.select_related(
        'ad_sender', 'ad_receiver'
    ).filter(
        ad_sender__user=user.id
    ).order_by('-created_at', '-status')


def get_received_proposals(user):
    """Получение полученных предложений обмена."""
    return ExchangeProposal.objects.select_related(
        'ad_sender', 'ad_receiver'
    ).filter(
        ad_receiver=user.id
    ).order_by('-created_at', '-status')
