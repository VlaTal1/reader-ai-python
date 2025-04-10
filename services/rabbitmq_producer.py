import asyncio
import logging
from typing import Optional

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractConnection, AbstractExchange

from core.config import settings

logger = logging.getLogger(__name__)


class RabbitMQProducer:
    def __init__(self):
        self.connection: Optional[AbstractConnection] = None
        self.channel: Optional[AbstractChannel] = None
        self.exchanges: dict[str, AbstractExchange] = {}
        self._connection_lock = asyncio.Lock()

    async def connect(self) -> None:
        async with self._connection_lock:
            if self.connection is not None and not self.connection.is_closed:
                return

            logger.info(f"Connecting to RabbitMQ: {settings.rabbitmq_url}")
            try:
                self.connection = await aio_pika.connect_robust(settings.rabbitmq_url)
                self.channel = await self.connection.channel()
                logger.info("Successfully connected to RabbitMQ")
            except Exception as e:
                logger.error(f"Failed to connect to RabbitMQ: {e}")
                if self.connection and not self.connection.is_closed:
                    await self.connection.close()
                self.connection = None
                raise

    async def get_exchange(self, exchange_name: str, exchange_type: str = "direct") -> AbstractExchange:
        if not exchange_name:
            return self.channel.default_exchange

        if exchange_name not in self.exchanges:
            exchange = await self.channel.declare_exchange(
                exchange_name,
                type=exchange_type,
                durable=True
            )
            self.exchanges[exchange_name] = exchange

        return self.exchanges[exchange_name]

    async def send_message(
            self,
            exchange_name: str,
            routing_key: str,
            message: str,
            exchange_type: str = "direct"
    ) -> None:
        if not self.connection or self.connection.is_closed:
            await self.connect()

        if not exchange_name:
            await self.channel.default_exchange.publish(
                aio_pika.Message(
                    body=message.encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=routing_key
            )
        else:
            exchange = await self.get_exchange(exchange_name, exchange_type)

            await exchange.publish(
                aio_pika.Message(
                    body=message.encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=routing_key
            )

        logger.info(f"Response sent: exchange={exchange_name}, routing_key={routing_key}")

    async def close(self) -> None:
        async with self._connection_lock:
            if self.connection and not self.connection.is_closed:
                logger.info("Closing connection to RabbitMQ")
                await self.connection.close()
                self.connection = None
                self.channel = None
                self.exchanges = {}
