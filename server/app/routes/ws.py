import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from server.app.dependencies import get_job_manager_ws as get_job_manager

logger = logging.getLogger(__name__)

router = APIRouter()


async def _forward(websocket: WebSocket, queue):
    try:
        while True:
            payload = await queue.get()
            await websocket.send_text(payload)
    except WebSocketDisconnect:
        pass


@router.websocket("/api/ws/jobs")
async def ws_jobs(websocket: WebSocket):
    await websocket.accept()
    job_manager = get_job_manager(websocket)
    queue = job_manager.subscribe()
    try:
        await _forward(websocket, queue)
    finally:
        job_manager.unsubscribe(queue)


@router.websocket("/api/ws/status")
async def ws_status(websocket: WebSocket):
    await websocket.accept()
    printer = websocket.app.state.printer_manager
    queue = printer.subscribe_status()
    try:
        while True:
            status = await queue.get()
            await websocket.send_json({"connection": status})
    except WebSocketDisconnect:
        pass
    finally:
        printer.unsubscribe_status(queue)
