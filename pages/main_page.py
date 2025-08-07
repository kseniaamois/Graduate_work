from typing import Optional
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import allure


class Main:
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input#find_film')
    SEARCH_BUTTON = (By.CSS_SELECTOR, 'input.el_18.submit.nice_button')
    YEAR_INPUT = (By.CSS_SELECTOR, 'input#year')
    CAPTCHA_BUTTON = (By.CSS_SELECTOR, '.CheckboxCaptcha-Button')
    ADVANCED_FILTER_BUTTON = (By.CSS_SELECTOR, '[aria-label="Расширенный поиск"]')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'button.styles_loginButton__LWZQp')
    PHONE_INPUT = (By.CSS_SELECTOR, 'input#passp-field-phone')

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.driver.get("https://www.kinopoisk.ru/")
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()

    @allure.step("Обрабатываем капчу, если она появляется.")
    def captcha(self) -> None:
        """
        Обрабатываем капчу, если она появляется на странице.
        Кликом по кнопке подтверждения.
        """
        try:
            captcha_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.CAPTCHA_BUTTON)
            )
            captcha_button.click()
            self.driver.implicitly_wait(20)
        except (NoSuchElementException, TimeoutException):
            # Капча не появилась — ничего делать не нужно
            pass

    @allure.step('Переход в расширенный фильтр с главной страницы.')
    def open_advanced_filter(self) -> None:
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ADVANCED_FILTER_BUTTON)
        ).click()

    @allure.step('Переход в ЛК. Кнопка "Войти".')
    def entrance_personal_account(self) -> None:
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        ).click()

    @allure.step('Ввод названия фильма в строку поиска и нажатие кнопки поиска.')
    def search(self, title: str) -> str:
        search_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SEARCH_INPUT)
        )
        search_input.clear()
        search_input.send_keys(title)
        self.driver.find_element(*self.SEARCH_BUTTON).click()
        return title

    @allure.step('Вытаскиваем название искомого фильма из плашки результатов.')
    def title(self) -> str:
        title_text = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.search_results_top'))
        ).text
        # Плашка вида: "поиск: Фишер • результаты: 30"
        split_title = title_text.split()
        if len(split_title) > 1:
            return split_title[1]
        return ""

    @allure.step('Поиск фильма по нескольким параметрам (название + год).')
    def search_title_year(self, title: str, year: str) -> None:
        title_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SEARCH_INPUT)
        )
        title_input.clear()
        title_input.send_keys(title)
        year_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.YEAR_INPUT)
        )
        year_input.clear()
        year_input.send_keys(year)
        self.driver.find_element(*self.SEARCH_BUTTON).click()

    @allure.step('Ввод телефонного номера для входа в ЛК.')
    def number_phone(self, num: str) -> None:
        phone_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.PHONE_INPUT)
        )
        phone_input.clear()
        phone_input.send_keys(num)

