from http import HTTPStatus

import pytest
from django.contrib.auth import get_user
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf

from ads.models import Ad, ExchangeProposal


pytestmark = pytest.mark.django_db

ONE_OBJECT: int = 1
TITLE: str = 'Название'
DESCRIPTIONS: str = 'Описание'
NEW_DESCRIPTIONS: str = 'Новое описание'
COMMENT: str = 'Тестовый комментарий'


@pytest.mark.parametrize(
    'url_reverse_edit, model, object, sub_object',
    (
        (
            lf('url_reverse_create_proposal'),
            ExchangeProposal,
            lf('ad'),
            lf('another_author')
        ),
        (
            lf('url_reverse_create_ad'),
            Ad,
            lf('category'),
            lf('condition')
        ),
    ),
)
def tests_anonymous_user_cant_create(
    client,
    url_reverse_authorization,
    url_reverse_edit,
    model,
    object,
    sub_object
) -> None:
    """Тест на создание предложения анонимом."""
    later_count: int = model.objects.count()
    if model == ExchangeProposal:
        post_data = {
            "ad_sender": object.id,
            "ad_receiver": sub_object.id,
            "comment": COMMENT,
        }
    else:
        post_data = {
            "title": TITLE,
            "descriptions": DESCRIPTIONS,
            "category": object,
            "condition": sub_object
        } 
    response = client.post(
        url_reverse_edit,
        data=post_data
    )
    assertRedirects(
        response,
        f'{url_reverse_authorization}?next={url_reverse_edit}'
    )
    count: int = model.objects.count()
    assert count == later_count


@pytest.mark.parametrize(
    'url_reverse_create, url_complete, model, object, sub_object',
    (
        (
            lf('url_reverse_create_proposal'),
            lf('url_reverse_profile'),
            ExchangeProposal,
            lf('ad'),
            lf('another_author')
        ),
        (
            lf('url_reverse_create_ad'),
            lf('url_reverse_index'),
            Ad,
            lf('category'),
            lf('condition')
        ),
    ),
)
def tests_user_can_create(
    author_client,
    url_reverse_create,
    url_complete,
    model,
    object,
    sub_object
) -> None:
    """Тест создания предложения и объявления залогиненому."""
    model.objects.all().delete()
    if model == ExchangeProposal:
        post_data = {
            "ad_sender": object.id,
            "ad_receiver": sub_object.id,
            "comment": COMMENT,
        }
    else:
        post_data = {
            "title": TITLE,
            "descriptions": DESCRIPTIONS,
            "category": object.id,
            "condition": sub_object.id
        }
    response = author_client.post(
        url_reverse_create,
        data=post_data
    )
    assertRedirects(response, url_complete)
    count = model.objects.count()
    assert count == ONE_OBJECT
    new_object = model.objects.get()
    if model == ExchangeProposal:
        assert new_object.ad_sender == object
        assert new_object.ad_receiver == sub_object
        assert new_object.comment == COMMENT
    else:
        assert new_object.descriptions == DESCRIPTIONS
        assert new_object.title == TITLE
        assert new_object.user == get_user(author_client)


def test_user_cant_viewing_proposal_of_another_user(
    another_author_client,
    author_client,
    url_reverse_profile,
    proposal,
) -> None:
    """Тест просмотр чужих предложений."""
    response = another_author_client.get(
        url_reverse_profile
    )
    assert ('sent_proposals' in response.context) is False
    assert ('received_proposals' in response.context) is False


def test_user_can_viewing_proposal_of_author(
    author_client,
    url_reverse_profile,
    proposal,
    proposal_receiver
) -> None:
    """Тест просмотр предложений."""
    response = author_client.get(
        url_reverse_profile
    )
    assert ('sent_proposals' in response.context) is True
    for g in response.context['sent_proposals']:
        assert g == proposal
    assert ('received_proposals' in response.context) is True
    for g in response.context['received_proposals']:
        assert g == proposal_receiver


@pytest.mark.parametrize(
    'url_reverse_edit, url_complete, model, object',
    (
        (
            lf('url_reverse_edit_proposal'),
            lf('url_reverse_profile'),
            ExchangeProposal,
            lf('proposal')
        ),
        (
            lf('url_reverse_edit_ad'),
            lf('url_reverse_detail_ad'),
            Ad,
            lf('ad')
        ),
    ),
)
def test_author_can_edit(
    author_client,
    url_reverse_edit,
    url_complete,
    model,
    object
) -> None:
    """Тест на изменения предложения и объявления автором."""
    if model == ExchangeProposal:
        post_data = {
                "status": ExchangeProposal.StatusChoices.ACCEPTED,
            }
    else:
        post_data = {
            "title": TITLE,
            "descriptions": NEW_DESCRIPTIONS,
            "category": object.category.id,
            "condition": object.condition.id
        }
    response = author_client.post(
        url_reverse_edit,
        data=post_data
    )
    assertRedirects(response, url_complete)
    new_object = model.objects.get(id=object.id)
    if model == ExchangeProposal:
        assert new_object.status == ExchangeProposal.StatusChoices.ACCEPTED
    else:
        assert new_object.descriptions == NEW_DESCRIPTIONS


@pytest.mark.parametrize(
    'url_reverse_delete, url_complete, model, object',
    (
        (
            lf('url_reverse_delete_ad'),
            lf('url_reverse_index'),
            Ad,
            lf('ad')
        ),
        (
            lf('url_reverse_delete_proposal'),
            lf('url_reverse_profile'),
            ExchangeProposal,
            lf('proposal')
        ),
    ),
)
def test_author_can_delete(
    author_client,
    url_reverse_delete,
    url_complete,
    model,
    object,
) -> None:
    """Тест на удаление объявления и предложения автором."""
    later_count = model.objects.count()
    response = author_client.delete(url_reverse_delete)
    assertRedirects(response, url_complete)
    count: int = model.objects.count()
    assert count == later_count - ONE_OBJECT


@pytest.mark.parametrize(
    'url_reverse_edit, model, object',
    (
        (
            lf('url_reverse_edit_ad'),
            Ad,
            lf('ad')
        ),
        (
            lf('url_reverse_edit_proposal'),
            ExchangeProposal,
            lf('proposal')
        ),
    ),
)
def test_user_cant_edit_of_another_user(
    another_author_client,
    url_reverse_edit,
    model,
    object
) -> None:
    """Тест изменение чужого объявления и предложения."""
    if model == Ad:
        post_data = {
            "title": TITLE,
            "descriptions": NEW_DESCRIPTIONS,
            "category": object.category.id,
            "condition": object.condition.id
        }
    else:
        post_data = {
            "status": ExchangeProposal.StatusChoices.ACCEPTED,
        }
    response = another_author_client.post(
        url_reverse_edit,
        data=post_data,
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    new_object = model.objects.get(id=object.id)
    if model == Ad:
        assert new_object.title == object.title
        assert new_object.user == object.user
        assert new_object.descriptions == object.descriptions
    else:
        assert new_object.status == new_object.status


def test_user_can_change_receiver_proposal(
    author_client,
    url_reverse_change_proposal,
    url_reverse_profile,
    proposal_receiver
) -> None:
    """Тест на принятие полученного объявления."""
    response = author_client.post(
        url_reverse_change_proposal,
    )
    assertRedirects(response, url_reverse_profile)
    new_proposal = ExchangeProposal.objects.get(id=proposal_receiver.id)
    assert new_proposal.status == ExchangeProposal.StatusChoices.ACCEPTED
