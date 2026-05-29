# ML Text Classifier (Russian Sentiment Analysis)

Сквозная ML-система для анализа тональности русскоязычных текстов. Включает:

- **REST API** на FastAPI с локальной моделью `cointegrated/rubert-tiny2` (sentiment analysis).
- **Telegram-бота** для удобного взаимодействия.
- **Docker-контейнеризацию** для воспроизводимости.
- **CI/CD** (GitHub Actions) – автоматическая сборка и публикация образа в GitHub Container Registry.

## Стек технологий

- Python 3.10
- FastAPI + Uvicorn
- Transformers (Hugging Face) + PyTorch (CPU)
- Docker
- GitHub Actions (CI/CD)
- Telegram Bot API (python-telegram-bot v13.15)

## Запуск API через Docker (основной способ)

```bash
cd ml-text-classifier
docker build -t ml-classifier .
docker run -d --name ml-api -p 8000:8000 ml-classifier

## Управление контейнером

```bash
docker start ml-api
docker stop ml-api
docker rm ml-api
docker logs ml-api

## Запуск Telegram-бота

```bash
set BOT_TOKEN=
set API_URL=http://localhost:8000/predict
python bot.py

## Работа с Git

```bash
git status
git add .
git commit -m ""
git push origin main
