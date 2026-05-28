import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="ML Text Classifier (Russian)",
    description="Сквозная ML-система для классификации текстовых обращений с использованием MLOps/DevOps практик",
    version="1.0.0"
)

class TextRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    label: str          # класс: например, "positive" или "negative"
    confidence: float   # уверенность модели

# -------------------------------------------------------------------
# 1. Выбор модели Hugging Face (русскоязычная для тональности)
#    Для демонстрации используется модель sentiment analysis.
#    В реальном проекте можно заменить на модель классификации обращений.
# -------------------------------------------------------------------
# Модель cointegrated/rubert-tiny2 возвращает метки "positive"/"negative"
# Бесплатный Inference API (без токена работает, но с ограничением ~30 запросов/мин)
HF_API_URL = "https://api-inference.huggingface.co/models/cointegrated/rubert-tiny2"
# Если хотите стабильнее, зарегистрируйтесь на huggingface.co и получите токен
HF_TOKEN = os.getenv("HF_TOKEN", "")   # можно оставить пустым

def call_hf_inference(text: str):
    """Отправляет текст в Hugging Face Inference API и возвращает (label, score)."""
    headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
    payload = {"inputs": text}
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=10)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail=f"HF API error: {response.text}")
        result = response.json()
        # Ожидаем список вида [{'label': 'positive', 'score': 0.98}, ...]
        if isinstance(result, list) and len(result) > 0:
            best = max(result, key=lambda x: x['score'])
            return best['label'], best['score']
        else:
            raise HTTPException(status_code=502, detail="Unexpected response format")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"ML service unavailable: {str(e)}")

# -------------------------------------------------------------------
# 2. Эндпоинты API
# -------------------------------------------------------------------
@app.get("/health")
def health():
    """Проверка работоспособности сервиса."""
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: TextRequest):
    """
    Классифицирует переданный текст.
    Пример запроса: {"text": "Это отличный сервис!"}
    Пример ответа: {"label": "positive", "confidence": 0.987}
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Empty text")
    label, confidence = call_hf_inference(request.text)
    return PredictionResponse(label=label, confidence=confidence)

# -------------------------------------------------------------------
# 3. Для локального запуска: uvicorn app:app --reload
# -------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)