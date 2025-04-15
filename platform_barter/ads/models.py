from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import ads.constants as constants


User = get_user_model()


class Category(models.Model):
    """Модель категорий."""
    title = models.TextField(
        max_length=constants.NAME_MAX_LENGTH,
        verbose_name='Название категории',
        help_text='Укажите название категории'
    )
    descriptions = models.TextField(
        verbose_name='Описание',
        help_text='Укажите описание'
    )
    slug = models.SlugField(
        max_length=constants.SLUG_MAX_LENGTH,
        unique=True,
        db_index=True,
        verbose_name='Cлаг',
        help_text='Укажите уникальный slug'
    )

    class Meta:
        """
        Метаданные модели Category.

        Атрибуты:
            - verbose_name: Название модели в единственном числе.
            - verbose_name_plural: Название модели во множественном числе.
        """

        ordering = ['id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        """
        Возвращает строковое представление категории.

        Returns:
            str: Название состояние, описание состояния и slug.
        """
        return f'{self.title} - {self.descriptions} - {self.slug} '


class Condition(models.Model):
    """Модель состояний."""
    title = models.TextField(
        max_length=constants.NAME_MAX_LENGTH,
        verbose_name='Название состояния',
        help_text='Укажите название состояния'
    )
    descriptions = models.TextField(
        verbose_name='Описание',
        help_text='Укажите описание'
    )

    class Meta:
        """
        Метаданные модели Condition.

        Атрибуты:
            - verbose_name: Название модели в единственном числе.
            - verbose_name_plural: Название модели во множественном числе.
        """

        ordering = ['id']
        verbose_name = 'Состояние'
        verbose_name_plural = 'Состояния'

    def __str__(self) -> str:
        """
        Возвращает строковое представление состояния.

        Returns:
            str: Название состояние и описание состояния.
        """
        return f'{self.title} - {self.descriptions} '


class Ad(models.Model):
    """Модель объявления."""
    
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Укажите пользователя'
    )
    title = models.TextField(
        max_length=constants.NAME_MAX_LENGTH,
        verbose_name='Название объявления',
        help_text='Укажите название объявления'
    )
    descriptions = models.TextField(
        verbose_name='Описание',
        help_text='Укажите описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        help_text='Укажите категорию'
    )
    condition = models.ForeignKey(
        Condition,
        on_delete=models.CASCADE,
        verbose_name='Состояние',
        help_text='Укажите состояние'
    )
    image = models.ImageField(
        'Фото',
        upload_to='images',
        blank=True
    )
    created_at = models.DateField(
        default=timezone.now,
        help_text='Время создания объявления',
        verbose_name='Дата и время создания',
        editable=True
    )

    class Meta:
        """
        Метаданные модели Ad.

        Атрибуты:
            - verbose_name: Название модели в единственном числе.
            - verbose_name_plural: Название модели во множественном числе.
        """

        ordering = ['id']
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self) -> str:
        """
        Возвращает строковое представление объявления.

        Returns:
            str: Название объявления, название категории, 
                username пользователя создавшего объявление и состояние.
        """
        return (f'{self.title} - {self.category.title} '
                f'- {self.user.username} - {self.condition.title}')


class ExchangeProposal(models.Model):
    """Модель предложений."""

    class StatusChoices(models.TextChoices):
        """
        Перечисление статусов для предложения.
        Используется для выбора статуса предложения.
        """

        AWAITING = 'awaiting', _('Ожидает')
        ACCEPTED = 'accepted', _('Принята')
        CANCELLED = 'cancelled', _('Отклонена')

    ad_sender = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        verbose_name='Объявление',
        help_text='Укажите объявление',
        related_name='proposals'
    )
    ad_receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Получатель',
        help_text='Укажите получателя',
        related_name='proposals'
    )
    comment = models.TextField(
        verbose_name='комментарий',
        help_text='Напишите комментарий к предложению'
    )
    status = models.TextField(
        max_length=constants.STATUS_MAX_LENGTH,
        choices=StatusChoices.choices,
        default=StatusChoices.AWAITING,
        help_text='Укажите статус',
        error_messages={
            'choices': 'Выберите правильный статус'
        },
        verbose_name='Статус предложения'
    )
    created_at = models.DateField(
        default=timezone.now,
        help_text='Время создания предложения',
        verbose_name='Дата и время создания',
        editable=True
    )

    class Meta:
        """
        Метаданные модели ExchangeProposal.

        Атрибуты:
            - verbose_name: Название модели в единственном числе.
            - verbose_name_plural: Название модели во множественном числе.
        """

        constraints = [
            models.UniqueConstraint(
                fields=['ad_sender', 'ad_receiver'],
                name='unique_ad_per_receiver'
            )
        ]
        ordering = ['id']
        verbose_name = 'Предложние'
        verbose_name_plural = 'Предложения'

    def __str__(self) -> str:
        """
        Возвращает строковое представление предложения.

        Returns:
            str: Название объявления и username получателя и статус.
        """
        return (f'{self.ad_sender.title} - {self.ad_receiver.username} '
                f'- {self.status}')
