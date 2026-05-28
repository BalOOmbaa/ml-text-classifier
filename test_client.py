import requests

url = "http://localhost:8000/predict"  # замените на ваш Railway URL после деплоя
data = {"text": "Это приложение работает просто великолепно! Спасибо разработчикам."}
response = requests.post(url, json=data)
print(response.json())