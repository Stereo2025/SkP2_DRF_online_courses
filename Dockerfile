FROM python:3.10-slim

WORKDIR /SkP2_DRF_online_courses

# Копируем и устанавливаем зависимости
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем только необходимые файлы
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
