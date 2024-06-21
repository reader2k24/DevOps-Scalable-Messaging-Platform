#!/bin/bash

# Скрипт для настройки окружения разработки в Linux

# Установка зависимостей
echo "Установка Python зависимостей..."
pip install -r backend/requirements.txt

echo "Установка зависимостей Node.js..."
cd frontend/
npm install
cd ..

# Настройка базы данных
echo "Настройка PostgreSQL базы данных..."
sudo -u postgres psql -f database/init.sql

echo "Настройка завершена!"
