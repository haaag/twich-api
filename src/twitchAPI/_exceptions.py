from __future__ import annotations

import httpx
import tenacity


class EnvValidationError(Exception):
    pass


class ExecutableNotFoundError(Exception):
    pass


class ItemNotPlaylableError(Exception):
    pass


class ChannelOfflineError(Exception):
    pass


class InvalidConfigFileError(Exception):
    pass


CONNECTION_EXCEPTION = (
    httpx.ConnectError,
    httpx.HTTPStatusError,
    httpx.ConnectTimeout,
)
EXCEPTIONS = (
    EnvValidationError,
    FileNotFoundError,
    NotImplementedError,
    tenacity.RetryError,
    InvalidConfigFileError,
    ChannelOfflineError,
)
