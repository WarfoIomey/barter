import pytest
from pytest_lazyfixture import lazy_fixture as lf

import ads.constants as constants


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url_reverse, check_object, context_object',
    (
        (
            lf('url_reverse_index'),
            lf('six_ads'),
            'object_list',
        ),
        (
            lf('url_reverse_profile'),
            lf('six_ads'),
            'page_obj',
        ),
        (
            lf('url_reverse_profile'),
            lf('six_ads_another_author'),
            'sent_proposals',
        ),
    ),
)
def test_status_count(
    url_reverse,
    check_object,
    context_object,
    author_client,
    another_author_client,
    six_proposals,
) -> None:
    """Тест на корректность количества отображаемых объектов."""
    response = author_client.get(url_reverse)
    object_list = response.context[context_object]
    count: int = 0
    if context_object == 'object_list':
        count = object_list.count()
        assert count == constants.PAGINATION_PER_PAGE_AD
    elif context_object == 'page_obj':
        for _ in object_list:
            count += 1
        assert count == constants.PAGINATION_PER_PAGE_AD
    elif context_object == 'sent_proposals':
        for _ in object_list:
            count += 1
        assert count == constants.PAGINATION_PER_PAGE_PROPOSAL
    else:
        for _ in object_list:
            count += 1
        assert count == constants.PAGINATION_PER_PAGE_PROPOSAL
