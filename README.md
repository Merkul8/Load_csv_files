# Load_csv_files
Load csv files with view colums

Проект выполнен с помощью фреймворка Django, были созданы две модели для работы с файлами и отображения дополнительной инфорации в шаблонах.
На сайте присутствует авторизация и аутентификация.
Загружаемые файлы фильтруются, есть возможность добавлять файлы только формата .csv, и при том - не пустые.
Файлы обрабатываются с помощью библиотеки csv.
Так же был создан образ на основе django приложения.
Запуск проекта: 
Первый способ: в директории csvsite/ с помощью команды "python manage.py runserver".
Второй способ: docker-compose up
