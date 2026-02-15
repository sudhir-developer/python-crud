
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from models import User
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form
app = FastAPI()
User.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    user_name = "Sudhir"
    age = 25
    products = ["Laptop", "Phone", "Headphones"]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Home",
        "name": user_name,
        "age": age,
        "products": products
    })


@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("about.html", {
        "request": request,
        "title": "About"
    })


@app.get("/contact", response_class=HTMLResponse)
def contact(request: Request):
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "title": "Contact"
    })

@app.get("/register", response_class=HTMLResponse)
def show_register_form(request: Request):
    return templates.TemplateResponse("register.html", {
        "request": request,
        "title": "Register"
    })
@app.get("/success", response_class=HTMLResponse)
def success_page(request: Request):
    
    db: Session = SessionLocal()
    users = db.query(User).all()   # 👈 sab users fetch karega
    db.close()

    return templates.TemplateResponse("success.html", {
        "request": request,
        "title": "Success",
        "users": users
    })

@app.post("/register")
def register_user(name: str = Form(...), age: int = Form(...)):

    db: Session = SessionLocal()

    new_user = User(name=name, age=age)
    db.add(new_user)
    db.commit()
    db.close()

    return RedirectResponse(url="/success", status_code=303)



@app.get("/users")
def get_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()

    user_list = []

    for user in users:
        user_list.append({
            "id": user.id,
            "name": user.name,
            "age": user.age
        })

    return JSONResponse(content=user_list)