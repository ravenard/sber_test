import requests
import os
import allure

# вот часть с переменными можно было вы в другое место вынести, но так проще
base_url = os.getenv('URL', 'http://localhost:8080')
card_url = base_url + '/get-card-info'


class HttpComponent:
    @allure.step('Подключаем клиент')
    def __init__(self):
        self.http = requests.Session()

    def post(self, url, data) -> requests.Response:
        return self.http.post(url, json=data)

    def get(self, url) -> requests.Response:
        return self.http.get(url)

    @allure.step('Проверяем главную страницу')
    def get_main_page(self) -> requests.Response:
        response = self.get(base_url)
        assert response.status_code == 200
        return response

    # тут бы лучше тело генерировать пидантиком
    def post_card(self, card: str) -> requests.Response:
        data = {
            'card_number': card
        }
        response = self.post(card_url, data)
        return response

    # здесь бы лучше валидацию на модели пидантика сделать
    @allure.step('Post correct card simple "card"')
    def post_card_success(self, card: str) -> requests.Response:
        response = self.post_card(card)
        assert response.status_code == 200
        assert response.json()['brand'] is not None
        assert response.json()['country'] is not None
        assert response.json()['type'] is not None
        return response

    @allure.step('Post correct card with details "card_details" ')
    def post_card_success_with_details(self, card_details) -> requests.Response:
        card = card_details['card_number']
        brand = card_details['brand']
        country = card_details['country']
        card_type = card_details['type']

        response = self.post_card(card)
        assert response.status_code == 200
        assert response.json()['brand'] == brand
        assert response.json()['country'] == country
        assert response.json()['type'] == card_type
        return response

    @allure.step('Post not found card "card"')
    def post_card_not_found(self, card: str) -> requests.Response:
        response = self.post_card(card)
        assert response.status_code == 404
        assert response.json()['brand'] == 'Информация не найдена.'
        return response

    @allure.step('Post invalid card "card"')
    def post_card_invalid(self, card: str) -> requests.Response:
        response = self.post_card(card)
        assert response.status_code == 400, f'{response.json()} {response.status_code}'
        return response
