# types.py
from __future__ import annotations

from typing import Any
from typing import Mapping
from typing import MutableMapping
from typing import Union

from twitchAPI.models.channels import ChannelInfo
from twitchAPI.models.channels import FollowedChannel
from twitchAPI.models.channels import FollowedChannelInfo
from twitchAPI.models.content import FollowedContentClip
from twitchAPI.models.content import FollowedContentVideo
from twitchAPI.models.streams import FollowedStream

QueryParamTypes = MutableMapping[str, Any]

HeaderTypes = Mapping[str, Any]

TwitchApiResponse = Mapping[str, Any]


TwitchChannel = Union[
    FollowedChannel,
    FollowedStream,
    FollowedChannelInfo,
    ChannelInfo,
]

TwitchContent = Union[
    FollowedContentClip,
    FollowedContentVideo,
    TwitchChannel,
]
