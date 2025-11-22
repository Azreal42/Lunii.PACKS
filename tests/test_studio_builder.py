from __future__ import annotations

from pkg.api.stories import StudioStory
from pkg.api.studio_builder import StudioStoryBuilder


def test_to_studio_story_round_trip() -> None:
    builder = StudioStoryBuilder(title="My Story", description="Desc", format_version=1, pack_version=1)
    stage_a = builder.add_stage_node(image="img/a.png", audio="audio/a.mp3")
    stage_b = builder.add_stage_node(image="img/b.png", audio="audio/b.mp3")
    action_id = builder.add_action_node([stage_b])
    builder.stage_nodes[0]["okTransition"] = {"actionNode": action_id, "optionIndex": 0}

    story = builder.to_studio_story()

    assert isinstance(story, StudioStory)
    assert story.title == "My Story"
    assert story.js_snodes[0]["okTransition"]["actionNode"] == action_id
    assert story.js_anodes[0]["global_index"] == 0
    assert story.js_snodes[0]["uuid"] == stage_a

    round_trip = story.to_dict()
    assert round_trip["title"] == "My Story"
    assert len(round_trip["stageNodes"]) == 2
    assert len(round_trip["actionNodes"]) == 1


def test_from_json_helper() -> None:
    builder = StudioStoryBuilder(title="Json Path")
    stage = builder.add_stage_node(image=None, audio=None)
    builder.add_action_node([stage])
    json_payload = builder.to_json()

    story = StudioStory.from_json(json_payload)

    assert story.title == "Json Path"
    assert len(story.js_snodes) == 1
    assert len(story.js_anodes) == 1
