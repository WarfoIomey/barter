from django import forms
from django.contrib.auth import get_user_model
from dal import autocomplete

from .models import Ad, Category, Condition, ExchangeProposal

User = get_user_model()


class AdForm(forms.ModelForm):
    """Форма для объявлений."""

    title = forms.CharField(
        label='Название объявления',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Напишите название"
            }
        )
    )
    descriptions = forms.CharField(
        label='Описание объявления',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Напишите описание"
            }
        )
    )
    category = forms.ModelChoiceField(
        label='Категория',
        queryset=Category.objects.all(),
        empty_label='Выберите категорию',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    condition = forms.ModelChoiceField(
        label='Состояние',
        queryset=Condition.objects.all(),
        empty_label='Выберите состояние',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Ad
        fields = (
            'title',
            'descriptions',
            'category',
            'condition',
            'image',
        )


class ExchangeProposalForm(forms.ModelForm):
    """Форма для предложений."""

    ad_sender = forms.ModelChoiceField(
        queryset=Ad.objects.none(),
        empty_label='Выберите объявление',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        label='Объявление'
    )
    ad_receiver = forms.ModelChoiceField(
        queryset=User.objects.none(),
        widget=autocomplete.ModelSelect2(
            url='ads:user-autocomplete',
            attrs={'class': 'form-control'}
        ),
        label='Получатель'
    )

    class Meta:
        model = ExchangeProposal
        fields = (
            'ad_sender',
            'ad_receiver',
            'comment',
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['ad_sender'].queryset = Ad.objects.filter(user=user)
            self.fields['ad_receiver'].queryset = User.objects.exclude(
                id=user.id
            )


class ChangeStatusProposalForm(forms.ModelForm):
    """Форма для изменения статуса предложения."""

    status = forms.ChoiceField(
        choices=ExchangeProposal.StatusChoices.choices,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        label='Статус'
    )

    class Meta:
        model = ExchangeProposal
        fields = (
            'status',
        )


class CategoryForm(forms.ModelForm):
    """Форма для категорий."""

    class Meta:
        model = Category
        fields = ('title', 'descriptions', 'slug')


class ConditionForm(forms.ModelForm):
    """Форма для состояний."""

    class Meta:
        model = Condition
        fields = ('title', 'descriptions')


class UserForm(forms.ModelForm):
    """Форма для пользователя."""
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )
