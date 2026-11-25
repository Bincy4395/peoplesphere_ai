from fastapi import FastAPI
from routers import employees, departments, projects
from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import get_db
from fastapi.middleware.cors import CORSMiddleware
from routers.chat import router as chat_router
from routers.documents import router as documents_router
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="PeopleSphere AI",
    description="AI-Powered Employee Management System",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees.router)
app.include_router(departments.router)
app.include_router(projects.router)
app.include_router(chat_router)
app.include_router(documents_router)

@app.get("/")
def home():
    return {
        "message":"WelcomePeopleSphere AI",
        "status": 200
    }


@app.get("/health/database")
def check_database(db: Session = Depends(get_db)):

    database_name = db.execute(
        text("SELECT DATABASE()")
    ).scalar_one()

    return {
        "status": "Connected successfully",
        "database": database_name
    }


# --------------------------------------------------
# 1. Customize OpenAPI Schema for Swagger File Uploads
# --------------------------------------------------

def custom_openapi():

    # --------------------------------------------------
    # 1.1 Return Cached Schema
    # --------------------------------------------------

    if app.openapi_schema:
        return app.openapi_schema

    # --------------------------------------------------
    # 1.2 Generate OpenAPI Schema
    # --------------------------------------------------

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes
    )

    # --------------------------------------------------
    # 1.3 Convert OpenAPI 3.1 File Schema to Binary Format
    # --------------------------------------------------

    def convert_file_schema(schema):

        if isinstance(schema, dict):

            if (
                schema.get("type") == "string"
                and schema.get("contentMediaType")
                == "application/octet-stream"
            ):
                schema.pop("contentMediaType", None)
                schema["format"] = "binary"

            for value in schema.values():
                convert_file_schema(value)

        elif isinstance(schema, list):

            for item in schema:
                convert_file_schema(item)

    convert_file_schema(openapi_schema)

    # --------------------------------------------------
    # 1.4 Set OpenAPI Version for Swagger Compatibility
    # --------------------------------------------------

    openapi_schema["openapi"] = "3.0.3"

    # --------------------------------------------------
    # 1.5 Cache and Return Schema
    # --------------------------------------------------

    app.openapi_schema = openapi_schema

    return app.openapi_schema


# --------------------------------------------------
# 2. Apply Custom OpenAPI Schema
# --------------------------------------------------

app.openapi = custom_openapi
