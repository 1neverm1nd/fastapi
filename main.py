from fastapi import FastAPI, Path, Query, Body, status
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse, RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid

# Инициализация приложения FastAPI
app = FastAPI()

# Статические файлы (каталог public)
app.mount("/static", StaticFiles(directory="public"), name="static")

# Условная база данных пользователей
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.id = str(uuid.uuid4())

people = [Person("Tom", 38), Person("Bob", 42), Person("Sam", 28)]

# Вспомогательная функция для поиска пользователя
def find_person(id):
    for person in people:
        if person.id == id:
            return person
    return None

# Модели для API
class User(BaseModel):
    name: str
    age: int

# task 1: Создание простого приложения, возвращающего HTML
@app.get("/", response_class=HTMLResponse)
def read_root():
    return "<h2>Hello, my name is danikoooo!</h2>"

# 2: Работа с путями (параметры пути)
@app.get("/users/{id}")
def get_user_by_id(id: int = Path(..., description="ID пользователя")):
    return {"user_id": id}

# task 3: Работа со строками запроса
@app.get("/items")
def read_item(name: str = Query(None, min_length=2), age: int = Query(None, ge=18)):
    return {"name": name, "age": age}

# tasl 4: Отправка JSON ответа
@app.get("/json")
def return_json():
    return {"message": "Hello, JSON!"}

# task 5: Отправка HTML ответа
@app.get("/html", response_class=HTMLResponse)
def return_html():
    return "<h2>Hello, this is HTML content!</h2>"

#task6: Отправка простого текста
@app.get("/text", response_class=PlainTextResponse)
def return_text():
    return "Hello, World!"

# task 7: Отправка файлов с сервера
@app.get("/download")
def download_file():
    return FileResponse("path_to_file.txt", media_type="text/plain", filename="download.txt")

# task 8: Работа с статусными кодами
@app.get("/notfound", status_code=status.HTTP_404_NOT_FOUND)
def not_found():
    return {"message": "Resource Not Found"}

#  9: Переадресация (редирект)
@app.get("/old-page")
def old_page():
    return RedirectResponse("/new-page")

@app.get("/new-page", response_class=PlainTextResponse)
def new_page():
    return "This is the new page!"

#  10: Статические файлы
@app.get("/static-file")
def get_static():
    return FileResponse("public/index.html")

#  11: Получение данных запроса (JSON)
@app.post("/create-user")
def create_user(user: User):
    people.append(Person(user.name, user.age))
    return {"message": f"User {user.name} added!"}

#  12: Простейший API для CRUD операций
@app.get("/api/users")
def get_people():
    return people

@app.get("/api/users/{id}")
def get_person(id: str):
    person = find_person(id)
    if not person:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found"})
    return person

@app.post("/api/users")
def create_person(user: User):
    person = Person(user.name, user.age)
    people.append(person)
