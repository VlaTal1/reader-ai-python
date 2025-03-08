import asyncio
import json
import logging
from typing import Callable, Optional

import aio_pika
from aio_pika.abc import AbstractIncomingMessage

from core.config import settings

logger = logging.getLogger(__name__)


class RabbitMQConsumer:
    def __init__(self):
        self.connection: Optional[aio_pika.Connection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self.queue: Optional[aio_pika.Queue] = None
        self.exchange: Optional[aio_pika.Exchange] = None
        self.callback = None
        self._connection_lock = asyncio.Lock()
        self._consuming = False
        self._connect_task = None

    async def connect(self) -> None:
        async with self._connection_lock:
            if self.connection is not None and not self.connection.is_closed:
                return

            logger.info(f"Connecting to RabbitMQ at {settings.rabbitmq_url}")
            try:
                self.connection = await aio_pika.connect_robust(settings.rabbitmq_url)

                self.channel = await self.connection.channel()

                self.exchange = await self.channel.declare_exchange(
                    settings.rabbitmq_exchange,
                    aio_pika.ExchangeType.DIRECT,
                    durable=True
                )

                self.queue = await self.channel.declare_queue(
                    settings.rabbitmq_queue,
                    durable=True
                )

                await self.queue.bind(
                    self.exchange,
                    routing_key=settings.rabbitmq_routing_key
                )

                logger.info("Successfully connected to RabbitMQ")
            except Exception as e:
                logger.error(f"Failed to connect to RabbitMQ: {e}")
                if self.connection and not self.connection.is_closed:
                    await self.connection.close()
                self.connection = None
                raise

    async def disconnect(self) -> None:
        async with self._connection_lock:
            self._consuming = False
            if self._connect_task:
                self._connect_task.cancel()
                try:
                    await self._connect_task
                except asyncio.CancelledError:
                    pass
                self._connect_task = None

            if self.connection and not self.connection.is_closed:
                logger.info("Closing RabbitMQ connection")
                await self.connection.close()
                self.connection = None
                self.channel = None
                self.queue = None
                self.exchange = None

    async def process_message(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            try:
                body = message.body.decode()
                logger.info(f"Received message: {body}")

                try:
                    payload = json.loads(body)
                except json.JSONDecodeError:
                    payload = body

                if self.callback:
                    await self.callback(payload)
                else:
                    logger.info(f"Processing message: {payload}")
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                raise

    async def start_consuming(self, callback: Optional[Callable] = None) -> None:
        if callback:
            self.callback = callback

        if self._consuming:
            return

        self._consuming = True

        async def connect_and_consume():
            while self._consuming:
                try:
                    await self.connect()
                    consumer_tag = await self.queue.consume(self.process_message)

                    while self._consuming and self.connection and not self.connection.is_closed:
                        await asyncio.sleep(1)

                except aio_pika.exceptions.ConnectionClosed:
                    logger.warning("RabbitMQ connection closed, reconnecting...")
                    await asyncio.sleep(5)
                except Exception as e:
                    logger.error(f"Error in RabbitMQ consumer: {e}")
                    await asyncio.sleep(5)

        self._connect_task = asyncio.create_task(connect_and_consume())
        logger.info("RabbitMQ consumer started")

    async def stop_consuming(self) -> None:
        logger.info("Stopping RabbitMQ consumer")
        await self.disconnect()


rabbitmq_consumer = RabbitMQConsumer()
