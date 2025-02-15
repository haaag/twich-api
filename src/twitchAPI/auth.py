from __future__ import annotations

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

from twitchAPI._exceptions import EnvValidationError

log = logging.getLogger(__name__)


def _validate_credentials(credentials: dict[str, str]) -> None:
    """
    Validates that all required environment variables are set.

    Raises:
        EnvValidationError: If any required variable is not set.
    """
    for k, v in credentials.items():
        if not v:
            err_msg = f'Missing required environment variable: {k}'
            raise EnvValidationError(err_msg)


def load_envs(filepath: str | None = None) -> None:
    """Load envs if path"""
    if not filepath:
        log.info('env: no env filepath specified')
        log.info('env: loading from .env or exported env vars')
        load_dotenv()
        return

    envfilepath = Path(filepath).expanduser()
    if not envfilepath.exists():
        err = f'{envfilepath=!s} not found'
        raise EnvValidationError(err)
    if not envfilepath.is_file():
        err = f'{envfilepath=!s} is not a file'
        raise EnvValidationError(err)

    log.info(f'env: loading envs from {envfilepath=!s}')
    load_dotenv(dotenv_path=envfilepath.as_posix())


class UserAuthenticator(BaseModel):
    """
    A class to handle user authentication for accessing Twitch API.

    Attributes:
        access_token (str | None): The access token for authenticating API requests.
        client_id (str | None): The client ID for the Twitch application.
        user_id (str | None): The user ID associated with the Twitch account.
        ok (bool): A flag indicating whether the credentials are valid. Default is False.

    Methods:
        validation(): Validates the credentials by checking the environment variables.
        load(file: str | None): Loads environment variables from a file and initializes
                                the class with the loaded credentials.
    """

    access_token: str | None
    client_id: str | None
    user_id: str | None
    ok: bool = False

    def validation(self) -> None:
        log.debug('validating envs')
        _validate_credentials(self.dict(exclude={'ok'}))
        self.ok = True

    @classmethod
    def load(cls, file: str | None = None) -> UserAuthenticator:
        load_envs(file)
        return cls(
            access_token=os.environ.get('TWITCH_ACCESS_TOKEN'),
            client_id=os.environ.get('TWITCH_CLIENT_ID'),
            user_id=os.environ.get('TWITCH_USER_ID'),
        )
