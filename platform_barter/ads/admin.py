from django.contrib import admin

from .models import Ad, Category, Condition, ExchangeProposal


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """Настройка админки для модели Ad."""

    list_display = (
        'user',
        'title',
        'descriptions',
        'category',
        'condition',
    )
    search_fields = ('user', 'title', 'category', 'condition')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка админки для модели Category."""

    list_display = ('title', 'slug')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    """Настройка админки для модели Condition."""

    list_display = ('title',)
    search_fields = ('title',)


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    """Настройка админки для модели ExchangeProposal."""

    list_display = (
        'ad_sender',
        'ad_receiver',
        'status',
    )
    search_fields = ('ad_sender', 'ad_receiver', 'status')
