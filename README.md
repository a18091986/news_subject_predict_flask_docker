# Определение категории новости

Стек:

ML: sklearn, pandas, numpy, lda

API: flask

Данные: парсинг новостей lenta.ru (категории: экономика, путешествия, спорт)

Задача: определить категорию новости (экономика, путешествия или спорт) по тексту или ссылке (ссылки только на новости lenta.ru)

Используемые признаки:

- текст новости (text)

Преобразования признаков: лемматизация

Модель: lda

### Клонируем репозиторий и создаем образ
```
$ git clone https://github.com/a18091986/news_subject_predict_flask_docker.git
$ cd news_subject_predict_flask_docker/subj_predict
$ docker build -t subject_predict .
```

### Запускаем контейнер

```
$ docker run -d -p 8180:8180 -p 8181:8181 -v <your_local_path_to_"news_subject_predict_flask_docker/files"_dir>:/app/files subject_predict
```

### Переходим на localhost:8181
