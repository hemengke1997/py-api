from enum import Enum
from dotenv import dotenv_values
from os.path import join, dirname


class Environment(str, Enum):
    DEV = "dev"
    TEST = "test"
    PROD = "prod"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


global_config = {}


class Env(metaclass=Singleton):
    def __init__(self, mode: str):
        self.mode = mode
        config = {**dotenv_values(join(dirname(__file__), f"../.env.{mode}")), "APP_ENV": mode}
        print(config, "ENV CONFIG")
        self.set_config(config)

    @staticmethod
    def get_formatted_env() -> str:
        return " | ".join(Environment)

    @staticmethod
    def set_config(c):
        global global_config
        global_config = c

    @staticmethod
    def get_config() -> dict:
        return global_config
