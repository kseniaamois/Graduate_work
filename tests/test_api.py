import pytest
import allure
import requests
from config import API_KEY, BASE_URL_API  # импорт конфигурации


@pytest.mark.api
@allure.id("Kinopoisk_api_01")
@allure.title("Поиск фильма по id. Позитивная проверка.")
@allure.severity("Critical")
@allure.tag("api")
@allure.label("testType", "api")
def test_search_by_id():
    movie_id = "4443734"  # ID фильма "Фишер (сериал)"
    with allure.step("Отправка запроса."):
        response = requests.get(
            f"{BASE_URL_API}/movie/{movie_id}",
            headers=API_KEY
        )
    with allure.step("Проверка статуса кода."):
        assert response.status_code == 200, (
            f"Ожидался 200, получен {response.status_code}"
        )
    with allure.step("Проверка соответствия id."):
        result = response.json()
        assert str(result.get("id")) == movie_id, (
            "ID в ответе не соответствует запросу"
        )
    with allure.step("Проверка, что ответ не пустой"):
        assert len(result) > 0, "Ответ пустой"


@pytest.mark.api
@allure.id("Kinopoisk_api_02")
@allure.title("Поиск фильма по названию. Позитивная проверка.")
@allure.severity("Critical")
@allure.tag("api")
@allure.label("testType", "api")
def test_search_film_by_name():
    name_film = "Фишер"
    with allure.step("Отправка запроса."):
        response = requests.get(
            f"{BASE_URL_API}/movie/search?query={name_film}",
            headers=API_KEY
        )
    with allure.step("Проверка статуса кода."):
        assert response.status_code == 200, (
            f"Ожидался 200, получен {response.status_code}"
        )
    with allure.step("Проверка первого результата по названию."):
        result = response.json()
        assert result.get("docs"), "Список фильмов пуст"
        first_name = str(result["docs"][0].get("name", "")).lower()
        assert "фишер" in first_name, (
            f"Имя фильма в ответе "
            f"'{result['docs'][0].get('name')}' не содержит "
            f"'{name_film}'"
        )


@pytest.mark.api
@allure.id("Kinopoisk_api_03")
@allure.title(
    "Поиск фильма по неверному id (вне диапазона). "
    "Негативная проверка."
)
@allure.severity("Normal")
@allure.tag("api")
@allure.label("testType", "api")
def test_search_error_id():
    wrong_id = "d1000000001"
    with allure.step("Отправка запроса."):
        response = requests.get(
            f"{BASE_URL_API}/movie/{wrong_id}",
            headers=API_KEY
        )
    with allure.step("Проверка статуса кода."):
        assert response.status_code == 400, (
            f"Ожидался 400, получен {response.status_code}"
        )


@pytest.mark.api
@allure.id("Kinopoisk_api_04")
@allure.title(
    "Поиск фильма по id без токена авторизации. "
    "Негативная проверка."
)
@allure.severity("Normal")
@allure.tag("api")
@allure.label("testType", "api")
def test_search_no_api_key():
    movie_id = "100"
    with allure.step("Отправка запроса без API-ключа."):
        response = requests.get(f"{BASE_URL_API}/movie/{movie_id}")
    with allure.step("Проверка статуса кода"):
        assert response.status_code == 401, (
            f"Ожидался 401, получен {response.status_code}"
        )


@pytest.mark.api
@allure.id("Kinopoisk_api_05")
@allure.title("Поиск фильмов по рейтингу и жанру. Позитивная проверка.")
@allure.severity("Normal")
@allure.tag("api")
@allure.label("testType", "api")
def test_rating_and_genre_filter():
    params = {
        "page": 10,
        "limit": 100,
        "rating.kp": "8-10",
        "genres.name": "комедия",
    }
    with allure.step("Отправка запроса с параметрами."):
        response = requests.get(
            f"{BASE_URL_API}/movie",
            params=params,
            headers=API_KEY
        )
    with allure.step("Проверка статуса кода."):
        assert response.status_code == 200, (
            f"Ожидался 200, получен {response.status_code}"
        )
    with allure.step("Проверка, что список фильмов не пустой."):
        movies = response.json().get("docs", [])
        assert movies, "Список фильмов пустой"
    with allure.step("Проверка рейтингов всех фильмов"):
        for movie in movies:
            rating = movie.get("rating", {}).get("kp")
            assert rating is not None, (
                f"Рейтинг у фильма '{movie.get('name')}' отсутствует"
            )
            assert 8 <= rating <= 10, (
                f"Рейтинг фильма '{movie.get('name')}' ({rating}) "
                "вне диапазона 8-10"
            )
