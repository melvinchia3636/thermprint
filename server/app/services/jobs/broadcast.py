"""Pub/sub broadcast mechanism for real-time event distribution.

Provides a simple in-process publish-subscribe pattern using asyncio queues.
Used by both :class:`JobManager` (job status updates) and :class:`PrinterManager`
(connection status updates) to push live events to WebSocket clients.
"""

import asyncio


class BroadcastService:
    """Fan-out broadcaster that delivers string payloads to all active subscribers."""

    def __init__(self):
        self._listeners: list[asyncio.Queue[str]] = []

    def subscribe(self, initial: str | None = None) -> asyncio.Queue[str]:
        """Register a new subscriber queue.

        If *initial* is provided it is enqueued immediately so the caller
        receives the current state on connect.
        """
        q: asyncio.Queue[str] = asyncio.Queue()
        if initial is not None:
            q.put_nowait(initial)
        self._listeners.append(q)
        return q

    def unsubscribe(self, q: asyncio.Queue[str]):
        """Remove a previously registered subscriber queue."""
        self._listeners.remove(q)

    def publish(self, payload: str):
        """Push a string payload to every active subscriber."""
        for q in self._listeners:
            q.put_nowait(payload)
