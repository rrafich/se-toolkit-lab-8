"""Settings for the observability MCP server."""

import os
from pydantic import BaseModel


class ObsSettings(BaseModel):
    """Observability service settings."""
    victorialogs_url: str = "http://victorialogs:9428"
    victoriatraces_url: str = "http://victoriatraces:10428"
    default_time_window: str = "1h"


def resolve_settings() -> ObsSettings:
    """Resolve settings from environment variables."""
    return ObsSettings(
        victorialogs_url=os.environ.get(
            "NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428"
        ),
        victoriatraces_url=os.environ.get(
            "NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:10428"
        ),
        default_time_window=os.environ.get("OBS_DEFAULT_TIME_WINDOW", "1h"),
    )
