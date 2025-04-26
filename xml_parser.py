import streamlit as st
import time
import csv
import io
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from xml.etree import ElementTree

st.set_page_config(page_title="Sitemap  Checker", layout="wide")
st.title("🕷️ Проверка Sitemap")

domain = st.text_input("Введите домен (например, https://example.com)")
delay = st.number_input("Задержка между запросами (в секундах)", min_value=0, max_value=30, value=1)

user_agent = st.text_input("Введите пользовательский агент",
                           value="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")

# Функция для получения всех URL из карты сайта с использованием ElementTree (стандартная библиотека)
def get_sitemap_urls(domain):
    sitemap_url = f"{domain}/sitemap.xml"
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()  # Проверка на успешный ответ
        tree = ElementTree.fromstring(response.content)

        urls = []

        # Если это индекс карты сайта
        if tree.tag.endswith("sitemapindex"):
            for sitemap in tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
                loc = sitemap.text
                if loc:
                    urls.extend(get_sitemap_urls(loc))  # Рекурсивно обрабатываем вложенные карты сайтов
        else:
            # Обычная карта сайта
            for url in tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
                loc = url.text
                if loc:
                    urls.append(loc)
        return urls
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка при получении sitemap: {e}")
        return []

if st.button("Начать проверку"):
    if not domain.startswith("http"):
        domain = "https://" + domain

    st.write(f"Загружаем sitemap с: `{domain}`")

    urls = get_sitemap_urls(domain)

    if not urls:
        st.warning("Ссылки в карте сайта не найдены.")
    else:
        st.success(f"Найдено {len(urls)} URL в sitemap.")

        # Настройка Selenium
        options = Options()
        options.add_argument("--start-maximized")  # Браузер не будет в headless-режиме
        options.add_argument(f"user-agent={user_agent}")  # Добавляем пользовательский агент
        options.add_argument("--disable-infobars")  # Убираем предупреждения о автоматизации
        options.add_argument("--headless")  # Используем headless режим для работы без GUI

        driver = webdriver.Chrome(options=options)

        progress = st.progress(0)
        status_text = st.empty()
        time_text = st.empty()
        results = []
        start_time = time.time()

        def get_status_code(url):
            try:
                response = requests.head(url, allow_redirects=True)
                return response.status_code
            except requests.exceptions.RequestException:
                return None

        for idx, url in enumerate(urls):
            try:
                status_code = get_status_code(url)
                driver.get(url)
                time.sleep(2)  # Подождать, чтобы страница успела прогрузиться
                page_title = driver.title  # Получаем титул страницы
            except Exception:
                status_code = "0"
                page_title = "Не удалось загрузить"

            results.append((url, status_code, page_title))

            elapsed = time.time() - start_time
            remaining = (len(urls) - idx - 1) * (delay + 2)

            status_text.markdown(f"🔍 Проверено: `{idx + 1} / {len(urls)}` — URL: **{url}**, Статус: **{status_code}**, Тайтл: **{page_title}**")
            time_text.markdown(f"⏱ Времени прошло: `{int(elapsed)} сек`, осталось: ~`{int(remaining)} сек`")
            progress.progress((idx + 1) / len(urls))
            time.sleep(delay)

        driver.quit()
        st.success("✅ Готово!")

        # Экспорт в CSV
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["URL", "Статус", "Тайтл"])
        writer.writerows(results)
        csv_data = csv_buffer.getvalue()

        st.download_button(
            label="📥 Скачать результат (CSV)",
            data=csv_data,
            file_name="selenium_sitemap_check.csv",
            mime="text/csv"
        )
