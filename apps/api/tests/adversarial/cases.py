"""Trap queries for the anti-spoiler adversarial suite (PROJECT.md section 11,
layer 4). Each case targets a single, isolated fact with a known
reveal_episode, so a leak has an unambiguous meaning: any result whose
reveal_episode exceeds user_episode.
"""

from dataclasses import dataclass


@dataclass
class AdversarialCase:
    query: str
    user_episode: int
    description: str


CASES = [
    AdversarialCase(
        query="what is the Beast Titan?",
        user_episode=20,
        description="Beast Titan (Zeke), actual reveal_episode = 26",
    ),
    AdversarialCase(
        query="what is the Founding Titan?",
        user_episode=35,
        description="Founding Titan (Eren), actual reveal_episode = 44",
    ),
    AdversarialCase(
        query="who was the first titan?",
        user_episode=50,
        description="Ymir Fritz, actual reveal_episode = 57",
    ),
]
