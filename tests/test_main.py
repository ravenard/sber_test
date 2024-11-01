import pytest
from test_client.client import HttpComponent
from utils.utils import test_data


@pytest.fixture
def connect_http():
    h = HttpComponent()
    yield h
    h.http.close()


class TestMain:
    def test_main_page(self, connect_http):
        connect_http.get_main_page()


class TestCardsIdentifier:

    @pytest.mark.parametrize('card', ['1234567890123456', '123567', '99999999'])
    def test_not_found_cards(self, connect_http, card):
        connect_http.post_card_not_found(card)

    @pytest.mark.parametrize('card', ['123', '123123123123123123123213123123', 'asdasdasd', 123123123123231])
    def test_invalid_cards(self, connect_http, card):
        # тут в приложении нет ограничения на длину поэтому тест упадет
        connect_http.post_card_invalid(card)

    @pytest.mark.parametrize('card', ['4219192416773905', '4219 1924 1677 3905'])
    def test_correct_cards(self, connect_http, card):
        # тут упадут тесты с картами, которые не написаны слитно
        connect_http.post_card_success(card)

    @pytest.mark.parametrize('card_details', test_data)
    def test_correct_cards_with_details(self, connect_http, card_details):
        connect_http.post_card_success_with_details(card_details)
