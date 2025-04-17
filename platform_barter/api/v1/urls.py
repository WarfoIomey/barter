from django.urls import include, path
from rest_framework import routers

from .views import (
    AdViewSet,
    CategoryViewSet,
    ConditionViewSet,
    ReceiverProposalViewSet,
    SenderProposalViewSet,
)


app_name = 'v1'

router = routers.DefaultRouter()


router.register('ads', AdViewSet, basename='ads_api')
router.register('category', CategoryViewSet, basename='category_api')
router.register('conditions', ConditionViewSet, basename='condition_api')
router.register(
    'sender-proposal',
    SenderProposalViewSet,
    basename='sender_proposal_api'
)
router.register(
    'receiver-proposal',
    ReceiverProposalViewSet,
    basename='receiver_proposal_api'
)

urlpatterns = [
    path('', include(router.urls)),
]