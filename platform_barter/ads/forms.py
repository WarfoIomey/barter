from django import forms
from django.contrib.auth import get_user_model
from dal import autocomplete

from .models import Ad, Category, Condition, ExchangeProposal

User = get_user_model()


class AdForm(forms.ModelForm):
    """Форма для объявлений."""

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Here goes the title"
            }
        )
    )
    descriptions = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Here goes the title"
            }
        )
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label='Выберите категорию',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    condition = forms.ModelChoiceField(
        queryset=Condition.objects.all(),
        empty_label='Выберите состояние',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    created_at = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            },
            format='%Y-%m-%d',
        ),
        required=False,
    )

    class Meta:
        model = Ad
        fields = (
            'title',
            'descriptions',
            'category',
            'condition',
            'image',
            'created_at',
        )


class ExchangeProposalForm(forms.ModelForm):
    """Форма для предложений."""

    ad_sender = forms.ModelChoiceField(
        queryset=Ad.objects.all(),
        empty_label='Выберите объявления',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ad_receiver = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='user-autocomplete',
            attrs={'class': 'form-control'}
        ),
        label='Получатель'
    )
    status = forms.ChoiceField(
        choices=ExchangeProposal.StatusChoices.choices,
        initial=ExchangeProposal.StatusChoices.AWAITING,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )
    created_at = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            },
            format='%Y-%m-%d',
        ),
        required=False,
    )

    class Meta:
        model = ExchangeProposal
        fields = (
            'ad_sender',
            'ad_receiver',
            'comment',
            'status',
            'created_at'
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

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )
