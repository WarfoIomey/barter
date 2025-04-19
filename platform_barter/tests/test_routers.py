from http import HTTPStatus

from django.urls import reverse
import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'reverse_url, parametrized_client, expected_status',
    (
        (
            lf('url_reverse_edit_ad'),
            lf('another_author_client'),
            HTTPStatus.NOT_FOUND),
        (
            lf('url_reverse_delete_ad'),
            lf('another_author_client'),
            HTTPStatus.NOT_FOUND
        ),
        (
            lf('url_reverse_edit_proposal'),
            lf('another_author_client'),
            HTTPStatus.NOT_FOUND),
        (
            lf('url_reverse_delete_proposal'),
            lf('another_author_client'),
            HTTPStatus.NOT_FOUND
        ),
        (
            lf('url_reverse_edit_ad'),
            lf('author_client'),
            HTTPStatus.OK
        ),
        (
            lf('url_reverse_delete_ad'),
            lf('author_client'),
            HTTPStatus.OK
        ),
        (
            lf('url_reverse_edit_proposal'),
            lf('author_client'),
            HTTPStatus.OK
        ),
        (
            lf('url_reverse_delete_proposal'),
            lf('author_client'),
            HTTPStatus.OK
        ),
        (
            lf('url_reverse_detail_ad'),
            lf('client'),
            HTTPStatus.OK
        ),
        (
            lf('url_reverse_index'),
            lf('client'),
            HTTPStatus.OK
        ),
        (
            lf('url_reverse_authorization'),
            lf('client'),
            HTTPStatus.OK
        ),
        (
            lf('url_reverse_logout'),
            lf('client'),
            HTTPStatus.OK
        ),
        (
            lf('url_reverse_signup'),
            lf('client'),
            HTTPStatus.OK
        ),
    ),
)
def test_availability(
    reverse_url: str,
    parametrized_client,
    expected_status,
) -> None:
    """Тесты на доступность."""
    if reverse_url == reverse('logout'):
        response = parametrized_client.post(reverse_url)
    else:
        response = parametrized_client.get(reverse_url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'reverse_url, login_url',
    (
        (lf('url_reverse_edit_ad'), lf('url_reverse_authorization')),
        (lf('url_reverse_delete_ad'), lf('url_reverse_authorization')),
        (lf('url_reverse_edit_proposal'), lf('url_reverse_authorization')),
        (lf('url_reverse_delete_proposal'), lf('url_reverse_authorization')),
    ),
)
def test_redirect_for_anonymous_client(
    client,
    login_url,
    reverse_url: str,
) -> None:
    """Тест на перенаправления на страницу входа."""
    expected_url: str = f'{login_url}?next={reverse_url}'
    response = client.get(reverse_url)
    print(response.url)
    print(expected_url)
    print(expected_url == response.url)
    assert response.status_code == 302
    assertRedirects(response, expected_url)
