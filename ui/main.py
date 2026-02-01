# import sys
# import os

# # Add the project root to sys.path to allow running this script directly
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from fastapi import FastAPI, Request
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles

# app = FastAPI()
# templates = Jinja2Templates(directory="ui/templates")
# app.mount("/static", StaticFiles(directory="ui/static"), name="static")

# @app.get("/login", response_class=HTMLResponse)
# def login(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("ui.main:app", host="0.0.0.0", port=8002, reload=True)
