import copy
import json
import uuid
from typing import List, Optional, TypedDict

from pkg.api.stories import StudioStory


class ControlSettings(TypedDict, total=False):
    wheel: int
    ok: int
    home: int
    pause: int
    autoplay: int


class TransitionSpec(TypedDict, total=False):
    actionNode: str
    optionIndex: int


class StageNodeSpec(TypedDict, total=False):
    uuid: str
    image: Optional[str]
    audio: Optional[str]
    okTransition: Optional[TransitionSpec]
    homeTransition: Optional[TransitionSpec]
    controlSettings: Optional[ControlSettings]


class ActionNodeSpec(TypedDict, total=False):
    id: str
    options: List[str]
    global_index: int


class StudioStoryBuilder:
    """Helper to build Studio story structures without hand-crafting JSON."""

    def __init__(self, title: str, description: str = "", format_version: int | str = 1, pack_version: int = 1):
        self.format_version: int | str = format_version
        self.pack_version: int = pack_version
        self.title: str = title
        self.description: str = description
        self.stage_nodes: List[StageNodeSpec] = []
        self.action_nodes: List[ActionNodeSpec] = []

    def add_action_node(self, options: List[str], action_id: Optional[str] = None) -> str:
        action_uuid = action_id or str(uuid.uuid4()).upper()
        action: ActionNodeSpec = {"id": action_uuid, "options": options, "global_index": len(self.action_nodes)}
        self.action_nodes.append(action)
        return action_uuid

    def add_stage_node(
        self,
        image: Optional[str],
        audio: Optional[str],
        ok_transition: Optional[TransitionSpec] = None,
        home_transition: Optional[TransitionSpec] = None,
        control_settings: Optional[ControlSettings] = None,
        stage_id: Optional[str] = None,
    ) -> str:
        stage_uuid = stage_id or str(uuid.uuid4()).upper()
        stage: StageNodeSpec = {
            "uuid": stage_uuid,
            "image": image,
            "audio": audio,
            "okTransition": ok_transition,
            "homeTransition": home_transition,
            "controlSettings": control_settings,
        }
        self.stage_nodes.append(stage)
        return stage_uuid

    def to_dict(self) -> dict:
        return {
            "format": self.format_version,
            "version": self.pack_version,
            "title": self.title,
            "description": self.description,
            "stageNodes": self.stage_nodes,
            "actionNodes": self.action_nodes,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def to_studio_story(self) -> StudioStory:
        """Instantiate a StudioStory object without JSON serialization."""
        story_payload = copy.deepcopy(self.to_dict())
        return StudioStory.from_dict(story_payload)
