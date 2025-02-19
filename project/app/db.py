import logging  # new
import os

from fastapi import FastAPI
from tortoise import Tortoise, run_async  # new
from tortoise.contrib.fastapi import register_tortoise

log = logging.getLogger("uvicorn") # new


TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["app.models.user", "app.models.tortoise", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.models.tortoise", "app.models.user"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )


# new
async def generate_schema() -> None:
    log.info("Initializing Tortoise...")

    await Tortoise.init(
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["models.user", "models.tortoise"]},
    )
    log.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


# new
if __name__ == "__main__":
    run_async(generate_schema())