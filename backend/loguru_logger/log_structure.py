import uuid

# from datetime import datetime
from typing import Optional
import datetime

from pydantic import BaseModel, Field, HttpUrl

# event_log (
#   id UUID PRIMARY KEY,
#   timestamp TIMESTAMP,
#   user_id UUID,
#   session_id UUID,
#   event_type TEXT,           -- e.g. 'item_viewed', 'added_to_cart'
#   context JSONB              -- free-form: item_id, cart_total, referrer, etc.
# )


class EventLog:
    id: uuid.UUID
    timestamp: datetime.date
    user_id: uuid.UUID
    session_id: uuid.UUID
    event_type: str
    context: dict


class RequestLog(BaseModel):
    timestamp: datetime = Field(
        default_factory=datetime.datetime.now(datetime.UTC)
    )

    # Request info
    method: str
    path: str
    http_version: str
    query_params: Optional[dict]
    body_excerpt: Optional[str]  # First 100–200 chars

    # Headers & client
    user_agent: str
    referer: Optional[HttpUrl] = None
    client_ip: str
    accept_language: str
    accept: str
    content_type: str
    x_api_key: str

    # Correlation / context
    correlation_id: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None

    # Optional performance / meta info
    duration_ms: Optional[float] = None
    status_code: Optional[int] = None
    response_size: Optional[int]

    # Logging meta
    log_level: str = "INFO"
