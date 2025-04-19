import pytest
from django.test.client import Client
from django.conf import settings
from django.urls import reverse

from ads.models import Ad, Category, Condition, ExchangeProposal
import ads.constants as constants


@pytest.fixture
def author(django_user_model):
    """Текущий пользователь."""
    return django_user_model.objects.create(username='User')


@pytest.fixture
def author_client(author):
    """Клиент текущего пользователя."""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def another_author(django_user_model):
    """Другой пользователь."""
    return django_user_model.objects.create(username='Другой')


@pytest.fixture
def another_author_client(another_author):
    """Клиент другого пользователя."""
    client = Client()
    client.force_login(another_author)
    return client


@pytest.fixture
def category():
    """Создание категории."""
    category = Category.objects.create(
        title='Категория',
        descriptions='Описание категории',
        slug='category',
    )
    return category


@pytest.fixture
def condition():
    """Создание состояния."""
    condition = Condition.objects.create(
        title='Б/У',
        descriptions='Описание Б/У',
    )
    return condition


@pytest.fixture
def ad(author, category, condition):
    """Создание объявления."""
    ad = Ad.objects.create(
        user=author,
        title='Название объявления',
        descriptions='Описание объявления',
        category=category,
        condition=condition,
    )
    return ad


@pytest.fixture
def six_ads(author, category, condition) -> None:
    """Создание 6 объявлений."""
    all_ads = [
        Ad(
            title=f'Объявление {index}',
            descriptions='Просто описание.',
            user=author,
            category=category,
            condition=condition,
        )
        for index in range(constants.PAGINATION_PER_PAGE_AD + 1)
    ]
    created_ads = Ad.objects.bulk_create(all_ads)
    return Ad.objects.filter(id__in=[ad.id for ad in created_ads])


@pytest.fixture
def six_ads_another_author(another_author, category, condition) -> None:
    """Создание 6 объявлений."""
    all_ads = [
        Ad(
            title=f'Объявление {index}',
            descriptions='Просто описание.',
            user=another_author,
            category=category,
            condition=condition,
        )
        for index in range(constants.PAGINATION_PER_PAGE_AD + 1)
    ]
    created_ads = Ad.objects.bulk_create(all_ads)
    return Ad.objects.filter(id__in=[ad.id for ad in created_ads])


@pytest.fixture
def ad_another_user(another_author, category, condition):
    """Создание объявления."""
    ad = Ad.objects.create(
        user=another_author,
        title='Название объявления пользователя',
        descriptions='Описание объявления пользователя',
        category=category,
        condition=condition,
    )
    return ad


@pytest.fixture
def proposal(ad, another_author):
    """Создание предложения."""
    proposal = ExchangeProposal.objects.create(
        ad_sender=ad,
        ad_receiver=another_author,
        comment='Тестовый комментарий',
    )
    return proposal


@pytest.fixture
def six_proposals(six_ads, another_author) -> None:
    """Создание 6 предложений."""
    all_proposals = [
        ExchangeProposal(
            ad_sender=ad,
            ad_receiver=another_author,
            comment=f'Тестовый комментарий {ad.id}'
        )
        for ad in six_ads
    ]
    ExchangeProposal.objects.bulk_create(all_proposals)


@pytest.fixture
def six_receiver_proposals(six_ads_another_author, author) -> None:
    """Создание 6 предложений."""
    all_proposals = [
        ExchangeProposal(
            ad_sender=ad,
            ad_receiver=author,
            comment=f'Тестовый комментарий {ad.id}'
        )
        for ad in six_ads_another_author
    ]
    ExchangeProposal.objects.bulk_create(all_proposals)


@pytest.fixture
def proposal_receiver(ad_another_user, author):
    """Создание предложения."""
    proposal = ExchangeProposal.objects.create(
        ad_sender=ad_another_user,
        ad_receiver=author,
        comment='Тестовый комментарий',
    )
    return proposal


@pytest.fixture
def url_reverse_profile(author) -> str:
    """Перенаправления на основную страницу."""
    return reverse(
            'ads:profile',
            args=(author.username,)
        )


@pytest.fixture
def url_reverse_index() -> str:
    """Перенаправления на основную страницу."""
    return reverse('ads:index')


@pytest.fixture
def url_reverse_create_ad() -> str:
    """Ссылка на страницу создания объявления."""
    return reverse('ads:create_ad')


@pytest.fixture
def url_reverse_detail_ad(ad) -> str:
    """Ссылка на страницу просмотра объявления."""
    return reverse('ads:ad_detail', args=(ad.id,))


@pytest.fixture
def url_reverse_edit_ad(ad) -> str:
    """Ссылка на страницу изменения объявления."""
    return reverse('ads:edit_ad', args=(ad.id,))


@pytest.fixture
def url_reverse_delete_ad(ad) -> str:
    """Ссылка на страницу удаления объявления."""
    return reverse('ads:delete_ad', args=(ad.id,))


@pytest.fixture
def url_reverse_create_proposal() -> str:
    """Ссылка на страницу создания предложения."""
    return reverse('ads:create_proposal')


@pytest.fixture
def url_reverse_edit_proposal(proposal) -> str:
    """Ссылка на страницу изменения предложения."""
    return reverse('ads:edit_proposal', args=(proposal.id,))


@pytest.fixture
def url_reverse_change_proposal(proposal_receiver) -> str:
    """Ссылка на страницу изменения предложения."""
    return reverse('ads:change_proposal', args=(
        proposal_receiver.id,
        ExchangeProposal.StatusChoices.ACCEPTED)
    )


@pytest.fixture
def url_reverse_delete_proposal(proposal) -> str:
    """Ссылка на страницу удаления предложения."""
    return reverse('ads:delete_proposal', args=(proposal.id,))


@pytest.fixture
def url_reverse_authorization() -> str:
    """Ссылка на страницу авторизации."""
    return reverse('login')


@pytest.fixture
def url_reverse_signup() -> str:
    return reverse('registration')


@pytest.fixture
def url_reverse_logout() -> str:
    return reverse('logout')
