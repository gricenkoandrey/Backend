from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from io import BytesIO
from PIL import Image
from transformers import pipeline
from fastapi.responses import StreamingResponse

# Создание FastAPI приложения
app = FastAPI()

# Настройка CORS для разрешения запросов с Frontend
origins = [
    "https://backendg-ikvbvfejn-gricenkoandreys-projects.vercel.app/",  # Заменить на URL твоего Frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Разрешаем запросы с этих доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы HTTP
    allow_headers=["*"],  # Разрешаем все заголовки
)

# Инициализация модели для генерации изображения
generator = pipeline("text-to-image", model="CompVis/stable-diffusion-v-1-4-original")

# Модель для передачи текста
class Prompt(BaseModel):
    prompt: str

@app.post("/api/generate")
async def generate_image(prompt: Prompt):
    # Генерация изображения на основе текста
    image = generator(prompt.prompt)[0]

    # Преобразуем изображение в байты для отправки клиенту
    byte_io = BytesIO()
    image.save(byte_io, "PNG")
    byte_io.seek(0)

    return StreamingResponse(byte_io, media_type="image/png")
