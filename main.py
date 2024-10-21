from fastapi import FastAPI, Path, Query, Body, status, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid

# Инициализация приложения FastAPI
app = FastAPI()


# Класс Person для пользователей
class Person:
    def __init__(self, name, age, subscribe=None):
        self.name = name
        self.age = age
        self.subscribe = subscribe
        self.id = str(uuid.uuid4())


people = []  # Список для хранения пользователей


# Показ формы для создания пользователя
@app.get("/create-user", response_class=HTMLResponse)
def get_create_user_form():
    return FileResponse("public/create_user.html")


# Обработка отправленных данных
@app.post("/create-user", response_class=HTMLResponse)
def create_user(name: str = Form(...), age: int = Form(...), subscribe: str = Form(None)):
    subscription_status = "Subscribed" if subscribe else "Not subscribed"
    new_user = Person(name, age, subscription_status)
    people.append(new_user)  # Добавляем пользователя в список

    # Возвращаем подтверждение
    return f"""
    <html>
        <body>
            <h2>User {name} (Age: {age}) created successfully!</h2>
            <p>Newsletter Subscription: {subscription_status}</p>
            <a href="/create-user">Create another user</a><br>
            <a href="/api/users">View all users in API</a>
        </body>
    </html>
    """


# Показ всех пользователей в API
@app.get("/api/users", response_class=JSONResponse)
def get_all_users():
    return [{"name": person.name, "age": person.age, "subscribe": person.subscribe} for person in people]


# Показ всех пользователей на странице HTML
@app.get("/users", response_class=HTMLResponse)
def get_all_users_html():
    if people:
        users_list = "".join([f"<li>{user.name} (Age: {user.age}) - {user.subscribe}</li>" for user in people])
    else:
        users_list = "<li>No users found</li>"

    return f"""
    <html>
        <head>
            <title>User List</title>
            <link rel="stylesheet" href="/static/styles.css">
        </head>
        <body>
            <h2>All Users</h2>
            <ul>
                {users_list}
            </ul>
            <a href="/create-user">Create another user</a>
        </body>
    </html>
    """


# Статические файлы (каталог public)
app.mount("/static", StaticFiles(directory="public"), name="static")


# Главная страница
@app.get("/", response_class=HTMLResponse)
def read_root():
    return FileResponse("public/index.html")


# Пример других маршрутов
@app.get("/json", response_class=JSONResponse)
def return_json():
    return {"message": "Hello, JSON!"}


@app.get("/html", response_class=HTMLResponse)
def return_html():
    return "<h2>Hello, this is HTML content!</h2>"


@app.get("/text", response_class=PlainTextResponse)
def return_text():
    return "Hello, World!"


# Отправка файлов с сервера
@app.get("/download")
def download_file():
    return FileResponse("path_to_file.txt", media_type="text/plain", filename="download.txt")


# Маршрут для 404
@app.get("/notfound", status_code=status.HTTP_404_NOT_FOUND)
def not_found():
    return {"message": "Resource Not Found"}


# Редирект на новую страницу
@app.get("/old-page")
def old_page():
    return RedirectResponse("/new-page")


@app.get("/new-page", response_class=PlainTextResponse)
def new_page():
    return "This is the new page!"


# CRUD API для работы с пользователями
@app.get("/api/users/{id}")
def get_person(id: str):
    person = next((person for person in people if person.id == id), None)
    if not person:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found"})
    return person


@app.post("/api/users")
def create_person(user: BaseModel):
    person = Person(user.name, user.age)
    people.append(person)
    return person


@app.put("/api/users/{id}")
def update_person(id: str, user: BaseModel):
    person = next((person for person in people if person.id == id), None)
    if not person:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found"})
    person.name = user.name
    person.age = user.age
    return person


@app.delete("/api/users/{id}")
def delete_person(id: str):
    person = next((person for person in people if person.id == id), None)
    if not person:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found"})
    people.remove(person)
    return {"message": "User deleted"}
