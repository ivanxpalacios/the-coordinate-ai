import json

import pytest

from label import label_episode_chunk, label_file


def make_episode_chunk(episode_number: int = 1, **overrides) -> dict:
    chunk = {
        "content": "some content",
        "chunk_index": 0,
        "source_url": "https://attackontitan.fandom.com/wiki/Some_Episode",
        "source_title": "Some Episode",
        "source_type": "episode",
        "episode_number": episode_number,
        "entity": None,
    }
    chunk.update(overrides)
    return chunk


def test_label_episode_chunk_copies_episode_number_to_reveal_episode():
    chunk = make_episode_chunk(episode_number=5)

    labeled = label_episode_chunk(chunk)

    assert labeled["reveal_episode"] == 5
    assert labeled["episode_number"] == 5
    assert labeled["content"] == chunk["content"]


def test_label_episode_chunk_rejects_non_episode_chunks():
    chunk = make_episode_chunk(source_type="character", episode_number=None)

    with pytest.raises(ValueError):
        label_episode_chunk(chunk)


def test_label_file_labels_every_line_in_order(tmp_path):
    path = tmp_path / "01_Some_Episode.jsonl"
    chunks = [make_episode_chunk(episode_number=1, chunk_index=i) for i in range(3)]
    path.write_text("\n".join(json.dumps(c) for c in chunks) + "\n", encoding="utf-8")

    label_file(path)

    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3
    for i, line in enumerate(lines):
        labeled = json.loads(line)
        assert labeled["chunk_index"] == i
        assert labeled["reveal_episode"] == 1

    assert not path.with_suffix(path.suffix + ".tmp").exists()


def test_label_file_leaves_original_untouched_and_cleans_tmp_on_failure(tmp_path):
    path = tmp_path / "01_Some_Episode.jsonl"
    good_chunk = make_episode_chunk(episode_number=1, chunk_index=0)
    bad_chunk = make_episode_chunk(episode_number=1, chunk_index=1, source_type="character")
    original_content = json.dumps(good_chunk) + "\n" + json.dumps(bad_chunk) + "\n"
    path.write_text(original_content, encoding="utf-8")

    with pytest.raises(ValueError):
        label_file(path)

    assert path.read_text(encoding="utf-8") == original_content
    assert not path.with_suffix(path.suffix + ".tmp").exists()