import django_filters

from ads.models import Ad, ExchangeProposal


class AdFilter(django_filters.FilterSet):
    """Фильтр для произведений."""

    title = django_filters.CharFilter(
        field_name='genre',
        lookup_expr='icontains'
    )
    descriptions = django_filters.CharFilter(
        field_name='descriptions',
        lookup_expr='icontains'
    )
    category = django_filters.CharFilter(
        field_name='category__title',
        lookup_expr='icontains'
    )
    condition = django_filters.CharFilter(
        field_name='condition__title',
        lookup_expr='icontains'
    )

    class Meta:
        model = Ad
        fields = ('title', 'descriptions', 'category', 'condition')


class ProposalFilter(django_filters.FilterSet):
    """Фильтр для предложений."""

    ad_sender = django_filters.CharFilter(
        field_name='ad_sender__title',
        lookup_expr='icontains'
    )
    ad_receiver = django_filters.CharFilter(
        field_name='ad_receiver__username',
        lookup_expr='icontains'
    )
    status = django_filters.ChoiceFilter(
        choices=ExchangeProposal.StatusChoices.choices
    )

    class Meta:
        model = ExchangeProposal
        fields = ('ad_sender', 'ad_receiver', 'status')
