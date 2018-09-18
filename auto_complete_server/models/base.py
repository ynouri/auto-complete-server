"""Abstract Base Class for auto-complete models."""

from abc import ABCMeta, abstractmethod


class BaseAutoCompleteModel(metaclass=ABCMeta):
    """Abstract base class for auto-complete models."""

    @abstractmethod
    def generate_completions(self, prefix):
        """Generate completions for a given prefix."""

    @abstractmethod
    def load(self, file):
        """Load a model from file."""
