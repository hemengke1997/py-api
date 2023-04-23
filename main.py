import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.application import settings, urls
from src.application.env import Env, DEV
import typer
import uvicorn

shell_app = typer.Typer()


def create_app():
    app = FastAPI(
        title="minko's 第一个python项目",
    )
    if settings.ALLOW_CREDENTIALS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.ALLOW_ORIGINS,
            allow_credentials=settings.ALLOW_CREDENTIALS,
            allow_methods=settings.ALLOW_METHODS,
            allow_headers=settings.ALLOW_HEADERS,
        )
    for url in urls.urlpatterns:
        app.include_router(url["ApiRouter"], prefix=url["prefix"], tags=url["tags"])

    return app


@shell_app.command()
def run(mode: str = typer.Option(DEV, help=f"运行环境，可传: {Env.get_formatted_env()}")):
    os.environ["APP_ENV"] = mode
    Env(mode)
    uvicorn.run("main:create_app", port=8000, factory=True, reload=(mode == DEV))


if __name__ == "__main__":
    shell_app()
