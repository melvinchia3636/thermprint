from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


FIELD_LABELS = {
    "width": "Width",
    "quality": "Quality",
    "speed": "Speed",
    "energy": "Energy",
    "contrast": "Contrast",
    "gamma": "Gamma",
    "rotate": "Rotation",
    "chunk_rows": "Chunk rows",
    "chunk_delay": "Chunk delay",
    "feed": "Paper feed",
}

RULE_MESSAGES = {
    "less_than_equal": "must be at most {le}",
    "greater_than_equal": "must be at least {ge}",
    "less_than": "must be less than {lt}",
    "greater_than": "must be greater than {gt}",
    "value_error": "invalid value",
    "missing": "is required",
    "string_too_short": "must be at least {min_length} characters",
    "string_too_long": "must be at most {max_length} characters",
}


def _format_error(err) -> str:
    field = err["loc"][-1] if err["loc"] else "body"
    label = FIELD_LABELS.get(field, str(field).replace("_", " ").title())
    input_val = err.get("input")
    ctx = err.get("ctx", {}) or {}
    rule = err["type"].split(".")[-1]
    msg_template = RULE_MESSAGES.get(rule, err.get("msg", "invalid"))
    try:
        detail = msg_template.format(**ctx)
    except KeyError:
        detail = err.get("msg", "invalid")
    if input_val is not None:
        return f"{label} {detail} (got {input_val!r})"
    return f"{label} {detail}"


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [_format_error(e) for e in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors},
    )
