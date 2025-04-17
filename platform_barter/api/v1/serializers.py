from django.contrib.auth import get_user_model
from rest_framework import serializers

from ads.models import Ad, Category, Condition, ExchangeProposal


User = get_user_model()


class AdSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""

    created_at = serializers.DateField(format="%Y-%m-%d", required=False)
    user = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )

    class Meta:
        model = Ad
        fields = (
            'id',
            'user',
            'title',
            'descriptions',
            'category',
            'condition',
            'image',
            'created_at'
        )


class ProposalSerializers(serializers.ModelSerializer):
    """Сериализатор для предложений."""

    ad_sender = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())
    status = serializers.ChoiceField(
        required=False,
        choices=ExchangeProposal.StatusChoices.choices
    )
    created_at = serializers.DateField(format="%Y-%m-%d", required=False)
    ad_receiver = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = ExchangeProposal
        fields = (
            'id',
            'ad_sender',
            'ad_receiver',
            'comment',
            'status',
            'created_at'
        )

    def create(self, validated_data):
        if ExchangeProposal.objects.filter(
            ad_sender=validated_data['ad_sender'],
            ad_receiver=validated_data['ad_receiver']
        ).exists():
            error = "Такое предложение уже существует"
            raise serializers.ValidationError(error)
        return super().create(validated_data)

    def validate(self, data):
        if data['ad_sender'].user.id == data['ad_receiver'].id:
            error = "Нельзя обменивать объявление само на себя"
            raise serializers.ValidationError(error)
        if self.instance and self.context['request'].method == 'PATCH':
            allowed_fields = {'status'}
            if set(data.keys()) - allowed_fields:
                raise serializers.ValidationError(
                    "При PATCH-запросе можно изменять только поле status"
                )
        return data


class CategorySerializers(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'descriptions',
            'slug',
        )


class ConditionSerializers(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Condition
        fields = (
            'id',
            'title',
            'descriptions',
        )
