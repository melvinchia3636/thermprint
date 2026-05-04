import asyncio
import logging

logger = logging.getLogger(__name__)


class BroadcastService:
    def __init__(self):
        self._listeners: list[asyncio.Queue[str]] = []

    def subscribe(self, initial: str | None = None) -> asyncio.Queue[str]:
        q: asyncio.Queue[str] = asyncio.Queue()
        if initial is not None:
            q.put_nowait(initial)
        self._listeners.append(q)
        return q

    def unsubscribe(self, q: asyncio.Queue[str]):
        self._listeners.remove(q)

    def publish(self, payload: str):
        for q in self._listeners:
            q.put_nowait(payload)
