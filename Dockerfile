# 1. Используем официальный Python-образ
FROM python:3.11-slim

# 2. Устанавливаем рабочую директорию
WORKDIR /app

# 3. Копируем файлы проекта
COPY . .

# 4. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 5. Указываем порт, на котором работает Flask
EXPOSE 5000

# 6. Команда запуска приложения
CMD ["python", "app.py"]