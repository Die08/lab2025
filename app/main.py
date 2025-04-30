from fastapi import FastAPI
from routers import books, frontend
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.include_router(books.router, tags=["books"])
app.include_router(frontend.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


if __name__ == "__main__":
    # TODO: if you launch the application from here, you must modify the
    #  relative path to the static folder (in this file) from "app/static" to
    #  "static" and the relative path to the templates folder (in
    #  routers/frontend.py file) from "app/templates" to "templates".
    import uvicorn
    uvicorn.run("main:app", reload=True)
