import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException
)
from pages.main_page import Main


@pytest.mark.ui
@allure.id('Kinopoisk_01')
@allure.feature('Поиск фильма. Без авторизации.')
@allure.title(
    'Поиск фильма/сериала по валидному названию. Позитивная проверка.'
)
@allure.description(
    'Проверить, что название введенного фильма соотвествует '
    'отображенному названию в верхней плашке '
    '"поиск: Фишер • результаты: 30"'
)
@allure.severity("Blocker")
@allure.tag("ui")
@allure.label("testType", "ui")
def test_search_movie__main_page(browser):
    main_page = Main(browser)
    main_page.captcha()
    main_page.open_advanced_filter()
    title_search = main_page.search("Фишер")

    wait = WebDriverWait(browser, 30)
    try:
        title_element = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div.search_results_top')
            )
        )
    except TimeoutException:
        pytest.fail(
            "Не удалось найти элемент с результатами поиска "
            "за отведённое время"
        )

    title_total_text = title_element.text
    # пример: "поиск: Фишер • результаты: 30"
    title_total = title_total_text.split()[1]

    with allure.step(
        'Проверка, что название введенного фильма '
        'соотвествует отображенному названию в верхней плашке.'
    ):
        assert title_search == title_total


@pytest.mark.ui
@allure.id('Kinopoisk_02')
@allure.feature('Поиск фильма. Без авторизации.')
@allure.title(
    'Поиск фильма/сериала в названии содержатся символы. '
    'Негативная проверка.'
)
@allure.description(
    'Ввести невалидное название фильма (символы), '
    'убедиться, что получаем сообщение: '
    '"К сожалению, по вашему запросу ничего не найдено..."'
)
@allure.severity("Minor")
@allure.tag("ui")
@allure.label("testType", "ui")
def test_negative_1_search(browser):
    main_page = Main(browser)
    main_page.captcha()
    main_page.open_advanced_filter()
    main_page.search("#")

    wait = WebDriverWait(browser, 30)
    try:
        message_element = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="block_left_pad"]/div/table/tbody/tr[1]/td/h2'
                )
            )
        )
    except TimeoutException:
        pytest.fail(
            "Не удалось найти сообщение об отсутствии результатов "
            "за отведённое время"
        )

    message = message_element.text
    assert message == "К сожалению, по вашему запросу ничего не найдено..."


@pytest.mark.ui
@allure.id('Kinopoisk_03')
@allure.feature('Поиск фильма. Без авторизации.')
@allure.title(
    'Поиск фильма/сериала с несуществующим названием. '
    'Негативная проверка.'
)
@allure.description(
    'Ввести несуществующее название фильма (бессмысленный набор символов), '
    'убедиться, что получаем сообщение: '
    '"К сожалению, по вашему запросу ничего не найдено..."'
)
@allure.severity("Minor")
@allure.tag("ui")
@allure.label("testType", "ui")
def test_negative_2_search(browser):
    main_page = Main(browser)
    main_page.captcha()
    main_page.open_advanced_filter()
    main_page.search("zxqweplmvn")

    wait = WebDriverWait(browser, 30)
    for attempt in range(3):  # попытки при StaleElementReferenceException
        try:
            message_element = wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="block_left_pad"]/div/table/tbody/tr[1]/td/h2'
                    )
                )
            )
            message = message_element.text
            break
        except StaleElementReferenceException:
            if attempt == 2:
                raise
    else:
        pytest.fail("Не удалось получить сообщение после нескольких попыток")

    assert message == "К сожалению, по вашему запросу ничего не найдено..."


@pytest.mark.ui
@allure.id('Kinopoisk_04')
@allure.feature('Поиск фильма. Без авторизации.')
@allure.title('Проверка активности кнопки "Смотреть фильм".')
@allure.severity("Blocker")
@allure.tag("ui")
@allure.label("testType", "ui")
def test_positive_button(browser):
    main_page = Main(browser)
    main_page.captcha()
    main_page.open_advanced_filter()

    main_page.search_title_year("Фишер", "2023")

    wait = WebDriverWait(browser, 30)
    try:
        film_link = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//a[contains(@class, 'js-serp-metrika') "
                    "and contains(text(), 'Фишер (сериал)')]"
                )
            )
        )
        film_link.click()
    except TimeoutException:
        pytest.fail(
            "Не удалось найти ссылку на фильм 'Фишер (сериал)' "
            "за отведённое время"
        )

    try:
        watch_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    'a[data-test-id="Watch"], button[data-test-id="Offer"]'
                )
            )
        )
        watch_button.click()
    except TimeoutException:
        pytest.fail(
            "Не удалось найти кнопку 'Смотреть фильм/Продолжить просмотр' "
            "за отведённое время"
        )

    # Можно добавить проверку перехода, например:
    # wait.until(EC.url_contains("login"))


@pytest.mark.ui
@allure.id('Kinopoisk_05')
@allure.feature('Авторизация.')
@allure.title(
    'Проверка валидности телефонного номера при входе в ЛК. '
    'Номер не зарегистрирован.'
)
@allure.description(
    'В случае если номер не зарегистрирован, '
    'то получаем сообщение: "Можно зарегистрировать новый аккаунт".'
)
@allure.severity("Blocker")
@allure.tag("ui")
@allure.label("testType", "ui")
def test_pozitive_phone_not_registered(browser):
    main_page = Main(browser)
    main_page.captcha()
    main_page.entrance_personal_account()

    with allure.step(
        'Ввод валидного телефонного номера, но не зарегистрированного.'
    ):
        main_page.number_phone("+79992083864")

    with allure.step(
        'Нажать кнопку "Войти" для перехода на страницу ввода СМС.'
    ):
        main_page.driver.find_element(
            By.CSS_SELECTOR,
            '[id="passp:sign-in"]'
        ).click()

    wait = WebDriverWait(browser, 30)
    try:
        message_element = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="root"]/div/div[2]/div[2]/div/div/div[2]/div[3]'
                    '/div/form/div/div[2]/div'
                )
            )
        )
    except TimeoutException:
        pytest.fail(
            "Не удалось найти сообщение "
            "'Можно зарегистрировать новый аккаунт' "
            "за отведённое время"
        )

    message = message_element.text
    assert message == "Можно зарегистрировать новый аккаунт"
