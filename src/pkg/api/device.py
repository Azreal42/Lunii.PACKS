from uuid import UUID

from pkg.api.devices import find_devices
from pkg.api.device_lunii import LuniiDevice, feed_stories
from pkg.api.stories import Story, StoryList


__all__ = ["LuniiDevice", "StoryList", "feed_stories", "find_devices", "story_name"]


def story_name(uuid: UUID) -> str:
    """Return the display name for a story UUID using loaded DBs."""
    return Story(uuid).name
