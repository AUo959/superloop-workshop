"""Frozen workload schedules for E001 v0.1."""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .model import LOOP_IDS, ROUTES, Offer, digest


SCENARIOS = (
    "balanced",
    "burst",
    "saturated_receiver",
    "slow_neighbor",
    "failed_neighbor",
    "circular_wait",
    "stale_feedback",
    "malformed_duplicate",
)
CONFIGURATIONS = ("central", "global_barrier", "local_cbf")
SEEDS = (17, 29, 43)


def _balanced_offers() -> list[Offer]:
    offers: list[Offer] = []
    for index, tick in enumerate(range(0, 120, 3)):
        source = LOOP_IDS[index % len(LOOP_IDS)]
        offers.append(Offer(tick=tick, work_id=f"regular-{index:03d}", source_loop=source))
    return offers


def build_offers(scenario: str) -> list[Offer]:
    """Return the immutable offered event stream for one scenario."""

    if scenario not in SCENARIOS:
        raise ValueError(f"unsupported scenario: {scenario}")
    if scenario == "circular_wait":
        return []

    offers = _balanced_offers()
    if scenario == "burst":
        for tick in (30, 60):
            for source in LOOP_IDS:
                for offset in range(4):
                    offers.append(
                        Offer(
                            tick=tick,
                            work_id=f"burst-{tick}-{source}-{offset}",
                            source_loop=source,
                        )
                    )
    elif scenario == "saturated_receiver":
        for offset in range(8):
            offers.append(
                Offer(
                    tick=30,
                    work_id=f"saturation-30-A-{offset}",
                    source_loop="A",
                )
            )
    elif scenario == "malformed_duplicate":
        offers.extend(
            (
                Offer(
                    tick=30,
                    work_id="malformed-30",
                    source_loop="A",
                    schema_version="unsupported.work.v0",
                ),
                Offer(
                    tick=30,
                    work_id="regular-000",
                    source_loop="A",
                    duplicate_replay=True,
                ),
            )
        )

    return sorted(
        offers,
        key=lambda offer: (
            offer.tick,
            offer.source_loop,
            offer.work_id,
            offer.schema_version,
        ),
    )


def offers_by_tick(offers: Iterable[Offer]) -> dict[int, list[Offer]]:
    indexed: dict[int, list[Offer]] = defaultdict(list)
    for offer in offers:
        indexed[offer.tick].append(offer)
    return dict(indexed)


def build_circular_preload() -> list[dict[str, object]]:
    """Return the canonical full-ring preload used by S6."""

    return [
        {
            "admitted_at": 0,
            "deadline": 60,
            "processed": True,
            "route": list(ROUTES[loop_id]),
            "route_index": 0,
            "source_loop": loop_id,
            "work_id": f"circular-{loop_id}-{index:02d}",
        }
        for loop_id in LOOP_IDS
        for index in range(8)
    ]


def workload_digest(scenario: str, seed: int) -> str:
    """Digest the canonical offered stream and seeded ordering context."""

    payload = {
        "scenario": scenario,
        "seed": seed,
        "offers": [offer.canonical() for offer in build_offers(scenario)],
        "circular_preload": build_circular_preload() if scenario == "circular_wait" else [],
    }
    return digest(payload)
