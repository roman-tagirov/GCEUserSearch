"""
Created on Fri 18 Oct by
Author: Q3t8/Q3ttA
About me: https://about.me/q3t8 // https://github.com/roman-tagirov // https://q3t8.ru/
Contact: q3t8.business@list.ru
"""

import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog,
    QMessageBox, QComboBox
)
from PyQt5.QtGui import QPixmap
from bs4 import BeautifulSoup

"""
Переход на сайт Google Custom Search Engine:

Откройте Google Custom Search Engine в вашем браузере.
Создание новой поисковой системы:

Нажмите кнопку "Add" (Добавить).

Настройка поисковой системы:

"Sites to search" (Сайты для поиска):
Введите любой сайт, например, example.com. Это необходимо для первоначального создания.
"Name of the search engine" (Название поисковой системы):
Введите имя, например, InfoSearchEngine.
Нажмите "Create" (Создать).

Настройка поиска по всему вебу:

После создания CSE вы попадёте на страницу её настроек. Нажмите "Control Panel" (Панель управления).
В разделе "Sites to search" нажмите "Edit" (Редактировать).
Удалите все введённые сайты.
Включите опцию "Search the entire web but emphasize included sites" (Искать по всему вебу, но выделять включённые сайты).
Нажмите "Save" (Сохранить).

Получение идентификатора поисковой системы (cx):

На странице "Control Panel" найдите раздел "Search engine ID" (Идентификатор поисковой системы).


Скопируйте этот идентификатор. Он понадобится вашему приложению для выполнения поисковых запросов. - GOOGLE_CSE_ID
Скопируйте этот идентификатор. Он понадобится вашему приложению для выполнения поисковых запросов. - GOOGLE_CSE_ID
Скопируйте этот идентификатор. Он понадобится вашему приложению для выполнения поисковых запросов. - GOOGLE_CSE_ID


"""
"""
ерейдите на Google Cloud Console:
Откройте Google Cloud Console в вашем браузере.
Войдите в свою учётную запись Google, если вы ещё этого не сделали.
Шаг 2: Создание или выбор проекта
Создание нового проекта (если необходимо):

В верхней части страницы найдите выпадающее меню проектов (рядом с логотипом Google Cloud).
Нажмите на него и выберите "New Project" (Новый проект).
Введите имя проекта, например, InfoSearchApp.
(Опционально) Выберите организацию или оставьте по умолчанию.
Нажмите "Create" (Создать).
Выбор существующего проекта:

Если у вас уже есть проект, который вы хотите использовать, выберите его из выпадающего списка.
Шаг 3: Включение Custom Search API
Переход к библиотеке API:

В левом боковом меню выберите "APIs & Services" (API и сервисы) > "Library" (Библиотека).
Поиск и включение Custom Search API:

В строке поиска введите Custom Search API.
Выберите "Custom Search API" из результатов поиска.
Нажмите "Enable" (Включить).

Шаг 4: Создание API ключа
Переход к разделу "Credentials" (Учётные данные):

В левом боковом меню выберите "APIs & Services" > "Credentials" (Учётные данные).
Создание нового API ключа:

Нажмите на кнопку "Create Credentials" (Создать учётные данные) в верхней части страницы.
В выпадающем меню выберите "API key".

Получение API ключа:

После создания ключа всплывет окно с вашим новым API ключом.


Нажмите "Copy" (Копировать) и сохраните ключ в безопасном месте. Он понадобится для вашего приложения. - GOOGLE_API_KEY
Нажмите "Copy" (Копировать) и сохраните ключ в безопасном месте. Он понадобится для вашего приложения. - GOOGLE_API_KEY
Нажмите "Copy" (Копировать) и сохраните ключ в безопасном месте. Он понадобится для вашего приложения. - GOOGLE_API_KEY


"""
GOOGLE_API_KEY = 'Your api key. Get from - google cloud console. Search in API&Services -> Custom Search API -> Enable -> in the left bar -> Credentials -> Create new credentials -> API key'
GOOGLE_CSE_ID = 'd211171cc7beb4863'

SOCIAL_NETWORKS = [
    'twitter.com',
    'facebook.com',
    'linkedin.com',
    'instagram.com',
    'vk.com',
    'ok.ru',
    't.me',
    'youtube.com'
]

LANGUAGES = {
    'Все языки': '',
    'Русский': 'lang_ru',
    'Английский': 'lang_en',
    'Испанский': 'lang_es',
    'Французский': 'lang_fr',
    'Немецкий': 'lang_de'
}

class InfoSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Бот для сбора информации о человеке')
        self.setGeometry(100, 100, 1000, 800)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        img_layout = QHBoxLayout()
        self.img_label = QLabel('Фото профиля (опционально):')
        self.img_display = QLabel()
        self.img_display.setFixedSize(150, 150)
        self.img_display.setStyleSheet("border: 1px solid black;")
        self.img_display.setScaledContents(True)
        self.btn_upload = QPushButton('Загрузить фото')
        self.btn_upload.clicked.connect(self.upload_image)
        img_layout.addWidget(self.img_label)
        img_layout.addWidget(self.img_display)
        img_layout.addWidget(self.btn_upload)
        layout.addLayout(img_layout)
        name_layout = QHBoxLayout()
        self.name_label = QLabel('Настоящее имя и фамилия:')
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        social_layout = QHBoxLayout()
        self.social_label = QLabel('Имя и фамилия в соцсетях (через запятую):')
        self.social_input = QLineEdit()
        social_layout.addWidget(self.social_label)
        social_layout.addWidget(self.social_input)
        layout.addLayout(social_layout)
        links_layout = QHBoxLayout()
        self.links_label = QLabel('Ссылки (через запятую):')
        self.links_input = QLineEdit()
        links_layout.addWidget(self.links_label)
        links_layout.addWidget(self.links_input)
        layout.addLayout(links_layout)
        language_layout = QHBoxLayout()
        self.language_label = QLabel('Язык данных:')
        self.language_combo = QComboBox()
        self.language_combo.addItems(LANGUAGES.keys())
        language_layout.addWidget(self.language_label)
        language_layout.addWidget(self.language_combo)
        layout.addLayout(language_layout)
        city_layout = QHBoxLayout()
        self.city_label = QLabel('Город:')
        self.city_input = QLineEdit()
        city_layout.addWidget(self.city_label)
        city_layout.addWidget(self.city_input)
        layout.addLayout(city_layout)
        self.btn_search = QPushButton('Начать поиск')
        self.btn_search.clicked.connect(self.start_search)
        layout.addWidget(self.btn_search)
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        layout.addWidget(self.results_display)
        self.btn_save = QPushButton('Сохранить результаты')
        self.btn_save.clicked.connect(self.save_results)
        layout.addWidget(self.btn_save)
        self.setLayout(layout)

    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите фото профиля",
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp)",
            options=options
        )
        if file_name:
            self.image_path = file_name
            pixmap = QPixmap(file_name)
            self.img_display.setPixmap(pixmap)

    def start_search(self):
        threading.Thread(target=self.perform_search).start()

    def perform_search(self):
        real_name = self.name_input.text().strip()
        social_names = [name.strip() for name in self.social_input.text().split(',') if name.strip()]
        links = [link.strip() for link in self.links_input.text().split(',') if link.strip()]
        selected_language = self.language_combo.currentText()
        language_param = LANGUAGES[selected_language]
        city = self.city_input.text().strip()
        if not real_name and not social_names and not links and not hasattr(self, 'image_path'):
            QMessageBox.warning(self, "Предупреждение", "Введите хотя бы одно поле для поиска.")
            return
        self.results_display.clear()
        aggregated_results = {}
        if hasattr(self, 'image_path'):
            self.results_display.append("=== Обратный поиск изображения ===\n")
            self.results_display.append("Функциональность обратного поиска изображения не реализована.\n\n")
        if real_name:
            self.results_display.append("=== Поиск по имени ===\n")
            query = f"{real_name} {city}" if city else real_name
            name_search_results = self.search_by_name(query, language_param)
            aggregated_results['name_search'] = name_search_results
            if 'items' in name_search_results:
                for item in name_search_results['items']:
                    title = item.get('title')
                    link = item.get('link')
                    snippet = item.get('snippet')
                    self.results_display.append(f"{title}\n{snippet}\nСсылка: {link}\n\n")
            else:
                self.results_display.append("Нет результатов.\n\n")
        if social_names:
            self.results_display.append("=== Поиск по именам в соцсетях ===\n")
            for social_name in social_names:
                self.results_display.append(f"Поиск по: {social_name}\n")
                query = f"{social_name} {city}" if city else social_name
                social_results = self.search_by_name(query, language_param, social_network=True)
                aggregated_results.setdefault('social_search', {})[social_name] = social_results
                if 'items' in social_results:
                    for item in social_results['items']:
                        title = item.get('title')
                        link = item.get('link')
                        snippet = item.get('snippet')
                        self.results_display.append(f"{title}\n{snippet}\nСсылка: {link}\n\n")
                else:
                    self.results_display.append("Нет результатов.\n\n")
        if links:
            self.results_display.append("=== Информация с предоставленных ссылок ===\n")
            links_info = self.extract_info_from_links(links)
            aggregated_results['provided_links_info'] = links_info
            for link, info in links_info.items():
                self.results_display.append(f"Ссылка: {link}\nИнформация: {info}\n\n")
        self.aggregated_results = aggregated_results

    def search_by_name(self, name, language_param, social_network=False):
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'q': name,
            'key': GOOGLE_API_KEY,
            'cx': GOOGLE_CSE_ID,
            'num': 10
        }
        if language_param:
            params['lr'] = language_param
        if social_network:
            site_query = ' OR '.join([f'site:{site}' for site in SOCIAL_NETWORKS])
            params['q'] = f"{name} ({site_query})"
        response = requests.get(url, params=params)
        if response.status_code != 200:
            self.results_display.append(f"Ошибка при поиске по имени: {response.status_code}\n{response.text}\n\n")
            return {}
        return response.json()

    def extract_info_from_links(self, links):
        extracted_info = {}
        for link in links:
            try:
                response = requests.get(link, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text = soup.get_text(separator=' ', strip=True)
                    extracted_info[link] = text[:500] + '...' if len(text) > 500 else text
                else:
                    extracted_info[link] = f"Статус код: {response.status_code}"
            except Exception as e:
                extracted_info[link] = f"Ошибка: {str(e)}"
        return extracted_info

    def save_results(self):
        if not hasattr(self, 'aggregated_results') or not self.aggregated_results:
            QMessageBox.warning(self, "Предупреждение", "Нет результатов для сохранения.")
            return
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить результаты",
            "",
            "Текстовые файлы (*.txt)",
            options=options
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    if 'name_search' in self.aggregated_results:
                        f.write("=== Поиск по имени ===\n")
                        for item in self.aggregated_results['name_search'].get('items', []):
                            title = item.get('title')
                            link = item.get('link')
                            snippet = item.get('snippet')
                            f.write(f"{title}\n{snippet}\nСсылка: {link}\n\n")
                        f.write("\n")
                    if 'social_search' in self.aggregated_results:
                        f.write("=== Поиск по именам в соцсетях ===\n")
                        for social_name, results in self.aggregated_results['social_search'].items():
                            f.write(f"Поиск по: {social_name}\n")
                            if 'items' in results:
                                for item in results['items']:
                                    title = item.get('title')
                                    link = item.get('link')
                                    snippet = item.get('snippet')
                                    f.write(f"{title}\n{snippet}\nСсылка: {link}\n\n")
                            else:
                                f.write("Нет результатов.\n\n")
                        f.write("\n")
                    if 'provided_links_info' in self.aggregated_results:
                        f.write("=== Информация с предоставленных ссылок ===\n")
                        for link, info in self.aggregated_results['provided_links_info'].items():
                            f.write(f"Ссылка: {link}\nИнформация: {info}\n\n")
                QMessageBox.information(self, "Успех", f"Результаты успешно сохранены в {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = InfoSearchApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
