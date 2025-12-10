from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, List

from events import Event


class EventSource(ABC):
    """Abstract base for any schedule source."""

    @abstractmethod
    def load(self) -> Iterable[Event]:
        """Return an iterable of events from the source."""

    def list(self) -> List[Event]:
        return list(self.load())
