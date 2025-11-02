import uvicorn

from rest_api_test.infrastructure.fastapi.create_app import create_app
from rest_api_test.utils.config.settings import get_settings

settings = get_settings()
app = create_app()


def main():
    uvicorn.run(app, host="0.0.0.0", port=settings.api_port, use_colors=True)


if __name__ == "__main__":
    main()
