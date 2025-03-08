import os

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "FastAPI RabbitMQ Consumer"

    # RabbitMQ настройки
    rabbitmq_host: str = Field(default=os.getenv("RABBITMQ_HOST", "localhost"))
    rabbitmq_port: int = Field(default=int(os.getenv("RABBITMQ_PORT", 5672)))
    rabbitmq_user: str = Field(default=os.getenv("RABBITMQ_USER", "guest"))
    rabbitmq_password: str = Field(default=os.getenv("RABBITMQ_PASSWORD", "guest"))
    rabbitmq_queue: str = Field(default=os.getenv("RABBITMQ_QUEUE", "my_queue"))
    rabbitmq_exchange: str = Field(default=os.getenv("RABBITMQ_EXCHANGE", "my_exchange"))
    rabbitmq_routing_key: str = Field(default=os.getenv("RABBITMQ_ROUTING_KEY", "my_routing_key"))

    @property
    def rabbitmq_url(self) -> str:
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}/"


settings = Settings()
