from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройка WebDriver
driver = webdriver.Chrome()  # Замените на путь к драйверу, если требуется
wait = WebDriverWait(driver, 10)

# URL тестируемого приложения
base_url = "http://example.com"  # Укажите ваш URL

# Утилита для проверки ожидаемого результата
def assert_text_in_element(locator, expected_text):
    element = wait.until(EC.visibility_of_element_located(locator))
    assert expected_text in element.text, f"Ожидалось '{expected_text}', но найдено '{element.text}'"

# Тест-кейс 1.1: Успешное создание объявления
def test_create_announcement_success():
    driver.get(f"{base_url}/create")
    driver.find_element(By.ID, "title").send_keys("Велосипед")
    driver.find_element(By.ID, "description").send_keys("Горный велосипед в хорошем состоянии")
    driver.find_element(By.ID, "price").send_keys("15000")
    driver.find_element(By.ID, "image_url").send_keys("https://example.com/image.jpg")
    driver.find_element(By.ID, "save_button").click()

    # Проверка
    assert_text_in_element((By.CLASS_NAME, "notification"), "Объявление успешно создано")
    assert_text_in_element((By.CLASS_NAME, "announcement-title"), "Велосипед")

# Тест-кейс 1.2: Попытка создания объявления с пустыми полями
def test_create_announcement_empty_fields():
    driver.get(f"{base_url}/create")
    driver.find_element(By.ID, "save_button").click()

    # Проверка
    assert_text_in_element((By.CLASS_NAME, "error"), "Все поля обязательны для заполнения")

# Тест-кейс 2.1: Успешное редактирование объявления
def test_edit_announcement_success():
    driver.get(f"{base_url}/announcement/1/edit")
    driver.find_element(By.ID, "title").clear()
    driver.find_element(By.ID, "title").send_keys("Модернизированный велосипед")
    driver.find_element(By.ID, "save_button").click()

    # Проверка
    assert_text_in_element((By.CLASS_NAME, "notification"), "Изменения сохранены")
    assert_text_in_element((By.CLASS_NAME, "announcement-title"), "Модернизированный велосипед")

# Тест-кейс 2.2: Попытка сохранить объявление с пустыми полями
def test_edit_announcement_empty_fields():
    driver.get(f"{base_url}/announcement/1/edit")
    driver.find_element(By.ID, "title").clear()
    driver.find_element(By.ID, "description").clear()
    driver.find_element(By.ID, "price").clear()
    driver.find_element(By.ID, "save_button").click()

    # Проверка
    assert_text_in_element((By.CLASS_NAME, "error"), "Все поля обязательны для заполнения")

# Тест-кейс 3.1: Успешный поиск по ключевому слову
def test_search_success():
    driver.get(base_url)
    search_field = driver.find_element(By.ID, "search")
    search_field.send_keys("велосипед")
    search_field.send_keys(Keys.RETURN)

    # Проверка
    assert_text_in_element((By.CLASS_NAME, "announcement-title"), "Велосипед")

# Тест-кейс 3.2: Поиск без результатов
def test_search_no_results():
    driver.get(base_url)
    search_field = driver.find_element(By.ID, "search")
    search_field.send_keys("несуществующий запрос")
    search_field.send_keys(Keys.RETURN)

    # Проверка
    assert_text_in_element((By.CLASS_NAME, "no-results"), "Объявления не найдены")

# Тест-кейс 3.3: Сброс результатов поиска
def test_search_reset():
    driver.get(base_url)
    search_field = driver.find_element(By.ID, "search")
    search_field.send_keys("велосипед")
    search_field.send_keys(Keys.RETURN)

    reset_button = driver.find_element(By.ID, "reset_button")
    reset_button.click()

    # Проверка
    assert_text_in_element((By.CLASS_NAME, "announcement-list"), "Все объявления")

# Выполнение всех тестов
def run_all_tests():
    try:
        test_create_announcement_success()
        test_create_announcement_empty_fields()
        test_edit_announcement_success()
        test_edit_announcement_empty_fields()
        test_search_success()
        test_search_no_results()
        test_search_reset()
        print("Все тесты успешно пройдены!")
    except AssertionError as e:
        print(f"Тест завершился с ошибкой: {e}")
    finally:
        driver.quit()

# Запуск
if __name__ == "__main__":
    run_all_tests()
