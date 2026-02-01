from fastapi import FastAPI
from app.api.v1.employees import router as employee_router
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.db.model import Base
from app.db.session import engine
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request

# Create tables
Base.metadata.create_all(bind=engine)


app = FastAPI(title="Employee Management System")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Page routes (must be before API routes to avoid conflicts)
@app.get("/", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/employees", response_class=HTMLResponse)
def employees_page(request: Request):
    return templates.TemplateResponse("employees.html", {"request": request})

@app.get("/create-employee", response_class=HTMLResponse)
def create_employee_page(request: Request):
    return templates.TemplateResponse("create_employee.html", {"request": request})

@app.get("/users", response_class=HTMLResponse)
def users_page(request: Request):
    return templates.TemplateResponse("users.html", {"request": request})

@app.get("/create-user", response_class=HTMLResponse)
def create_user_page(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})

# API routes
app.include_router(employee_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")


# @app.get("/")
# def home():
#     return {"hi"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)