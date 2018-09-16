from abc import ABCMeta, abstractmethod


class BaseAutoCompleteModel(metaclass=ABCMeta):
    """Abstract base class for auto-complete models."""

    def __init__(self, max_completions=5):
        """Init the model with a maximum number of returned completions."""
        self.max_completions = max_completions

    @abstractmethod
    def generate_completions(prefix):
        """Generate completions for a given prefix."""

    @abstractmethod
    def load(self, file):
        """Load a model from file."""
