"""Representation-only helpers for E002 canonical telemetry."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from typing import Any


LOOP_IDS = ("A", "B", "C")
INTERLOCKS = {"AB": ("A", "B"), "BC": ("B", "C"), "CA": ("C", "A")}
CAPACITY = 8
DEADLINE_TICKS = 60
PHASE_PERIODS = (2, 3, 4, 6)


def canonical_json(value: Any) -> str:
    """Serialize a JSON-compatible value deterministically."""

    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def digest(value: Any) -> str:
    """Return the SHA-256 digest of canonical JSON."""

    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def raw_digest(value: bytes | str) -> str:
    """Return the SHA-256 digest of exact bytes or UTF-8 text."""

    payload = value.encode("utf-8") if isinstance(value, str) else value
    return hashlib.sha256(payload).hexdigest()


def rational(value: Fraction | int) -> dict[str, int]:
    """Encode an integer or reduced fraction using the E002 wire form."""

    fraction = value if isinstance(value, Fraction) else Fraction(value, 1)
    return {"numerator": fraction.numerator, "denominator": fraction.denominator}


def parse_rational(value: dict[str, int]) -> Fraction:
    """Decode and validate an E002 rational object."""

    fraction = Fraction(value["numerator"], value["denominator"])
    if rational(fraction) != value:
        raise ValueError(f"noncanonical rational: {value}")
    return fraction


@dataclass
class WorkState:
    """Reconstructed active work state, derived only from trace events."""

    work_id: str
    location: str
    admitted_at: int
    processed: bool = False
    process_count: int = 0
    ready_since: int | None = None
    provenance_complete: bool = True
    lease_fresh_until: int | None = None


def auc(scores_and_labels: list[tuple[Fraction, int]]) -> Fraction | None:
    """Calculate exact ROC-AUC with average-rank tie semantics."""

    positive_count = sum(label == 1 for _, label in scores_and_labels)
    negative_count = sum(label == 0 for _, label in scores_and_labels)
    if not positive_count or not negative_count:
        return None
    grouped: dict[Fraction, list[int]] = {}
    for score, label in scores_and_labels:
        counts = grouped.setdefault(score, [0, 0])
        counts[label] += 1
    wins_twice = 0
    lower_negatives = 0
    for score in sorted(grouped):
        negatives, positives = grouped[score]
        wins_twice += 2 * positives * lower_negatives
        wins_twice += positives * negatives
        lower_negatives += negatives
    return Fraction(wins_twice, 2 * positive_count * negative_count)
