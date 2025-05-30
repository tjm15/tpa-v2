"""
Shared Redis-backed cache and Celery task utilities for LLM orchestration.
Intended for use by both backend and tpa_ai_engine.
"""
import os
import redis
from celery import Celery, Task
import json
import asyncio
from typing import Any, Optional, Awaitable

# Redis config from env or defaults
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Celery config from env or defaults
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)

# Redis cache interface
class LLMRedisCache:
    def __init__(self, prefix: str = "llm_cache:"):
        self.r = redis.Redis.from_url(REDIS_URL)
        self.prefix = prefix

    def _key(self, key: str) -> str:
        return f"{self.prefix}{key}"

    def get(self, key: str) -> Optional[Any]:
        value = self.r.get(self._key(key))
        if asyncio.iscoroutine(value):
            value = asyncio.run(value)
        elif isinstance(value, Awaitable):
            # Awaitables that are not coroutines cannot be run with asyncio.run
            # You may want to handle them differently or raise an error
            raise TypeError("Cannot handle non-coroutine Awaitable in sync context")
        if value is None:
            return None
        if isinstance(value, (bytes, bytearray)):
            value = value.decode('utf-8')
        if not isinstance(value, str):
            return None
        return json.loads(value)

    def set(self, key: str, value: Any, ex: int = 3600):
        self.r.set(self._key(key), json.dumps(value), ex=ex)

    def delete(self, key: str):
        self.r.delete(self._key(key))

# Celery app factory
_celery_app = None

def get_celery_app(name: str = "llm_tasks") -> Celery:
    global _celery_app
    if _celery_app is None:
        _celery_app = Celery(
            name,
            broker=CELERY_BROKER_URL,
            backend=CELERY_RESULT_BACKEND
        )
        _celery_app.conf.update(
            task_serializer='json',
            result_serializer='json',
            accept_content=['json'],
            timezone='UTC',
            enable_utc=True,
        )
    return _celery_app

# Example base task for LLM calls
class LLMTask(Task):
    abstract = True
    cache = LLMRedisCache()

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        # Optionally store result in cache
        cache_key = kwargs.get('cache_key')
        if cache_key:
            self.cache.set(cache_key, retval)

# Usage:
# from shared_utils.llm_task_queue import get_celery_app, LLMTask, LLMRedisCache
# app = get_celery_app()
# @app.task(base=LLMTask)
# def my_llm_task(...): ...
