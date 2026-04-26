#!/bin/bash

# Останавливать скрипт при любой ошибке
set -e

echo " Начинаю настройку проекта..."

# 1. Инициализация DVC (если еще не сделана)
if [ ! -d ".dvc" ]; then
    dvc init --no-scm
    echo " DVC инициализирован."
fi

# 2. Настройка удаленного хранилища
dvc remote add -d myremote s3://datasets -f
dvc remote modify myremote endpointurl http://147.45.147.94:9000

# 3. Настройка ключей доступа
dvc remote modify myremote access_key_id admin
dvc remote modify myremote secret_access_key password
echo "Удаленное хранилище настроено."

# 4. Добавление данных под контроль DVC
if [ -f "titanic.csv" ]; then
    dvc add titanic.csv
    echo " Файл titanic.csv добавлен в DVC."
else
    echo " Ошибка: Файл titanic.csv не найден в папке!"
fi

# 5. Фиксация изменений в Git
git add .dvc/config .gitignore titanic.csv.dvc
git diff --staged --quiet || git commit -m "Автоматическая настройка DVC и данных"

echo " Все настройки зафиксированы в Git."

# 6. Попытка отправить данные ( сервер был недоступен)
echo " Попытка отправить данные на сервер..."
dvc push || echo " Сервер недоступен, но локальная настройка завершена успешно!"

echo " Скрипт завершил работу!"
