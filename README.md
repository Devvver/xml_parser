# xml_parser
Парсинг xml карты сайта и тестовый парсинг данных с Селениумом

# 🕷️ Новый инструмент: Проверка Sitemap с заголовками страниц!

[Исходный код взят с телеграм канала ChatGPT, AI, Python для SEO](https://t.me/python_seo)



Создали удобное веб-приложение на **Streamlit**, которое:

- 🔍 Загружает все ссылки из `sitemap.xml` (поддержка вложенных карт);
- ✅ Проверяет код ответа каждой страницы (200, 404 и другие);
- 🌐 Автоматически открывает каждую ссылку через **Selenium**;
- 🏷️ Извлекает заголовок страницы (`<title>`);
- ⚙️ Позволяет настроить свой **User-Agent** и **задержку между запросами**;
- 📊 Отображает процесс работы: сколько осталось, сколько прошло времени ⏱;
- 📥 После завершения — позволяет скачать все результаты в **CSV**.

---

## ⚙️ Используемые технологии:

- **Python** — основной язык
- **Streamlit** — удобный веб-интерфейс
- **Selenium** — автоматизация открытия страниц
- **ElementTree** — обработка структуры sitemap.xml
- **CSV** — сохранение результатов

---

## 🚀 Как работает

1. Вводите домен сайта.
2. Программа загружает все ссылки из `sitemap.xml`.
3. Каждая страница открывается через Selenium.
4. Определяется HTTP-статус и заголовок страницы.
5. В реальном времени показывается ход выполнения.
6. После окончания можно скачать файл со всеми данными.

---

## 📋 Примечания

- Если вместо sitemap вернётся HTML-страница — будет выведено предупреждение.
- Поддерживается вложенная структура карт сайта.
- Работает в **headless** режиме (без открытия браузера на экране).

---

## 📦 Требования

- Python 3.8+
- Установленные библиотеки:
  ```bash
  pip install streamlit selenium

