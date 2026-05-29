FROM python:3.10-slim

WORKDIR /app

# Устанавливаем минимальные системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements
COPY requirements.txt .

# Устанавливаем CPU-версию torch
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Устанавливаем остальные зависимости и чистим кэш
RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

# Копируем код и модель
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]