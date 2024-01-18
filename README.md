Первая задача:

Файлы конфигурации лежат в папке settings:
1) Конфигурация сервиса: settings/config.json
2) Конфигурация логгера: settings/logging.conf

При желании можно примонтировать свои файлы конфигурации
Пути до файлов конфигурации задаются переменными SRVC_CONFIG(конфигурация сервера) и SRVC_LOG(конфигурация логгера)

Запуск в докере производится командой
```commandline
docker compose up --build
```
после запуска сервис доступен по адресу http://127.0.0.1:8010

Документация swagger доступна по адресу http://127.0.0.1:8010/docs

Поле phone валидируется регулярным выражением.
В поле address можно записать любые текстовые данные



Решение второй задачи:

```
UPDATE full_names SET status = short_names.status
FROM short_names
WHERE full_names.name ILIKE short_names.name || '.%'
```