from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import os

app = FastAPI(title="ML Text Classifier (Russian Model)")

class TextRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    label: str
    confidence: float

# Загружаем модель из локальной папки './model'
MODEL_PATH = "./model"

print("Loading model from local folder...")
classifier = pipeline("sentiment-analysis", model=MODEL_PATH, tokenizer=MODEL_PATH)
print("Model loaded successfully!")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: TextRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Empty text")
    result = classifier(request.text)[0]
    label_map = {"LABEL_0": "negative", "LABEL_1": "positive"}
    human_label = label_map.get(result['label'], result['label'])
    return PredictionResponse(label=human_label, confidence=result['score'])
