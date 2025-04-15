from .models import Ad


def get_ads():
    """Получение постов"""
    return Ad.objects.select_related(
        'user', 'category', 'condition'
    ).order_by('-created_at')
