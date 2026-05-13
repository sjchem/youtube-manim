"""Tennis scoring helpers and score-state graph generation."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

POINT_LABELS = ["0", "15", "30", "40"]


@dataclass(frozen=True)
class ScoreState:
    """A tennis score state represented by point counts."""

    server_points: int
    receiver_points: int

    @property
    def label(self) -> str:
        """Return a tennis-style label for this state."""

        return score_label(self.server_points, self.receiver_points)


def score_label(server_points: int, receiver_points: int) -> str:
    """Return the display label for a tennis game score."""

    if is_game_over(server_points, receiver_points):
        return "Game Server" if server_points > receiver_points else "Game Receiver"
    if server_points >= 3 and receiver_points >= 3:
        if server_points == receiver_points:
            return "Deuce"
        return "Ad-In" if server_points > receiver_points else "Ad-Out"
    return f"{POINT_LABELS[server_points]}-{POINT_LABELS[receiver_points]}"


def is_game_over(server_points: int, receiver_points: int) -> bool:
    """Return True when either player has won the game."""

    leader = max(server_points, receiver_points)
    return leader >= 4 and abs(server_points - receiver_points) >= 2


def next_state(state: ScoreState, server_wins_point: bool) -> ScoreState:
    """Advance one point from a score state."""

    if server_wins_point:
        return ScoreState(state.server_points + 1, state.receiver_points)
    return ScoreState(state.server_points, state.receiver_points + 1)


def generate_paths(target_server: int, target_receiver: int) -> list[tuple[int, ...]]:
    """Return W/L paths ending at an exact non-deuce score.

    A path is encoded as 1 for a server point and 0 for a receiver point.
    The final point is always a server win for 4-0, 4-1, and 4-2 paths.
    """

    total = target_server + target_receiver
    if target_server != 4 or target_receiver not in {0, 1, 2}:
        raise ValueError("Only 4-0, 4-1, and 4-2 server-win paths are supported")

    paths: list[tuple[int, ...]] = []
    for prefix in product((0, 1), repeat=total - 1):
        path = (*prefix, 1)
        if sum(path) == target_server and len(path) - sum(path) == target_receiver:
            paths.append(path)
    return paths


def generate_deuce_paths() -> list[tuple[int, ...]]:
    """Return all six-point paths that reach 3-3 deuce."""

    return [path for path in product((0, 1), repeat=6) if sum(path) == 3]


def score_state_graph(max_points: int = 7) -> tuple[list[str], list[tuple[str, str, str]]]:
    """Create nodes and labeled edges for a compact tennis score graph."""

    nodes: dict[str, ScoreState] = {}
    edges: set[tuple[str, str, str]] = set()
    queue = [ScoreState(0, 0)]

    while queue:
        state = queue.pop(0)
        label = state.label
        nodes[label] = state
        if is_game_over(state.server_points, state.receiver_points):
            continue
        if state.server_points + state.receiver_points >= max_points:
            continue
        for won, edge_label in [(True, "W"), (False, "L")]:
            nxt = next_state(state, won)
            edges.add((label, nxt.label, edge_label))
            if nxt.label not in nodes and nxt not in queue:
                queue.append(nxt)

    return list(nodes), sorted(edges)
