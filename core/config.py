import os

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "Test Generation Service"

    # RabbitMQ settings
    rabbitmq_host: str = Field(default=os.getenv("RABBITMQ_HOST", "localhost"))
    rabbitmq_port: int = Field(default=int(os.getenv("RABBITMQ_PORT", 5672)))
    rabbitmq_user: str = Field(default=os.getenv("RABBITMQ_USER", "guest"))
    rabbitmq_password: str = Field(default=os.getenv("RABBITMQ_PASSWORD", "guest"))
    rabbitmq_request_queue: str = Field(default=os.getenv("RABBITMQ_REQUEST_QUEUE", "test_generation_request"))
    rabbitmq_exchange: str = Field(default=os.getenv("RABBITMQ_EXCHANGE", "test_generation_exchange"))
    rabbitmq_response_queue: str = Field(default=os.getenv("RABBITMQ_RESPONSE_QUEUE", "test_generation_response"))
    rabbitmq_routing_key: str = Field(default=os.getenv("RABBITMQ_ROUTING_KEY", "generate_test"))

    # MinIO settings
    minio_endpoint: str = Field(default=os.getenv("MINIO_ENDPOINT", "localhost:9000"))
    minio_access_key: str = Field(default=os.getenv("MINIO_ACCESS_KEY", "minioadmin"))
    minio_secret_key: str = Field(default=os.getenv("MINIO_SECRET_KEY", "minioadmin"))
    minio_bucket: str = Field(default=os.getenv("MINIO_BUCKET", "books"))
    minio_secure: bool = Field(default=bool(int(os.getenv("MINIO_SECURE", "0"))))

    # Temporary file storage
    temp_dir: str = Field(default=os.getenv("TEMP_DIR", "/tmp"))

    @property
    def rabbitmq_url(self) -> str:
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}/"


settings = Settings()
