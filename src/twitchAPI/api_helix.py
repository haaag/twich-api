from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any

import httpx
from httpx import URL
from tenacity import before_sleep_log
from tenacity import retry
from tenacity import retry_if_not_exception_type
from tenacity import stop_after_attempt
from tenacity import wait_fixed

from twitchAPI import constants
from twitchAPI import utils

if TYPE_CHECKING:
    from twitchAPI._types import HeaderTypes
    from twitchAPI._types import QueryParamTypes
    from twitchAPI._types import TwitchApiResponse
    from twitchAPI.auth import UserAuthenticator


log = logging.getLogger(__name__)


@dataclass
class HelixAPI:
    def __init__(self, auth: UserAuthenticator) -> None:
        self.auth = auth
        self.base_url = constants.TWITCH_HELIX_BASE_URL
        self.client = httpx.AsyncClient(headers=self._get_request_headers())
        self.channels = HelixChannels(api=self)
        self.content = HelixContent(api=self)

    def __post_init__(self) -> None:
        if not self.auth.ok:
            self.auth.validation()

    def _get_request_headers(self) -> HeaderTypes:
        return {
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': self.auth.client_id,
            'Authorization': f'Bearer {self.auth.access_token}',
        }

    def _set_params(self, params: QueryParamTypes, requested_items: int) -> QueryParamTypes:
        """Sets the parameters for the request."""
        params['first'] = min(constants.MAX_ITEMS_PER_REQUEST, requested_items)
        log.debug('params: %s', params)
        return params

    async def close(self) -> None:
        """Properly close the HTTPX async client."""
        if self.client and not self.client.is_closed:
            await self.client.aclose()

    async def send_request(self, url: URL, query_params: QueryParamTypes, timeout: int = 5) -> httpx.Response:
        """Sends a request to the Twitch Helix API."""
        r = await self.client.get(url, params=query_params, timeout=timeout)
        r.raise_for_status()
        return r

    def _has_pagination(self, data: TwitchApiResponse) -> bool:
        return data.get('pagination', {}).get('cursor') is not None

    @retry(
        stop=stop_after_attempt(constants.MAX_RETRY_ATTEMPTS),
        wait=wait_fixed(constants.RETRY_DELAY),
        before_sleep=before_sleep_log(log, logging.WARN),
        retry=retry_if_not_exception_type(httpx.ConnectError),
    )
    async def request_get(
        self,
        endpoint_url: URL,
        params: QueryParamTypes,
        max_items: int = constants.DEFAULT_REQUESTED_ITEMS,
        items_collected: int = 0,
    ) -> TwitchApiResponse:
        # TODO: this method handles `pagination`, remove the logic?
        # If pagination is needed, maybe, it should be handled externally.
        url = self.base_url.join(endpoint_url)
        query_params_dict = self._set_params(params, max_items)
        response = await self.send_request(url, query_params_dict, timeout=10)
        data = response.json()
        items_collected += len(data['data'])

        if not self._has_pagination(data):
            return data

        if max_items >= items_collected:
            next_cursor = data['pagination']['cursor']
            remaining_items = max_items - items_collected

            params['after'] = next_cursor
            params['first'] = min(constants.MAX_ITEMS_PER_REQUEST, remaining_items)
            more_data = await self.request_get(
                endpoint_url=endpoint_url,
                params=params,
                max_items=max_items,
                items_collected=items_collected,
            )
            data['data'].extend(more_data['data'][:remaining_items])
        return data

    @retry(
        stop=stop_after_attempt(constants.MAX_RETRY_ATTEMPTS),
        wait=wait_fixed(constants.RETRY_DELAY),
        before_sleep=before_sleep_log(log, logging.WARN),
        retry=retry_if_not_exception_type(httpx.ConnectError),
    )
    async def request_get_no_pagination(
        self,
        endpoint_url: URL,
        params: QueryParamTypes,
        max_items: int = constants.DEFAULT_REQUESTED_ITEMS,
    ) -> TwitchApiResponse:
        """Send a GET request and return the JSON response."""
        url = self.base_url.join(endpoint_url)
        query_params_dict = self._set_params(params, max_items)
        response = await self.send_request(url, query_params_dict, timeout=10)
        return response.json()


class HelixContent:
    def __init__(self, api: HelixAPI) -> None:
        self._api = api

    # def __post_init__(self) -> None:
    #     if not self.api.credentials.ok:
    #         self.api.credentials.validation()

    async def clips(self, user_id: str) -> list[dict[str, Any]]:
        """Gets one or more video clips that were captured from streams."""
        # https://dev.twitch.tv/docs/api/reference#get-clips
        endpoint = URL('clips')
        params = {'broadcaster_id': user_id, 'is_featured': True}
        response = await self._api.request_get(
            endpoint,
            params,
            max_items=constants.MAX_ITEMS_PER_REQUEST,
        )
        data = response['data']
        log.info("got user_id='%s' clips len='%s'", user_id, len(data))
        return data

    async def videos(self, user_id: str) -> list[dict[str, Any]]:
        """
        Gets information about one or more published videos.

        Args:
            user_id (str): The ID of the user.
            highlight (bool, optional): A flag indicating whether to retrieve
            only highlights (default is False).

        Returns:
            TwitchChannelVideos: An iterable containing information about the
            videos.
        """
        # https://dev.twitch.tv/docs/api/reference#get-videos
        log.debug("getting user_id='%s' videos", user_id)
        endpoint = URL('videos')
        params = {
            'user_id': user_id,
            'period': 'week',
            'type': 'archive',
        }
        response = await self._api.request_get(endpoint, params, max_items=50)
        data = response['data']
        log.info("got user_id='%s' videos len='%s'", user_id, len(data))
        return data

    async def search_categories(self, query: str) -> list[Any]:
        """
        Gets the games or categories that match the specified query.
        """
        # https://dev.twitch.tv/docs/api/reference/#search-categories
        log.debug(f"searching for categories with query='{query}'")
        endpoint = URL('search/categories')
        params = {'query': query}
        response = await self._api.request_get(endpoint, params)
        return response['data']

    async def games_info(self, game_ids: list[str]) -> list[dict[str, Any]]:
        """
        Gets information about specified categories or games.
        """
        # https://dev.twitch.tv/docs/api/reference/#get-games
        data: list[dict[str, Any]] = []
        endpoint = URL('games')
        for batch in utils.group_into_batches(game_ids, constants.MAX_ITEMS_PER_REQUEST):
            response = await self._api.request_get(endpoint, {'id': batch})
            data.extend(response.get('data', []))
        log.debug("games_info_len='%s'", len(data))
        return data

    async def top_games(self, items_max: int = constants.MAX_ITEMS_PER_REQUEST) -> dict[str, Any]:
        """
        Gets information about all broadcasts on Twitch.
        """
        # https://dev.twitch.tv/docs/api/reference/#get-top-games
        endpoint = URL('games/top')
        response = await self._api.request_get(endpoint, params={}, max_items=items_max)
        log.debug("top_games_len='%s'", len(response['data']))
        return response['data']


class HelixChannels:
    """
    A class for interacting with the Twitch Channels API.

    The Channels API allows users to retrieve information about channels,
    search for channels, and get a list of channels that the user follows.
    """

    def __init__(self, api: HelixAPI) -> None:
        self._api = api

    async def streams(self) -> list[dict[str, Any]]:
        """
        Gets a list of live streams of broadcasters that the specified user follows.

        Returns:
            TwitchStreams: A list of live streams.
        """
        # https://dev.twitch.tv/docs/api/reference#get-followed-streams
        max_followed_streams = 500
        log.debug(f'getting a list of live streams, max={max_followed_streams}')
        endpoint = URL('streams/followed')
        params = {'user_id': self._api.auth.user_id}
        response = await self._api.request_get(endpoint, params, max_items=max_followed_streams)
        return response['data']

    async def all(self) -> list[dict[str, Any]]:
        """
        Gets a list of broadcasters that the specified user follows.
        """
        # https://dev.twitch.tv/docs/api/reference/#get-followed-channels
        max_followed_channels = 500
        log.debug(f'getting list that user follows, max={max_followed_channels}')
        endpoint = URL('channels/followed')
        params = {'user_id': self._api.auth.user_id}
        response = await self._api.request_get(endpoint, params, max_items=max_followed_channels)
        return response['data']

    async def ids(self) -> list[int]:
        """
        Gets a list of broadcasters's ids that the specified user follows.
        """
        # https://dev.twitch.tv/docs/api/reference/#get-followed-channels
        max_followed_channels = 500
        log.debug(f'getting list that user follows, max={max_followed_channels}')
        endpoint = URL('channels/followed')
        params = {'user_id': self._api.auth.user_id}
        response = await self._api.request_get(endpoint, params, max_items=max_followed_channels)
        return [c['broadcaster_id'] for c in response['data']]

    async def info(self, user_id: str) -> list[dict[str, Any]]:
        """
        Fetches information about one channel.
        """
        # https://dev.twitch.tv/docs/api/reference#get-channel-information
        log.debug('getting information about channel')
        endpoint = URL('channels')
        params = {'broadcaster_id': user_id}
        response = await self._api.request_get(endpoint, params)
        return response['data']

    async def users_info(self, login_ids: list[str]) -> list[dict[str, Any]]:
        """
        Gets information about one or more users.
        """
        # https://dev.twitch.tv/docs/api/reference/#get-users
        log.debug(f'getting information about a {login_ids=}')
        data: list[dict[str, Any]] = []
        endpoint = URL('users')
        for batch in utils.group_into_batches(login_ids, constants.MAX_ITEMS_PER_REQUEST):
            response = await self._api.request_get(endpoint, {'id': batch})
            data.extend(response.get('data', []))
        return data

    async def info_ids(self, broadcaster_ids: list[str]) -> list[dict[str, Any]]:
        """
        Gets information about more channels.
        """
        # https://dev.twitch.tv/docs/api/reference#get-channel-information
        data: list[dict[str, Any]] = []
        endpoint = URL('channels')

        for batch in utils.group_into_batches(broadcaster_ids, constants.MAX_ITEMS_PER_REQUEST):
            response = await self._api.request_get(endpoint, {'broadcaster_id': batch})
            data.extend(response.get('data', []))
        return data

    async def search(self, query: str, live_only: bool = True) -> list[dict[str, Any]]:
        """
        Gets the channels that match the specified query and have
        streamed content within the past 6 months.
        """
        # https://dev.twitch.tv/docs/api/reference/#search-channels
        log.debug(f"searching for channels with query='{query}'")
        endpoint = URL('search/channels')
        params = {'query': query, 'live_only': live_only}
        response = await self._api.request_get(endpoint, params)
        return response['data']

    async def streams_by_game_id(
        self,
        game_id: int,
        max_items: int = constants.DEFAULT_REQUESTED_ITEMS,
    ) -> list[Any]:
        """
        Gets a list of all streams.
        """
        # https://dev.twitch.tv/docs/api/reference/#get-streams
        log.debug(f"getting streams from game_id='{game_id}'")
        endpoint = URL('streams')
        params = {'game_id': game_id}
        response = await self._api.request_get(endpoint, params, max_items=max_items)
        return response['data']

    async def top_streams(self) -> dict[str, Any]:
        """
        Gets a list of all streams.
        """
        # https://dev.twitch.tv/docs/api/reference/#get-streams
        endpoint = URL('streams')
        response = await self._api.request_get(endpoint, params={}, max_items=100)
        log.debug("top_streams_len='%s'", len(response['data']))
        return response['data']
