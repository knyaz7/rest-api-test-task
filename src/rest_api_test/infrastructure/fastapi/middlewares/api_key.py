import secrets

from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse


def register_api_key_middleware(
    app: FastAPI,
    *,
    header_name: str,
    api_key: str,
    allow_paths: set[str] = {"/api/docs", "/openapi.json", "/redoc"},
):
    @app.middleware("http")
    async def _(request: Request, call_next):
        if request.url.path in allow_paths:
            return await call_next(request)

        supplied_key = request.headers.get(header_name)

        if not supplied_key or not secrets.compare_digest(supplied_key, api_key):
            return JSONResponse(
                {"detail": "Invalid or missing API key"}, status_code=401
            )

        return await call_next(request)


def enable_api_key_in_swagger(app: FastAPI, header_name: str) -> None:
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

        components = schema.setdefault("components", {})
        sec = components.setdefault("securitySchemes", {})
        sec["APIKeyHeader"] = {
            "type": "apiKey",
            "in": "header",
            "name": header_name,
            "description": "Paste your API key to authorize requests.",
        }

        schema["security"] = [{"APIKeyHeader": []}]

        app.openapi_schema = schema
        return app.openapi_schema

    app.openapi = custom_openapi
