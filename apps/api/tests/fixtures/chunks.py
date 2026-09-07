"""Synthetic chunks for the adversarial suite (tests/adversarial/cases.py).

Not the real ingested dataset — these exist only to give the reveal_episode
filter something real to filter. Each case in cases.py needs at least one
fixture chunk whose content is semantically close to its query, so that if
the WHERE clause in retrieval.py were ever removed, the leak would actually
rank high enough to be returned and the test would catch it.
"""

FIXTURE_CHUNKS = [
    {
        "content": "The Beast Titan is a Titan controlled by Zeke Yeager, who can command"
        " other Titans by shouting orders at them.",
        "source_title": "Beast Titan (fixture)",
        "source_url": "fixture://beast-titan",
        "entity": "Zeke Yeager",
        "reveal_episode": 26,
    },
    {
        "content": "The Founding Titan is the Titan that can control all Subjects of Ymir"
        " and alter their memories.",
        "source_title": "Founding Titan (fixture)",
        "source_url": "fixture://founding-titan",
        "entity": "Eren Yeager",
        "reveal_episode": 44,
    },
    {
        "content": "Ymir Fritz was the first person to become a Titan, nearly 2000 years"
        " ago, and the source of all Titan power.",
        "source_title": "Ymir Fritz (fixture)",
        "source_url": "fixture://ymir-fritz",
        "entity": "Ymir Fritz",
        "reveal_episode": 57,
    },
    # Low-episode distractor: gives search_chunks something to legitimately
    # return below every case's threshold, so the WHERE clause has real
    # filtering work to do instead of an empty table trivially passing.
    {
        "content": "The Scout Regiment investigates Titans outside the Walls and reports"
        " back to the government.",
        "source_title": "Scout Regiment (fixture)",
        "source_url": "fixture://scout-regiment",
        "entity": None,
        "reveal_episode": 5,
    },
]
