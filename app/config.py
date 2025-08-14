import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass(frozen=True)
class MySQLConfig:
    host: str
    port: int
    user: str
    password: str
    database: str
    connect_timeout: int = 10


class Config:
    def __init__(self) -> None:
        load_dotenv()
        self.mysql = MySQLConfig(
            host=os.getenv("MYSQL_HOST", "127.0.0.1"),
            port=int(os.getenv("MYSQL_PORT", "3306")),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "leverx_homework_3"),
            connect_timeout=int(os.getenv("MYSQL_CONNECT_TIMEOUT", "10")),
        )


def get_config() -> Config:
    return Config()
