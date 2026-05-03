from fastapi import APIRouter, Request

from server.app.services.printer_service import ConnectionStatus

router = APIRouter(prefix="/api", tags=["Status"])


@router.get("/status", response_model=dict)
async def get_status(request: Request):
    printer = request.app.state.printer_manager
    return {"connection": printer.status.value}
