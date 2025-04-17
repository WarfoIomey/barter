from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from .serializers import (
    AdSerializer,
    CategorySerializers,
    ConditionSerializers,
    ProposalSerializers
)
from .permissions import (
    IsAdminOrReadOnly,
    IsChangeAuthor,
    IsChangeAuthorProposal
)
from .filters import AdFilter, ProposalFilter
from ads.models import Ad, Category, Condition, ExchangeProposal
from ads.utils import get_sent_proposals, get_received_proposals


User = get_user_model()


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения списка категорий."""

    serializer_class = CategorySerializers
    queryset = Category.objects.all()
    http_method_names = ['get',]
    permission_classes = (IsAdminOrReadOnly,)


class ConditionViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения списка состояний."""

    serializer_class = ConditionSerializers
    queryset = Condition.objects.all()
    http_method_names = ['get',]
    permission_classes = (IsAdminOrReadOnly,)


class SenderProposalViewSet(viewsets.ModelViewSet):
    """Вьюсет для реализации CRUD операций над отправленными предложениями."""

    serializer_class = ProposalSerializers
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsChangeAuthorProposal,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProposalFilter

    def get_queryset(self):
        """Получение всех отправленных предложений."""
        proposal = get_sent_proposals(self.request.user)
        return proposal

    def perform_create(self, serializer):
        serializer.save(
            status=ExchangeProposal.StatusChoices.AWAITING,
        )


class ReceiverProposalViewSet(viewsets.ModelViewSet):
    """Вьюсет для получение и изменение всех полученных предложений."""

    serializer_class = ProposalSerializers
    http_method_names = ['get', 'patch']
    permission_classes = (IsChangeAuthorProposal,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProposalFilter

    def get_queryset(self):
        proposal = get_received_proposals(self.request.user)
        return proposal

    def partial_update(self, request, *args, **kwargs):
        allowed_field = 'status'
        if set(request.data.keys()) != {allowed_field}:
            raise ValidationError('Можно менять только'
                                  f'одно поле {allowed_field}.')
        return super().partial_update(request, *args, **kwargs)


class AdViewSet(viewsets.ModelViewSet):
    """Вьюсет для реализации CRUD операций над объявлениями."""

    serializer_class = AdSerializer
    queryset = Ad.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsChangeAuthor,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
        )
